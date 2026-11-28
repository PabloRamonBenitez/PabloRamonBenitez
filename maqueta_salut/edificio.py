"""Definicion del Hotel Salut SOLO con medidas de fotos y de Bing (no hereda nada del modelo 3D anterior).
Coordenadas (m): calle Ivana Mazepy = eje x (y=0, fachada a la calle del ala corta); ala larga hacia +y
(perpendicular a la calle, Bing F35/F48: 83-90 grados); cara interior del ala larga en x=0.
Fuentes de cada cota entre corchetes."""
import math
import numpy as np
from manifold3d import Manifold, CrossSection, OpType

SEG = 96
# ------------------------------------------------------------------ alturas [F09, F14]
Z_PB = 3.2          # techo planta baja, unica en toda la base   [PASADA 1: F15 época, autobús como escala]
Z_P1 = 7.3          # coronacion planta primera = terraza         [F09 7,3 / F14 7,2]
Z_BAR = 11.0        # techo del bar [coherencia: misma planta que el bloque alto del ala corta (seccion AA/BB)]
Z_BAR_C = 11.5      # cubierta volada del bar = bloque alto
Z_ALTO = 11.5       # bloque alto del ala corta                    [F01, seccion AA del usuario ~12]
Z_LADR = 9.0        # bloque de ladrillo                           [F01]
Z_CU0 = 10.4                   # cuello (base)                     [F09; se revisa en fase 4]
Z_B0, N_PL, F = 13.9, 6, 3.1   # barril: 6 plantas de 3,1 (5 con ventanas + pavés) [FASE 1: F09, dinteles cada 40 px]
Z_CU1 = 12.2                   # cara superior del cuello; encima, menculas y fondo inclinado hasta el barril [FASE 4: F02, F18, F50]
Z_ALETA0 = 15.2                # borde inferior visible de las aletas; debajo, ménsulas [F09]
Z_B1 = Z_B0 + N_PL * F         # 32,6
Z_T1 = 38.2                    # tambor de ojos                    [F09 5,4]
Z_G1 = 40.5                    # banda acristalada                 [F09 2,3]
Z_V1 = 43.7                    # visera                            [F09 3,2]
Z_R1 = 49.1                    # remate (sin antenas)              [F09 total 49,1]
# ------------------------------------------------------------------ radios / anchos [F09, F14, F01]
R_COL = 3.25        # columna 6,5                                   [F09 6,5 / F14 6,0]
R_CU = 9.0          # cuello Ø18 [FASE 4: F01 16,9 · F02 19,4 · época 0,63 D]
R_B = 14.4          # borde de balcones; aletas hasta 15,3 (30,6)   [escala]
R_AL = 15.3
R_T = 13.55         # tambor de ojos 27,1                           [F01, F09, F14]
R_G = 10.85         # banda acristalada 21,7                        [F09]
R_V = 12.8          # visera 25,6                                   [F09 25,6 / F01 25,3; Google 24,35]
R_R = 5.6           # remate 11,2                                   [F09 11,2 / F14 10,3 / F01 10,0]
OFF_V = (-0.4, -4.2)    # visera desplazada ~4,2 m hacia la plaza    [PASADA 1: ajuste conjunto C02 + C04]
OFF_R = (0.6, 0.0)      # remate casi en el eje                     [F09]
N_AL = 19               # muros radiales                            [fuentes + F09]
# ------------------------------------------------------------------ planta [Bing F36-F39 + F09]
W_P = 12.74         # ancho del ala larga                           [Bing 12,74]
W_BAR = 6.21        # bar (mitad interior)                          [Bing 6,21]
L_L = 94.8          # largo total del ala larga desde la calle      [Google 94,82]
L_FIN = 7.81        # tramo final sin bar                           [Bing 7,81]
W_EXT = 15.7        # ancho maximo con la concha                    [Google 15,7]
import os
A_CH = math.radians(float(os.environ.get("ACH", "57")))   # angulo del chaflan con la calle [provisional]
TH_L = math.radians(float(os.environ.get("THL", "112")))   # angulo interior de la L (calle - ala larga) [FASE 2: F35/F58 ~102]
# ====== FUENTE UNICA: todas las cotas se leen del CUADRO DE COTAS (cotas.py); lo de arriba queda como historial
import cotas as _K
# VERSIÓN MOLDE (SALUT_MOLDE=1): mismo edificio con el detalle que admite un molde de silicona para colar hormigón a 1:339
# (1 mm = 0,34 m): grosores ≥ 0,6 m, rendijas ≥ 0,35 m, relieves ≥ 0,25 m; sin barandillas abiertas ni lamas sueltas
MOLDE = os.environ.get("SALUT_MOLDE") == "1"
GM = 0.6 if MOLDE else None                 # grosor mínimo en la versión molde
_v = _K.V
Z_PB, Z_P1, Z_BAR, Z_BAR_C, Z_ALTO = _v["Z_PB"], _v["Z_P1"], _v["Z_BAR"], _v["Z_BARC"], _v["Z_ALTO"]
Z_CU0, Z_CU1, Z_ALETA0, Z_B0, F, N_PL = _v["Z_CU0"], _v["Z_CU1"], _v["Z_ALE"], _v["Z_B0"], _v["F"], int(_v["N_PL"])
Z_B1 = Z_B0 + N_PL * F
Z_T1, Z_G1, Z_V1, Z_R1 = _v["Z_T1"], _v["Z_G1"], _v["Z_V1"], _v["Z_R1"]
R_COL, R_CU, R_B, R_AL, R_T, R_G, R_V, R_R = _v["R_COL"], _v["R_CU"], _v["R_B"], _v["R_AL"], _v["R_T"], _v["R_G"], _v["R_V"], _v["R_R"]
RF = R_B - _v["BAL_P"]


def niveles_suelo():
    """FUENTE ÚNICA de las cotas de suelo del barril (cara superior de cada forjado = suelo de habitación y de balcón):
    1.ª planta sobre el fondo plano (Z_BI + canto), resto sobre cada canto (Z_B0 + i·F + canto), la última es la cubierta.
    La usan los forjados de las secciones, la escalera (rellanos de planta), el 3D y la auditoría [usuario 26/11]."""
    FC_ = _v["FOR_C"]
    return [_v["Z_BI"] + FC_] + [Z_B0 + i * F + FC_ for i in range(1, N_PL + 1)]                     # fachada de ventanas de las habitaciones (balcón de BAL_P) [usuario 26/11]
OFF_V, OFF_R, N_AL = (_v["OV_X"], _v["OV_Y"]), (_v["OR_X"], _v["OR_Y"]), int(_v["N_AL"])
FASE_AL = math.radians(_v.get("FASE_AL", 0.0))   # giro del módulo radial [MGF Alamy]
OFF_B = (_v["OB_X"], _v["OB_Y"])
W_P, W_BAR, L_L, L_FIN, W_EXT = _v["W_P"], _v["W_BAR"], _v["L_L"], _v["L_FIN"], _v["W_EXT"]
Y_CUNA = _v["Y_CA"] + _v["R_FIN"]           # pie de la concha sobre la fachada (≈ Bing 59,67)
A_CH, TH_L = math.radians(_v["ACH"]), math.radians(_v["THL"])
REST, COL, HOT = _v["REST_L"], _v["COL"], _v["HOT_L"]
L_CH = _v["L_CHF"]                          # chaflan reducido [usuario]
KC = (W_P, 0.0)                             # esquina exterior de la L: un solo chaflan que muere en la fachada del ala larga [usuario: sin doble chaflán]
PHI = TH_L - math.pi / 2                    # giro de la calle respecto a la posicion perpendicular
US = (math.cos(math.pi / 2 + TH_L), math.sin(math.pi / 2 + TH_L))   # direccion de la calle hacia el ala corta
NS = (US[1], -US[0])                        # normal hacia dentro de la calle
_angC = math.pi - TH_L - A_CH               # triangulo KC-A1-C (ley de senos)
_a = L_CH * math.sin(_angC) / math.sin(TH_L)
_c = L_CH * math.sin(A_CH) / math.sin(TH_L)
A1 = (KC[0] + _a * US[0], KC[1] + _a * US[1])   # arranque del chaflan en la calle
C = (KC[0], KC[1] + _c)                     # fin del chaflan en el borde exterior de la concha
U = ((C[0] - A1[0]) / L_CH, (C[1] - A1[1]) / L_CH)
N = (-U[1], U[0])                           # hacia dentro
RET = _v["RET"]           # la columna asoma por delante de la planta primera [F09/F18]
RETR = _v["RETR"]          # retranqueo de la planta baja bajo la planta primera [F09, F14, F47]
_k = _v["T_POS"] * L_CH                     # eje de la torre sobre el chaflan, algo a la derecha [usuario]
T = (A1[0] + _k * U[0] + (R_COL - RET) * N[0], A1[1] + _k * U[1] + (R_COL - RET) * N[1])   # eje de la torre
L_C, W_C = _v["L_C"], _v["W_C"]       # ala corta: extremo de la calle en x=-L_C, fondo 12   [F01, estimado]
D_FAR = W_EXT + L_C         # longitud de la fachada a la calle desde la esquina exterior


def SWP(x, y):
    """punto del ala corta dado en coordenadas 'de L recta' (x hacia -calle, y hacia dentro) -> planta real"""
    s, t = W_P - x, y
    return (KC[0] + s * US[0] + t * NS[0], KC[1] + s * US[1] + t * NS[1])


def _inter(p, d, q, e):
    den = d[0] * e[1] - d[1] * e[0]
    s = ((q[0] - p[0]) * e[1] - (q[1] - p[1]) * e[0]) / den
    return (p[0] + s * d[0], p[1] + s * d[1])
L_LADR = _v["L_LAD"]                # bloque de ladrillo del extremo, sobre pilares       [F01]
# escalera: SECTOR del cilindro (≈ 2 módulos): muros radiales hacia el centro, cerrada hasta la fachada del
# barril y tramos al aire tras una pantalla de lamas en el arco exterior; cubierta en cuña [usuario; F08, F11, F58, F36]
ESC_ANG = math.pi / 2                                                 # eje del sector: paralelo al ala, desde el eje de la torre [F58]
ESC_R0, ESC_R1, ESC_RC = _v["ESC_R0"], _v["ESC_R1"], _v["ESC_RC"]
ESC_HA = math.radians(_v["ESC_SEC"]) / 2                             # semiángulo
ESC_W = ESC_R1 - ESC_R0
ESC_HB = math.radians(_v["ESC_SECB"]) / 2                            # semiángulo del cuerpo en cuña
ESC_WY = 2 * ESC_R1 * math.sin(ESC_HB)                               # cuerda exterior del cuerpo


def esc_ang_pt(r, da):
    """punto a radio r y ángulo ESC_ANG + da desde el eje de la torre"""
    return (T[0] + r * math.cos(ESC_ANG + da), T[1] + r * math.sin(ESC_ANG + da))


def esc_pt(r, v):
    """compatibilidad: v = desplazamiento perpendicular (aprox. con ángulo v/r)"""
    return esc_ang_pt(r, v / max(r, 1e-6))


def esc_sector_poly(r0, r1, n=16):
    arco1 = [esc_ang_pt(r1, -ESC_HA + 2 * ESC_HA * k / n) for k in range(n + 1)]
    arco0 = [esc_ang_pt(r0, ESC_HA - 2 * ESC_HA * k / n) for k in range(n + 1)]
    return arco1 + arco0


ESC_POLY = esc_sector_poly(ESC_R0, ESC_R1, 6)
ESC_Y0 = min(p[1] for p in ESC_POLY); ESC_Y1 = max(p[1] for p in ESC_POLY)    # solo para encuadres


def P(X, Y):
    """coordenadas de torre (X a lo largo del chaflan, Y hacia dentro) -> planta"""
    return (T[0] + X * U[0] + Y * N[0], T[1] + X * U[1] + Y * N[1])


def caja(x0, x1, y0, y1, z0, z1):
    return Manifold.cube((x1 - x0, y1 - y0, z1 - z0)).translate((x0, y0, z0))


def prisma(poly, z0, z1):
    return Manifold.extrude(CrossSection([poly]), z1 - z0).translate((0, 0, z0))


def cil(c, r, z0, z1, seg=SEG):
    return Manifold.cylinder(z1 - z0, r, r, seg).translate((c[0], c[1], z0))

def baranda(c, r, z0, h, paso=2.0):
    """barandilla ABIERTA (transparente en las fotos): pasamanos + travesaño + postes cada ~2 m [Alamy: se ve a través]"""
    if MOLDE: return Manifold()                                 # molde: una barandilla abierta no se puede colar en hormigón
    n = max(int(2 * math.pi * r / paso), 8)
    ps = [Manifold.cube((0.09, 0.09, h)).translate((r - 0.1, -0.045, z0)).rotate((0, 0, 360 * k / n)) for k in range(n)]
    anillo = lambda za, ha: cil(c, r, za, za + ha) - cil(c, r - 0.07, za - 0.1, za + ha + 0.1)
    out = anillo(z0 + h - 0.07, 0.07) + anillo(z0 + 0.5, 0.07)
    for p in ps: out = out + p.translate((c[0], c[1], 0))
    return out



def plantas_base():
    """poligonos de planta baja y planta primera (definicion unica), con L de angulo interior TH_L"""
    t = 0.0                            # sin cara a 90 grados: el chaflan llega directo a la fachada del ala
    Q = (C[0] + t * N[0], C[1] + t * N[1])
    F0 = SWP(-L_C, 0.0); F1 = SWP(-L_C, W_C)
    IC = _inter(SWP(-L_C, W_C), U, (0.0, 0.0), (0.0, 1.0))         # línea posterior del ala corta paralela al chaflán: sin 90° [usuario]
    g = _K.planta()
    ARC = [tuple(p) for p in g["ARC"]]
    P1 = [F0, A1, C] + ARC + [(W_P, g["YS"]), (W_P, L_L), (0.0, L_L), IC, F1]     # el chaflán sigue hasta E90 [F09, usuario]
    o_s = (KC[0] + RETR * NS[0], KC[1] + RETR * NS[1])            # paralela retranqueada a la calle
    o_c = (A1[0] + RETR * N[0], A1[1] + RETR * N[1])              # paralela retranqueada al chaflan
    a1 = _inter(o_s, US, o_c, U)
    b1 = _inter(o_c, U, (W_P - RETR, 0.0), (0.0, 1.0))
    y_arc = Q[1] + _v["D_HOTF"] + _v["U_ARC"] * (Y_CUNA - Q[1] - _v["D_HOTF"])   # la PB en sombra solo bajo el arco; después muro ciego [usuario 26/11]
    PB = [SWP(-L_C, RETR), a1, b1, (W_P - RETR, y_arc), (W_P, y_arc), (W_P, L_L),
          (0.0, L_L), IC, SWP(-L_C, W_C)]
    return dict(P1=P1, PB=PB, Q=Q, IC=IC)


def bloque_alto_poligono(n=16):
    """planta del bloque alto del ala corta (real): de la medianera, con el cuerpo volado VOL_V sobre la calle en
    VOL_L m; lado inclinado paralelo al chaflán; remate hacia la torre en arco cóncavo equidistante al tambor (R_AC)
    hasta la fachada posterior (línea A) [croquis del usuario, foto frontal, foto al pie de la torre]"""
    US_, NS_ = np.array(US), np.array(NS); Uv = np.array(U); Tv = np.array(T)
    d = np.array([-(Uv @ US_), Uv @ NS_])
    if d[1] < 0: d = -d
    sw = lambda q: np.array(SWP(q[0], q[1]))
    x0 = -L_C; P1 = np.array([x0 + _v["VOL_L"], -_v["VOL_V"]])
    # C: sobre el lado inclinado (paralelo al chaflán) a distancia A–C de A (esquina del vuelo en la medianera) [triangulación]
    A0 = np.array([x0, -_v["VOL_V"]]); w = P1 - A0
    tC = -(w @ d) + math.sqrt((w @ d) ** 2 - (w @ w) + _v["AC_TRI"] ** 2)
    Rc = float(np.linalg.norm(sw(P1 + tC * d) - Tv)) + 1e-6; _v["R_AC"] = Rc; tip = None
    for t in np.linspace(0, 60, 6001):
        q = P1 + t * d
        if q[1] >= W_C: break
        if np.linalg.norm(sw(q) - Tv) <= Rc: tip = q; break
    pts = [sw((x0, -_v["VOL_V"])), sw(P1)]
    if tip is None:
        tq = P1 + (W_C - P1[1]) / d[1] * d
        pts += [sw(tq), sw((x0, W_C))]
        return [tuple(p) for p in pts]
    a0 = math.atan2(*(sw(tip) - Tv)[::-1])
    xs = np.linspace(tip[0], x0, 4000); qr = None
    for x in xs:
        if np.linalg.norm(sw((x, W_C)) - Tv) >= Rc: qr = np.array([x, W_C]); break
    a1 = math.atan2(*(sw(qr) - Tv)[::-1])
    if a1 - a0 > math.pi: a1 -= 2 * math.pi
    if a0 - a1 > math.pi: a1 += 2 * math.pi
    arc = [Tv + Rc * np.array([math.cos(a0 + (a1 - a0) * k / n), math.sin(a0 + (a1 - a0) * k / n)]) for k in range(n + 1)]
    pts += [sw(tip)] + arc[1:] + [sw((x0, W_C))]
    return [tuple(p) for p in pts]


def curva_poligono():
    """meseta de la esquina a +Z_P1 (cubierta de la prolongación del chaflán): C → E90 → curva → (W_EXT, yS) → (W_P, yS);
    borde con peto: sobre la banda del hotel (C→E90) y a lo largo de la curva"""
    g = _K.planta()
    ARC = [tuple(p) for p in g["ARC"]]
    poly = [tuple(g["C"])] + ARC + [(W_P, g["YS"])]
    borde = [tuple(g["C"])] + ARC
    return poly, borde


def plataforma_curva():
    from shapely.geometry import LineString, Polygon as SP
    from shapely.geometry.polygon import orient
    poly, borde = curva_poligono()
    P = orient(SP(poly).buffer(0), 1.0)
    out = []
    for side in (True, False):
        g = LineString(borde).buffer((GM or 0.25) if side else -(GM or 0.25), single_sided=True).intersection(P)
        if g.area > 1.0:
            for gm in getattr(g, "geoms", [g]):
                if gm.geom_type == "Polygon" and gm.area > 0.05:
                    gm = orient(gm, 1.0)
                    out.append(prisma(list(gm.exterior.coords)[:-1], Z_P1 - 0.01, Z_P1 + 1.0))       # peto 1 m
            break
    # final del giro: el peto se cierra en U (∩) en el extremo junto a la columna [F78, curvas azules del usuario]
    from shapely.geometry import LineString as _LS
    g = _K.planta(); C_ = np.array(g["C"]); E9 = np.array(g["E90"])
    d = (E9 - C_) / np.linalg.norm(E9 - C_); n = np.array(N); w = _v["GIRO_W"]
    th = np.linspace(0, math.pi, 24)
    cen = C_ + n * w / 2
    arco = [tuple(cen - n * (w / 2) * math.cos(t) - d * (w / 2) * math.sin(t)) for t in th]
    lin = _LS(arco + [tuple(C_ + n * w + d * _v["GIRO_L"])])
    u_ = orient(lin.buffer(0.125, cap_style=2), 1.0)
    out.append(prisma(list(u_.exterior.coords)[:-1], Z_P1 - 0.01, Z_P1 + 1.0))
    return out


def base():
    pl = plantas_base()
    s = [prisma(pl["PB"], 0, Z_PB + 0.01), prisma(pl["P1"], Z_PB, Z_P1)]
    xA = W_P - _a                     # arranque del chaflan en coordenadas 'de L recta'
    def ROT(m):                          # coordenadas 'de L recta' -> planta real (giro de la calle alrededor de KC)
        return m.translate((-KC[0], -KC[1], 0)).rotate((0, 0, math.degrees(PHI))).translate((KC[0], KC[1], 0))
    sc = []
    # ala corta: bloque alto (planta 2) con cuerpo volado sobre la calle y remate curvo hacia la torre; planta 1 con
    # logia bajo el vuelo junto a la medianera [croquis del usuario, foto frontal del ala corta]
    from shapely.geometry import Polygon as _SP
    from shapely.geometry.polygon import orient as _or
    ba = list(_or(_SP(bloque_alto_poligono()).buffer(0), 1.0).exterior.coords)[:-1]
    s.append(prisma(ba, _v["Z_VOL0"], Z_ALTO))
    # 10 lucernarios en diente de sierra sobre la cubierta de planta 1 del ala corta: 5 en línea y 5 en otra
    # disposición (escalonados) [F01 1984, usuario 26/11]
    def diente(x, y):
        perfil = CrossSection([[(0.0, 0.0), (1.6, 0.0), (0.0, 1.0)]])          # cara vertical acristalada + faldón inclinado
        if perfil.area() <= 0: perfil = CrossSection([[(0.0, 0.0), (0.0, 1.0), (1.6, 0.0)]])
        return Manifold.extrude(perfil, 1.6).rotate((90, 0, 0)).translate((x - 0.8, y + 0.8, Z_P1 - 0.01))
    # 10 LUCERNARIOS PIRAMIDALES sobre la cubierta del bloque alto, junto a la medianera [F01 1984: «se ven distintos», son
    # pirámides de base cuadrada, no dientes de sierra · usuario 27/11]. Disposición H1, DECIDIDA POR EL USUARIO (27/11, duda 8):
    # dos filas de 5 paralelas a la medianera, la 2.ª a tresbolillo
    def piramide(x, y):
        b_, h_ = _v["PIR_B"], _v["PIR_H"]
        return Manifold.extrude(CrossSection.square((b_, b_), True), h_, 0, 0.0, (0.0, 0.0)).translate((x, y, Z_ALTO - 0.01))
    x1_ = -L_C + 0.6 + _v["PIR_B"] / 2; S_ = _v["PIR_S"]
    for i in range(5):
        sc.append(piramide(x1_, 0.9 + S_ * i))                                # fila 1, junto a la medianera
        sc.append(piramide(x1_ + S_, 0.9 + S_ / 2 + S_ * i))                 # fila 2, a tresbolillo
    s.append(ROT(Manifold.batch_boolean(sc, OpType.Add)))
    # ala larga: bar en la mitad interior hasta el tramo final; terraza con peto en la mitad exterior [F47, Bing]
    yb0 = pl["Q"][1] + _v["R2_Y0"]                                      # arranca tras el vuelo del cuello (rellano del giro en U delante) [usuario 26/11]
    yb1 = L_L - L_FIN                                                   # 1984: el bar acaba sobre la 1a ventana [F01, F47]
    yr1 = yb0 + _v["R2_L"]                                              # fin de la rampa-cubierta
    s += [caja(0, W_BAR, yr1 - 0.01, yb1, Z_P1 - 0.01, Z_BAR),
          caja(0, W_BAR + _v["V_BAR"], yr1 - 0.01, yb1 + _v["V_BAR"], Z_BAR, Z_BAR_C),     # cubierta plana volada en frente y extremo
          *([] if MOLDE else [caja(0, 0.1, yb1, L_L, Z_P1 - 0.01, Z_P1 + 1.1)]),   # barandilla borde patio de la terraza abierta [F47]
          caja(W_P - (GM or 0.3), W_P, pl["Q"][1] + _v["D_HOTF"], L_L, Z_P1 - 0.01, Z_P1 + _v["H_PET"]),  # peto exterior [F73 +8,5] (la meseta de la esquina abre a la terraza)
          *([] if MOLDE else [caja(0, W_P - 0.3, L_L - 0.25, L_L - 0.15, _v["Z_FIN"] - 0.01, _v["Z_FIN"] + 1.1)])]   # testero a cota terraza + barandilla [F73]
    # concha: franja exterior que se estrecha de W_EXT a W_P hasta Y_CUNA; alta junto al hotel (+7,3) y baja en
    # curva al suelo; debajo, planta baja hundida [F47, F09, Bing]
    y0 = pl["Q"][1] + _v["D_HOTF"]          # la concha empieza tras la banda del hotel sobre la fachada del ala [C04]
    # RAMPA (F71): plano inclinado de ancho constante pegado a la fachada exterior del ala; sube desde el suelo
    # (lejos de la torre) hasta la terraza de la planta primera junto a la banda del hotel; peto en el borde exterior.
    WR = W_EXT - W_P
    # RAMPA DE ACCESO PÚBLICO A LA TERRAZA-RESTAURANTE (+Z_P1): nace en la plaza junto a los huecos del ala (pie en
    # Y_CUNA ≈ Bing 59,67) y sube HACIA LA TORRE hasta la terraza, con perfil curvo convexo [F76, F47, F71, F01];
    # vista desde el testero (F73) su pendiente de ~40 m se ve en escorzo como una "curva" corta.
    YB = Y_CUNA; LR = YB - y0; C_ = _v["RAMPA_C"]
    Y_ARC = y0 + _v["U_ARC"] * (Y_CUNA - y0)
    def zr(yy):
        u = min(max((yy - y0) / LR, 0.0), 1.0)
        return max(0.05, _v["Z_CON"] * (1 - u))                            # rampa RECTA: pendiente constante por donde suben los coches [usuario 28/11]
    def zs(yy):         # intradós del arco bajo la rampa junto al hotel (paso en planta baja) [F47, F71, F76]
        if yy >= Y_ARC: return 0.0
        u = (yy - y0) / (Y_ARC - y0); ud = _v["ARC_D"]                 # horizontal hasta ARC_D y curva al suelo [G3, usuario]
        w = 0.0 if u <= ud else (u - ud) / (1 - ud)
        return max(0.0, min(_v["Z_ARC"] * (1 - w), zr(yy) - 0.6))          # intradós recto (antes curvo): la rampa no tiene línea curva [usuario 28/11]
    def f(v):
        x, y, z = v
        yy = y0 + min(max(y, 0.0), 1.0) * LR
        lo, hi = zs(yy), zr(yy)
        xi = W_P - _v["FAC_R"] - 0.3                     # la rampa entra 0,3 en la fachada de ventanas retranqueada: unida al edificio, sin rendija [usuario 28/11]
        return (xi + x * (W_EXT - xi), yy, lo + z * (hi - lo))
    rampa = Manifold.cube((1, 1, 1)).refine(60).warp(f)
    yp = y0                                                                       # el peto de la rampa sigue al de la curva
    def fp(v):
        x, y, z = v
        yy = yp + min(max(y, 0.0), 1.0) * (YB - yp)
        pe_ = GM or 0.25
        return (W_P + WR - pe_ + x * pe_, yy, zr(yy) - 0.01 + z * _v["H_PET"])   # peto como el de la terraza (+8,50 junto al hotel)
    peto = Manifold.cube((1, 1, 1)).refine(40).warp(fp)
    s += [rampa, peto]
    # ESQUINA [usuario, F09, F18]: la rampa abre hacia fuera en curva y llega a 90° al chaflán prolongado (E90);
    # la meseta a +Z_P1 es la cubierta de esa prolongación (hotel debajo); peto en la curva y sobre la banda del hotel
    s += plataforma_curva()
    # EL TECHO DEL RESTAURANTE EMPIEZA EN RAMPA [usuario, F76, F71]: junto a la torre la cubierta del bar nace a la
    # cota de la terraza (+Z_P1) y sube en rampa, en todo el ancho de la cubierta, hasta la cubierta plana (+Z_BARC);
    # debajo, el restaurante con techo inclinado. Se sube a la azotea andando por la propia cubierta.
    WB = W_BAR + _v["V_BAR"]
    def fw(v):                                   # cuerpo del restaurante bajo el techo inclinado: solo hasta la fachada (W_BAR)
        x, y, z = v
        u = min(max(y, 0.0), 1.0)
        zt = Z_P1 + u * (Z_BAR_C - Z_P1)
        return (x * W_BAR, yb0 + u * (yr1 - yb0), Z_P1 - 0.01 + z * (zt - Z_P1 + 0.01))
    eb = Z_BAR_C - Z_BAR                         # canto de la cubierta
    def fv(v):                                   # vuelo del techo inclinado: LOSA (debajo, terraza abierta), no macizo
        x, y, z = v
        u = min(max(y, 0.0), 1.0)
        zt = Z_P1 + u * (Z_BAR_C - Z_P1)
        return (W_BAR - 0.01 + x * (WB - W_BAR + 0.01), yb0 + u * (yr1 - yb0), max(Z_P1 - 0.01, zt - eb) + z * (zt - max(Z_P1 - 0.01, zt - eb)))
    cuna = Manifold.cube((1, 1, 1)).refine(30).warp(fw) + Manifold.cube((1, 1, 1)).refine(30).warp(fv)
    # el restaurante y su vuelo ACABAN CONTRA EL PIE DE LA CAJA DE ESCALERA (cuña ±ESC_HB hasta la celosía): una línea común,
    # sin solapes ni astillas entre los dos cuerpos [usuario 26/11: «ese punto es muy raro»]
    _n = 16
    _pp = [esc_ang_pt(ESC_RC + 0.3, -ESC_HB + 2 * ESC_HB * k / _n) for k in range(_n + 1)] + \
          [esc_ang_pt(ESC_R0, ESC_HB - 2 * ESC_HB * k / _n) for k in range(_n + 1)]
    _cs = CrossSection([_pp]); _cs = _cs if _cs.area() > 0 else CrossSection([_pp[::-1]])
    PIE_ESC = Manifold.extrude(_cs, 30.0).translate((0, 0, 0.0))
    cuna = cuna - PIE_ESC
    def barand(x0_):
        def g(v):
            x, y, z = v
            u = min(max(y, 0.0), 1.0)
            zt = Z_P1 + u * (Z_BAR_C - Z_P1)
            return (x0_ + x * 0.1, yb0 + u * (yr1 - yb0), zt - 0.01 + z * 1.0)
        return Manifold.cube((1, 1, 1)).refine(20).warp(g)
    s += [cuna] + ([] if MOLDE else [barand(WB - 0.1), barand(0.0),
          caja(0, WB, yb1 + _v["V_BAR"] - 0.1, yb1 + _v["V_BAR"], Z_BAR_C - 0.01, Z_BAR_C + 1.0),    # barandilla azotea (extremo)
          caja(WB - 0.1, WB, yr1 - 0.01, yb1 + _v["V_BAR"], Z_BAR_C - 0.01, Z_BAR_C + 1.0),           # lado largo (F73 barandilla roja)
          caja(0, 0.1, yr1 - 0.01, yb1 + _v["V_BAR"], Z_BAR_C - 0.01, Z_BAR_C + 1.0)])                # lado patio
    m = Manifold.batch_boolean(s, OpType.Add)
    # huecos de ventanas (franjas continuas casi a paño) [F09, F14]
    hue = []
    # logia de planta 1 bajo el vuelo: hueco retranqueado LOG_D entre muro de medianera (0,6), pilar (0,7) y muro final (0,25)
    ld, lx = _v["LOG_D"], _v["LOG_PX"]; x0l = -L_C
    lx0, lx1 = x0l + _v["LOG_X0"], x0l + _v["LOG_X1"]
    m = m - ROT(caja(lx0, lx1, -1, ld, Z_PB + 0.01, Z_P1 - 0.01))
    m = m + ROT(caja(x0l + lx - 0.35, x0l + lx + 0.35, 0, ld, Z_PB, Z_P1))                       # pilar intermedio
    m = m + ROT(caja(lx0, lx1, 0, GM or 0.25, Z_PB, Z_PB + 1.0))                                 # antepecho / poyete
    # puertas del hotel en planta baja junto a la columna [usuario, F18]
    for hh in __import__("ventanas").catalogo():
        if hh["grupo"] in ("hotel puertas PB", "bloque alto posterior", "cristalera PB concha", "chaflán PB cristalera", "ala corta garaje"):
            if hh["grupo"] == "chaflán PB cristalera": continue                    # cristalera a paño que hace esquina: sin hueco, ni en molde ni en detalle [usuario 28/11]
            a = math.degrees(math.atan2(hh["n"][1], hh["n"][0]))
            pr_ = {"chaflán PB cristalera": 0.12, "ala corta garaje": _v["GAR_P"]}.get(hh["grupo"], 0.6)   # fondo del hueco hacia dentro
            b = Manifold.cube((pr_ + 0.6, hh["w"], hh["z1"] - hh["z0"])).translate((-pr_, -hh["w"] / 2, hh["z0"]))
            hue.append(b.rotate((0, 0, a)).translate((hh["p"][0], hh["p"][1], 0)))
    # HUECOS DEL ALA LARGA (pasada 11, proporciones F73/F01/F47): 11 arriba, 7 abajo bajo los 7 más cercanos al
    # testero, intereje S_VEN, hueco 0,47 S; marco que sale MAR_P y vidrio MAR_R por detrás del frente del marco
    import ventanas as VT                                # catálogo único de huecos (mismo que planos)
    p_, rr_, bd = _v["MAR_P"], _v["MAR_R"], _v["MAR_B"]
    XF = W_P - _v["FAC_R"]                                # fachada de ventanas retranqueada 0,80 bajo el canto volado [usuario 26/11]
    # empieza donde la rampa ya tapa toda la altura bajo la banda (sin línea vertical sobre la rampa) y llega hasta el testero:
    # sin muro de canto ni «tacón» en la esquina; la banda superior vuela FAC_R también en la esquina [usuario 22/11, 23/11, 27/11]
    _y0r = plantas_base()["Q"][1] + _v["D_HOTF"]
    _yrc = _y0r + (Y_CUNA - _y0r) * (1 - (Z_P1 - _v["FAC_B"]) / _v["Z_CON"]) ** (1 / _v["RAMPA_P"])
    m = m - (caja(XF, W_P + 0.05, _yrc, L_L + 0.05, -0.1, Z_P1 - _v["FAC_B"]) - rampa)   # el retranqueo corta el muro, no la rampa: sin rendija junto al edificio [usuario 28/11]
    marcos = []
    for h in VT.catalogo():
        if not h["grupo"].startswith("ala larga"): continue
        y0_, y1_ = h["p"][1] - h["w"] / 2, h["p"][1] + h["w"] / 2; z0, z1 = h["z0"], h["z1"]
        if not MOLDE: marcos.append(caja(XF - 0.01, XF + p_, y0_ - bd, y1_ + bd, z0 - bd, z1 + bd))   # molde: sin marcos (relieve 0,08)
        if not MOLDE: marcos.append(caja(XF - 0.01, XF + p_ + 0.06, y0_ - bd - 0.05, y1_ + bd + 0.05, z0 - bd - 0.1, z0 - bd))  # alféizar con goterón
        hue.append(caja(XF + p_ - rr_, XF + 1, y0_, y1_, z0, z1))                 # hueco hasta el vidrio
    # testero: puerta de servicio con marquesina saliente y ventana encima [F73: a 0,49-0,63 del ancho desde la esquina exterior]
    hue.append(caja(W_P - 0.63 * W_P, W_P - 0.49 * W_P, L_L - 0.3, L_L + 1, 0.0, 2.6))
    hue.append(caja(W_P - 0.55 * W_P, W_P - 0.43 * W_P, L_L - 0.3, L_L + 1, 4.6, 5.3))
    px0, px1, pd, pe = _v["POR_X0"], _v["POR_X1"], _v["POR_D"], max(_v["POR_E"], GM or 0)
    marcos += [caja(px0, px0 + pe, L_L - 0.01, L_L + pd, 0.0, 4.4),                  # porche: muros a los lados de la puerta [usuario, F73]
               caja(px1 - pe, px1, L_L - 0.01, L_L + pd, 0.0, 4.4),
               caja(px0, px1, L_L - 0.01, L_L + pd, 4.0, 4.4),                         # marquesina sobre los muros
               *([caja(W_P - 0.3, W_P, L_L - 0.01, L_L + _v["ESQ_D"], 0.0, _v["Z_FIN"] + 1.1)] if _v["ESQ_D"] > 0.01 else [])]   # muro de esquina (quitado: ESQ_D = 0)
    m = m + Manifold.batch_boolean(marcos, OpType.Add)
    m = m - Manifold.batch_boolean(hue, OpType.Add)
    # chaflan (coordenadas de torre): franjas de ventanas restaurante / hotel
    rot = math.degrees(math.atan2(U[1], U[0]))
    def en_torre(mm):
        return mm.rotate((0, 0, rot)).translate((T[0], T[1], 0))
    yf = -(R_COL - RET)
    # FASE 3 (F50 con personas como escala, F09): seccion de las bandas del chaflan
    #   restaurante: PB hasta +4,5 (toldos) · vidrio +4,6/+6,4 · rotulo hasta +7,3
    #   hotel: puertas 2,3 · PB hasta +3,1 · canto de hormigon volado +3,1/+4,3 · vidrio +4,3/+6,0 · rotulo
    xr0, xr1 = -_k, -R_COL
    xh0, xh1 = R_COL, R_COL + HOT + 3.0
    # (sin «sofito a +4,5»: salía de los toldos de F50, que no son arquitectura [usuario 22/11 y 26/11]: banda plana sobre la PB)
    hue_t = [caja(xr0 + 0.4, xr1 - 0.3, yf - 1, yf + 0.3, 4.6, 6.4)]                            # vidrio restaurante
    xh1 = R_COL + _v["HOT_L"]                                                                      # hotel: de la columna a E90 [F09, F18]
    m = m + en_torre(caja(xh0, xh1, yf - 0.3, yf + 2.0, 3.1, 4.3))
    hue_t.append(caja(xh0 + 0.3, xh1 - 0.4, yf - 1, yf + 0.3, 4.35, 6.0))
    m = m - en_torre(caja(xh0 + 0.5, xh1 - 0.3, yf - 1, yf + RETR, -1, 3.12))                      # entrada del hotel bajo la banda (sin caras coplanarias)
    m = m - en_torre(Manifold.batch_boolean(hue_t, OpType.Add))
    # montantes entre paños: se leen las 5 y pico ventanas del restaurante y las 4 y pico del hotel [F09, F18, usuario]
    import ventanas as VTc
    mont = []
    for hh in VTc.catalogo():
        if not hh["grupo"].startswith("chaflán"): continue
        t_ = np.array(hh["t"]); n_ = np.array(hh["n"]); p_ = np.array(hh["p"])
        for s_ in (-1, 1):
            c_ = p_ + t_ * s_ * (hh["w"] / 2 + 0.075)              # montante sobre el paño: sale 0,15 y entra 0,15 en el muro
            mt = Manifold.cube((0.15, 0.3, hh["z1"] - hh["z0"])).translate((-0.075, -0.15, hh["z0"]))
            mont.append(mt.rotate((0, 0, math.degrees(math.atan2(t_[1], t_[0])))).translate((c_[0], c_[1], 0)))
    # cristalera PB del chaflán: no hay hueco; la vidriera es una piel de 0,12 a paño de la fachada que hace esquina [usuario 28/11]
    glas = []
    if not MOLDE:                                               # molde: el vidrio no se cuela (como antes)
        for hh in VTc.catalogo():
            if hh["grupo"] != "chaflán PB cristalera": continue
            a = math.degrees(math.atan2(hh["n"][1], hh["n"][0]))
            # de suelo a +3,20: la planta baja llega a +3,10 bajo el canto del hotel (cotas: PB hasta +3,1); solapa 0,1 con el canto
            g_ = Manifold.cube((0.12, hh["w"] + 0.3, 3.2 + 0.05)).translate((-0.12, -(hh["w"] + 0.3) / 2, -0.05))
            glas.append(g_.rotate((0, 0, a)).translate((hh["p"][0], hh["p"][1], 0)))
    return m if MOLDE else m + Manifold.batch_boolean(mont + glas, OpType.Add)




def lucernarios_cuello():
    """6 lucernarios piramidales pequeños sobre la terraza a +Z_P1, pegados a la columna bajo el cuello, desde donde llega
    la rampa de la concha hasta debajo de la escalera (juntos ≈ 75°) [usuario 26/11, F78]. Devuelve [dict(c, a, l, h, z)]."""
    out = []
    for a in np.radians(np.linspace(_v["LUC_A0"], _v["LUC_A1"], 6)):
        out.append(dict(c=(T[0] + _v["LUC_CR"] * math.cos(a), T[1] + _v["LUC_CR"] * math.sin(a)), a=float(a),
                        l=_v["LUC_CL"], h=_v["LUC_CH"], z=Z_P1))
    return out

def letrero():
    """letrero САЛЮТ en ARCO alrededor del remate, repetido dos veces (palabra 1 hacia Alamy, palabra 2 hacia F09),
    letras en planos tangentes a radio R_R + SIG_R [usuario 22/11 «letras circulares alrededor»; Alamy, F09, F08, F01, F19].
    Devuelve [dict(ch, c=(x,y) centro en planta, rot=grados de la normal (radial hacia fuera), w, z0, z1)] – 3D y planos."""
    pr = P(_v["OR_X"], _v["OR_Y"]); r = R_R + _v["SIG_R"]; da = _v["SIG_AW"] / 5; out = []
    for a0 in (_v["SIG_A0"], _v["SIG_A1"]):
        for i, ch in enumerate("САЛЮТ"):
            a = math.radians(a0 + (i + 0.5) * da)
            out.append(dict(ch=ch, c=(pr[0] + r * math.cos(a), pr[1] + r * math.sin(a)), rot=math.degrees(a),
                            w=2 * r * math.sin(math.radians(da / 2)) - 0.3, z0=_v["SIG_Z0"], z1=_v["SIG_Z1"]))
    return out


def letras_volumen(pr):
    """САЛЮТ ×2 en VOLUMEN: cada letra con la forma del glifo (DejaVu Sans Bold), alto SIG_Z1 − SIG_Z0, extruida hacia fuera en su
    plano tangente al arco [usuario 22/11 «letras circulares», 27/11 «letras en volumen arriba»; Alamy, F09, F08, F19].
    Detalle: 0,40 de espesor, a R_R + SIG_R (sobre su bastidor). Molde: trazos engrosados a ≥ 0,6 y pegadas al remate (relieve 0,6)."""
    from matplotlib.textpath import TextPath
    from matplotlib.font_manager import FontProperties
    from shapely.geometry import Polygon as SPo
    from shapely.ops import unary_union
    from manifold3d import FillRule
    fp = FontProperties(family="DejaVu Sans", weight="bold")
    hz = _v["SIG_Z1"] - _v["SIG_Z0"]
    out = []
    for L_ in letrero():
        tp = TextPath((0, 0), L_["ch"], size=1.0, prop=fp)
        polys = [SPo(p) for p in tp.to_polygons() if len(p) > 2]
        g = None
        for p in sorted(polys, key=lambda q: -abs(q.area)):     # contornos exteriores y agujeros (regla par-impar)
            g = p.buffer(0) if g is None else (g.difference(p) if g.contains(p) else g.union(p.buffer(0)))
        x0, y0, x1, y1 = g.bounds; k = hz / (y1 - y0)
        from shapely import affinity
        g = affinity.translate(affinity.scale(g, k, k, origin=(0, 0)), -k * (x0 + x1) / 2, -k * y0)
        if MOLDE: g = g.buffer(0.12, join_style=2)               # trazos ≥ 0,6 para que el hormigón no se rompa
        lw = 2 * (R_R + _v["SIG_R"]) * math.sin(math.radians(_v["SIG_AW"] / 10)) * 0.92
        if g.bounds[2] - g.bounds[0] > lw:                       # que quepa en su hueco del arco
            f = lw / (g.bounds[2] - g.bounds[0]); g = affinity.scale(g, f, 1.0, origin=(0, 0))
        rings = []
        for gg in getattr(g, "geoms", [g]):
            rings.append(list(gg.exterior.coords)[:-1]); rings += [list(i.coords)[:-1] for i in gg.interiors]
        dep = 0.6 if MOLDE else 0.4
        pr_ = Manifold.extrude(CrossSection(rings, FillRule.EvenOdd), dep)       # letra en XY, espesor en Z
        a = math.radians(L_["rot"])
        rb = R_R - 0.05          # cara trasera de la letra: pegada al remate en detalle y en molde (antes, en detalle, flotaba 1,3 m sobre un bastidor nunca modelado)
        pr_ = pr_.rotate((90, 0, 0)).rotate((0, 0, math.degrees(a) + 90))         # X → tangente (CCW), Z → arriba, −Y → hacia fuera
        out.append(pr_.translate((pr[0] + rb * math.cos(a), pr[1] + rb * math.sin(a), _v["SIG_Z0"])))
    return out


def gargolas():
    """gárgolas de los balcones: una por módulo (centrada entre aletas) y por planta, en el canto del forjado bajo la
    ranura, de la 2.ª planta a la cubierta del barril; fuera del sector de la escalera [F18, F08; usuario 22/11].
    Solo para planos (Ø 0,12: no sale en el molde). Devuelve [(x, y, z, azimut_rad)]."""
    out = []
    for k in range(N_AL):
        a = 2 * math.pi * (k + 0.5) / N_AL + FASE_AL
        if abs(math.remainder(a - ESC_ANG, 2 * math.pi)) < ESC_HA + math.radians(4): continue
        for i in range(1, N_PL + 1):
            z = Z_B0 + i * F + _v["FOR_C"] - 0.15
            out.append((T[0] + R_B * math.cos(a), T[1] + R_B * math.sin(a), z, a))
    return out


def fuente():
    """fuente en media luna al pie de la columna, hacia la plaza (1984) [F01, F14, F15; usuario 26/11]: vaso de radio FU_R
    con bordillo de 0,3 y altura FU_H, cortado por el plano del eje de la torre (mitad hacia −N)."""
    r, h = _v["FU_R"], _v["FU_H"]
    vaso = cil(T, r, 0.0, h) - cil(T, r - 0.3, 0.15, h + 0.1)                       # el vaso apoya contra la columna (sin rendija)
    if MOLDE: return Manifold()                                # molde: fuera (una lámina de 0,3 en la cara de colada se rompería)
    ang = math.degrees(math.atan2(N[1], N[0]))
    medio = Manifold.cube((2 * r + 2, r + 1, h + 1)).translate((-(r + 1), 0, -0.5)).rotate((0, 0, ang - 90 + 180))
    return vaso ^ medio.translate((T[0], T[1], 0))


def torre():
    s = [cil(T, R_COL, 0, Z_CU0 + 0.1),
         Manifold.cylinder(4.0, _v["R_CONO"], R_COL, SEG).translate((T[0], T[1], 0)),   # pie de columna (recto: el 'cono' era un toldo)
         cil(T, R_CU, Z_CU0, Z_CU1 + 0.05),                                             # CUELLO (base del tambor de habitaciones) [F70, F14, F09]
         ]                                                   # (sin losa volada: el cuello acaba en ángulo recto) [F18, usuario 26/11]
    # (sin fuente: retirada por el usuario 27/11, «está mal»)
    # vigas radiales bajo el barril y barril con forjados/poyetes + aletas
    zbi = _v["Z_BI"]                                         # FONDO PLANO del barril a +Z_BI = +Z_CU1, borde en ángulo recto [F09, F18, F14, usuario]
    s.append(cil(T, R_B, zbi, niveles_suelo()[0] if not MOLDE else max(niveles_suelo()[0], zbi + 0.7)))   # fondo plano = forjado de la 1.ª planta
    for k in range(N_AL):                                   # 19 vigas radiales rectas bajo el fondo, del cuello a la banda [F18, F14, usuario]
        a = math.degrees(2 * math.pi * k / N_AL + FASE_AL)
        vw = 0.7 if MOLDE else 0.4
        vg = Manifold.cube((R_B - 0.05 - (R_CU - 0.3), vw, _v["VIG_H"] + 0.01)).translate((R_CU - 0.3, -vw / 2, zbi - _v["VIG_H"]))
        s.append(vg.rotate((0, 0, a)).translate((T[0], T[1], 0)))
    rf = RF                                                  # fachada de ventanas tras el balcón de BAL_P [usuario 26/11]
    FC, FR, FP = _v["FOR_C"], _v["FOR_R"], _v["FOR_P"]          # sección de planta del barril [MGF Alamy]
    s.append(cil(T, rf, _v["Z_BI"], Z_B1 + 0.4))
    s.append(cil(T, R_B, _v["Z_BI"], _v["Z_BI"] + _v["BAN_1"]) - cil(T, R_B - (GM or 0.25), _v["Z_BI"] - 0.1, _v["Z_BI"] + _v["BAN_1"] + 0.1))  # 1.ª planta: banda continua sin ranura delante del pavés [F09, F18]
    for i in range(1, N_PL):
        z = Z_B0 + i * F
        if MOLDE:                                               # molde: canto + ranura (0,27 = 0,8 mm) + poyete en una sola banda maciza
            s.append(cil(T, R_B, z, z + FC + FR + FP) - cil(T, rf - 0.1, z - 0.1, z + FC + FR + FP + 0.05)); continue
        s.append(cil(T, R_B, z, z + FC) - cil(T, rf - 0.1, z - 0.1, z + FC + 0.05))          # canto del forjado [MGF Alamy]
        s.append(cil(T, R_B, z + FC + FR, z + FC + FR + FP) - cil(T, R_B - 0.25, z + FC, z + FC + FR + FP + 0.05))  # poyete tras la ranura [MGF Alamy]
    s.append(cil(T, R_B, Z_B1, Z_B1 + FC))
    s.append(baranda(T, R_B - 0.05, Z_B1 + FC, _v["BAR_B"]))   # peto + barandilla 1,1 m de la cubierta del barril [F09, F08]
    for k in range(N_AL):
        a = 2 * math.pi * k / N_AL + FASE_AL
        aw = 0.7 if MOLDE else 0.4
        al = Manifold.cube((R_B - rf + 0.1, aw, Z_B1 + FC - _v["Z_BI"])).translate((rf - 0.1, -aw / 2, _v["Z_BI"]))      # dentro de la banda, desde el fondo
        al = al + Manifold.cube((R_AL - R_B + 0.05, aw, Z_B1 + FC - Z_ALETA0)).translate((R_B - 0.05, -aw / 2, Z_ALETA0))  # fuera: escalón en ángulo recto en la 2.ª planta
        s.append(al.rotate((0, 0, math.degrees(a))).translate((T[0], T[1], 0)))
    # tambor de ojos, banda, visera, remate
    zp = Z_T1 - _v["H_PT"]                                  # pasillo de servicio entre tambor y banda [F08]
    s.append(cil(T, R_T, Z_B1, Z_T1) if MOLDE else cil(T, R_T, Z_B1, zp) + (cil(T, R_T, zp - 0.01, Z_T1) - cil(T, R_T - 0.25, zp, Z_T1 + 0.1)))   # tambor + peto (molde: macizo)
    import ventanas as VT0
    for oj in [h for h in VT0.catalogo() if h["tipo"] == "ojo"]:
        a = math.degrees(math.atan2(oj["n"][1], oj["n"][0]))
        ojo = Manifold.cylinder(_v["OJO_V"] + 0.1, _v["OJO_D"] / 2, _v["OJO_D"] / 2, 24).rotate((0, 90, 0)).translate((R_T - 0.1, 0, _v["OJO_Z"]))
        s.append(ojo.rotate((0, 0, a)).translate((T[0], T[1], 0)))
    pv = P(*OFF_V); pr = P(*OFF_R)
    pb_ = P(*OFF_B)                                       # banda descentrada hacia la plaza [Alamy]
    s.append(cil(pb_, R_G - 0.3, Z_T1 - _v["H_PT"], Z_G1))
    nm = int(2 * math.pi * R_G / 2.4)
    for k in (range(0) if MOLDE else range(nm)):                # montantes de la banda acristalada [F10, F17] (molde: no)
        mt = Manifold.cube((0.5, 0.25, Z_G1 - Z_T1 + _v["H_PT"])).translate((R_G - 0.45, -0.125, Z_T1 - _v["H_PT"]))
        s.append(mt.rotate((0, 0, 360 * k / nm)).translate((pb_[0], pb_[1], 0)))
    s.append(cil(pv, R_V, Z_G1, Z_V1))
    s.append(baranda(pv, R_V, Z_V1, 1.0))                  # barandilla abierta de la cubierta de la visera [F08, Alamy]
    s.append(cil(pr, R_R, Z_V1, Z_R1))
    s.append(cil(pr, _v["REM_ZR"], Z_V1 - 0.01, Z_V1 + _v["REM_ZH"]))      # zócalo (poyete) del remate [Alamy]
    s += letras_volumen(pr)                                  # letrero САЛЮТ ×2: letras en volumen con su forma (usuario 27/11)
    for L_ in ([] if True else letrero()):                    # (antes: placas rectangulares)
        if MOLDE:                                               # molde: letras en relieve de 0,5 sobre el remate (sueltas a 1,5 m se romperían)
            a_ = math.radians(L_["rot"]); rl = R_R + 0.2; wl = 2 * rl * math.sin(math.radians(_v["SIG_AW"] / 10)) - 0.45
            c_ = (pr[0] + rl * math.cos(a_), pr[1] + rl * math.sin(a_))
            _l = Manifold.cube((0.6, wl, L_["z1"] - L_["z0"])).translate((-0.3, -wl / 2, L_["z0"]))
            s.append(_l.rotate((0, 0, L_["rot"])).translate((c_[0], c_[1], 0))); continue
        _l = Manifold.cube((0.3, L_["w"], L_["z1"] - L_["z0"])).translate((-0.15, -L_["w"] / 2, L_["z0"]))
        s.append(_l.rotate((0, 0, L_["rot"])).translate((L_["c"][0], L_["c"][1], 0)))
    pl_ = P(_v["LUC_X"], _v["LUC_Y"])                        # lucernario piramidal de 12 costillas sobre la visera [fotos 25/11]
    s.append(Manifold.cylinder(0.25, _v["LUC_R"] + 0.15, _v["LUC_R"] + 0.15, 12).translate((pl_[0], pl_[1], Z_V1 - 0.01)))
    s.append(Manifold.cylinder(_v["LUC_H"], _v["LUC_R"], 0.25, 12).translate((pl_[0], pl_[1], Z_V1 + 0.24)))
    # ESCALERA en sector: quita las plantas/balcones/aletas del barril en ese sector y pone el núcleo cerrado
    def sector(r0, r1, z0, z1, da0=None, da1=None):
        da0 = -ESC_HA if da0 is None else da0; da1 = ESC_HA if da1 is None else da1
        n = 24
        pts = [esc_ang_pt(r1, da0 + (da1 - da0) * k / n) for k in range(n + 1)] + [esc_ang_pt(r0, da1 - (da1 - da0) * k / n) for k in range(n + 1)]
        cs = CrossSection([pts])
        if cs.area() <= 0: cs = CrossSection([pts[::-1]])
        return Manifold.extrude(cs, z1 - z0).translate((0, 0, z0))
    m = Manifold.batch_boolean(s, OpType.Add)
    # 1) el cilindro se interrumpe en ESC_SEC grados (balcones, aletas, forjados, fachada)
    RS, ZI, ZO = _v["ESC_RS"], _v["ESC_ZI"], _v["ESC_Z1"]
    m = m - sector(ESC_R0 + 0.3, R_AL + 1.0, Z_CU1, Z_T1 + 0.01, -ESC_HA + 0.01, ESC_HA - 0.01)
    m = m - sector(RS, R_AL + 1.0, Z_T1, ZO + 0.5, -ESC_HA + 0.01, ESC_HA - 0.01)
    if MOLDE:                                                   # molde: las dos aletas que flanquean el hueco de la escalera, enteras (el corte las dejaba en 0,35)
        for kk in range(N_AL):
            a = 2 * math.pi * kk / N_AL + FASE_AL
            if abs(abs(math.remainder(a - ESC_ANG, 2 * math.pi)) - ESC_HA) < math.radians(1.5):
                al = Manifold.cube((R_AL - (R_B - 1.3) + 0.05, 0.7, Z_B1 + _v["FOR_C"] - Z_ALETA0)).translate((R_B - 1.3, -0.35, Z_ALETA0))
                al = al + Manifold.cube((R_B - RF + 0.1, 0.7, Z_B1 + _v["FOR_C"] - _v["Z_BI"])).translate((RF - 0.1, -0.35, _v["Z_BI"]))
                m = m + al.rotate((0, 0, math.degrees(a))).translate((T[0], T[1], 0))
    # 2) cuerpo en cuña; por debajo pasa la rampa. Por encima del tambor la caja solo llega hasta RS (cielo hasta la banda)
    #    y su cubierta baja de ZO (fuera) a ZI (dentro) [Alamy, collage]
    esc = [sector(ESC_R0, ESC_RC, _v["ESC_Z0"], Z_T1, -ESC_HB, ESC_HB),
           # (el muro de coronación va aparte, sobre la cubierta del tambor: ver MURO_ESC más abajo)
           sector(ESC_RC - (GM or 0.2), ESC_RC, Z_T1 - 0.01, Z_T1 + 1.1, -ESC_HB, ESC_HB)]      # peto bajo sobre el cuerpo
    # cubierta inclinada de la caja de escalera: plano de ESC_ZI (en ESC_RS) a ESC_Z1 (en ESC_R1 + 0,3); corta cuerpo y lamas [Alamy]
    _ri, _ro = _v["ESC_RS"] - 1.0, ESC_R1 + 1.5
    _sl = (_v["ESC_Z1"] - _v["ESC_ZI"]) / (ESC_R1 + 0.3 - _v["ESC_RS"])
    _pts = [(_ri, _v["ESC_ZI"] + (_ri - _v["ESC_RS"]) * _sl), (_ro, _v["ESC_ZI"] + (_ro - _v["ESC_RS"]) * _sl), (_ro, 70.0), (_ri, 70.0)]
    _cs = CrossSection([_pts]); _cs = _cs if _cs.area() > 0 else CrossSection([_pts[::-1]])
    CORTE_ESC = Manifold.extrude(_cs, 14.0).translate((0, 0, -7.0)).rotate((90, 0, 0)).rotate((0, 0, math.degrees(ESC_ANG))).translate((T[0], T[1], 0))
    RR = _v["ESC_RR"]
    for d0, d1 in ((-ESC_HA, -ESC_HB), (ESC_HB, ESC_HA)):                              # 3) franjas retranqueadas a cada lado
        esc.append(sector(ESC_R0, RR, Z_CU1, Z_B1 + FC, d0, d1))                     #    fachada retranqueada (macizo detrás)
        for i in range(N_PL + 1):                                                       #    forjados vistos con barandilla [F08, F11]
            z = Z_B0 + i * F
            zs_ = z + FC                                                     # cara superior = suelo (niveles_suelo)
            esc.append(sector(RR, rf, z, max(zs_, z + (GM or 0)), d0, d1))
            esc.append(sector(rf - (GM or 0.08), rf, zs_, zs_ + 1.0, d0, d1))
    m = m + (Manifold.batch_boolean(esc, OpType.Add) - CORTE_ESC)
    # MURO de coronación: radial en el eje de la cuña, apoyado en la cubierta del tambor, de RS hasta el borde del tambor
    # (las lamas siguen por fuera, más bajas); coronación inclinada que vierte hacia dentro: ZI en RS → ZO en el borde
    # [dron 26/11 del usuario: muro sobre la terraza del tambor, acaba en su borde, «caída de agua hacia el interior»;
    #  foto de frente: bloque a la izquierda de las lamas subiendo hacia fuera; F09: no asoma a la derecha de la visera; alturas Alamy]
    _ro_m = R_T + _v["ESC_MO"]
    _pm = [(RS, Z_T1 - 0.01), (_ro_m, Z_T1 - 0.01), (_ro_m, ZO), (RS, ZI)]
    _cm = CrossSection([_pm]); _cm = _cm if _cm.area() > 0 else CrossSection([_pm[::-1]])
    MURO_ESC = Manifold.extrude(_cm, GM or 0.3).translate((0, 0, -(GM or 0.3) / 2)).rotate((90, 0, 0)).rotate((0, 0, math.degrees(ESC_ANG))).translate((T[0], T[1], 0))
    m = m + MURO_ESC
    m = m + sector(ESC_R0, ESC_RC, _v["ESC_ZL"] - 0.3, _v["ESC_ZL"], -ESC_HB, ESC_HB)     # forjado superior de la escalera (sin hueco visto) [usuario 26/11]
    # pie de la escalera: núcleo de hormigón bajo la losa blanca y celosía baja de lamas sobre la terraza [F78, foto de frente]
    _hn = ESC_HB * _v["ESC_NU"]
    m = m + sector(ESC_R0 + 1.0, ESC_RC - 0.6, Z_P1 - 0.01, _v["ESC_Z0"] + 0.01, -_hn, _hn)
    m = m + sector(ESC_R0, ESC_RC + 0.3, _v["ESC_Z0"] - _v["ESC_LE"], _v["ESC_Z0"], -ESC_HB, ESC_HB)   # losa blanca [foto de frente]
    # cristalera suelo-techo con dintel entre tambor y escalera (lado izquierdo) y puerta del tambor [foto de frente, usuario]
    _zb = Z_B1 + FC; _d0, _d1 = -ESC_HA, -ESC_HB
    m = m + sector(_v["ESC_RR"] - (GM or 0.05), _v["ESC_RR"], _zb, _v["CR_Z1"], _d0, _d1) + sector(_v["ESC_RR"] - 0.3, _v["ESC_RR"] + 0.2, _v["CR_Z1"], Z_T1, _d0, _d1)
    import ventanas as VTp
    for hh in VTp.catalogo():
        if hh["grupo"] == "tambor puerta":
            a_ = math.degrees(math.atan2(hh["n"][1], hh["n"][0]))
            m = m - Manifold.cube((0.6, hh["w"], hh["z1"] - hh["z0"])).translate((R_T - 0.3, -hh["w"] / 2, hh["z0"])).rotate((0, 0, a_)).translate((T[0], T[1], 0))
    # ventanas de las habitaciones: un hueco por modulo entre aletas, sobre el poyete [F04, F06, F09]
    import ventanas as VT                                # catálogo único de huecos (mismo que planos)
    hue = []
    for hh in VT.catalogo():
        if not hh["grupo"].startswith("torre planta"): continue
        a = math.degrees(math.atan2(hh["n"][1], hh["n"][0]))
        h = Manifold.cube((0.5, hh["w"], hh["z1"] - hh["z0"])).translate((rf - 0.25, -hh["w"] / 2, hh["z0"]))
        hue.append(h.rotate((0, 0, a)).translate((T[0], T[1], 0)))
    for hh in VT.catalogo():
        if hh["grupo"] == "escalera puertas":
            a = math.degrees(math.atan2(hh["n"][1], hh["n"][0]))
            h = Manifold.cube((1.2, hh["w"], hh["z1"] - hh["z0"])).translate((_v["ESC_RC"] - 0.6, -hh["w"] / 2, hh["z0"]))
            hue.append(h.rotate((0, 0, a)).translate((T[0], T[1], 0)))
            continue
        if hh["grupo"] != "escalera retranqueo" or MOLDE: continue      # molde: sin estas ventanas (dejaban una lámina de 0,25 junto a la cuña)
        a = math.degrees(math.atan2(hh["n"][1], hh["n"][0]))
        h = Manifold.cube((0.8, hh["w"], hh["z1"] - hh["z0"])).translate((_v["ESC_RR"] - 0.5, -hh["w"] / 2, hh["z0"]))
        hue.append(h.rotate((0, 0, a)).translate((T[0], T[1], 0)))
    m = m - Manifold.batch_boolean(hue, OpType.Add)
    # pantalla de lamas que forra el cuerpo en cuña por su cara exterior y sus dos caras laterales, separada 0,3 [F08, F11, F13]
    lam = []
    def lama(r, da, rot_r=True, z0=None, z1=None):
        _e = _v["LAMA_E"] / 2                                          # lamas finas (canto 0,25 hacia fuera, espesor LAMA_E) [dron, usuario]
        z0 = _v["ESC_Z0"] + 0.3 if z0 is None else z0; z1 = _v["ESC_ZL"] if z1 is None else z1
        return (caja(-0.125, 0.125, -_e, _e, z0, z1) if rot_r else caja(-_e, _e, -0.125, 0.125, z0, z1)) \
            .translate((r, 0, 0)).rotate((0, 0, math.degrees(ESC_ANG + da))).translate((T[0], T[1], 0))
    nl = int(_v["LAMA_N"]) - 1                                  # 16 surcos en el frente [usuario]
    zg0, zg1 = _v["ESC_Z0"] + 0.3, _v["ESC_ZL"] - 0.3           # los surcos van de la losa a 0,3 bajo la cubierta: la cubierta queda maciza [usuario 28/11]
    dl = math.atan2(0.6, ESC_RC)
    if not MOLDE:                                               # detalle: la pantalla es un bloque macizo con surcos, no lamas sueltas [usuario 28/11]
        _e = _v["LAMA_E"] / 2
        bloque = [sector(ESC_RC - 0.01, ESC_R1, _v["ESC_Z0"] + 0.3, _v["ESC_ZL"], -ESC_HB, ESC_HB),
                  sector(rf, ESC_R1, _v["ESC_Z0"] + 0.3, _v["ESC_ZL"], -ESC_HB - dl, -ESC_HB + 0.01),
                  sector(rf, ESC_R1, _v["ESC_Z0"] + 0.3, _v["ESC_ZL"], ESC_HB - 0.01, ESC_HB + dl)]
        surcos = []
        for k in range(nl + 1):                                 # frente: surcos finos (0,04) a paso de 0,07
            da = -ESC_HB + 2 * ESC_HB * k / nl
            surcos.append(caja(ESC_R1 - 0.25, ESC_R1 + 0.1, -_e / 2, _e / 2, zg0, zg1)
                          .rotate((0, 0, math.degrees(ESC_ANG + da))).translate((T[0], T[1], 0)))
        for sg in (-1, 1):                                      # costados: surcos de 0,08 cada LAMA_P, 0,25 hacia dentro desde la cara exterior
            t0, t1 = (-0.1, 0.25) if sg < 0 else (-0.25, 0.1)
            r = rf + 0.2
            while r < ESC_R1 - 0.3:
                surcos.append(caja(r - _e, r + _e, t0, t1, zg0, zg1)
                              .rotate((0, 0, math.degrees(ESC_ANG + sg * (ESC_HB + dl)))).translate((T[0], T[1], 0)))
                r += _v["LAMA_P"]
        cortes = []
        for hh in VT.catalogo():                                # delante de las puertas el bloque se abre
            if hh["grupo"] == "escalera puertas":
                a = math.degrees(math.atan2(hh["n"][1], hh["n"][0]))
                corte = Manifold.cube((1.5, hh["w"] + 0.4, hh["z1"] - hh["z0"])).translate((ESC_RC - 0.1, -hh["w"] / 2 - 0.2, hh["z0"]))
                cortes.append(corte.rotate((0, 0, a)).translate((T[0], T[1], 0)))
        lam.append(Manifold.batch_boolean(bloque, OpType.Add) - Manifold.batch_boolean(cortes + surcos, OpType.Add))
    # los dos bordes del corte del barril, cerrados con lamas de la coronación del tambor hacia abajo [fotos 25/11, usuario]
    for sg in (1,):                                            # solo el borde derecho: el izquierdo está libre (puerta y cristalera) [foto de frente]
        r = _v["ESC_RR"] + 0.2
        while r < R_B:
            lam.append(lama(r, sg * (ESC_HA - math.atan2(0.2, r)), rot_r=False, z0=Z_B0, z1=Z_T1))
            r += _v["LAMA_P"]
    nlc = int(2 * ESC_HB * ESC_RC / _v["LAMA_P"])
    for k in range(nlc + 1):                                    # celosía baja al pie de la escalera
        lam.append(lama(ESC_RC + 0.1, -ESC_HB + 2 * ESC_HB * k / nlc, z0=Z_P1, z1=Z_P1 + _v["ESC_CB"]))
    if MOLDE:                                                   # molde: la pantalla de lamas (0,08 cada 0,35) se cuela como un volumen macizo
        z0l, z1l = _v["ESC_Z0"] + 0.3, _v["ESC_ZL"]; dl = math.atan2(0.6, ESC_RC)
        lam = [sector(ESC_RC - 0.01, ESC_R1, z0l, z1l, -ESC_HB, ESC_HB),                          # frente
               sector(rf, ESC_R1, z0l, z1l, -ESC_HB - dl, -ESC_HB + 0.01), sector(rf, ESC_R1, z0l, z1l, ESC_HB - 0.01, ESC_HB + dl),   # costados
               sector(_v["ESC_RR"] + 0.1, R_B, Z_B0, Z_T1, ESC_HA - math.atan2(0.6, R_B), ESC_HA),                                # borde dcho. del corte
               sector(ESC_RC - 0.6, ESC_RC + 0.25, Z_P1, Z_P1 + _v["ESC_CB"], -ESC_HB, ESC_HB)]                                 # celosía baja
    m = m + (Manifold.batch_boolean(lam, OpType.Add) - CORTE_ESC)
    for L_ in lucernarios_cuello():                             # lucernarios piramidales bajo el cuello [F78]
        pir = Manifold.cylinder(L_["h"], L_["l"] / math.sqrt(2), 0.0, 4).rotate((0, 0, 45 + math.degrees(L_["a"])))
        m = m + pir.translate((L_["c"][0], L_["c"][1], L_["z"]))
    return m


def edificio():
    return base() + torre()


if __name__ == "__main__":
    m = edificio()
    print("ok", m.status(), "T=", tuple(round(v, 2) for v in T), "A1=", tuple(round(v, 2) for v in A1), "C=", tuple(round(v, 2) for v in C))
    print(plantas_base())
