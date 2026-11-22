"""Hotel Salut (Kyiv) - modelo 3D v2, a partir de fotos.
Cotas en METROS reales; se exporta en mm escalado a ALTURA_MM (15 cm -> ~1:330).
Proporciones medidas en la foto frontal con teleobjetivo (planta F = 3 m, cuerpo D = 9,6 F).
Ejes: +Y = fachada trasera (caja de escalera), -Y = fachada principal (calle Ivana Mazepy).
"""
import math
import numpy as np
from manifold3d import Manifold, CrossSection, OpType, FillRule

ALTURA_MM = 150.0          # altura total deseada de la maqueta
SEG = 128
F = 3.0                      # altura de planta
N_DIV = 19                   # divisiones angulares (muros radiales)
PASO = 360.0 / N_DIV

# --- niveles (m) ---
Z_COL0, Z_TERRAZA = 0.0, 9.0          # columna desde el suelo; cubierta del estilobato
Z_CUELLO0, Z_CUELLO1 = 11.2, 15.1     # cuello; encima, intrados inclinado con vigas radiales
Z_HAB0 = 15.8                         # forjado inferior de las habitaciones
N_PLANTAS = 6
Z_HAB1 = Z_HAB0 + N_PLANTAS * F       # 33.3
Z_OJOS0, Z_OJOS1 = Z_HAB1, Z_HAB1 + 5.3   # tambor con "ojos" (~1,75 plantas)
Z_VID0, Z_VID1 = Z_OJOS1, Z_OJOS1 + 2.6        # banda acristalada
Z_VIS_INF, Z_VIS_BORDE, Z_VIS1 = Z_VID1, Z_VID1 + 0.3, Z_VID1 + 2.3  # visera: arranque inferior, borde, cubierta
Z_TOP0, Z_TOP1 = Z_VIS1, Z_VIS1 + 5.2     # tambor del letrero
# --- radios (m) ---
R_B = 14.4                   # borde de balcones (D = 28,8 m)
FONDO_BALCON = 1.8
R_CUELLO, R_COL = 9.1, 3.0   # cuello 0,63 D; columna ~6 m de diametro (foto frontal)
R_OJOS = 12.7                # el tambor deja una terraza de servicio de ~1,7 m
R_VID, R_VIS, R_VIS_INF = 9.7, 12.1, 10.0
R_TOP = 4.8
OFF_VIS = (-2.2, -1.8)       # la VISERA es la que va claramente descentrada (fotos frontal, epoca y aerea)
OFF_VID = (-0.8, -0.6)       # la banda acristalada va casi centrada sobre el tambor
OFF_TOP = (0.0, 0.5)         # tambor superior casi en el eje, algo hacia la escalera
# --- caja de escalera trasera ---
ESC_MEDIO = 4.5
ESC_Y0, ESC_Y1 = 8.0, R_B + 0.4
ESC_Z1 = Z_OJOS1 + 1.2


def cil(r, z0, z1, c=(0, 0), seg=SEG):
    return Manifold.cylinder(z1 - z0, r, r, seg).translate((c[0], c[1], z0))


def anillo(ri, ro, z0, z1, c=(0, 0)):
    return cil(ro, z0, z1, c) - cil(ri, z0 - 0.01, z1 + 0.01, c)


def caja(x0, x1, y0, y1, z0, z1):
    return Manifold.cube((x1 - x0, y1 - y0, z1 - z0)).translate((x0, y0, z0))


def placa_rz(pts, espesor, ang, c=(0, 0)):
    """Poligono en el plano radio-altura, extruido con 'espesor' y girado al angulo 'ang' (grados)."""
    area = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1]
               for i in range(len(pts)))
    if area < 0:
        pts = pts[::-1]
    m = Manifold.extrude(CrossSection([pts]), espesor).translate((0, 0, -espesor / 2))
    return m.rotate((90, 0, 0)).rotate((0, 0, ang)).translate((c[0], c[1], 0))


def radios_planta(i):
    rb = R_B * (1 + 0.02 * math.sin(math.pi * (i + 0.5) / N_PLANTAS))   # ligero barril
    return rb, rb - FONDO_BALCON


def cuerpo_habitaciones():
    balc, fijo = [], []
    rw_min = min(radios_planta(i)[1] for i in range(N_PLANTAS))
    fijo.append(cil(rw_min, Z_HAB0, Z_HAB1 + 0.5))               # fachada de ventanas (continua)
    # intrados inclinado: del cuello sube hasta el borde inferior del barril (paneles entre vigas)
    fijo.append(Manifold.cylinder(Z_HAB0 - Z_CUELLO1 + 0.02, R_CUELLO, radios_planta(0)[0] - 0.05, SEG)
                .translate((0, 0, Z_CUELLO1 - 0.01)))
    for i in range(N_PLANTAS):
        rb, rw = radios_planta(i)
        z0 = Z_HAB0 + i * F
        fijo.append(cil(rw, z0, z0 + F))
        if i == 0:
            # primera planta del barril: cerrada con pavés, banda inferior gruesa a paño del borde
            balc.append(anillo(rw - 0.1, rb, z0, z0 + 1.0))
            balc.append(anillo(rw - 0.1, rb - 1.0, z0 + 1.0, z0 + F))
        else:
            balc.append(anillo(rw - 0.1, rb - 0.05, z0, z0 + 0.25))   # losa del balcon
            balc.append(anillo(rb - 0.35, rb - 0.05, z0, z0 + 0.5))   # canto del forjado
            balc.append(anillo(rb - 0.25, rb, z0 + 0.75, z0 + 1.5))   # poyete elevado (ranura debajo)
        for k in range(N_DIV):
            ang = 90 + PASO * k
            balc.append(placa_rz([(rw - 0.2, z0), (rb - 0.2, z0), (rb - 0.2, z0 + F), (rw - 0.2, z0 + F)], 0.4, ang))
            if i == 0:
                # aleta con escalon: arriba sobresale 0,9 m, abajo 0,3 m y baja 0,6 m en angulo recto
                balc.append(placa_rz([(rb - 0.3, z0 + 1.0), (rb + 0.9, z0 + 1.0), (rb + 0.9, z0 + F),
                                      (rb - 0.3, z0 + F)], 0.4, ang))
                # viga radial: del cuello al borde; canto creciente hacia el centro, extremo en angulo recto
                balc.append(placa_rz([(R_CUELLO - 0.4, z0 + 1.05), (rb + 0.3, z0 + 1.05), (rb + 0.3, z0 - 0.6),
                                      (R_CUELLO - 0.4, Z_CUELLO1 - 0.3)], 0.5, ang))
            else:
                balc.append(placa_rz([(rb - 0.3, z0 + 0.75), (rb + 0.9, z0 + 0.75), (rb + 0.9, z0 + F),
                                      (rb - 0.3, z0 + F)], 0.4, ang))
            # canalon / gargola: un punto en el centro de cada balcon, en el canto del forjado
            if i > 0:
                g_ = Manifold.cylinder(0.45, 0.13, 0.13, 16).rotate((0, 90, 0)).translate((rb - 0.25, 0, z0 + 0.28))
                balc.append(g_.rotate((0, 0, ang + PASO / 2)))
    rb, rw = radios_planta(N_PLANTAS - 1)
    balc.append(anillo(rw - 0.1, rb - 0.05, Z_HAB1, Z_HAB1 + 0.5))   # cubierta / canto superior
    for k in range(N_DIV):
        g_ = Manifold.cylinder(0.45, 0.13, 0.13, 16).rotate((0, 90, 0)).translate((rb - 0.25, 0, Z_HAB1 + 0.28))
        balc.append(g_.rotate((0, 0, 90 + PASO * (k + 0.5))))
    balcones = Manifold.batch_boolean(balc, OpType.Add)
    # los anillos de balcones terminan en seco contra la caja de escalera
    balcones = balcones - caja(-ESC_MEDIO - 0.2, ESC_MEDIO + 0.2, 0, 30, Z_HAB0 - 3, Z_HAB1 + 1)
    return Manifold.batch_boolean(fijo + [balcones], OpType.Add)


def tambor_ojos():
    p = [cil(R_OJOS, Z_OJOS0, Z_OJOS1) - cil(R_OJOS - 0.35, Z_OJOS1 - 0.9, Z_OJOS1 + 1)]   # peto de 0,9 m
    p.append(cil(R_OJOS - 0.3, Z_OJOS1 - 0.95, Z_OJOS1 - 0.85))
    zc = Z_OJOS0 + 0.5 * (Z_OJOS1 - Z_OJOS0)
    for k in range(N_DIV):
        ang = 90 + PASO * (k + 0.3)
        if abs(((ang - 90 + 180) % 360) - 180) < 36:   # junto a la escalera: muro liso con las puertas
            continue
        # "ojo": aro corto con anillos concentricos (sale poco del tambor)
        def eje_x(h, r, x0):
            return Manifold.cylinder(h, r, r, 40).rotate((0, 90, 0)).translate((x0, 0, 0))
        tubo = eje_x(0.7, 0.78, R_OJOS - 0.2)                  # aro exterior (Ø 1,56 m): sobresale 0,5 m
        hueco = eje_x(0.4, 0.58, R_OJOS + 0.1)                 # rebaje
        tubo = tubo - hueco + eje_x(0.3, 0.38, R_OJOS + 0.05)  # anillo interior
        hueco = eje_x(0.3, 0.16, R_OJOS + 0.1)                 # centro hundido
        p.append((tubo - hueco).rotate((0, 0, ang)).translate((0, 0, zc)))
    t = Manifold.batch_boolean(p, OpType.Add)
    for ang in (90 - 27, 90 + 27):   # puertas de servicio a la terraza, a ambos lados de la escalera
        puerta = caja(R_OJOS - 0.3, R_OJOS + 0.5, -0.45, 0.45, Z_OJOS0 + 0.5, Z_OJOS0 + 2.6)
        t = t - puerta.rotate((0, 0, ang))
    return t


def letras(texto, alto, espesor):
    """Letras extruidas (fuente DejaVu Sans Bold), centradas, en el plano XZ mirando a -Y."""
    from matplotlib.textpath import TextPath
    from matplotlib.font_manager import FontProperties
    tp = TextPath((0, 0), texto, size=1.0, prop=FontProperties(family="DejaVu Sans", weight="bold"))
    polys = [np.asarray(p) for p in tp.to_polygons() if len(p) > 2]
    cs = CrossSection([p.tolist() for p in polys], FillRule.EvenOdd)
    x0, y0, x1, y1 = cs.bounds()
    cs = cs.translate((-(x0 + x1) / 2, -y0)).scale((alto / (y1 - y0),) * 2)
    return Manifold.extrude(cs, espesor).rotate((90, 0, 0)).translate((0, espesor / 2, 0))


def remate():
    p = []
    # banda acristalada con montantes
    p.append(cil(R_VID - 0.2, Z_VID0, Z_VIS_INF + 0.2, OFF_VID))
    n_mont = int(2 * math.pi * R_VID / 2.4)
    for k in range(n_mont):
        p.append(placa_rz([(R_VID - 0.3, Z_VID0), (R_VID + 0.15, Z_VID0), (R_VID + 0.15, Z_VIS_INF + 0.1),
                           (R_VID - 0.3, Z_VIS_INF + 0.1)], 0.3, 360 * k / n_mont, OFF_VID))
    # visera: intrados inclinado + canto + nervios radiales debajo
    p.append(Manifold.cylinder(Z_VIS_BORDE - Z_VIS_INF, R_VIS_INF, R_VIS, SEG)
             .translate((OFF_VIS[0], OFF_VIS[1], Z_VIS_INF)))
    p.append(cil(R_VIS, Z_VIS_BORDE - 0.01, Z_VIS1, OFF_VIS))
    for k in range(24):
        p.append(placa_rz([(R_VIS_INF + 0.1, Z_VIS_INF + 0.05), (R_VIS - 0.1, Z_VIS_BORDE),
                           (R_VIS - 0.1, Z_VIS_BORDE - 0.45)], 0.3, 15 * k, OFF_VIS))
    # claraboya de cristal en piramide sobre la cubierta de la visera (delante)
    a = math.radians(-115)
    pir = Manifold.extrude(CrossSection.square((2.4, 2.4), True), 1.3, 0, 0, (0.02, 0.02))
    p.append(pir.translate((OFF_VIS[0] + 8.5 * math.cos(a), OFF_VIS[1] + 8.5 * math.sin(a), Z_VIS1 - 0.01)))
    # tambor superior con cubierta ligeramente abombada
    p.append(cil(R_TOP, Z_TOP0 - 0.01, Z_TOP1, OFF_TOP))
    p.append(Manifold.sphere(R_TOP, SEG).scale((1, 1, 0.14)).translate((OFF_TOP[0], OFF_TOP[1], Z_TOP1)))
    # letrero: letras sueltas siguiendo la curva del tambor superior (delante-derecha)
    R_L = R_TOP + 0.3
    piezas = [letras(ch, 2.3, 0.35) for ch in "САЛЮТ"]
    anchos = [m_.bounding_box()[3] - m_.bounding_box()[0] for m_ in piezas]
    hueco_l = 0.35
    total = sum(anchos) + hueco_l * (len(anchos) - 1)
    th = math.radians(-50) - (total / 2) / R_L
    for m_, w_ in zip(piezas, anchos):
        th += (w_ / 2) / R_L
        p.append(m_.translate((0, 0, Z_TOP0 + 1.2)).rotate((0, 0, math.degrees(th) + 90))
                 .translate((OFF_TOP[0] + R_L * math.cos(th), OFF_TOP[1] + R_L * math.sin(th), 0)))
        th += (w_ / 2 + hueco_l) / R_L
    return Manifold.batch_boolean(p, OpType.Add)


def escalera():
    p = [caja(-ESC_MEDIO, ESC_MEDIO, ESC_Y0, ESC_Y1, Z_TERRAZA - 0.1, ESC_Z1)]
    # tramo izquierdo retranqueado (jaula de escalera abierta)
    hueco = caja(2.3, ESC_MEDIO + 0.1, ESC_Y1 - 1.0, ESC_Y1 + 0.1, Z_CUELLO1, Z_OJOS1 - 0.5)
    p = [p[0] - hueco]
    # lamas verticales en tres planos escalonados
    x = -ESC_MEDIO + 0.2
    while x < 2.1:
        dy = 0.35 if (x // 2.2) % 2 == 0 else 0.0
        p.append(caja(x - 0.15, x + 0.15, ESC_Y1 - 0.05, ESC_Y1 + 0.35 + dy, Z_TERRAZA + 0.5, Z_OJOS1 - 0.3))
        x += 0.9
    for sx in (-1, 1):   # lamas en los costados
        y = ESC_Y0 + 1.0
        while y < ESC_Y1 - 0.5:
            xx = sx * (ESC_MEDIO + 0.2)
            p.append(caja(xx - 0.2, xx + 0.2, y - 0.15, y + 0.15, Z_TERRAZA + 0.5, Z_HAB0))
            y += 0.9
    p.append(caja(-1.5, 1.5, 10.0, 13.0, 0, Z_TERRAZA))       # pilar bajo la caja
    return Manifold.batch_boolean(p, OpType.Add)


def base_y_estilobato():
    p = [cil(R_COL, Z_COL0, Z_CUELLO0 + 0.1), cil(R_CUELLO, Z_CUELLO0, Z_CUELLO1 + 0.05),
         cil(R_CUELLO + 0.4, Z_CUELLO0, Z_CUELLO0 + 0.8)]          # losa inferior del cuello, algo volada
    for k in range(16):   # anillo de piramides invertidas bajo el cuello
        p.append(placa_rz([(R_COL - 0.2, Z_CUELLO0 + 0.05), (R_CUELLO - 0.3, Z_CUELLO0 + 0.05),
                           (R_COL + 0.3, Z_TERRAZA)], 1.6, 22.5 * k + 11))
    # ---------------- estilobato en L con chaflan (esquema del usuario + Google Maps) ----------------
    # Coordenadas de "solar": ala larga a lo largo de +Ys (94,8 x 15,7 m), su borde inferior (Ys=0) es la calle;
    # ala corta a lo largo de la calle hacia -Xs. El chaflan corta la esquina exterior desde el rincon interior
    # (0,0) hasta la fachada exterior del ala larga (15,7; 9,4) y la columna queda sobre el chaflan.
    W_L, L_L = 15.7, 94.8            # ala larga (medida en Google Maps)
    L_C, W_C = 24.0, 12.0            # ala corta junto a la calle (foto aerea: bloque alto ~16 m + bloque de ladrillo)
    # chaflan medido en la foto frontal: restaurante 11,6 m + columna 6 m + hotel 9,6 m = 27,2 m
    L_CH, D_REST = 27.2, 14.6        # longitud del chaflan; distancia del extremo izquierdo al eje de la columna
    A_CH = math.radians(31)          # angulo del chaflan (del esquema; no medible en las fotos)
    A1 = (W_L - L_CH * math.cos(A_CH), 0.0)
    A2 = (W_L, L_CH * math.sin(A_CH))
    ang = math.atan2(A2[1] - A1[1], A2[0] - A1[0])
    ux, uy = math.cos(ang), math.sin(ang)            # direccion del chaflan  (= +X de la torre)
    nx, ny = -math.sin(ang), math.cos(ang)           # hacia el interior     (= +Y de la torre, escalera)
    col = (A1[0] + D_REST * ux, A1[1] + D_REST * uy)  # columna sobre el chaflan
    RET = 1.5                                        # la columna asoma 1,5 m por delante del chaflan
    cen = (col[0] + RET * nx, col[1] + RET * ny)     # eje de la torre en coordenadas de solar
    def a_torre(m):
        return m.translate((-cen[0], -cen[1], 0)).rotate((0, 0, -math.degrees(ang)))
    L_pts = [(-L_C, 0), (W_L, 0), (W_L, L_L), (0, L_L), (0, W_C), (-L_C, W_C)]
    planta_L = CrossSection([L_pts]) - CrossSection([[A1, (W_L + 5, -5), (W_L + 5, A2[1] + (5 * math.tan(ang))), A2]])
    def caja_s(x0, x1, y0, y1, z0, z1):
        return caja(x0, x1, y0, y1, z0, z1)
    H_ALA = 11.5
    Y_T = A2[1] + 38.0               # fin del tramo alto con terraza y ventanas (foto aerea)
    solido = [Manifold.extrude(planta_L, H_ALA) ^ caja_s(-1, W_L + 1, A2[1] - 0.01, Y_T, -1, 30),   # tramo alto (3 plantas)
              Manifold.extrude(planta_L, 7.0) ^ caja_s(-1, W_L + 1, Y_T - 0.01, L_L + 1, -1, 30),     # resto del ala, mas bajo y ciego
              Manifold.extrude(planta_L, Z_TERRAZA) ^ caja_s(-1, W_L + 1, -1, A2[1] + 0.01, -1, 30),  # tramo del hotel junto a la torre
              # ---- ala corta, seccion AA: frontal volado (restaurante) + bloque alto detras ----
              Manifold.extrude(planta_L, 8.9) ^ caja_s(-L_C + 5.0, -0.01, -1, 6.0, -1, 30),         # frontal: banda del restaurante
              caja_s(-L_C + 5.0, -2.0, 5.5, W_C, 0, 12.0),                                         # bloque alto con lucernarios
              caja_s(-2.5, 0.01, 5.5, W_C, 0, 8.2),                                                # pieza baja junto a la torre
              caja_s(-L_C, -L_C + 5.0, 0, W_C, 0, 9.6),                                            # bloque de ladrillo del extremo
              caja_s(-4, W_L + 4, L_L - 11, L_L, 0, 9.0),                                          # remate transversal del fondo (maqueta original)
              # ---- ala larga, seccion BB: bar alto en el lado interior con voladizo sobre la terraza ----
              caja_s(0.0, 6.0, A2[1] - 3, A2[1] + 22, 0, 14.6),                                     # bar
              caja_s(5.9, 8.0, A2[1] - 3, A2[1] + 22, 14.0, 14.6),                                  # voladizo del bar sobre la terraza
              caja_s(W_L - 0.3, W_L, A2[1], Y_T, H_ALA - 0.01, H_ALA + 1.0),                        # peto de la terraza (lado exterior)
              caja_s(0, W_L, Y_T - 0.3, Y_T, H_ALA - 0.01, H_ALA + 1.0),                            # peto de la terraza (final)
              Manifold.hull_points([(6.6, Y_T + 2, 6.99), (9.0, Y_T + 2, 6.99), (7.8, Y_T + 2, 8.2),
                                    (6.6, L_L - 13, 6.99), (9.0, L_L - 13, 6.99), (7.8, L_L - 13, 8.2)])]  # lucernario en cumbrera
    for i in range(6):                                                                              # una fila de lucernarios en diente de sierra
        pir = Manifold.extrude(CrossSection.square((1.5, 1.5), True), 1.1, 0, 0, (0.05, 0.05))
        solido.append(pir.translate((-L_C + 6.6 + 2.2 * i, 8.5, 11.99)))
    # superficie curva del relieve (fotos aerea y frontal): cubierta inclinada y curva pegada a la fachada exterior
    # del ala larga, desde el bloque del hotel; lleva el relieve de estrellas y cubre los bajos comerciales.
    U_C, L_R, H_A, H_B = 5.0, 28.0, 7.0, 3.2
    perfil = [(0.0, 0.0), (U_C, 0.0), (U_C, H_B)]
    for k in range(1, 12):
        u = U_C * (1 - k / 12)
        perfil.append((u, H_B + (H_A - H_B) * math.sqrt(1 - (u / U_C) ** 2)))
    perfil.append((0.0, H_A))
    cuerpo_r = Manifold.extrude(CrossSection([perfil]), L_R).rotate((90, 0, 0)).rotate((0, 0, 0))
    # tras rotate(90,0,0): x=u, z=altura, y va de 0 a -L_R  -> lo damos la vuelta para que crezca en +Y
    cuerpo_r = cuerpo_r.mirror((0, 1, 0))
    planta_r = [(0, 0), (U_C, 0)]
    for k in range(13):
        t_ = k / 12; y = 16 + 12 * t_
        planta_r.append((U_C * math.sqrt(max(0.0, 1 - t_ ** 2)), y))
    planta_r.append((0, L_R))
    recorte = Manifold.extrude(CrossSection([planta_r]), 20).translate((0, 0, -1))
    relieve = (cuerpo_r ^ recorte) - caja(2.5, U_C + 1, -1, L_R + 1, -1, H_B - 0.2)    # bajos comerciales bajo el voladizo
    solido.append(relieve.translate((W_L - 0.05, A2[1], 0)))
    huecos = [
        # fachada a la calle del ala corta (restaurante): planta baja retranqueada + banda de ventanas
        caja_s(-L_C + 5.5, -0.5, -1, 4.2, -1, 3.0),                                                 # planta baja del restaurante, hundida bajo el volado
        caja_s(-L_C + 6.5, A1[0], -1, 0.4, 4.4, 7.0),                                              # banda de ventanas del restaurante (calle)
        caja_s(-L_C - 1, -L_C + 5.0, -1, W_C - 2.0, -1, 3.6),                                        # hueco sobre pilares en el extremo de la calle
    ]
    for k in range(11):                                                                             # dos filas de ~11 ventanas, solo en el tramo alto
        yk = A2[1] + 3.0 + 3.1 * k
        for z0 in (7.4, 9.4):
            huecos.append(caja_s(W_L - 0.3, W_L + 1, yk, yk + 1.6, z0, z0 + 1.3))
    est = Manifold.batch_boolean(solido, OpType.Add) - Manifold.batch_boolean(huecos, OpType.Add)
    for xp in (-L_C + 0.6, -L_C + 4.4):                                                             # pilares del hueco
        for yp in (0.6, W_C - 3.0):
            est = est + caja_s(xp - 0.4, xp + 0.4, yp - 0.4, yp + 0.4, 0, 3.7)
    est = a_torre(est)
    # huecos del chaflan (en coordenadas de la torre: chaflan en Y = -RET)
    X_R0, X_H1 = -D_REST, L_CH - D_REST                  # extremos del chaflan en coordenadas de la torre
    est = est - Manifold.batch_boolean([
        caja(X_R0 - 1, -R_COL - 0.2, -RET - 2, -RET + 2.0, -1, 3.0),     # planta baja del restaurante
        caja(X_R0 + 1.0, -R_COL - 0.8, -RET - 2, -RET + 0.4, 4.0, 6.6),  # ventanas del restaurante
        caja(R_COL + 0.2, X_H1 - 0.3, -RET - 2, 5.5, -1, 3.8),           # hueco de la entrada del hotel
        caja(R_COL + 0.8, X_H1 - 1.0, -RET - 2, -RET + 0.4, 4.6, 7.4),   # ventanas sobre la entrada
    ], OpType.Add)
    p.append(est)
    fuente = anillo(5.0, 5.6, 0, 0.5) - caja(-7, 7, 0, 7, -1, 1)              # fuente al pie de la columna
    p.append(fuente)
    return Manifold.batch_boolean(p, OpType.Add)


def construir():
    partes = [base_y_estilobato(), cuerpo_habitaciones(), tambor_ojos(), remate(), escalera()]
    m = Manifold.batch_boolean(partes, OpType.Add)
    alto_real = m.bounding_box()[5] - m.bounding_box()[2]
    f = ALTURA_MM / alto_real
    print(f'altura real estimada {alto_real:.1f} m -> escala 1:{1000 / f:.0f}')
    return m.scale((f, f, f))


if __name__ == "__main__":
    import trimesh
    m = construir()
    mesh = m.to_mesh()
    t = trimesh.Trimesh(np.asarray(mesh.vert_properties)[:, :3], np.asarray(mesh.tri_verts), process=False)
    t.export("Hotel_Salut_15cm.stl")
    print("estanco:", t.is_watertight, "caja mm:", np.round(t.bounds[1] - t.bounds[0], 1), "triangulos:", len(t.faces))
