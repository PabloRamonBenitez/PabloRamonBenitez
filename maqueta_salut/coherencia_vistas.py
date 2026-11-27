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
 ("rampa de acceso a mitad (perfil convexo P2)", ztop(V["W_P"] + 1.5, (y0 + E.Y_CUNA) / 2), V["Z_CON"] * (1 - 0.5 ** V["RAMPA_P"])),
 ("largo ala larga L_L (muro, sin porche ni esquina)", float((m ^ E.caja(0.5, 2, 30, 200, 6, 6.5)).bounding_box()[4]), V["L_L"]),
]
yv = V["L_L"] - V["VEN_FIN"] - V["VEN_W"] + 0.2
for z, nm, ref in ((V["VA_0"] + 0.5, "vidrio fila alta (MAR_R tras el frente del marco)", V["W_P"] - V["FAC_R"] + V["MAR_P"] - V["MAR_R"]), (V["VB_0"] + 0.4, "vidrio fila baja", V["W_P"] - V["FAC_R"] + V["MAR_P"] - V["MAR_R"])):
    xs = [hueco(0, yv + k * 0.1, z) for k in range(10)]
    chk.append((nm, min(x for x in xs if x is not None), ref))
xs = [hueco(0, y0 + 3 + k * 0.25, V["VA_0"] + 0.5) or 99 for k in range(16)]
chk.append(("sin ventanas donde la rampa es alta", min(x for x in xs if x is not None), V["W_P"] + 0.0))
# recuento de huecos en la fila alta y la baja a lo largo de toda la fachada exterior
def contar(z):
    ys = np.arange(E.Y_CUNA + 0.2 if z < 3 else E._v["Y_CA"] - 1, V["L_L"], 0.1); dentro = [ (hueco(0, y, z) or 99) < V["W_P"] - V["FAC_R"] - 0.04 for y in ys ]
    return sum(1 for a, b in zip(dentro, dentro[1:]) if b and not a)
chk.append(("nº ventanas fila alta (tramo tras la rampa)", contar((V["VA_0"] + V["VA_1"]) / 2), V["N_VEN"]))
chk.append(("nº huecos fila baja", contar((V["VB_0"] + V["VB_1"]) / 2), V["N_VEN_B"]))
r = m ^ E.caja(V["W_P"] + 1.4, V["W_P"] + 1.6, y0 + 1, y0 + 1.2, 0.5, 1.0)
chk.append(("hueco bajo el arco junto al hotel (vacío = 0)", 0.0 if r.is_empty() else 1.0, 0.0))
t = E.torre()
import math
def _hay(r, da, z):
    px, py = E.esc_ang_pt(r, da)
    return not (t ^ E.caja(px - 0.04, px + 0.04, py - 0.04, py + 0.04, z - 0.04, z + 0.04)).is_empty()
dm = (E.ESC_HA + E.ESC_HB) / 2; zm = E.Z_B0 + 2 * E.F + 2.0
chk.append(("escalera: balcones quitados en el hueco del cilindro (vacío = 1)", float(not _hay(E.R_B - 0.3, dm, E.Z_B0 + 1.2)), 1.0))
chk.append(("escalera: cuerpo en cuña cerrado", float(_hay(13.0, 0.0, 20.0)), 1.0))
chk.append(("escalera: fachada retranqueada presente (r < RR)", float(_hay(V["ESC_RR"] - 0.2, dm + 0.03, E.Z_B0 + 0.6)), 1.0))
chk.append(("escalera: delante del retranqueo, vacío hasta la barandilla", float(not _hay(V["ESC_RR"] + 0.6, dm, zm)), 1.0))
chk.append(("escalera: ventana en la fachada retranqueada (vacío = 1)", float(not _hay(V["ESC_RR"] - 0.2, dm, E.Z_B0 + 2 * E.F + 1.8)), 1.0))
chk.append(("escalera: lamas a los lados de la cuña", float(any(_hay(rr, E.ESC_HB + math.atan2(0.45, rr), 20.0) for rr in [13.4 + 0.05 * i for i in range(24)])), 1.0))
chk.append(("escalera: no sobresale más allá de las lamas", float(not _hay(V["ESC_R1"] + 0.3, 0.0, 20.0)), 1.0))
px, py = E.esc_ang_pt(E.R_T - 0.2, 0.0)      # sobre el muro de coronación (eje de la cuña, cerca del borde del tambor) [dron, duda 7]
bb3 = (t ^ E.caja(px - 0.1, px + 0.1, py - 0.1, py + 0.1, -1, 80)).bounding_box()
chk.append(("escalera: coronación del muro en r = R_T − 0,2 (ESC_ZI dentro → ESC_Z1 en el borde del tambor; vierte hacia dentro)", bb3[5], V["ESC_ZI"] + (E.R_T - 0.2 - V["ESC_RS"]) * (V["ESC_Z1"] - V["ESC_ZI"]) / (E.R_T + V["ESC_MO"] - V["ESC_RS"])))
chk.append(("escalera: la losa blanca arranca a ESC_Z0 junto al núcleo (F78)", (t ^ E.caja(*(lambda q: (q[0]-.05, q[0]+.05, q[1]-.05, q[1]+.05))(E.esc_ang_pt(12.0, 0.8 * E.ESC_HB)), 9, 30)).bounding_box()[2], V["ESC_Z0"] - V["ESC_LE"]))
yb0_ = E.plantas_base()["Q"][1] + V["R2_Y0"]; yr1_ = yb0_ + V["R2_L"]
chk.append(("rampa 1 llega a la cota de la terraza (sin escalón)", V["Z_CON"], V["Z_P1"]))
chk.append(("techo del restaurante: arranca a cota de terraza junto a la torre", ztop(3.0, yb0_ + 0.2), E.Z_P1 + (E.Z_BAR_C - E.Z_P1) * 0.2 / V["R2_L"]))
chk.append(("techo del restaurante: a mitad de la rampa", ztop(3.0, (yb0_ + yr1_) / 2), (E.Z_P1 + E.Z_BAR_C) / 2))
chk.append(("techo del restaurante: llega a la azotea", ztop(3.0, yr1_ + 1.0), E.Z_BAR_C))
_tt = E.torre(); _m2 = E.base()
_xs, _ys = E.esc_ang_pt(13.0, 0.8 * E.ESC_HB)          # junto al núcleo (el núcleo baja a la terraza, F78)
_zr = ztop(_xs, _ys) if False else None
_bot = (_tt ^ E.caja(_xs - .1, _xs + .1, _ys - .1, _ys + .1, 0, 60)).bounding_box()[2]
_zramp = E.Z_P1 + (_ys - yb0_) / V["R2_L"] * (E.Z_BAR_C - E.Z_P1)
chk.append(("la cubierta inclinada del restaurante pasa bajo la losa de la escalera sin tocarla (no es de paso)", float(_bot - _zramp >= 0.5), 1.0))
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
# nuevas (pasada 16)
_px, _py = E.esc_ang_pt(E.R_B, 0.0)
chk.append(("hueco 11 por encima de la concha (concha bajo su alféizar)", ztop(V["W_P"] + 0.5, V["L_L"] - V["VEN_FIN"] - 10 * V["S_VEN"] - V["VEN_W"] / 2), 0.0 if False else min(ztop(V["W_P"] + 0.5, V["L_L"] - V["VEN_FIN"] - 10 * V["S_VEN"] - V["VEN_W"] / 2), V["VA_0"])))
_t = E.torre()
_v_ = E.P(*E.OFF_V)
chk.append(("barandilla en la cubierta de la visera", float((_t ^ E.caja(_v_[0] + E.R_V - 0.06, _v_[0] + E.R_V - 0.02, _v_[1] - 0.05, _v_[1] + 0.05, E.Z_V1 + 0.5, E.Z_V1 + 0.6)).is_empty() == False), 1.0))
_q = (E.T[0] - E.R_T + 0.6, E.T[1])
chk.append(("pasillo entre tambor y banda (vacío a +Z_T1−0,5)", float((_t ^ E.caja(_q[0] - .05, _q[0] + .05, _q[1] - .05, _q[1] + .05, E.Z_T1 - 0.5, E.Z_T1 - 0.4)).is_empty()), 1.0))
chk.append(("peto del tambor hasta +Z_T1", float(not (_t ^ E.caja(E.T[0] - E.R_T + 0.05, E.T[0] - E.R_T + 0.15, E.T[1] - .05, E.T[1] + .05, E.Z_T1 - 0.2, E.Z_T1 - 0.1)).is_empty()), 1.0))
chk.append(("remate: coronación", (_t ^ E.caja(*(lambda p: (p[0]-.2, p[0]+.2, p[1]-.2, p[1]+.2))(E.P(*E.OFF_R)), 40, 60)).bounding_box()[5], V["Z_R1"]))
_pb = E.P(V["OB_X"], V["OB_Y"]); _q = (_pb[0] - (V["R_G"] - 0.5) * E.N[0], _pb[1] - (V["R_G"] - 0.5) * E.N[1])
chk.append(("banda descentrada hacia la plaza (vidrio a R_G del centro de la banda)", float(not (_t ^ E.caja(_q[0]-.05, _q[0]+.05, _q[1]-.05, _q[1]+.05, 39.5, 39.6)).is_empty()), 1.0))
chk.append(("entrada a la terraza abierta sobre la banda del hotel", ztop(V["W_P"] - 0.15, E.plantas_base()["Q"][1] + 2.0), V["Z_P1"]))
chk.append(("barandilla en el lado largo de la azotea del bar", ztop(V["W_BAR"] + V["V_BAR"] - 0.05, 60.0), E.Z_BAR_C + 1.0))
_pc, _bc = E.curva_poligono()
_mid = _bc[len(_bc) // 2]
chk.append(("plataforma de giro a +7,2 (curva exterior)", ztop(_mid[0] + 0.15 * (_pc[0][0] - _mid[0]), _mid[1] + 0.15 * (_pc[0][1] - _mid[1])), V["Z_P1"]))
chk.append(("peto curvo de la plataforma de giro", ztop(_mid[0] + 0.04 * (_pc[0][0] - _mid[0]), _mid[1] + 0.04 * (_pc[0][1] - _mid[1])), V["Z_P1"] + 1.0))
_fe = E.P(E.R_COL + 3.0, -(E.R_COL - E.RET) - 1.5); _r = m ^ E.caja(_fe[0] - .1, _fe[0] + .1, _fe[1] - .1, _fe[1] + .1, 1.0, 5.0)
chk.append(("fachada del chaflán libre: entrada del hotel sin losa delante", float(_r.is_empty()), 1.0))
import cotas as _KK
_g = _KK.planta(); _a0, _a1 = np.array(_g["ARC"][0]), np.array(_g["ARC"][1]); _tan = (_a1 - _a0) / np.linalg.norm(_a1 - _a0)
chk.append(("la curva de la rampa llega al chaflán a 90° (|cos|)", abs(float(_tan @ np.array(E.U))), 0.0))
chk.append(("la curva sale hacia fuera (x de E90 > borde recto de la rampa)", float(_g["E90"][0] > V["W_EXT"]), 1.0))
import ventanas as _VT
chk.append(("paños de la planta 1 del chaflán: restaurante (5 y pico)", sum(1 for h in _VT.catalogo() if h["grupo"] == "chaflán restaurante"), 6))
chk.append(("paños enteros del hotel (4) + resto macizo junto a E90 (m)", sum(1 for h in _VT.catalogo() if h["grupo"] == "chaflán hotel") + round(V["HOT_L"] - 4 * V["M_CH"], 2) / 10, 4 + round(V["HOT_L"] - 4 * V["M_CH"], 2) / 10))
chk.append(("hotel: de la columna a E90 = HOT_L", float(np.linalg.norm(np.array(_g["E90"]) - (np.array(E.T) - (E.R_COL - E.RET) * np.array(E.N))) - E.R_COL), V["HOT_L"]))
_y = V["L_L"] + V["POR_D"] - 0.2
chk.append(("porche del testero: muro izquierdo", ztop(V["POR_X0"] + 0.15, _y), 4.4))
chk.append(("porche del testero: muro derecho", ztop(V["POR_X1"] - 0.15, _y), 4.4))
chk.append(("porche: paso libre delante de la puerta (vacío bajo la marquesina = 1)", float((m ^ E.caja(5.5, 5.7, _y - .1, _y + .1, 1.0, 2.0)).is_empty()), 1.0))
chk.append(("testero sin muro de esquina: nada sobresale del testero en la esquina exterior (vacío = 1)", float((t ^ E.caja(V["W_P"] - 0.2, V["W_P"] - 0.1, V["L_L"] + 0.55, V["L_L"] + 0.65, 4.95, 5.05)).is_empty()), 1.0))
_sw = lambda x, y: E.SWP(x, y)
_q = _sw(-V["L_C"] + 3.0, -V["VOL_V"] + 0.3)
chk.append(("cuerpo volado: vuela VOL_V sobre la calle, a cota del bloque alto", ztop(*_q), V["Z_ALTO"]))
_r = m ^ E.caja(_q[0] - .1, _q[0] + .1, _q[1] - .1, _q[1] + .1, 1.0, V["Z_VOL0"] - 0.2)
chk.append(("bajo el vuelo, paso libre hasta Z_VOL0 (vacío = 1)", float(_r.is_empty()), 1.0))
_q = _sw(-V["L_C"] + 1.8, 0.9)
chk.append(("logia de planta 1 hueca (vacío a +5,5 = 1)", float((m ^ E.caja(_q[0] - .05, _q[0] + .05, _q[1] - .05, _q[1] + .05, 5.4, 5.5)).is_empty()), 1.0))
_q = _sw(-V["L_C"] + V["LOG_PX"], 0.9)
chk.append(("pilar intermedio de la logia", float(not (m ^ E.caja(_q[0] - .05, _q[0] + .05, _q[1] - .05, _q[1] + .05, 5.4, 5.5)).is_empty()), 1.0))
import math as _mt
_ba = E.bloque_alto_poligono(); _d = min(_mt.dist(p, E.T) for p in _ba[3:-1])
chk.append(("remate del bloque alto equidistante al tambor (R_AC)", _d, V["R_AC"]))
_pl = E.P(V["LUC_X"], V["LUC_Y"])
chk.append(("lucernario sobre la visera", (E.torre() ^ E.caja(_pl[0] - .1, _pl[0] + .1, _pl[1] - .1, _pl[1] + .1, 0, 60)).bounding_box()[5], V["Z_V1"] + 0.24 + V["LUC_H"]))
chk.append(("canto de la visera 1,90 m (MGF Alamy)", V["Z_V1"] - V["Z_G1"], 1.9))
_hp = [h for h in VT.catalogo() if h["grupo"] == "hotel puertas PB"]
chk.append(("puertas del hotel abiertas en PB", sum(float((m ^ E.caja(h["p"][0] - h["n"][0] * 0.4 - .05, h["p"][0] - h["n"][0] * 0.4 + .05, h["p"][1] - h["n"][1] * 0.4 - .05, h["p"][1] - h["n"][1] * 0.4 + .05, 1.0, 1.1)).is_empty()) for h in _hp), len(_hp)))
_g2 = _KK.planta(); _F1 = np.array(E.SWP(-V["L_C"], V["W_C"])); _IC = np.array(_g2["IC"])
_dr = (_IC - _F1) / np.linalg.norm(_IC - _F1)
chk.append(("línea posterior del ala corta paralela al chaflán (|sen| con U)", abs(float(_dr[0] * E.U[1] - _dr[1] * E.U[0])), 0.0))
chk.append(("rincón del patio sin 90° (ángulo, grados)", round(math.degrees(math.acos(abs(float(_dr[1])))), 1), round(math.degrees(math.acos(abs(float(E.U[1])))), 1)))
chk.append(("X: medianera → A1 (sale de la triangulación, no se fija a mano)", float(np.linalg.norm(np.array(E.SWP(-V["L_C"], 0)) - np.array(_g2["A1"]))), 22.75))
_baT = [np.array(p) for p in E.bloque_alto_poligono()]
_A, _B, _C = _baT[0], _baT[1], _baT[2]
chk.append(("triangulación A–B (vuelo)", float(np.linalg.norm(_B - _A)), 7.3))
chk.append(("triangulación A–C", float(np.linalg.norm(_C - _A)), 16.66))
chk.append(("triangulación A–D EXACTA (D = esquina exterior del testero)", float(np.linalg.norm(np.array([V["W_EXT"], V["L_L"]]) - _A)), 106.69))
chk.append(("triangulación D–C dentro del 1,5 % (usuario): error relativo ≤ 0,015", abs(float(np.linalg.norm(np.array([V["W_EXT"], V["L_L"]]) - _C)) / 95.17 - 1), 0.0))
out = ["| comprobación | medido en la geometría | cuadro | estado |", "|---|---|---|---|"]
# ---- piezas nuevas (fotos 25/11): mismo cuadro de cotas en el 3D y en el catálogo que usan los planos
import ventanas as _VT
_cat = _VT.catalogo()
_hay3 = lambda p, z, h=0.04: not (_t ^ E.caja(p[0] - h, p[0] + h, p[1] - h, p[1] + h, z - h, z + h)).is_empty()
_tp = [h for h in _cat if h["grupo"] == "tambor puerta"][0]
_pin = (_tp["p"][0] - 0.15 * _tp["n"][0], _tp["p"][1] - 0.15 * _tp["n"][1])
chk.append(("puerta del tambor junto a la escalera: hueco en el muro (vacío = 1)", float(not _hay3(_pin, _tp["z0"] + 1.0)), 1.0))
_a = E.ESC_ANG - E.ESC_HA - math.pi / V["N_AL"]
_po = (E.T[0] + (E.R_T + 0.4) * math.cos(_a), E.T[1] + (E.R_T + 0.4) * math.sin(_a))
chk.append(("sin ojo en el módulo junto a la escalera (lado izq.) (vacío = 1)", float(not _hay3(_po, V["OJO_Z"])), 1.0))
chk.append(("ojos en el catálogo (planos) = ojos del 3D", float(sum(1 for h in _cat if h["grupo"] == "tambor ojos")), 13.0))
_am = -(E.ESC_HA + E.ESC_HB) / 2
chk.append(("cristalera suelo-techo en el hueco izq. a la altura del tambor", float(_hay3(E.esc_ang_pt(V["ESC_RR"] - 0.025, _am), E.Z_B1 + 2.0, 0.02)), 1.0))
chk.append(("dintel de la cristalera", float(_hay3(E.esc_ang_pt(V["ESC_RR"], _am), (V["CR_Z1"] + E.Z_T1) / 2)), 1.0))
chk.append(("borde izq. del corte sin lamas (vacío = 1)", float(not any(_hay3(E.esc_ang_pt(rr, -(E.ESC_HA - math.atan2(0.2, rr))), 25.0, 0.03) for rr in [V["ESC_RR"] + 0.2 + 0.05 * i for i in range(40)])), 1.0))
chk.append(("borde dcho. del corte con lamas", float(any(_hay3(E.esc_ang_pt(rr, E.ESC_HA - math.atan2(0.2, rr)), 25.0, 0.03) for rr in [V["ESC_RR"] + 0.2 + 0.05 * i for i in range(40)])), 1.0))
chk.append(("encima del tambor solo el muro: vacío en el eje de la escalera a +40", float(not _hay3(E.esc_ang_pt(V["ESC_RC"] - 1.0, 0.0), 40.0)), 1.0))
_L = E.letrero()
chk.append(("letrero: 10 letras en volumen (САЛЮТ ×2 en arco) presentes en el 3D", float(len(E.letras_volumen(E.P(V["OR_X"], V["OR_Y"])))), 10.0))
_pr = E.P(V["OR_X"], V["OR_Y"])
chk.append(("zócalo (poyete) del remate", float(_hay3((_pr[0] + (V["REM_ZR"] - 0.2), _pr[1]), E.Z_V1 + V["REM_ZH"] / 2)), 1.0))
_pv = E.P(V["OV_X"], V["OV_Y"])
chk.append(("barandilla de la visera abierta: vacío entre pasamanos y travesaño", float(not all(_hay3((_pv[0] + (E.R_V - 0.035) * math.cos(q), _pv[1] + (E.R_V - 0.035) * math.sin(q)), E.Z_V1 + 0.75, 0.02) for q in np.linspace(0, 2 * math.pi, 37)[:-1] + math.radians(5))), 1.0))
# ---- ronda absoluta (26/11 tarde): H1–H4 y P3–P5
_k = round((E.ESC_ANG + math.pi - E.FASE_AL) / (2 * math.pi / V["N_AL"]) - 0.5)
_am = 2 * math.pi * (_k + 0.5) / V["N_AL"] + E.FASE_AL                  # centro de un módulo opuesto a la escalera
_pm = lambda r: (E.T[0] + r * math.cos(_am), E.T[1] + r * math.sin(_am))
chk.append(("1.ª planta: banda continua sin ranura (macizo en la cota de la ranura)", float(_hay3(_pm(E.R_B - 0.1), E.Z_B0 + E.F - 1.40 - 0.6)), 1.0))
chk.append(("fondo plano: vacío bajo el borde exterior entre vigas", float(not _hay3(_pm(E.R_B - 0.3), V["Z_BI"] - 0.3)), 1.0))
_av = 2 * math.pi * (_k + 1) / V["N_AL"] + E.FASE_AL; _pv_ = lambda r: (E.T[0] + r * math.cos(_av), E.T[1] + r * math.sin(_av))
chk.append(("viga radial bajo el fondo (en el eje de una aleta, 0,3 bajo el fondo)", float(_hay3(_pv_((E.R_CU + E.R_B) / 2), V["Z_BI"] - 0.3)), 1.0))
chk.append(("fondo de la viga en ángulo recto: vacío bajo Z_BI − VIG_H", float(not _hay3(_pv_((E.R_CU + E.R_B) / 2), V["Z_BI"] - V["VIG_H"] - 0.15)), 1.0))
chk.append(("1.ª planta: la aleta NO sobresale de la banda (vacío en R_B + 0,4)", float(not _hay3(_pv_(E.R_B + 0.4), (V["Z_BI"] + V["Z_ALE"]) / 2)), 1.0))
chk.append(("2.ª planta: la aleta sí sobresale (macizo en R_B + 0,4)", float(_hay3(_pv_(E.R_B + 0.4), V["Z_ALE"] + 1.0)), 1.0))
chk.append(("cuello sin losa volada (vacío en R_CU + 0,3 a +Z_CU0 + 0,3)", float(not _hay3(_pm(E.R_CU + 0.3), V["Z_CU0"] + 0.3)), 1.0))
chk.append(("fondo plano: macizo junto al cuello sobre +Z_CU1", float(_hay3(_pm(E.R_CU + 0.3), E.Z_CU1 + 0.1)), 1.0))
chk.append(("sin fuente (retirada por el usuario 27/11): vacío delante de la columna", float(not _hay3((E.T[0] - E.N[0] * (V["FU_R"] - 0.15), E.T[1] - E.N[1] * (V["FU_R"] - 0.15)), 0.2)), 1.0))
chk.append(("visera/tambor = media de F01, F02, F09, F14, F23 (0,951)", E.R_V / E.R_T, 0.951))
chk.append(("remate/tambor = media de las 5 fotos (0,379)", E.R_R / E.R_T, 0.379))
chk.append(("F09: la visera vuela fuera del peto del barril por la izquierda (0,9 m)", -(V["OV_X"] - E.R_V) - E.R_B, 0.9))
chk.append(("gárgolas: una por módulo y planta fuera de la escalera (17 × 6)", float(len(E.gargolas())), 102.0))
# ---- duda 7 (dron del usuario 26/11): muro de coronación sobre la cubierta del tambor, en el eje de la cuña
chk.append(("muro de coronación sobre el tambor (macizo en el eje, a media longitud, +1 m)", float(_hay3(E.esc_ang_pt((V["ESC_RS"] + E.R_T) / 2, 0.0), E.Z_T1 + 1.0)), 1.0))
chk.append(("nada por encima del tambor fuera de su borde (r R_T+0,8, +40,5)", float(not _hay3(E.esc_ang_pt(E.R_T + 0.8, 0.0), 40.5)), 1.0))
_lat9 = (E.R_T + V["ESC_MO"]) * math.sin(E.ESC_ANG - math.radians(320.0)); _vis9 = V["OV_X"] + E.R_V
chk.append(("F09: el extremo del muro no asoma a la derecha de la visera (lateral − borde visera ≤ 0,25)", max(0.0, _lat9 - _vis9), 0.0))
# ---- plantas de habitaciones (usuario 26/11): balcón de BAL_P; interiores solo en planos (el 3D queda macizo)
_ab = 2 * math.pi * (_k + 0.5) / V["N_AL"] + E.FASE_AL; _zb = E.Z_B0 + 3 * E.F + 2.0
_pb = lambda r: (E.T[0] + r * math.cos(_ab), E.T[1] + r * math.sin(_ab))
chk.append(("balcón de BAL_P: vacío entre la fachada de ventanas y el poyete", float(not _hay3(_pb(E.RF + 0.6), _zb)), 1.0))
chk.append(("fachada de ventanas en R_B − BAL_P", float(_hay3(_pb(E.RF - 0.4), _zb - 1.7)), 1.0))
# ---- 27/11: muro de ventanas del ala larga hasta el testero (sin tacón), garaje del ala corta, cristaleras de PB del chaflán
chk.append(("ala larga: fachada retranqueada hasta el testero (vacío en la esquina bajo la banda)", float(not _hay3((V["W_P"] - 0.3, V["L_L"] - 0.15), 3.0)), 1.0))
_ga = [h for h in _cat if h["grupo"] == "ala corta garaje"][0]
_gi = np.array(_ga["p"]) - np.array(_ga["n"]) * 2.0
chk.append(("ala corta: hueco de garaje (vacío 2 m dentro, a 1,5 m)", float(not _hay3(tuple(_gi), 1.5)), 1.0))
chk.append(("chaflán: cristaleras de PB en el catálogo (restaurante + hotel)", float(sum(1 for h in _cat if h["grupo"] == "chaflán PB cristalera") >= 4), 1.0))
for n, a, b in chk:
    ok = abs(a - b) < (2.0 if "tolerancia 2" in n else 0.1 if ("A–D" in n) else 0.25 if ("curva" in n or "X:" in n) else 0.12) or (("|cos|" in n or "|sen|" in n) and a < 0.02) or (n.startswith("sin ventanas") and a > V["W_P"] - 0.05) or ("1,5 %" in n and a <= 0.015)
    out.append(f"| {n} | {a:.2f} | {b:.2f} | {'OK' if ok else 'NO'} |")
open("COHERENCIA_VISTAS.md", "w").write("# Coherencia entre vistas y cuadro de cotas\n\n" + "\n".join(out) + "\n")
print("\n".join(out))
