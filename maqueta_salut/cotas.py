"""CUADRO DE COTAS UNICO del Hotel Salut. Fuente de TODO (planos 2D y, al final, el volumen).
Cada cota: valor (m o grados) y origen. Los elementos 2D/3D se derivan de aqui, sin pasar por ningun modelo."""
import math
import numpy as np

COTAS = {
 # --- alturas de la base
 "Z_PB":   (3.2,  "techo de planta baja, única en toda la base", "F15 (época, autobús como escala)"),
 "Z_P1":   (7.2,  "coronación de planta primera = terraza (7,1 ± 0,3)", "rangos: F09 7,3 · F14 7,2 · F15 7,2 · F70 6,5"),
 "Z_BAR":  (10.5, "techo del acristalamiento del bar (vidrio +9,6…+10,5 visto tras el testero)", "F73 (escala puerta testero) 10,5 ± 0,8 · F76 maqueta ~10"),
 "Z_BARC": (11.5, "cubierta volada del bar (= bloque alto ala corta)", "F73 11,3 ± 1,1 · sección AA usuario · F76 ~10,4 (orientativa)"),
 "Z_ALTO": (11.5, "bloque alto del ala corta", "F01, sección AA del usuario"),
 "Z_LAD0": (0.0,  "el ladrillo arranca del suelo", "F72"),
 "Z_FIN":  (7.2,  "testero del ala larga: corona a la cota de la terraza (NO hay bloque alto); barandilla encima", "F73: testero +7,1 ± 0,9; lo alto que se ve detrás es el extremo del bar · F76"),
 "N_VEN": (11, "huecos fila alta", "F73 11 · F01 11 · F47 11"),
 "VEN_W": (1.6, "ancho del hueco (0,47 S)", "F73 ajuste proyectivo: hueco/intereje 0,47"),
 "VEN_FIN": (2.94, "macizo esquina testero → borde del 1er hueco (1,1 S al centro)", "F01 1,22 S · F47 1,05 S (F73 actual 2,5 S: anotado)"),
 "Z_ARC":  (3.2,  "arranque del arco bajo la rampa (hueco de la planta baja hundida)", "F47 vacío oscuro bajo la concha · F71 curva · F76 arco"),
 "U_ARC":  (0.72, "fracción de la rampa donde el arco llega al suelo", "F71 / F47 (estimado ± 0,1)"),
 "S_VEN": (3.4, "intereje de huecos del ala larga", "fila equiespaciada (F73 1,0 px, F01 1,3, F47 1,6); escala: huecos ~cuadrados (usuario) y arco a 35 m (Bing) → 2,94–3,55 → 3,4"),
 "N_VEN_B": (7, "huecos fila baja, bajo los 7 más cercanos al testero", "F01 7 · F47 7 · usuario 7"),
 "MAR_P": (0.08, "relieve del marco del hueco sobre el muro", "F73 perfiles: 0,08 / 0,07 / 0,07"),
 "MAR_B": (0.27, "banda del marco", "F73: 0,08–0,09 S"),
 "MAR_R": (0.16, "del frente del marco al vidrio (2 × relieve)", "F73 escalón interior ≈ 2× exterior · usuario"),
 "R2_L": (19.0, "rampa del techo del restaurante: desde la terraza junto a la torre (+7,2) hasta la cubierta plana del bar (+11,5)", "usuario · F76 (la cubierta baja hasta la terraza junto a la torre) · F71 (tramo inclinado junto a la torre)"),
 "Y_CA":   (55.9, "pie de la rampa de acceso − R_FIN (el pie sobre la fachada es Y_CA + R_FIN = 58,9)", "Bing 59,67 · F73: el hueco 11 se ve por encima de la rampa"),
 "R_FIN":  (3.0,  "desarrollo de la curva final de la concha (cae casi vertical arriba y se abre abajo)", "F73 (tramo alto casi vertical), F71, F47 (estimado ± 2)"),
 "ESC_Y": (22.71, "centro de la caja a lo largo del eje radial", "F58 · ESC_R0/ESC_R1"),
 "ESC_Z1": (40.5, "coronación del cuerpo de escalera: llega a la cara inferior de la visera", "F08: la caja sube por delante del tambor hasta debajo de la visera"),
 "ESC_R0": (5.65, "escalera: muro interior en arco (borde del pasillo anular)", "radio del núcleo 3,25 + pasillo 2,2 + muro"),
 "ESC_R1": (15.9, "cara exterior de la pantalla de lamas (separada 0,3 del cuerpo)", "F08, F11: lamas separadas del muro"),
 "ESC_SEC": (41.0, "hueco en el cilindro (grados) donde se interrumpen balcones y aletas", "F08: balcones acaban a 9,5° y vuelven a 50,9° de la visual"),
 "ESC_RC": (15.3, "cara exterior del cuerpo cerrado de la escalera", "F08: lamas al nivel de las puntas de las aletas"),
 "ESC_SECB": (25.0, "cuerpo de escalera en cuña (grados), centrado en el hueco, forrado de lamas", "F08: lamas de 18,5° hasta ~43° (su cara lateral se ve en escorzo) · usuario"),
 "ESC_RR": (11.0, "fachada retranqueada con ventanas a cada lado de la cuña (radio)", "F08 franja oscura 9,5°–18,5° con barandillas y huecos, ~1,6 m detrás de la línea de vidrio · F11 · usuario"),
 "H_PT": (1.0, "peto del tambor sobre el pasillo de servicio entre tambor y banda", "F08: pasillo y peto entre el tambor y la banda acristalada"),
 "R_ENT": (3.0, "abertura del peto de la terraza donde llega la rampa 1", "lógica de recorrido"),
 "RAMPA_C": (0.2, "convexidad del perfil de la rampa de acceso: z = Z_CON·(1−u)·(1+c·u); pendiente 14 % arriba, 22 % abajo", "F76 (maqueta: rampa curva desde la plaza), F47, F71"),
 "R_CURVA": (8.0, "radio exterior de la curva con la que la rampa de acceso da la vuelta a la esquina del chaflán (a +7,2)", "F76 maqueta (curva con arco debajo junto a la torre) · foto Sam Glover (cara curva bajo el barril) · foto del hotel (entrada bajo la losa)"),
 "E_PLAT": (1.0, "canto de la losa de la curva / plataforma sobre la entrada del hotel", "estimado"),
 "H_PET":  (1.3,  "peto exterior de la terraza del ala larga (corona ≈ +8,5)", "F73 esquina del testero +8,5 ± 0,6"),
 "VA_0": (4.63, "alféizar fila alta (0,545 H)", "F73 vertical exacta, 3 huecos ±0,006 H"),
 "VA_1": (6.32, "dintel fila alta (0,743 H)", "F73 vertical exacta, 3 huecos ±0,002 H"),
 "VB_0": (1.19, "alféizar fila baja (mismo alto de hueco que la alta)", "F01/F47 huecos iguales arriba y abajo"),
 "VB_1": (2.87, "dintel fila baja (0,338 H)", "F73 vertical exacta, 3 huecos ±0,002 H"),
 "L_HOR":  (6.0,  "cuerpo de hormigón sobre pilares en el extremo del ala corta", "F72 (estimado ± 2)"),
 "Z_LAD1": (10.0, "coronación de la caja de ladrillo", "F01, F19"),
 "Z_CON":  (7.2,  "llegada de la rampa de acceso a la terraza-restaurante = cota de la terraza", "lógica de recorrido · peto F09 +8,3 ± 0,8"),
 # --- torre
 "Z_CU0":  (10.4, "base del cuello", "F09"),
 "Z_CU1":  (13.9, "cara superior del cuello = cara inferior del barril (primer forjado)", "F09 14,4 ± 0,6 ajustado por coherencia con Z_B0 (pasada 7)"),
 "Z_ALE":  (15.2, "borde inferior de las aletas (fin de las ménsulas)", "F09"),
 "Z_B0":   (13.9, "primer forjado del barril", "F09 (paso 3,10)"),
 "F":      (3.10, "altura de planta del barril", "F09: dinteles cada 40 px"),
 "N_PL":   (6,    "plantas del barril (5 de ventanas + pavés)", "F09"),
 "Z_T1":   (38.2, "coronación del tambor de ojos", "F09"),
 "Z_G1":   (40.5, "coronación de la banda acristalada", "F09"),
 "Z_V1":   (43.7, "coronación de la visera", "F09"),
 "Z_R1": (50.1, "coronación del remate (sin antenas)", "F09: 6,4 m sobre el borde superior de la visera (12,9 px/m de los forjados) · antes 49,1"),
 "R_COL":  (3.25, "radio de la columna (Ø 6,5)", "F09, F14"),
 "R_CONO": (3.25, "pie de la columna: recto (lo que parecía un cono era un toldo)", "usuario; F15/F18"),
 "R_CU":   (9.0,  "radio del cuello (Ø 18)", "F01, F02"),
 "R_B":    (14.4, "radio del borde de balcones", "escala"),
 "R_AL":   (15.3, "radio a la punta de las aletas (Ø 30,6)", "escala"),
 "R_T":    (13.55,"radio del tambor de ojos (Ø 27,1)", "F01, F09, F14"),
 "R_G":    (10.85,"radio de la banda acristalada (Ø 21,7)", "F09"),
 "R_V":    (12.8, "radio de la visera (Ø 25,6)", "F09; Google 24,35"),
 "R_R": (4.95, "radio del remate", "F09 9,8 · F08 9,7 · F14 10,3 · F01 10,0 · F70 9,6 (diámetros)"),
 "OV_X": (-2.4, "desplazamiento de la visera a lo largo del chaflán", "F09 (frontal): centro de la visera 2,3–2,5 m a la izquierda del tambor + F08 (otra dirección): 1,7 m → resuelto en 2 direcciones"),
 "OV_Y": (-2.15, "desplazamiento de la visera hacia la plaza (−)", "F09 + F08 (ver OV_X); antes −4,2 (calibración C02/C04)"),
 "OR_X":   (0.6,  "desplazamiento del remate", "F09"),
 "N_AL":   (19,   "aletas / muros radiales", "fuentes + F09"),
 "ESC_W": (8.8, "largo radial de la caja (ESC_R1 − ESC_R0)", "F36 cubierta 8,3–8,8 m"),
 "ESC_X": (5.43, "eje de la escalera: radial desde el centro de la torre a lo largo del ala larga (dentro del ala)", "F58 (cenital casi vertical): la caja está en el encuentro barril–ala, dentro de la franja del ala · usuario"),
 # --- planta
 "W_P":    (12.74,"ancho del ala larga", "Bing"),
 "W_BAR":  (6.21, "ancho del bar (mitad interior)", "Bing"),
 "V_BAR":  (1.2,  "vuelo de la cubierta del bar sobre la terraza", "F47"),
 "L_L":    (94.8, "largo total del ala larga desde la calle", "Google 94,82"),
 "L_FIN":  (7.81, "tramo final sin bar: el bar llega casi al testero", "Bing (usuario) 7,81 · F73 extremo del bar tras el testero · F47 fachada acristalada del bar con barandilla a lo largo de la terraza"),
 "W_EXT":  (15.7, "ancho máximo con la concha", "Google"),
 "THL":  (95.0, "ángulo interior de la L (ala larga – calle)", "estimación por rangos: 95,0 ± 2,3° (ESTIMACIONES.md)"),
 "ACH":    (45.0, "chaflán simétrico que corta la esquina de 90°", "usuario + mapa Bing (chaflán ~ bisectriz)"),
 "REST":   (14.3, "frente del restaurante en el chaflán", "C04 calibrada"),
 "COL":    (6.5,  "columna en el chaflán", "F09"),
 "HOT":    (11.4, "frente del hotel en el chaflán", "C04 calibrada"),
 "L_CHF":  (20.0, "longitud del chaflán (reducido: la torre baja hacia la calle y deja sitio al vestíbulo)", "usuario"),
 "T_POS":  (0.536, "posición del eje de la torre sobre el chaflán (0 = calle, 1 = ala larga)", "estimación por rangos: eje a 7,3 ± 2,0 m de la fachada exterior del ala (ESTIMACIONES.md)"),
 "D_HOTF": (5.1, "la banda del hotel sigue por la fachada exterior del ala antes de la rampa", "C04: la banda acaba en x=455 (recalculado con la torre al 54 %)"),
 "RET":    (1.5,  "lo que asoma la columna delante de la planta primera", "F09/F18"),
 "RETR":   (2.5,  "retranqueo de la planta baja bajo la planta primera", "F09, F14, F47"),
 "L_C":    (24.0, "largo del ala corta desde la esquina exterior", "F01 (estimado)"),
 "W_C":    (12.74,"fondo del ala corta (igual que el ala larga)", "mapa Bing: las dos alas del mismo ancho"),
 "L_LAD":  (5.0,  "largo de la caja de ladrillo", "F01"),
}
V = {k: v[0] for k, v in COTAS.items()}
import os as _os
for _k in ("ACH", "THL"):
    if _os.environ.get(_k):
        V[_k] = float(_os.environ[_k])


# ======================================================================== geometria de planta (2D)
def planta():
    g = dict(V)
    th, a = math.radians(V["THL"]), math.radians(V["ACH"])
    LCH = V["L_CHF"]
    angC = math.pi - th - a
    _a = LCH * math.sin(angC) / math.sin(th); _c = LCH * math.sin(a) / math.sin(th)
    US = np.array([math.cos(math.pi / 2 + th), math.sin(math.pi / 2 + th)]); NS = np.array([US[1], -US[0]])
    KC = np.array([V["W_P"], 0.0]); A1 = KC + _a * US; C = KC + np.array([0, _c])
    U = (C - A1) / LCH; N = np.array([-U[1], U[0]])
    T = A1 + V["T_POS"] * LCH * U + (V["R_COL"] - V["RET"]) * N
    def SWP(x, y):             # ala corta en coordenadas "de L recta"
        return KC + (V["W_P"] - x) * US + y * NS
    def inter(p, d, q, e):
        den = d[0] * e[1] - d[1] * e[0]; s = ((q[0] - p[0]) * e[1] - (q[1] - p[1]) * e[0]) / den
        return p + s * d
    Q = C.copy()
    IC = inter(SWP(0, V["W_C"]), US, np.array([0.0, 0.0]), np.array([0.0, 1.0]))
    P1 = [SWP(-V["L_C"], 0), A1, C, Q, np.array([V["W_P"], Q[1]]), np.array([V["W_P"], V["L_L"]]),
          np.array([0, V["L_L"]]), IC, SWP(-V["L_C"], V["W_C"])]
    o_s = KC + V["RETR"] * NS; o_c = A1 + V["RETR"] * N
    a1 = inter(o_s, US, o_c, U); b1 = inter(o_c, U, np.array([V["W_P"] - V["RETR"], 0]), np.array([0.0, 1.0]))
    YC = V["Y_CA"] + V["R_FIN"]
    PB = [SWP(-V["L_C"] + V["L_LAD"], V["RETR"]), a1, b1, np.array([V["W_P"] - V["RETR"], YC]),
          np.array([V["W_P"], YC]), np.array([V["W_P"], V["L_L"]]), np.array([0, V["L_L"]]), IC,
          SWP(-V["L_C"] + V["L_LAD"], V["W_C"])]
    P = lambda X, Y: T + X * U + Y * N
    return dict(T=T, U=U, N=N, A1=A1, C=C, Q=Q, KC=KC, US=US, NS=NS, SWP=SWP, P=P, P1=P1, PB=PB, IC=IC, YC=YC, xA=V["W_P"] - _a)


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
    yb0 = max(g["Q"][1], T[1] + V_["ESC_R1"] + 0.3)          # el bar empieza detrás de la escalera
    import math as _mm
    pri("techo del restaurante en rampa", [(0, yb0), (V_["W_BAR"] + V_["V_BAR"], yb0), (V_["W_BAR"] + V_["V_BAR"], yb0 + V_["R2_L"]), (0, yb0 + V_["R2_L"])], V_["Z_P1"], V_["Z_BARC"], "Z25")
    pri("bar", [(0, yb0), (V_["W_BAR"], yb0), (V_["W_BAR"], V_["L_L"] - V_["L_FIN"]), (0, V_["L_L"] - V_["L_FIN"])], V_["Z_P1"], V_["Z_BAR"], "Z25")
    pri("cubierta del bar", [(0, yb0), (V_["W_BAR"] + V_["V_BAR"], yb0), (V_["W_BAR"] + V_["V_BAR"], V_["L_L"] - V_["L_FIN"]), (0, V_["L_L"] - V_["L_FIN"])], V_["Z_BAR"], V_["Z_BARC"], "Z25")
    pri("peto terraza", [(V_["W_P"] - 0.3, yb0), (V_["W_P"], yb0), (V_["W_P"], V_["L_L"]), (V_["W_P"] - 0.3, V_["L_L"])], V_["Z_P1"], V_["Z_P1"] + V_["H_PET"], "Z26")
    pri("concha", [(V_["W_P"], g["Q"][1]), (V_["W_EXT"], g["Q"][1]), (V_["W_P"], g["YC"])], 0, V_["Z_CON"], "Z21")
    # torre
    cil("pie cónico", T, V_["R_COL"], 0, 4.0, "Z10", r0=V_["R_CONO"])
    cil("columna", T, V_["R_COL"], 0, V_["Z_CU0"], "Z10")
    cil("cuello", T, V_["R_CU"], V_["Z_CU0"], V_["Z_CU1"], "Z09")
    cil("ménsulas / fondo", T, V_["R_AL"], V_["Z_CU1"], V_["Z_ALE"], "Z08", r0=V_["R_CU"])
    zb1 = V_["Z_B0"] + V_["N_PL"] * V_["F"]
    cil("barril", T, V_["R_AL"], V_["Z_ALE"], zb1 + 0.65, "Z06")
    cil("tambor de ojos", T, V_["R_T"], zb1 + 0.65, V_["Z_T1"], "Z04")
    cil("banda acristalada", T, V_["R_G"], V_["Z_T1"] - V_["H_PT"], V_["Z_G1"], "Z03")
    cil("visera", P(V_["OV_X"], V_["OV_Y"]), V_["R_V"], V_["Z_G1"], V_["Z_V1"], "Z02")
    cil("remate", P(V_["OR_X"], 0), V_["R_R"], V_["Z_V1"], V_["Z_R1"], "Z01")
    import math as _m
    _ang = _m.atan2(V_["ESC_Y"] - T[1], V_["ESC_X"] - T[0]); _hb = _m.radians(V_["ESC_SECB"]) / 2
    _pt = lambda r, d: (T[0] + r * _m.cos(_ang + d), T[1] + r * _m.sin(_ang + d))
    pri("escalera (cuña)", [_pt(V_["ESC_RC"], -_hb + 2 * _hb * k / 8) for k in range(9)] + [_pt(V_["ESC_R0"], _hb - 2 * _hb * k / 8) for k in range(9)], 0, V_["ESC_Z1"], "Z29")
    return E, g


def niveles():
    zb1 = V["Z_B0"] + V["N_PL"] * V["F"]
    return [(0, "±0"), (V["Z_PB"], "techo PB"), (V["Z_P1"], "planta 1 / terraza"), (V["Z_BARC"], "bar / bloque alto"),
            (V["Z_CU0"], "cuello"), (V["Z_ALE"], "aletas"), (zb1, "cubierta barril"), (V["Z_T1"], "tambor"),
            (V["Z_G1"], "banda"), (V["Z_V1"], "visera"), (V["Z_R1"], "remate")]

# Margen (±) de cada cota: medido en varias fotos ≈ 0,3-0,6 · una foto ≈ 1 · estimado ≈ 1,5-2 · satélite ≈ 1
RANGOS = {
 "Z_PB": 0.3, "Z_P1": 0.3, "Z_BAR": 0.8, "Z_BARC": 0.8, "Z_ALTO": 1.0, "Z_LAD0": 0.5, "Z_FIN": 0.9, "H_PET": 0.6, "VA_0": 0.5, "VA_1": 0.6, "VB_0": 0.3, "VB_1": 0.4, "L_HOR": 2.0,
 "Z_LAD1": 1.0, "Z_CON": 0.8, "Z_CU0": 0.6, "Z_CU1": 0.6, "Z_ALE": 0.6, "Z_B0": 0.4, "F": 0.05, "N_PL": 0,
 "Z_T1": 0.5, "Z_G1": 0.5, "Z_V1": 0.5, "Z_R1": 0.6, "R_COL": 0.3, "R_CONO": 0.3, "R_CU": 0.5, "R_B": 0.3,
 "R_AL": 0.3, "R_T": 0.5, "R_G": 0.5, "R_V": 0.6, "R_R": 0.25, "OV_X": 1.0, "OV_Y": 1.5, "OR_X": 0.5, "N_AL": 0,
 "ESC_W": 1.5, "ESC_X": 1.0, "H_PT": 0.3, "R_ENT": 1.0, "R_CURVA": 3.0, "E_PLAT": 0.3, "RAMPA_C": 0.1, "ESC_SEC": 4.0, "ESC_SECB": 4.0, "ESC_RR": 0.8, "ESC_RC": 1.0, "ESC_Y": 2.0, "ESC_Z1": 0.8, "W_P": 0.5, "W_BAR": 0.5, "V_BAR": 0.5, "L_L": 1.0, "L_FIN": 0.5, "Y_CA": 0.6, "R_FIN": 2.0, "S_VEN": 0.3, "N_VEN_B": 0, "MAR_P": 0.02, "MAR_B": 0.05, "MAR_R": 0.04, "R2_L": 3.0, "N_VEN": 0, "VEN_W": 0.2, "VEN_FIN": 1.5, "Z_ARC": 0.5, "U_ARC": 0.1, "D_CUNA": 1.0,
 "W_EXT": 1.0, "THL": 2.3, "ACH": 8.0, "REST": 1.0, "COL": 0.3, "HOT": 1.0, "L_CHF": 3.0, "T_POS": 0.1,
 "D_HOTF": 2.0, "RET": 0.5, "RETR": 0.5, "L_C": 3.0, "W_C": 1.0, "L_LAD": 1.5,
}
