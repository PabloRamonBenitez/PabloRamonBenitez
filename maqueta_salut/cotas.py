"""CUADRO DE COTAS UNICO del Hotel Salut. Fuente de TODO (planos 2D y, al final, el volumen).
Cada cota: valor (m o grados) y origen. Los elementos 2D/3D se derivan de aqui, sin pasar por ningun modelo."""
import math
import numpy as np

COTAS = {
 # --- alturas de la base
 "Z_PB":   (3.2,  "techo de planta baja, única en toda la base", "F15 (época, autobús como escala)"),
 "Z_P1":   (7.3,  "coronación de planta primera = terraza", "F09 7,3 / F14 7,2 / F15 7,2"),
 "Z_BAR":  (11.0, "techo del bar sobre la terraza", "coherencia: = bloque alto ala corta"),
 "Z_BARC": (11.5, "cubierta volada del bar", "= bloque alto (sección AA/BB)"),
 "Z_ALTO": (11.5, "bloque alto del ala corta", "F01, sección AA del usuario"),
 "Z_LAD0": (5.0,  "base de la caja de ladrillo elevada", "F19"),
 "Z_LAD1": (10.0, "coronación de la caja de ladrillo", "F01, F19"),
 "Z_CON":  (8.5,  "arranque de la concha / muro del relieve", "F09, F18"),
 # --- torre
 "Z_CU0":  (10.4, "base del cuello", "F09"),
 "Z_CU1":  (12.2, "cara superior del cuello", "F02, F18, F50"),
 "Z_ALE":  (15.2, "borde inferior de las aletas (fin de las ménsulas)", "F09"),
 "Z_B0":   (13.9, "primer forjado del barril", "F09 (paso 3,10)"),
 "F":      (3.10, "altura de planta del barril", "F09: dinteles cada 40 px"),
 "N_PL":   (6,    "plantas del barril (5 de ventanas + pavés)", "F09"),
 "Z_T1":   (38.2, "coronación del tambor de ojos", "F09"),
 "Z_G1":   (40.5, "coronación de la banda acristalada", "F09"),
 "Z_V1":   (43.7, "coronación de la visera", "F09"),
 "Z_R1":   (49.1, "coronación del remate (sin antenas)", "F09"),
 "R_COL":  (3.25, "radio de la columna (Ø 6,5)", "F09, F14"),
 "R_CONO": (4.9,  "radio del pie cónico de la columna a nivel de suelo", "F15, F01"),
 "R_CU":   (9.0,  "radio del cuello (Ø 18)", "F01, F02"),
 "R_B":    (14.4, "radio del borde de balcones", "escala"),
 "R_AL":   (15.3, "radio a la punta de las aletas (Ø 30,6)", "escala"),
 "R_T":    (13.55,"radio del tambor de ojos (Ø 27,1)", "F01, F09, F14"),
 "R_G":    (10.85,"radio de la banda acristalada (Ø 21,7)", "F09"),
 "R_V":    (12.8, "radio de la visera (Ø 25,6)", "F09; Google 24,35"),
 "R_R":    (5.6,  "radio del remate (Ø 11,2)", "F09"),
 "OV_X":   (-0.4, "desplazamiento de la visera a lo largo del chaflán", "ajuste C02 + C04"),
 "OV_Y":   (-4.2, "desplazamiento de la visera hacia la plaza (−)", "ajuste C02 + C04"),
 "OR_X":   (0.6,  "desplazamiento del remate", "F09"),
 "N_AL":   (19,   "aletas / muros radiales", "fuentes + F09"),
 "ESC_W":  (10.0, "ancho de la caja de escalera", "F08"),
 "ESC_X":  (7.74, "eje de la escalera (dentro de la L, pegada a la fachada exterior del ala)", "usuario: en línea con el ala; comprobación entre planos"),
 # --- planta
 "W_P":    (12.74,"ancho del ala larga", "Bing"),
 "W_BAR":  (6.21, "ancho del bar (mitad interior)", "Bing"),
 "V_BAR":  (1.2,  "vuelo de la cubierta del bar sobre la terraza", "F47"),
 "L_L":    (94.8, "largo total del ala larga desde la calle", "Google 94,82"),
 "L_FIN":  (7.81, "tramo final sin bar", "Bing"),
 "D_CUNA": (35.13,"distancia del fin de la concha al fondo", "Bing"),
 "W_EXT":  (15.7, "ancho máximo con la concha", "Google"),
 "THL":    (112.0,"ángulo interior de la L (calle–ala larga)", "F35/F58 102-114; C02 recalibrada"),
 "ACH":    (57.0, "ángulo del chaflán con el ala larga (incógnita)", "F01 55-58 (no fiable)"),
 "REST":   (14.3, "frente del restaurante en el chaflán", "C04 calibrada"),
 "COL":    (6.5,  "columna en el chaflán", "F09"),
 "HOT":    (11.4, "frente del hotel en el chaflán", "C04 calibrada"),
 "RET":    (1.5,  "lo que asoma la columna delante de la planta primera", "F09/F18"),
 "RETR":   (2.5,  "retranqueo de la planta baja bajo la planta primera", "F09, F14, F47"),
 "L_C":    (24.0, "largo del ala corta desde la esquina exterior", "F01 (estimado)"),
 "W_C":    (12.0, "fondo del ala corta", "F01 (estimado)"),
 "L_LAD":  (5.0,  "largo de la caja de ladrillo", "F01"),
}
V = {k: v[0] for k, v in COTAS.items()}


# ======================================================================== geometria de planta (2D)
def planta():
    g = dict(V)
    th, a = math.radians(V["THL"]), math.radians(V["ACH"])
    LCH = V["REST"] + V["COL"] + V["HOT"]
    angC = math.pi - th - a
    _a = LCH * math.sin(angC) / math.sin(th); _c = LCH * math.sin(a) / math.sin(th)
    US = np.array([math.cos(math.pi / 2 + th), math.sin(math.pi / 2 + th)]); NS = np.array([US[1], -US[0]])
    KC = np.array([V["W_EXT"], 0.0]); A1 = KC + _a * US; C = KC + np.array([0, _c])
    U = (C - A1) / LCH; N = np.array([-U[1], U[0]])
    T = A1 + (V["REST"] + V["COL"] / 2) * U + (V["R_COL"] - V["RET"]) * N
    def SWP(x, y):             # ala corta en coordenadas "de L recta"
        return KC + (V["W_EXT"] - x) * US + y * NS
    def inter(p, d, q, e):
        den = d[0] * e[1] - d[1] * e[0]; s = ((q[0] - p[0]) * e[1] - (q[1] - p[1]) * e[0]) / den
        return p + s * d
    t = (V["W_P"] - C[0]) / N[0]; Q = C + t * N
    IC = inter(SWP(0, V["W_C"]), US, np.array([0.0, 0.0]), np.array([0.0, 1.0]))
    P1 = [SWP(-V["L_C"], 0), A1, C, Q, np.array([V["W_P"], Q[1]]), np.array([V["W_P"], V["L_L"]]),
          np.array([0, V["L_L"]]), IC, SWP(-V["L_C"], V["W_C"])]
    o_s = KC + V["RETR"] * NS; o_c = A1 + V["RETR"] * N
    a1 = inter(o_s, US, o_c, U); b1 = inter(o_c, U, np.array([V["W_P"] - V["RETR"], 0]), np.array([0.0, 1.0]))
    YC = V["L_L"] - V["D_CUNA"]
    PB = [SWP(-V["L_C"] + V["L_LAD"], V["RETR"]), a1, b1, np.array([V["W_P"] - V["RETR"], YC]),
          np.array([V["W_P"], YC]), np.array([V["W_P"], V["L_L"]]), np.array([0, V["L_L"]]), IC,
          SWP(-V["L_C"] + V["L_LAD"], V["W_C"])]
    P = lambda X, Y: T + X * U + Y * N
    return dict(T=T, U=U, N=N, A1=A1, C=C, Q=Q, KC=KC, US=US, NS=NS, SWP=SWP, P=P, P1=P1, PB=PB, IC=IC, YC=YC, xA=V["W_EXT"] - _a)


# ======================================================================== elementos (tipo, nombre, huella, z0, z1)
def elementos():
    g = planta(); V_ = V; T = g["T"]; P = g["P"]; SWP = g["SWP"]
    E = []
    def pri(nombre, poly, z0, z1, zona=""): E.append(dict(t="pri", n=nombre, p=[np.array(q, float) for q in poly], z0=z0, z1=z1, zona=zona))
    def cil(nombre, c, r, z0, z1, zona="", r0=None): E.append(dict(t="cil", n=nombre, c=np.array(c, float), r=r, r0=r0 if r0 else r, z0=z0, z1=z1, zona=zona))
    pri("planta baja", g["PB"], 0, V_["Z_PB"], "base")
    pri("planta primera", g["P1"], V_["Z_PB"], V_["Z_P1"], "base")
    xA = g["xA"]
    pri("bloque alto ala corta", [SWP(-V_["L_C"] + V_["L_LAD"], 5.5), SWP(xA - 1, 5.5), SWP(xA - 1, V_["W_C"]), SWP(-V_["L_C"] + V_["L_LAD"], V_["W_C"])], V_["Z_P1"], V_["Z_ALTO"], "Z18")
    pri("caja de ladrillo", [SWP(-V_["L_C"], 0), SWP(-V_["L_C"] + V_["L_LAD"], 0), SWP(-V_["L_C"] + V_["L_LAD"], V_["W_C"]), SWP(-V_["L_C"], V_["W_C"])], V_["Z_LAD0"], V_["Z_LAD1"], "Z19")
    yb0 = g["Q"][1]
    pri("bar", [(0, yb0), (V_["W_BAR"], yb0), (V_["W_BAR"], V_["L_L"] - V_["L_FIN"]), (0, V_["L_L"] - V_["L_FIN"])], V_["Z_P1"], V_["Z_BAR"], "Z25")
    pri("cubierta del bar", [(0, yb0), (V_["W_BAR"] + V_["V_BAR"], yb0), (V_["W_BAR"] + V_["V_BAR"], V_["L_L"] - V_["L_FIN"]), (0, V_["L_L"] - V_["L_FIN"])], V_["Z_BAR"], V_["Z_BARC"], "Z25")
    pri("peto terraza", [(V_["W_P"] - 0.3, yb0), (V_["W_P"], yb0), (V_["W_P"], V_["L_L"]), (V_["W_P"] - 0.3, V_["L_L"])], V_["Z_P1"], V_["Z_P1"] + 1.0, "Z26")
    pri("concha", [(V_["W_P"], g["Q"][1]), (V_["W_EXT"], g["Q"][1]), (V_["W_P"], g["YC"])], 0, V_["Z_CON"], "Z21")
    # torre
    cil("pie cónico", T, V_["R_COL"], 0, 4.0, "Z10", r0=V_["R_CONO"])
    cil("columna", T, V_["R_COL"], 0, V_["Z_CU0"], "Z10")
    cil("cuello", T, V_["R_CU"], V_["Z_CU0"], V_["Z_CU1"], "Z09")
    cil("ménsulas / fondo", T, V_["R_AL"], V_["Z_CU1"], V_["Z_ALE"], "Z08", r0=V_["R_CU"])
    zb1 = V_["Z_B0"] + V_["N_PL"] * V_["F"]
    cil("barril", T, V_["R_AL"], V_["Z_ALE"], zb1 + 0.65, "Z06")
    cil("tambor de ojos", T, V_["R_T"], zb1 + 0.65, V_["Z_T1"], "Z04")
    cil("banda acristalada", T, V_["R_G"], V_["Z_T1"], V_["Z_G1"], "Z03")
    cil("visera", P(V_["OV_X"], V_["OV_Y"]), V_["R_V"], V_["Z_G1"], V_["Z_V1"], "Z02")
    cil("remate", P(V_["OR_X"], 0), V_["R_R"], V_["Z_V1"], V_["Z_R1"], "Z01")
    xe = V_["ESC_X"]; y0 = T[1] + 10.0; y1 = T[1] + V_["R_AL"] + 1.0
    pri("escalera", [(xe - V_["ESC_W"] / 2, y0), (xe + V_["ESC_W"] / 2, y0), (xe + V_["ESC_W"] / 2, y1), (xe - V_["ESC_W"] / 2, y1)], 0, V_["Z_T1"] + 1.0, "Z29")
    return E, g


def niveles():
    zb1 = V["Z_B0"] + V["N_PL"] * V["F"]
    return [(0, "±0"), (V["Z_PB"], "techo PB"), (V["Z_P1"], "planta 1 / terraza"), (V["Z_BARC"], "bar / bloque alto"),
            (V["Z_CU0"], "cuello"), (V["Z_ALE"], "aletas"), (zb1, "cubierta barril"), (V["Z_T1"], "tambor"),
            (V["Z_G1"], "banda"), (V["Z_V1"], "visera"), (V["Z_R1"], "remate")]
