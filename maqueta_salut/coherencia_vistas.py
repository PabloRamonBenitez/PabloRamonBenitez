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
 ("terraza ala larga (planta / secc. S3 / alzado 2)", ztop(V["W_BAR"] + 2, 70), V["Z_P1"]),
 ("peto exterior terraza", ztop(V["W_P"] - 0.15, 70), V["Z_P1"] + V["H_PET"]),
 ("cubierta del bar", ztop(2, 70), V["Z_BARC"]),
 ("tramo final sin bar (testero)", ztop(3, V["L_L"] - 3), V["Z_FIN"]),
 ("barandilla del testero", ztop(3, V["L_L"] - 0.2), V["Z_FIN"] + 1.1),
 ("rampa arriba (superficie)", ztop(V["W_P"] + 1.5, y0 + 0.3), V["Z_CON"]),
 ("rampa a mitad", ztop(V["W_P"] + 1.5, (y0 + E.Y_CUNA) / 2), V["Z_CON"] * (1 - 0.25) ** 0.5),
 ("largo ala larga L_L", float(np.asarray(me.vert_properties)[:, 1].max()), V["L_L"]),
]
yv = E.Y_CUNA + 1.0
for z, nm, ref in ((V["VA_0"] + 0.5, "ventana fila alta (fondo del hueco)", V["W_P"] - 0.3), (V["VB_0"] + 0.4, "ventana fila baja", V["W_P"] - 0.3)):
    xs = [hueco(0, yv + k * 0.25, z) for k in range(16)]
    chk.append((nm + " tras la rampa", min(x for x in xs if x is not None), ref))
xs = [hueco(0, y0 + 3 + k * 0.25, V["VA_0"] + 0.5) for k in range(16)]
chk.append(("sin ventanas donde la rampa es alta", min(x for x in xs if x is not None), V["W_P"] + 0.0))
out = ["| comprobación | medido en la geometría | cuadro | estado |", "|---|---|---|---|"]
for n, a, b in chk:
    ok = abs(a - b) < 0.12 or (n.startswith("sin ventanas") and a > V["W_P"] - 0.05)
    out.append(f"| {n} | {a:.2f} | {b:.2f} | {'OK' if ok else 'NO'} |")
open("COHERENCIA_VISTAS.md", "w").write("# Coherencia entre vistas y cuadro de cotas\n\n" + "\n".join(out) + "\n")
print("\n".join(out))
