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
_v = _K.V
Z_PB, Z_P1, Z_BAR, Z_BAR_C, Z_ALTO = _v["Z_PB"], _v["Z_P1"], _v["Z_BAR"], _v["Z_BARC"], _v["Z_ALTO"]
Z_CU0, Z_CU1, Z_ALETA0, Z_B0, F, N_PL = _v["Z_CU0"], _v["Z_CU1"], _v["Z_ALE"], _v["Z_B0"], _v["F"], int(_v["N_PL"])
Z_B1 = Z_B0 + N_PL * F
Z_T1, Z_G1, Z_V1, Z_R1 = _v["Z_T1"], _v["Z_G1"], _v["Z_V1"], _v["Z_R1"]
R_COL, R_CU, R_B, R_AL, R_T, R_G, R_V, R_R = _v["R_COL"], _v["R_CU"], _v["R_B"], _v["R_AL"], _v["R_T"], _v["R_G"], _v["R_V"], _v["R_R"]
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
    PB = [SWP(-L_C, RETR), a1, b1, (W_P - RETR, Y_CUNA), (W_P, Y_CUNA), (W_P, L_L),
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
        g = LineString(borde).buffer(0.25 if side else -0.25, single_sided=True).intersection(P)
        if g.area > 1.0:
            for gm in getattr(g, "geoms", [g]):
                if gm.geom_type == "Polygon" and gm.area > 0.05:
                    gm = orient(gm, 1.0)
                    out.append(prisma(list(gm.exterior.coords)[:-1], Z_P1 - 0.01, Z_P1 + 1.0))       # peto 1 m
            break
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
    for i in range(3):                                      # claraboyas piramidales sobre la cubierta de planta 1, detrás de la línea A [aéreas actuales]
        x = -L_C + 6.5 + 2.2 * i
        sc.append(Manifold.extrude(CrossSection.square((1.6, 1.6), True), 0.9, 0, 0, (0.05, 0.05)).translate((x, W_C + 2.0, Z_P1 - 0.01)))
    s.append(ROT(Manifold.batch_boolean(sc, OpType.Add)))
    # ala larga: bar en la mitad interior hasta el tramo final; terraza con peto en la mitad exterior [F47, Bing]
    yb0 = pl["Q"][1] + 0.5                                              # la rampa del techo arranca junto a la torre y pasa bajo la escalera
    yb1 = L_L - L_FIN                                                   # 1984: el bar acaba sobre la 1a ventana [F01, F47]
    yr1 = yb0 + _v["R2_L"]                                              # fin de la rampa-cubierta
    s += [caja(0, W_BAR, yr1 - 0.01, yb1, Z_P1 - 0.01, Z_BAR),
          caja(0, W_BAR + _v["V_BAR"], yr1 - 0.01, yb1 + _v["V_BAR"], Z_BAR, Z_BAR_C),     # cubierta plana volada en frente y extremo
          caja(0, 0.1, yb1, L_L, Z_P1 - 0.01, Z_P1 + 1.1),                         # barandilla borde patio de la terraza abierta [F47]
          caja(W_P - 0.3, W_P, pl["Q"][1] + _v["D_HOTF"], L_L, Z_P1 - 0.01, Z_P1 + _v["H_PET"]),  # peto exterior [F73 +8,5] (la meseta de la esquina abre a la terraza)
          caja(0, W_P - 0.3, L_L - 0.25, L_L - 0.15, _v["Z_FIN"] - 0.01, _v["Z_FIN"] + 1.1)]   # testero a cota terraza + barandilla [F73]
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
        return max(0.05, _v["Z_CON"] * (1 - u) * (1 + C_ * u))
    def zs(yy):         # intradós del arco bajo la rampa junto al hotel (paso en planta baja) [F47, F71, F76]
        if yy >= Y_ARC: return 0.0
        u = (yy - y0) / (Y_ARC - y0)
        return max(0.0, min(_v["Z_ARC"] * math.sqrt(max(0.0, 1 - u ** 2)), zr(yy) - 0.6))
    def f(v):
        x, y, z = v
        yy = y0 + min(max(y, 0.0), 1.0) * LR
        lo, hi = zs(yy), zr(yy)
        return (W_P - 0.02 + x * WR, yy, lo + z * (hi - lo))
    rampa = Manifold.cube((1, 1, 1)).refine(60).warp(f)
    yp = y0                                                                       # el peto de la rampa sigue al de la curva
    def fp(v):
        x, y, z = v
        yy = yp + min(max(y, 0.0), 1.0) * (YB - yp)
        return (W_P + WR - 0.25 + x * 0.25, yy, zr(yy) - 0.01 + z * 1.0)          # peto de 1 m en el borde exterior
    peto = Manifold.cube((1, 1, 1)).refine(40).warp(fp)
    s += [rampa, peto]
    # ESQUINA [usuario, F09, F18]: la rampa abre hacia fuera en curva y llega a 90° al chaflán prolongado (E90);
    # la meseta a +Z_P1 es la cubierta de esa prolongación (hotel debajo); peto en la curva y sobre la banda del hotel
    s += plataforma_curva()
    # EL TECHO DEL RESTAURANTE EMPIEZA EN RAMPA [usuario, F76, F71]: junto a la torre la cubierta del bar nace a la
    # cota de la terraza (+Z_P1) y sube en rampa, en todo el ancho de la cubierta, hasta la cubierta plana (+Z_BARC);
    # debajo, el restaurante con techo inclinado. Se sube a la azotea andando por la propia cubierta.
    WB = W_BAR + _v["V_BAR"]
    def fw(v):
        x, y, z = v
        u = min(max(y, 0.0), 1.0)
        zt = Z_P1 + u * (Z_BAR_C - Z_P1)
        return (x * WB, yb0 + u * (yr1 - yb0), Z_P1 - 0.01 + z * (zt - Z_P1 + 0.01))
    cuna = Manifold.cube((1, 1, 1)).refine(30).warp(fw)
    def barand(x0_):
        def g(v):
            x, y, z = v
            u = min(max(y, 0.0), 1.0)
            zt = Z_P1 + u * (Z_BAR_C - Z_P1)
            return (x0_ + x * 0.1, yb0 + u * (yr1 - yb0), zt - 0.01 + z * 1.0)
        return Manifold.cube((1, 1, 1)).refine(20).warp(g)
    s += [cuna, barand(WB - 0.1), barand(0.0),
          caja(0, WB, yb1 + _v["V_BAR"] - 0.1, yb1 + _v["V_BAR"], Z_BAR_C - 0.01, Z_BAR_C + 1.0),    # barandilla azotea (extremo)
          caja(WB - 0.1, WB, yr1 - 0.01, yb1 + _v["V_BAR"], Z_BAR_C - 0.01, Z_BAR_C + 1.0),           # lado largo (F73 barandilla roja)
          caja(0, 0.1, yr1 - 0.01, yb1 + _v["V_BAR"], Z_BAR_C - 0.01, Z_BAR_C + 1.0)]                 # lado patio
    m = Manifold.batch_boolean(s, OpType.Add)
    # huecos de ventanas (franjas continuas casi a paño) [F09, F14]
    hue = []
    # logia de planta 1 bajo el vuelo: hueco retranqueado LOG_D entre muro de medianera (0,6), pilar (0,7) y muro final (0,25)
    ld, lx = _v["LOG_D"], _v["LOG_PX"]; x0l = -L_C
    lx0, lx1 = x0l + _v["LOG_X0"], x0l + _v["LOG_X1"]
    m = m - ROT(caja(lx0, lx1, -1, ld, Z_PB + 0.01, Z_P1 - 0.01))
    m = m + ROT(caja(x0l + lx - 0.35, x0l + lx + 0.35, 0, ld, Z_PB, Z_P1))                       # pilar intermedio
    m = m + ROT(caja(lx0, lx1, 0, 0.25, Z_PB, Z_PB + 1.0))                                       # antepecho / poyete
    # puertas del hotel en planta baja junto a la columna [usuario, F18]
    for hh in __import__("ventanas").catalogo():
        if hh["grupo"] in ("hotel puertas PB", "bloque alto posterior"):
            a = math.degrees(math.atan2(hh["n"][1], hh["n"][0]))
            b = Manifold.cube((1.2, hh["w"], hh["z1"] - hh["z0"])).translate((-0.6, -hh["w"] / 2, hh["z0"]))
            hue.append(b.rotate((0, 0, a)).translate((hh["p"][0], hh["p"][1], 0)))
    # HUECOS DEL ALA LARGA (pasada 11, proporciones F73/F01/F47): 11 arriba, 7 abajo bajo los 7 más cercanos al
    # testero, intereje S_VEN, hueco 0,47 S; marco que sale MAR_P y vidrio MAR_R por detrás del frente del marco
    import ventanas as VT                                # catálogo único de huecos (mismo que planos)
    p_, rr_, bd = _v["MAR_P"], _v["MAR_R"], _v["MAR_B"]
    marcos = []
    for h in VT.catalogo():
        if not h["grupo"].startswith("ala larga"): continue
        y0_, y1_ = h["p"][1] - h["w"] / 2, h["p"][1] + h["w"] / 2; z0, z1 = h["z0"], h["z1"]
        marcos.append(caja(W_P - 0.01, W_P + p_, y0_ - bd, y1_ + bd, z0 - bd, z1 + bd))
        marcos.append(caja(W_P - 0.01, W_P + p_ + 0.06, y0_ - bd - 0.05, y1_ + bd + 0.05, z0 - bd - 0.1, z0 - bd))  # alféizar con goterón
        hue.append(caja(W_P + p_ - rr_, W_P + 1, y0_, y1_, z0, z1))                 # hueco hasta el vidrio
    # testero: puerta de servicio con marquesina saliente y ventana encima [F73: a 0,49-0,63 del ancho desde la esquina exterior]
    hue.append(caja(W_P - 0.63 * W_P, W_P - 0.49 * W_P, L_L - 0.3, L_L + 1, 0.0, 2.6))
    hue.append(caja(W_P - 0.55 * W_P, W_P - 0.43 * W_P, L_L - 0.3, L_L + 1, 4.6, 5.3))
    px0, px1, pd, pe = _v["POR_X0"], _v["POR_X1"], _v["POR_D"], _v["POR_E"]
    marcos += [caja(px0, px0 + pe, L_L - 0.01, L_L + pd, 0.0, 4.4),                  # porche: muros a los lados de la puerta [usuario, F73]
               caja(px1 - pe, px1, L_L - 0.01, L_L + pd, 0.0, 4.4),
               caja(px0, px1, L_L - 0.01, L_L + pd, 4.0, 4.4),                         # marquesina sobre los muros
               caja(W_P - 0.3, W_P, L_L - 0.01, L_L + _v["ESQ_D"], 0.0, _v["Z_FIN"] + 1.1)]   # muro de esquina en toda la altura [F73]
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
    m = m - en_torre(caja(xr0 - 0.5, xr1, yf - 1, yf + RETR + 0.01, Z_PB - 0.01, 4.5))          # sofito del restaurante a +4,5
    hue_t = [caja(xr0 + 0.4, xr1 - 0.3, yf - 1, yf + 0.3, 4.6, 6.4)]                            # vidrio restaurante
    xh1 = R_COL + _v["HOT_L"]                                                                      # hotel: de la columna a E90 [F09, F18]
    m = m + en_torre(caja(xh0, xh1, yf - 0.3, yf + 2.0, 3.1, 4.3))
    hue_t.append(caja(xh0 + 0.3, xh1 - 0.4, yf - 1, yf + 0.3, 4.35, 6.0))
    m = m - en_torre(caja(xh0 + 0.5, xh1 - 0.3, yf - 1, yf + RETR, -1, 3.1))                       # entrada del hotel bajo la banda
    return m - en_torre(Manifold.batch_boolean(hue_t, OpType.Add))


def torre():
    s = [cil(T, R_COL, 0, Z_CU0 + 0.1),
         Manifold.cylinder(4.0, _v["R_CONO"], R_COL, SEG).translate((T[0], T[1], 0)),   # pie de columna (recto: el 'cono' era un toldo) cil(T, R_CU, Z_CU0, Z_CU1 + 0.05),
         cil(T, R_CU + 0.6, Z_CU0, Z_CU0 + 0.6)]                       # losa inferior del cuello, volada [F18, F50]
    # vigas radiales bajo el barril y barril con forjados/poyetes + aletas
    s.append(cil(T, R_B - 0.1, Z_CU1 - 0.01, Z_ALETA0 + 0.05))   # fondo del barril (sofito plano a la cota de las aletas)
    for k in range(N_AL):                                   # 19 ménsulas triangulares: de la punta de la aleta al borde del cuello
        a = math.degrees(2 * math.pi * k / N_AL + FASE_AL)
        pts = [(R_CU - 0.3, Z_CU1), (R_CU - 0.3, Z_ALETA0 + 0.05), (R_AL, Z_ALETA0 + 0.05)]
        pl_ = Manifold.extrude(CrossSection([pts]), 0.4).translate((0, 0, -0.2)).rotate((90, 0, 0))
        if pl_.volume() <= 0:
            pl_ = Manifold.extrude(CrossSection([pts[::-1]]), 0.4).translate((0, 0, -0.2)).rotate((90, 0, 0))
        s.append(pl_.rotate((0, 0, a)).translate((T[0], T[1], 0)))
    rf = R_B - 1.8
    FC, FR, FP = _v["FOR_C"], _v["FOR_R"], _v["FOR_P"]          # sección de planta del barril [MGF Alamy]
    s.append(cil(T, rf, Z_B0, Z_B1 + 0.4))
    for i in range(N_PL):
        z = Z_B0 + i * F
        s.append(cil(T, R_B, z, z + FC) - cil(T, rf - 0.1, z - 0.1, z + FC + 0.05))          # canto del forjado [MGF Alamy]
        s.append(cil(T, R_B, z + FC + FR, z + FC + FR + FP) - cil(T, R_B - 0.25, z + FC, z + FC + FR + FP + 0.05))  # poyete tras la ranura [MGF Alamy]
    s.append(cil(T, R_B, Z_B1, Z_B1 + FC))
    s.append(baranda(T, R_B - 0.05, Z_B1 + FC, _v["BAR_B"]))   # peto + barandilla 1,1 m de la cubierta del barril [F09, F08]
    for k in range(N_AL):
        a = 2 * math.pi * k / N_AL + FASE_AL
        al = Manifold.cube((R_AL - rf + 0.2, 0.4, Z_B1 + FC - Z_ALETA0)).translate((rf - 0.1, -0.2, Z_ALETA0))
        s.append(al.rotate((0, 0, math.degrees(a))).translate((T[0], T[1], 0)))
    # tambor de ojos, banda, visera, remate
    zp = Z_T1 - _v["H_PT"]                                  # pasillo de servicio entre tambor y banda [F08]
    s.append(cil(T, R_T, Z_B1, zp) + (cil(T, R_T, zp - 0.01, Z_T1) - cil(T, R_T - 0.25, zp, Z_T1 + 0.1)))   # tambor + peto
    import ventanas as VT0
    for oj in [h for h in VT0.catalogo() if h["tipo"] == "ojo"]:
        a = math.degrees(math.atan2(oj["n"][1], oj["n"][0]))
        ojo = Manifold.cylinder(_v["OJO_V"] + 0.1, _v["OJO_D"] / 2, _v["OJO_D"] / 2, 24).rotate((0, 90, 0)).translate((R_T - 0.1, 0, _v["OJO_Z"]))
        s.append(ojo.rotate((0, 0, a)).translate((T[0], T[1], 0)))
    pv = P(*OFF_V); pr = P(*OFF_R)
    pb_ = P(*OFF_B)                                       # banda descentrada hacia la plaza [Alamy]
    s.append(cil(pb_, R_G - 0.3, Z_T1 - _v["H_PT"], Z_G1))
    nm = int(2 * math.pi * R_G / 2.4)
    for k in range(nm):                                     # montantes de la banda acristalada [F10, F17]
        mt = Manifold.cube((0.5, 0.25, Z_G1 - Z_T1 + _v["H_PT"])).translate((R_G - 0.45, -0.125, Z_T1 - _v["H_PT"]))
        s.append(mt.rotate((0, 0, 360 * k / nm)).translate((pb_[0], pb_[1], 0)))
    s.append(cil(pv, R_V, Z_G1, Z_V1))
    s.append(baranda(pv, R_V, Z_V1, 1.0))                  # barandilla abierta de la cubierta de la visera [F08, Alamy]
    s.append(cil(pr, R_R, Z_V1, Z_R1))
    s.append(cil(pr, _v["REM_ZR"], Z_V1 - 0.01, Z_V1 + _v["REM_ZH"]))      # zócalo (poyete) del remate [Alamy]
    # letrero САЛЮТ: 5 letras en un plano frente a la cámara de Alamy, delante del remate, la de la izquierda volada sobre la celosía [Alamy]
    _ca = math.radians(_v["VISTA_ALAMY"]); _hc = (math.cos(_ca), math.sin(_ca)); _dr = (math.cos(_ca + math.pi / 2), math.sin(_ca + math.pi / 2))
    _prf = (pr[0] - T[0]) * _hc[0] + (pr[1] - T[1]) * _hc[1]
    _w = (_v["SIG_S1"] - _v["SIG_S0"]) / 5
    for _i in range(5):
        _sc = _v["SIG_S0"] + (_i + 0.5) * _w; _dd = _prf + R_R + 0.5
        _l = Manifold.cube((0.3, _w - 0.3, _v["SIG_Z1"] - _v["SIG_Z0"])).translate((-0.15, -(_w - 0.3) / 2, _v["SIG_Z0"]))
        _l = _l.rotate((0, 0, math.degrees(_ca))).translate((T[0] + _dd * _hc[0] + _sc * _dr[0], T[1] + _dd * _hc[1] + _sc * _dr[1], 0))
        s.append(_l)
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
    # 2) cuerpo en cuña; por debajo pasa la rampa. Por encima del tambor la caja solo llega hasta RS (cielo hasta la banda)
    #    y su cubierta baja de ZO (fuera) a ZI (dentro) [Alamy, collage]
    esc = [sector(ESC_R0, ESC_RC, _v["ESC_Z0"], Z_T1, -ESC_HB, ESC_HB), sector(RS, ESC_RC, Z_T1 - 0.01, ZO, -ESC_HB, ESC_HB)]
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
            esc.append(sector(RR, rf, z, z + 0.3, d0, d1))
            esc.append(sector(rf - 0.08, rf, z + 0.3, z + 1.3, d0, d1))
    m = m + (Manifold.batch_boolean(esc, OpType.Add) - CORTE_ESC)
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
        if hh["grupo"] != "escalera retranqueo": continue
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
    nl = int(_v["LAMA_N"]) - 1                                  # 16 lamas en el frente [usuario]
    for k in range(nl + 1):
        lam.append(lama(ESC_R1 - 0.25, -ESC_HB + 2 * ESC_HB * k / nl))
    for hh in VT.catalogo():                                   # las lamas se abren delante de las puertas
        if hh["grupo"] == "escalera puertas":
            a = math.degrees(math.atan2(hh["n"][1], hh["n"][0]))
            corte = Manifold.cube((1.5, hh["w"] + 0.4, hh["z1"] - hh["z0"])).translate((ESC_RC - 0.1, -hh["w"] / 2 - 0.2, hh["z0"]))
            lam = [l_ - corte.rotate((0, 0, a)).translate((T[0], T[1], 0)) for l_ in lam]
    for sg in (-1, 1):
        r = rf + 0.2
        while r < ESC_R1 - 0.3:
            lam.append(lama(r, sg * (ESC_HB + math.atan2(0.45, r)), rot_r=False))
            r += _v["LAMA_P"]
    # los dos bordes del corte del barril, cerrados con lamas de la coronación del tambor hacia abajo [fotos 25/11, usuario]
    for sg in (-1, 1):
        r = _v["ESC_RR"] + 0.2
        while r < R_B:
            lam.append(lama(r, sg * (ESC_HA - math.atan2(0.2, r)), rot_r=False, z0=Z_B0, z1=Z_T1))
            r += _v["LAMA_P"]
    return m + (Manifold.batch_boolean(lam, OpType.Add) - CORTE_ESC)


def edificio():
    return base() + torre()


if __name__ == "__main__":
    m = edificio()
    print("ok", m.status(), "T=", tuple(round(v, 2) for v in T), "A1=", tuple(round(v, 2) for v in A1), "C=", tuple(round(v, 2) for v in C))
    print(plantas_base())
