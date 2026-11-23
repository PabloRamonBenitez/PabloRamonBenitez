"""Comprobacion cruzada: la geometria de la que salen plantas, secciones y alzados se mide en puntos fijos
y se compara con el cuadro de cotas. Si algo no coincide, el plano no coincide con el cuadro."""
import numpy as np
import edificio as E
V = E._v
m = E.base()
me = m.to_mesh()
def ztop(x, y):        # sonda vertical fina
    r = m ^ E.caja(x - 0.03, x + 0.03, y - 0.03, y + 0.03, -1, 100)
    return 0.0 if r.is_empty() else float(r.bounding_box()[5])
def hueco(x, y, z):    # sonda horizontal: cara mas exterior del solido a esa altura (fondo del hueco si hay ventana)
    r = m ^ E.caja(V["W_P"] - 3, V["W_P"] + 0.01, y - 0.03, y + 0.03, z - 0.03, z + 0.03)
    return None if r.is_empty() else float(r.bounding_box()[3])
y0 = E.plantas_base()["Q"][1] + V["D_HOTF"]
chk = [
 ("terraza ala larga junto al bar (planta / secc. S3 / alzado 2)", ztop(11.6, 50), V["Z_P1"]),
 ("peto exterior terraza", ztop(V["W_P"] - 0.15, 70), V["Z_P1"] + V["H_PET"]),
 ("cubierta del bar (a mitad del bar)", ztop(2, (E.plantas_base()["Q"][1] + V["L_L"] - V["L_FIN"]) / 2), V["Z_BARC"]),
 ("terraza tras el fin del bar", ztop(3, V["L_L"] - V["L_FIN"] + 5), V["Z_P1"]),
 ("tramo final sin bar (testero)", ztop(3, V["L_L"] - 3), V["Z_FIN"]),
 ("barandilla del testero", ztop(3, V["L_L"] - 0.2), V["Z_FIN"] + 1.1),
 ("rampa arriba (superficie)", ztop(V["W_P"] + 1.5, y0 + 0.3), V["Z_CON"]),
 ("concha a mitad (coronación alta)", ztop(V["W_P"] + 1.5, (y0 + V["Y_CA"]) / 2), V["Z_CON"]),
 ("concha: curva final a media altura", ztop(V["W_P"] + 0.5, V["Y_CA"] + V["R_FIN"] * (1 - 0.866)), V["Z_CON"] * 0.5),
 ("largo ala larga L_L (muro, sin la marquesina)", float((m ^ E.caja(0.5, 2, 30, 200, 6, 6.5)).bounding_box()[4]), V["L_L"]),
]
yv = V["L_L"] - V["VEN_FIN"] - V["VEN_W"] + 0.2
for z, nm, ref in ((V["VA_0"] + 0.5, "vidrio fila alta (MAR_R tras el frente del marco)", V["W_P"] + V["MAR_P"] - V["MAR_R"]), (V["VB_0"] + 0.4, "vidrio fila baja", V["W_P"] + V["MAR_P"] - V["MAR_R"])):
    xs = [hueco(0, yv + k * 0.1, z) for k in range(10)]
    chk.append((nm, min(x for x in xs if x is not None), ref))
xs = [hueco(0, y0 + 3 + k * 0.25, V["VA_0"] + 0.5) or 99 for k in range(16)]
chk.append(("sin ventanas donde la rampa es alta", min(x for x in xs if x is not None), V["W_P"] + 0.0))
# recuento de huecos en la fila alta y la baja a lo largo de toda la fachada exterior
def contar(z):
    ys = np.arange(E.Y_CUNA - 5, V["L_L"], 0.1); dentro = [ (hueco(0, y, z) or 99) < V["W_P"] - 0.04 for y in ys ]
    return sum(1 for a, b in zip(dentro, dentro[1:]) if b and not a)
chk.append(("nº ventanas fila alta (tramo tras la rampa)", contar((V["VA_0"] + V["VA_1"]) / 2), V["N_VEN"]))
chk.append(("nº huecos fila baja", contar((V["VB_0"] + V["VB_1"]) / 2), V["N_VEN_B"]))
r = m ^ E.caja(V["W_P"] + 1.4, V["W_P"] + 1.6, y0 + 1, y0 + 1.2, 0.5, 1.0)
chk.append(("hueco bajo el arco junto al hotel (vacío = 0)", 0.0 if r.is_empty() else 1.0, 0.0))
t = E.torre()
def _hay(r, da, z):
    px, py = E.esc_ang_pt(r, da)
    return not (t ^ E.caja(px - 0.04, px + 0.04, py - 0.04, py + 0.04, z - 0.04, z + 0.04)).is_empty()
chk.append(("escalera: balcón del barril quitado en el eje del sector (vacío = 1)", float(not _hay(E.R_B - 0.3, 0.0, E.Z_B0 + 1.2)), 1.0))
chk.append(("escalera: muro radial de carga presente", float(_hay((V["ESC_R0"] + V["ESC_RC"]) / 2, E.ESC_HA - 0.01, 20.0)), 1.0))
chk.append(("escalera: tramos al aire (vacío entre fachada y lamas a media altura de tramo)", float(not _hay((V["ESC_RC"] + V["ESC_R1"]) / 2, 0.0, E.Z_P1 + 0.5 + 0.8)), 1.0))
chk.append(("escalera: no sobresale de R_AL + lamas", float(not _hay(V["ESC_R1"] + 0.2, 0.0, 20.0)), 1.0))
px, py = E.esc_ang_pt(V["ESC_R1"] - 0.3, 0)
bb3 = (t ^ E.caja(px - 0.1, px + 0.1, py - 0.1, py + 0.1, -1, 80)).bounding_box()
chk.append(("escalera: coronación (cubierta en cuña, borde exterior)", bb3[5], V["ESC_Z1"]))
chk.append(("escalera: baja al suelo (muro radial)", (t ^ E.caja(*(lambda q: (q[0]-.05, q[0]+.05, q[1]-.05, q[1]+.05))(E.esc_ang_pt((V["ESC_R0"] + V["ESC_RC"]) / 2, E.ESC_HA - 0.01)), -1, 1)).bounding_box()[2], 0.0))
yb0_ = E.plantas_base()["Q"][1]
chk.append(("rampa 2 a mitad", ztop(V["W_BAR"] + V["V_BAR"] + 1.2, yb0_ + V["R2_Y0"] + V["R2_L"] / 2), E.Z_P1 + 0.5 * (E.Z_BARC - E.Z_P1) if hasattr(E, "Z_BARC") else (E.Z_P1 + E.Z_BAR_C) / 2))
chk.append(("relieve del marco (frente)", float((m ^ E.caja(V["W_P"], V["W_P"] + 1, V["L_L"] - V["VEN_FIN"] + 0.1, V["L_L"] - V["VEN_FIN"] + 0.2, V["VA_1"] + 0.1, V["VA_1"] + 0.2)).bounding_box()[3]), V["W_P"] + V["MAR_P"]))
import ventanas as VT
tm_ = E.edificio(); okh = 0; tot = 0
for h in VT.catalogo():
    if h["tipo"] not in ("ventana",) or not (h["grupo"].startswith("ala larga") or h["grupo"].startswith("torre planta")): continue
    tot += 1
    px, py = h["p"][0] - h["n"][0] * 0.05, h["p"][1] - h["n"][1] * 0.05; zc_ = (h["z0"] + h["z1"]) / 2
    r = tm_ ^ E.caja(px - 0.03, px + 0.03, py - 0.03, py + 0.03, zc_ - 0.03, zc_ + 0.03)
    okh += r.is_empty()
chk.append(("huecos del catálogo abiertos en el 3D (ala + torre)", okh, tot))
out = ["| comprobación | medido en la geometría | cuadro | estado |", "|---|---|---|---|"]
for n, a, b in chk:
    ok = abs(a - b) < (0.25 if "curva" in n else 0.12) or (n.startswith("sin ventanas") and a > V["W_P"] - 0.05)
    out.append(f"| {n} | {a:.2f} | {b:.2f} | {'OK' if ok else 'NO'} |")
open("COHERENCIA_VISTAS.md", "w").write("# Coherencia entre vistas y cuadro de cotas\n\n" + "\n".join(out) + "\n")
print("\n".join(out))
