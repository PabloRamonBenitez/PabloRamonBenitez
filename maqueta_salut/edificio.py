"""Definicion del Hotel Salut SOLO con medidas de fotos y de Bing (no hereda nada del modelo 3D anterior).
Coordenadas (m): calle Ivana Mazepy = eje x (y=0, fachada a la calle del ala corta); ala larga hacia +y
(perpendicular a la calle, Bing F35/F48: 83-90 grados); cara interior del ala larga en x=0.
Fuentes de cada cota entre corchetes."""
import math
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
Y_CUNA = L_L - 35.13    # la concha se junta con la fachada a 35 m del fondo [Bing 35,13]
W_EXT = 15.7        # ancho maximo con la concha                    [Google 15,7]
import os
A_CH = math.radians(float(os.environ.get("ACH", "57")))   # angulo del chaflan con la calle [provisional]
TH_L = math.radians(float(os.environ.get("THL", "112")))   # angulo interior de la L (calle - ala larga) [FASE 2: F35/F58 ~102]
REST, COL, HOT = 14.3, 6.5, 11.4            # tramos del chaflan    [C04 calibrada: 14,3 + 6,5 + 11,4]
# ====== FUENTE UNICA: todas las cotas se leen del CUADRO DE COTAS (cotas.py); lo de arriba queda como historial
import cotas as _K
_v = _K.V
Z_PB, Z_P1, Z_BAR, Z_BAR_C, Z_ALTO = _v["Z_PB"], _v["Z_P1"], _v["Z_BAR"], _v["Z_BARC"], _v["Z_ALTO"]
Z_CU0, Z_CU1, Z_ALETA0, Z_B0, F, N_PL = _v["Z_CU0"], _v["Z_CU1"], _v["Z_ALE"], _v["Z_B0"], _v["F"], int(_v["N_PL"])
Z_B1 = Z_B0 + N_PL * F
Z_T1, Z_G1, Z_V1, Z_R1 = _v["Z_T1"], _v["Z_G1"], _v["Z_V1"], _v["Z_R1"]
R_COL, R_CU, R_B, R_AL, R_T, R_G, R_V, R_R = _v["R_COL"], _v["R_CU"], _v["R_B"], _v["R_AL"], _v["R_T"], _v["R_G"], _v["R_V"], _v["R_R"]
OFF_V, OFF_R, N_AL = (_v["OV_X"], _v["OV_Y"]), (_v["OR_X"], 0.0), int(_v["N_AL"])
W_P, W_BAR, L_L, L_FIN, W_EXT = _v["W_P"], _v["W_BAR"], _v["L_L"], _v["L_FIN"], _v["W_EXT"]
Y_CUNA = L_L - _v["D_CUNA"]
A_CH, TH_L = math.radians(_v["ACH"]), math.radians(_v["THL"])
REST, COL, HOT = _v["REST"], _v["COL"], _v["HOT"]
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
# escalera trasera: en linea con el ala larga, dentro de la L [usuario]
ESC_W, ESC_Y0, ESC_Y1 = _v["ESC_W"], T[1] + 9.0, T[1] + R_B + _v["ESC_L"]   # planta alargada radial [F73, F13, F75]


def P(X, Y):
    """coordenadas de torre (X a lo largo del chaflan, Y hacia dentro) -> planta"""
    return (T[0] + X * U[0] + Y * N[0], T[1] + X * U[1] + Y * N[1])


def caja(x0, x1, y0, y1, z0, z1):
    return Manifold.cube((x1 - x0, y1 - y0, z1 - z0)).translate((x0, y0, z0))


def prisma(poly, z0, z1):
    return Manifold.extrude(CrossSection([poly]), z1 - z0).translate((0, 0, z0))


def cil(c, r, z0, z1, seg=SEG):
    return Manifold.cylinder(z1 - z0, r, r, seg).translate((c[0], c[1], z0))


def plantas_base():
    """poligonos de planta baja y planta primera (definicion unica), con L de angulo interior TH_L"""
    t = 0.0                            # sin cara a 90 grados: el chaflan llega directo a la fachada del ala
    Q = (C[0] + t * N[0], C[1] + t * N[1])
    F0 = SWP(-L_C, 0.0); F1 = SWP(-L_C, W_C)
    IC = _inter(SWP(0, W_C), US, (0.0, 0.0), (0.0, 1.0))           # rincon interior de la L
    P1 = [F0, A1, C, Q, (W_P, Q[1]), (W_P, L_L), (0.0, L_L), IC, F1]
    o_s = (KC[0] + RETR * NS[0], KC[1] + RETR * NS[1])            # paralela retranqueada a la calle
    o_c = (A1[0] + RETR * N[0], A1[1] + RETR * N[1])              # paralela retranqueada al chaflan
    a1 = _inter(o_s, US, o_c, U)
    b1 = _inter(o_c, U, (W_P - RETR, 0.0), (0.0, 1.0))
    PB = [SWP(-L_C + L_LADR, RETR), a1, b1, (W_P - RETR, Y_CUNA), (W_P, Y_CUNA), (W_P, L_L),
          (0.0, L_L), IC, SWP(-L_C + L_LADR, W_C)]
    return dict(P1=P1, PB=PB, Q=Q, IC=IC)


def base():
    pl = plantas_base()
    s = [prisma(pl["PB"], 0, Z_PB + 0.01), prisma(pl["P1"], Z_PB, Z_P1)]
    xA = W_P - _a                     # arranque del chaflan en coordenadas 'de L recta'
    def ROT(m):                          # coordenadas 'de L recta' -> planta real (giro de la calle alrededor de KC)
        return m.translate((-KC[0], -KC[1], 0)).rotate((0, 0, math.degrees(PHI))).translate((KC[0], KC[1], 0))
    sc = []
    # ala corta: bloque alto (detras de la banda del restaurante) y ladrillo sobre pilares en el extremo
    sc.append(caja(-L_C + L_LADR, xA - 1.0, 5.5, W_C, Z_P1 - 0.01, Z_ALTO))
    L_HOR = _v["L_HOR"]
    sc.append(caja(-L_C, -L_C + L_HOR, 0, W_C, _v["Z_PB"], _v["Z_P1"]))                     # extremo: cuerpo de hormigon sobre pilares [F72]
    sc.append(caja(-L_C + L_HOR, -L_C + L_HOR + L_LADR, 0, W_C, 0, _v["Z_LAD1"]))          # volumen de ladrillo del suelo a cubierta [F72]
    for xp in (-L_C + 0.6, -L_C + _v["L_HOR"] - 0.6):
        for yp in (0.6, W_C - 0.6):
            sc.append(caja(xp - 0.35, xp + 0.35, yp - 0.35, yp + 0.35, 0, 5.01))
    for i in range(6):                                      # lucernarios en diente de sierra [F01]
        x = -L_C + L_LADR + 1.5 + 2.0 * i
        sc.append(Manifold.extrude(CrossSection.square((1.4, 1.4), True), 1.0, 0, 0, (0.05, 0.05)).translate((x, 8.5, Z_ALTO - 0.01)))
    mq = Manifold.sphere(1.0, 48).scale((4.0, 2.2, 1.6)) ^ caja(-5, 5, 0, 3, 0, 2)
    sc.append(mq.translate((xA - 7.0, 0.3, 0)))                       # marquesina curva [PASADA 1: F15]
    s.append(ROT(Manifold.batch_boolean(sc, OpType.Add)))
    # ala larga: bar en la mitad interior hasta el tramo final; terraza con peto en la mitad exterior [F47, Bing]
    yb0 = pl["Q"][1]
    yb1 = L_L - L_FIN                                                   # 1984: el bar acaba sobre la 1a ventana [F01, F47]
    s += [caja(0, W_BAR, yb0, yb1, Z_P1 - 0.01, Z_BAR),
          caja(0, W_BAR + _v["V_BAR"], yb0, yb1 + _v["V_BAR"], Z_BAR, Z_BAR_C),     # cubierta volada en frente y extremo
          caja(0, 0.1, yb1, L_L, Z_P1 - 0.01, Z_P1 + 1.1),                         # barandilla borde patio de la terraza abierta [F47]
          caja(W_P - 0.3, W_P, yb0, L_L, Z_P1 - 0.01, Z_P1 + _v["H_PET"]),             # peto exterior terraza [F73 +8,5]
          caja(0, W_P - 0.3, L_L - 0.25, L_L - 0.15, _v["Z_FIN"] - 0.01, _v["Z_FIN"] + 1.1)]   # testero a cota terraza + barandilla [F73]
    # concha: franja exterior que se estrecha de W_EXT a W_P hasta Y_CUNA; alta junto al hotel (+7,3) y baja en
    # curva al suelo; debajo, planta baja hundida [F47, F09, Bing]
    y0 = pl["Q"][1] + _v["D_HOTF"]          # la concha empieza tras la banda del hotel sobre la fachada del ala [C04]
    # RAMPA (F71): plano inclinado de ancho constante pegado a la fachada exterior del ala; sube desde el suelo
    # (lejos de la torre) hasta la terraza de la planta primera junto a la banda del hotel; peto en el borde exterior.
    WR = W_EXT - W_P
    YA, YB = _v["Y_CA"], _v["Y_CA"] + _v["R_FIN"]
    LR = YB - y0
    Y_ARC = y0 + _v["U_ARC"] * (Y_CUNA - y0)
    def zr(yy):         # coronación: alta (Z_CON) hasta YA; curva final cóncava: casi vertical arriba, abierta abajo [F73, F71, F47]
        if yy <= YA: return _v["Z_CON"]
        t = min((yy - YA) / (YB - YA), 1.0)
        return max(0.05, _v["Z_CON"] * (1 - math.sqrt(max(0.0, 1 - (1 - t) ** 2))))
    def zs(yy):         # intradós del arco bajo la concha junto al hotel [F47 vacío oscuro, F71, F76]
        if yy >= Y_ARC: return 0.0
        u = (yy - y0) / (Y_ARC - y0)
        return min(_v["Z_ARC"] * math.sqrt(max(0.0, 1 - u ** 2)), zr(yy) - 0.6)
    def wr(yy):         # ancho en planta: WR hasta YA, se cierra hasta el espesor de un muro en YB
        return WR if yy <= YA else max(0.3, WR * (1 - (yy - YA) / (YB - YA)))
    def f(v):
        x, y, z = v
        yy = y0 + min(max(y, 0.0), 1.0) * (YA - y0)
        lo, hi = zs(yy), zr(yy)
        return (W_P - 0.02 + x * WR, yy, lo + z * (hi - lo))
    rampa = Manifold.cube((1, 1, 1)).refine(60).warp(f)
    # curva final: perfil (y, z) exacto extruido en el ancho, que se cierra hacia la fachada
    prof = [(YA - 0.05, 0.0), (YA - 0.05, _v["Z_CON"])] + [(YA + (YB - YA) * k / 40, zr(YA + (YB - YA) * k / 40)) for k in range(1, 41)] + [(YB, 0.0)]
    cs = CrossSection([prof])
    if cs.area() <= 0: cs = CrossSection([prof[::-1]])
    fin = Manifold.extrude(cs, 1.0).rotate((90, 0, 0)).rotate((0, 0, 90))      # (y,z) -> plano y-z, espesor en x
    bb = fin.bounding_box()
    fin = fin.translate((-bb[0], 0, 0)).scale((WR, 1, 1)).translate((W_P - 0.02, 0, 0))
    def taper(v):
        x, y, z = v
        return (W_P - 0.02 + (x - W_P + 0.02) * max(0.3, WR * (1 - (y - YA) / (YB - YA))) / WR if y > YA else x, y, z)
    rampa = rampa + fin.warp(taper)
    def fp(v):
        x, y, z = v
        yy = y0 + min(max(y, 0.0), 1.0) * min(LR, YA - y0)
        return (W_P + wr(yy) - 0.25 + x * 0.25, yy, zr(yy) - 0.01 + z * 1.0)   # peto de 1 m sobre el tramo alto
    peto = Manifold.cube((1, 1, 1)).refine(40).warp(fp)
    s += [rampa, peto]
    # RAMPA 2 (F71, F76): de la terraza (+Z_P1) a la azotea del bar (+Z_BARC), por fuera del bar, junto a la torre;
    # bajo su llegada, arco de paso; barandilla en el borde de la azotea (la roja de F73/F71)
    xr2 = W_BAR + _v["V_BAR"]
    ya2 = yb0 + _v["R2_Y0"]; yz2 = ya2 + _v["R2_L"]
    def f2(v):
        x, y, z = v
        u = min(max(y, 0.0), 1.0)
        zt = Z_P1 + u * (Z_BAR_C - Z_P1)
        return (xr2 - 0.01 + x * _v["R2_W"], ya2 + u * (yz2 - ya2), Z_P1 - 0.01 + z * (zt - Z_P1 + 0.01))
    rampa2 = Manifold.cube((1, 1, 1)).refine(30).warp(f2)
    def f2p(v):
        x, y, z = v
        u = min(max(y, 0.0), 1.0)
        zt = Z_P1 + u * (Z_BAR_C - Z_P1)
        return (xr2 + _v["R2_W"] - 0.2 + x * 0.2, ya2 + u * (yz2 - ya2), zt - 0.01 + z * 1.0)
    s += [rampa2, Manifold.cube((1, 1, 1)).refine(30).warp(f2p),
          caja(xr2, xr2 + _v["R2_W"], yz2, yb1 + _v["V_BAR"], Z_BAR, Z_BAR_C),                       # paso a la azotea
          caja(xr2 + _v["R2_W"] - 0.1, xr2 + _v["R2_W"], yz2, yb1 + _v["V_BAR"], Z_BAR_C - 0.01, Z_BAR_C + 1.0),
          caja(0, xr2, yb1 + _v["V_BAR"] - 0.1, yb1 + _v["V_BAR"], Z_BAR_C - 0.01, Z_BAR_C + 1.0)]   # barandilla azotea
    m = Manifold.batch_boolean(s, OpType.Add)
    # arco de paso bajo la llegada de la rampa 2 [F71, F76]
    arc = Manifold.cylinder(_v["R2_W"] + 2, _v["ARC2_W"] / 2, _v["ARC2_W"] / 2, 48).rotate((0, 90, 0))
    arc = (arc.translate((xr2 - 1, yz2 - _v["ARC2_W"] / 2 - 0.5, Z_P1 + 1.2)) + caja(xr2 - 1, xr2 + _v["R2_W"] + 1, yz2 - _v["ARC2_W"] - 0.5, yz2 - 0.5, Z_P1, Z_P1 + 1.2))
    m = m - arc
    # huecos de ventanas (franjas continuas casi a paño) [F09, F14]
    hue = [ROT(caja(-L_C + L_LADR + 0.4, xA, -1, 0.3, 4.6, 6.6))]
    # HUECOS DEL ALA LARGA (pasada 11, proporciones F73/F01/F47): 11 arriba, 7 abajo bajo los 7 más cercanos al
    # testero, intereje S_VEN, hueco 0,47 S; marco que sale MAR_P y vidrio MAR_R por detrás del frente del marco
    n, nb, w, S_ = int(_v["N_VEN"]), int(_v["N_VEN_B"]), _v["VEN_W"], _v["S_VEN"]
    p_, rr_, bd = _v["MAR_P"], _v["MAR_R"], _v["MAR_B"]
    marcos = []
    for i in range(n):                                   # i = 0 junto al testero
        y1_ = L_L - _v["VEN_FIN"] - i * S_; y0_ = y1_ - w
        filas = [(_v["VA_0"], _v["VA_1"])] + ([(_v["VB_0"], _v["VB_1"])] if i < nb else [])
        for z0, z1 in filas:
            marcos.append(caja(W_P - 0.01, W_P + p_, y0_ - bd, y1_ + bd, z0 - bd, z1 + bd))
            marcos.append(caja(W_P - 0.01, W_P + p_ + 0.06, y0_ - bd - 0.05, y1_ + bd + 0.05, z0 - bd - 0.1, z0 - bd))  # alféizar con goterón
            hue.append(caja(W_P + p_ - rr_, W_P + 1, y0_, y1_, z0, z1))           # hueco hasta el vidrio
    # testero: puerta de servicio con marquesina saliente y ventana encima [F73: a 0,49-0,63 del ancho desde la esquina exterior]
    hue.append(caja(W_P - 0.63 * W_P, W_P - 0.49 * W_P, L_L - 0.3, L_L + 1, 0.0, 2.6))
    hue.append(caja(W_P - 0.55 * W_P, W_P - 0.43 * W_P, L_L - 0.3, L_L + 1, 4.6, 5.3))
    marcos.append(caja(W_P - 0.71 * W_P, W_P - 0.36 * W_P, L_L - 0.01, L_L + 1.2, 3.1, 4.4))
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
    if L_CH - _k - R_COL > 1.0:                                                                    # tramo de hotel en el chaflan (si queda)
        m = m + en_torre(caja(xh0, L_CH - _k, yf - 0.3, yf + 2.0, 3.1, 4.3))
        hue_t.append(caja(xh0 + 0.3, L_CH - _k - 0.4, yf - 1, yf + 0.3, 4.35, 6.0))
    # banda del hotel sobre la fachada exterior del ala larga, desde el fin del chaflan hasta la concha [C04]
    yc0, yc1 = C[1] + 0.3, C[1] + _v["D_HOTF"] - 0.3
    m = m + caja(W_P - 2.0, W_P + 0.3, C[1], C[1] + _v["D_HOTF"], 3.1, 4.3)                      # canto volado
    m = m - caja(W_P - 0.3, W_P + 1.0, yc0, yc1, 4.35, 6.0)                                       # vidrio
    m = m - caja(W_P - RETR, W_P + 1.0, C[1], C[1] + _v["D_HOTF"], -1, 3.1)                       # entrada del hotel en hueco                    # vidrio hotel
    return m - en_torre(Manifold.batch_boolean(hue_t, OpType.Add))


def torre():
    s = [cil(T, R_COL, 0, Z_CU0 + 0.1),
         Manifold.cylinder(4.0, _v["R_CONO"], R_COL, SEG).translate((T[0], T[1], 0)),   # pie de columna (recto: el 'cono' era un toldo) cil(T, R_CU, Z_CU0, Z_CU1 + 0.05),
         cil(T, R_CU + 0.6, Z_CU0, Z_CU0 + 0.6)]                       # losa inferior del cuello, volada [F18, F50]
    # vigas radiales bajo el barril y barril con forjados/poyetes + aletas
    s.append(cil(T, R_B - 0.1, Z_CU1 - 0.01, Z_ALETA0 + 0.05))   # fondo del barril (sofito plano a la cota de las aletas)
    for k in range(N_AL):                                   # 19 ménsulas triangulares: de la punta de la aleta al borde del cuello
        a = math.degrees(2 * math.pi * k / N_AL)
        pts = [(R_CU - 0.3, Z_CU1), (R_CU - 0.3, Z_ALETA0 + 0.05), (R_AL, Z_ALETA0 + 0.05)]
        pl_ = Manifold.extrude(CrossSection([pts]), 0.4).translate((0, 0, -0.2)).rotate((90, 0, 0))
        if pl_.volume() <= 0:
            pl_ = Manifold.extrude(CrossSection([pts[::-1]]), 0.4).translate((0, 0, -0.2)).rotate((90, 0, 0))
        s.append(pl_.rotate((0, 0, a)).translate((T[0], T[1], 0)))
    rf = R_B - 1.8
    s.append(cil(T, rf, Z_B0, Z_B1 + 0.4))
    for i in range(N_PL):
        z = Z_B0 + i * F
        s.append(cil(T, R_B, z, z + 0.65) - cil(T, rf - 0.1, z - 0.1, z + 0.7))          # canto del forjado 0,65 [F09]
        s.append(cil(T, R_B, z + 0.75, z + 1.65) - cil(T, R_B - 0.25, z + 0.7, z + 1.7))  # poyete 0,90 tras ranura 0,10 [F09]
    s.append(cil(T, R_B, Z_B1, Z_B1 + 0.65))
    s.append(cil(T, R_B, Z_B1 + 0.65, Z_B1 + 1.05) - cil(T, R_B - 0.2, Z_B1, Z_B1 + 1.2))   # peto terraza de servicio (+33,55) [F09]
    for k in range(N_AL):
        a = 2 * math.pi * k / N_AL
        al = Manifold.cube((R_AL - rf + 0.2, 0.4, Z_B1 + 0.65 - Z_ALETA0)).translate((rf - 0.1, -0.2, Z_ALETA0))
        s.append(al.rotate((0, 0, math.degrees(a))).translate((T[0], T[1], 0)))
    # tambor de ojos, banda, visera, remate
    s.append(cil(T, R_T, Z_B1, Z_T1))
    for k in range(N_AL):
        a = math.degrees(2 * math.pi * (k + 0.5) / N_AL)
        ojo = Manifold.cylinder(0.5, 0.8, 0.8, 24).rotate((0, 90, 0)).translate((R_T - 0.1, 0, (Z_B1 + Z_T1) / 2))
        s.append(ojo.rotate((0, 0, a)).translate((T[0], T[1], 0)))
    pv = P(*OFF_V); pr = P(*OFF_R)
    s.append(cil(T, R_G - 0.3, Z_T1, Z_G1))
    nm = int(2 * math.pi * R_G / 2.4)
    for k in range(nm):                                     # montantes de la banda acristalada [F10, F17]
        mt = Manifold.cube((0.5, 0.25, Z_G1 - Z_T1)).translate((R_G - 0.45, -0.125, Z_T1))
        s.append(mt.rotate((0, 0, 360 * k / nm)).translate((T[0], T[1], 0)))
    s.append(cil(pv, R_V, Z_G1, Z_V1))
    s.append(cil(pr, R_R, Z_V1, Z_R1))
    # escalera trasera, en linea con el ala larga [usuario, F11-F13]
    xe = _v["ESC_X"]                             # eje de la escalera (cuadro de cotas)
    s.append(caja(xe - ESC_W / 2, xe + ESC_W / 2, ESC_Y0, ESC_Y1, 0.0, Z_T1 + 1.0))   # la escalera baja hasta el suelo [coherencia]
    m = Manifold.batch_boolean(s, OpType.Add)
    # entrante (hueco hacia dentro) en la cara hacia el patio, entre dos hojas macizas: se ven los rellanos [F75, F13]
    ym = (T[1] + R_B + ESC_Y1) / 2
    xi = xe - ESC_W / 2
    m = m - caja(xi - 0.5, xi + _v["ESC_REC"], ym - _v["ESC_RL"] / 2, ym + _v["ESC_RL"] / 2, Z_P1 + 0.5, Z_T1 + 0.2)
    for k in range(int((Z_T1 - Z_P1) / (F / 2))):                                     # rellanos vistos en el entrante
        zr = Z_P1 + 0.5 + k * F / 2
        m = m + caja(xi + _v["ESC_REC"] - 1.4, xi + _v["ESC_REC"], ym - _v["ESC_RL"] / 2, ym + _v["ESC_RL"] / 2, zr, zr + 0.25)
    # ventanas de las habitaciones: un hueco por modulo entre aletas, sobre el poyete [F04, F06, F09]
    hue = []
    for i in range(N_PL):
        z = Z_B0 + i * F
        for k in range(N_AL):
            a = math.degrees(2 * math.pi * (k + 0.5) / N_AL)
            if i == 0:
                h = Manifold.cube((0.5, 2.6, 1.4)).translate((rf - 0.25, -1.3, z + 1.7))   # pavés [F09]
            else:
                h = Manifold.cube((0.5, 2.4, 1.4)).translate((rf - 0.25, -1.2, z + 1.7))   # ventana hasta el forjado superior [F09]
            hue.append(h.rotate((0, 0, a)).translate((T[0], T[1], 0)))
    m = m - Manifold.batch_boolean(hue, OpType.Add)
    # lamas verticales de la escalera trasera [F11-F13]
    lam = []
    x = xe - ESC_W / 2 + 0.4
    while x < xe + ESC_W / 2 - 0.3:                                     # testa
        lam.append(caja(x - 0.12, x + 0.12, ESC_Y1, ESC_Y1 + 0.5, Z_P1 + 0.5, Z_T1 + 0.5))
        x += 0.8
    y = T[1] + R_B + 0.3
    while y < ESC_Y1 - 0.2:                                             # lados largos
        if abs(y - ym) > _v["ESC_RL"] / 2:
            for xx in (xe - ESC_W / 2 - 0.5, xe + ESC_W / 2):
                lam.append(caja(xx, xx + 0.5, y - 0.12, y + 0.12, Z_P1 + 0.5, Z_T1 + 0.5))
        y += 0.8
    return m + Manifold.batch_boolean(lam, OpType.Add)


def edificio():
    return base() + torre()


if __name__ == "__main__":
    m = edificio()
    print("ok", m.status(), "T=", tuple(round(v, 2) for v in T), "A1=", tuple(round(v, 2) for v in A1), "C=", tuple(round(v, 2) for v in C))
    print(plantas_base())
