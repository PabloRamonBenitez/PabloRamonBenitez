"""Definicion del Hotel Salut SOLO con medidas de fotos y de Bing (no hereda nada del modelo 3D anterior).
Coordenadas (m): calle Ivana Mazepy = eje x (y=0, fachada a la calle del ala corta); ala larga hacia +y
(perpendicular a la calle, Bing F35/F48: 83-90 grados); cara interior del ala larga en x=0.
Fuentes de cada cota entre corchetes."""
import math
from manifold3d import Manifold, CrossSection, OpType

SEG = 96
# ------------------------------------------------------------------ alturas [F09, F14]
Z_PB = 3.9          # techo planta baja                          [F09 3,9 / F14 3,6]
Z_P1 = 7.3          # coronacion planta primera = terraza         [F09 7,3 / F14 7,2]
Z_BAR = 10.6        # techo del bar (una planta sobre la terraza) [F47 proporcion con la banda]
Z_BAR_C = 11.1      # cubierta volada del bar
Z_ALTO = 11.5       # bloque alto del ala corta                    [F01, seccion AA del usuario ~12]
Z_LADR = 9.0        # bloque de ladrillo                           [F01]
Z_CU0 = 10.4                   # cuello (base)                     [F09; se revisa en fase 4]
Z_B0, N_PL, F = 13.9, 6, 3.1   # barril: 6 plantas de 3,1 (5 con ventanas + pavés) [FASE 1: F09, dinteles cada 40 px]
Z_CU1 = Z_B0
Z_ALETA0 = 15.2                # borde inferior visible de las aletas; debajo, ménsulas [F09]
Z_B1 = Z_B0 + N_PL * F         # 32,6
Z_T1 = 38.2                    # tambor de ojos                    [F09 5,4]
Z_G1 = 40.5                    # banda acristalada                 [F09 2,3]
Z_V1 = 43.7                    # visera                            [F09 3,2]
Z_R1 = 49.1                    # remate (sin antenas)              [F09 total 49,1]
# ------------------------------------------------------------------ radios / anchos [F09, F14, F01]
R_COL = 3.25        # columna 6,5                                   [F09 6,5 / F14 6,0]
R_CU = 7.5          # cuello 15,0                                   [F09]
R_B = 14.4          # borde de balcones; aletas hasta 15,3 (30,6)   [escala]
R_AL = 15.3
R_T = 13.55         # tambor de ojos 27,1                           [F01, F09, F14]
R_G = 10.85         # banda acristalada 21,7                        [F09]
R_V = 12.8          # visera 25,6                                   [F09 25,6 / F01 25,3; Google 24,35]
R_R = 5.6           # remate 11,2                                   [F09 11,2 / F14 10,3 / F01 10,0]
OFF_V = (-2.4, -0.4)    # visera desplazada hacia el restaurante     [F09 2,4 a la izquierda]
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
A_CH = math.radians(float(os.environ.get("ACH", "57")))   # angulo del chaflan con la calle [F01: 55-58; provisional]
REST, COL, HOT = 12.8, 6.5, 9.6             # tramos del chaflan    [F09]
L_CH = REST + COL + HOT
U = (math.cos(A_CH), math.sin(A_CH))
N = (-U[1], U[0])                           # hacia dentro
# la esquina del hotel (fin del chaflan) cae en el borde exterior de la concha (x = W_EXT) [dibujo del usuario]
A1 = (W_EXT - L_CH * U[0], 0.0)             # arranque del chaflan en la calle
C = (A1[0] + L_CH * U[0], A1[1] + L_CH * U[1])
RET = 1.5           # la columna asoma por delante de la planta primera [F09/F18]
RETR = 2.5          # retranqueo de la planta baja bajo la planta primera [F09, F14, F47]
_k = REST + COL / 2
T = (A1[0] + _k * U[0] + (R_COL - RET) * N[0], A1[1] + _k * U[1] + (R_COL - RET) * N[1])   # eje de la torre
L_C, W_C = 24.0, 12.0       # ala corta: extremo de la calle en x=-L_C, fondo 12   [F01, estimado]
L_LADR = 5.0                # bloque de ladrillo del extremo, sobre pilares       [F01]
# escalera trasera: en linea con el ala larga, dentro de la L [usuario]
ESC_W, ESC_Y0, ESC_Y1 = 8.0, T[1] + 10.0, T[1] + R_AL + 1.0


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
    """poligonos de planta baja y planta primera (definicion unica)"""
    def sobre_linea(off, k):           # punto de la paralela al chaflan desplazada 'off' hacia dentro, en x o y = k
        pass
    # planta primera: frente en la calle (y=0) y en la linea del chaflan; acaba en C con cara a 90 grados
    # que vuelve hasta la fachada del ala larga (x = W_P)
    t = (W_P - C[0]) / N[0]            # avance desde C hacia dentro hasta la fachada del ala
    Q = (C[0] + t * N[0], C[1] + t * N[1])
    P1 = [(-L_C, 0.0), A1, C, Q, (W_P, Q[1]), (W_P, L_L), (0.0, L_L), (0.0, W_C), (-L_C, W_C)]
    # planta baja: retranqueada RETR en la calle y en el chaflan; en el ala larga hasta la fachada
    a1 = (A1[0] + RETR * (math.tan(A_CH / 2)), RETR)       # interseccion de las dos paralelas retranqueadas
    # punto donde la paralela al chaflan (retranqueada) corta x = W_P - RETR
    def corte_x(xk):
        o = (A1[0] + RETR * N[0], A1[1] + RETR * N[1])
        s = (xk - o[0]) / U[0]
        return (xk, o[1] + s * U[1])
    PB = [(-L_C + L_LADR, RETR), a1, corte_x(W_P - RETR), (W_P - RETR, Y_CUNA), (W_P, Y_CUNA), (W_P, L_L),
          (0.0, L_L), (0.0, W_C), (-L_C + L_LADR, W_C)]
    return dict(P1=P1, PB=PB, Q=Q)


def base():
    pl = plantas_base()
    s = [prisma(pl["PB"], 0, Z_PB + 0.01), prisma(pl["P1"], Z_PB, Z_P1)]
    # ala corta: bloque alto (detras de la banda del restaurante) y ladrillo sobre pilares en el extremo
    s.append(caja(-L_C + L_LADR, A1[0] - 1.0, 5.5, W_C, Z_P1 - 0.01, Z_ALTO))
    s.append(caja(-L_C, -L_C + L_LADR, 0, W_C, Z_PB, Z_LADR))
    for xp in (-L_C + 0.6, -L_C + L_LADR - 0.6):
        for yp in (0.6, W_C - 0.6):
            s.append(caja(xp - 0.35, xp + 0.35, yp - 0.35, yp + 0.35, 0, Z_PB + 0.01))
    for i in range(6):                                      # lucernarios en diente de sierra [F01]
        x = -L_C + L_LADR + 1.5 + 2.0 * i
        s.append(Manifold.extrude(CrossSection.square((1.4, 1.4), True), 1.0, 0, 0, (0.05, 0.05)).translate((x, 8.5, Z_ALTO - 0.01)))
    # ala larga: bar en la mitad interior hasta el tramo final; terraza con peto en la mitad exterior [F47, Bing]
    yb0 = pl["Q"][1]
    s += [caja(0, W_BAR, yb0, L_L - L_FIN, Z_P1 - 0.01, Z_BAR),
          caja(0, W_BAR + 1.2, yb0, L_L - L_FIN, Z_BAR, Z_BAR_C),
          caja(W_P - 0.3, W_P, yb0, L_L, Z_P1 - 0.01, Z_P1 + 1.0),
          caja(W_BAR, W_P, L_L - 0.3, L_L, Z_P1 - 0.01, Z_P1 + 1.0)]
    # concha: franja exterior que se estrecha de W_EXT a W_P hasta Y_CUNA; alta junto al hotel (+7,3) y baja en
    # curva al suelo; debajo, planta baja hundida [F47, F09, Bing]
    y0 = pl["Q"][1]
    def f(v):
        x, y, z = v
        y = min(max(y, 0.0), 1.0)
        return (W_P - 0.02 + x * max(0.05, (W_EXT - W_P) * (1 - y)), y0 + y * (Y_CUNA - y0), Z_PB * (1 - y) + z * max(0.05, (Z_P1 - Z_PB * (1 - y)) * max(0.0, 1 - y) ** 1.3))
    concha = Manifold.cube((1, 1, 1)).refine(30).warp(f)
    s.append(concha)
    m = Manifold.batch_boolean(s, OpType.Add)
    # huecos de ventanas (franjas continuas casi a paño) [F09, F14]
    hue = [caja(-L_C + L_LADR + 0.4, A1[0], -1, 0.3, 4.6, 6.6)]
    for k in range(10):                                     # ala larga: 2 filas de 10 en la mitad del fondo [F47]
        y = 52.0 + 1.2 + 4.0 * k
        for z0 in (1.2, 4.6):
            hue.append(caja(W_P - 0.3, W_P + 1, y, y + 1.6, z0, z0 + 1.6))
    m = m - Manifold.batch_boolean(hue, OpType.Add)
    # chaflan (coordenadas de torre): franjas de ventanas restaurante / hotel
    rot = math.degrees(A_CH)
    def en_torre(mm):
        return mm.rotate((0, 0, rot)).translate((T[0], T[1], 0))
    yf = -(R_COL - RET)
    hue_t = [caja(-REST - COL / 2 + 0.4, -R_COL - 0.3, yf - 1, yf + 0.3, 4.6, 6.6),
             caja(R_COL + 0.3, R_COL + HOT - 0.4, yf - 1, yf + 0.3, 4.6, 6.6)]
    return m - en_torre(Manifold.batch_boolean(hue_t, OpType.Add))


def torre():
    s = [cil(T, R_COL, 0, Z_CU0 + 0.1), cil(T, R_CU, Z_CU0, Z_CU1 + 0.05)]
    # vigas radiales bajo el barril y barril con forjados/poyetes + aletas
    s.append(Manifold.cylinder(Z_B0 - Z_CU1 + 0.05, R_CU, R_B - 0.1, SEG).translate((T[0], T[1], Z_CU1)))
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
    xe = W_BAR / 2 + 0.5
    s.append(caja(xe - ESC_W / 2, xe + ESC_W / 2, ESC_Y0, ESC_Y1, Z_P1 - 0.01, Z_T1 + 1.0))
    m = Manifold.batch_boolean(s, OpType.Add)
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
    while x < xe + ESC_W / 2 - 0.3:
        lam.append(caja(x - 0.12, x + 0.12, ESC_Y1, ESC_Y1 + 0.5, Z_P1 + 0.5, Z_T1 + 0.5))
        x += 0.8
    return m + Manifold.batch_boolean(lam, OpType.Add)


def edificio():
    return base() + torre()


if __name__ == "__main__":
    m = edificio()
    print("ok", m.status(), "T=", tuple(round(v, 2) for v in T), "A1=", tuple(round(v, 2) for v in A1), "C=", tuple(round(v, 2) for v in C))
    print(plantas_base())
