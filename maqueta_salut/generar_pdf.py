"""Genera el PDF de planos y plantillas de la maqueta del Hotel Salut (1:300)."""
import math
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm as MM
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from geometria import *

OUT = "Hotel_Salut_maqueta_1-300.pdf"
GRIS = colors.Color(0.45, 0.45, 0.45)
AZUL = colors.Color(0.1, 0.3, 0.6)
ROJO = colors.Color(0.75, 0.15, 0.1)


def texto(c, x, y, s, size=9, font="Helvetica", color=colors.black):
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawString(x * MM, y * MM, s)
    c.setFillColor(colors.black)


def parrafo(c, x, y, lineas, size=9, lead=4.6, font="Helvetica"):
    for ln in lineas:
        f = font
        if ln.startswith("**"):
            ln, f = ln[2:], "Helvetica-Bold"
        texto(c, x, y, ln, size, f)
        y -= lead
    return y


def pie(c, n, ancho):
    texto(c, 15, 8, f"Hotel Salut (Kyiv, 1984) - maqueta 1:300 - hoja {n}", 7, color=GRIS)
    texto(c, ancho - 75, 8, "Cotas reales ESTIMADAS (sin planos publicados)", 7, color=GRIS)


def barra_control(c, x, y):
    """Barra de 100 mm para comprobar que se imprimio al 100 %."""
    c.setLineWidth(0.4)
    c.rect(x * MM, y * MM, 100 * MM, 3 * MM)
    for i in range(0, 101, 10):
        c.line((x + i) * MM, y * MM, (x + i) * MM, (y + (5 if i % 50 == 0 else 4)) * MM)
        if i % 50 == 0:
            texto(c, x + i - 2, y + 6, f"{i}", 6)
    for i in range(0, 100, 20):
        c.rect((x + i) * MM, y * MM, 10 * MM, 3 * MM, fill=1)
    texto(c, x, y - 4, "Control de impresion: esta barra debe medir 100 mm exactos (imprimir al 100 %, sin 'ajustar a pagina').", 7)


def elipse(c, cx, cy, a, b, dash=None, width=0.5, color=colors.black):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    if dash:
        c.setDash(*dash)
    c.ellipse((cx - a) * MM, (cy - b) * MM, (cx + a) * MM, (cy + b) * MM)
    c.setDash()
    c.setStrokeColor(colors.black)


def cota_h(c, x0, x1, y, etiqueta, size=6.5):
    c.setLineWidth(0.25)
    c.line(x0 * MM, y * MM, x1 * MM, y * MM)
    for x in (x0, x1):
        c.line(x * MM, (y - 1.2) * MM, x * MM, (y + 1.2) * MM)
    c.setFont("Helvetica", size)
    c.drawCentredString((x0 + x1) / 2 * MM, (y + 1) * MM, etiqueta)


def cota_v(c, x, y0, y1, etiqueta, size=6.5):
    c.setLineWidth(0.25)
    c.line(x * MM, y0 * MM, x * MM, y1 * MM)
    for y in (y0, y1):
        c.line((x - 1.2) * MM, y * MM, (x + 1.2) * MM, y * MM)
    c.saveState()
    c.translate((x - 1) * MM, (y0 + y1) / 2 * MM)
    c.rotate(90)
    c.setFont("Helvetica", size)
    c.drawCentredString(0, 0, etiqueta)
    c.restoreState()


def f(m):  # formato de cota: "12,0 m / 40,0 mm"
    return f"{m:.1f} m = {mm(m):.1f} mm".replace(".", ",")


# ---------------------------------------------------------------- HOJA 1
def hoja_portada(c):
    W, H = A4
    texto(c, 15, 280, "Hotel Salut (Salyut), Kyiv", 20, "Helvetica-Bold")
    texto(c, 15, 272, "Planos y plantillas para una maqueta en yeso - escala 1:300 (altura ~10,3 cm)", 11)
    y = 260
    y = parrafo(c, 15, y, [
        "**QUE SE REPRESENTA: EL EDIFICIO CONSTRUIDO (terminado en 1984)",
        "Arquitecto principal Avraam Miletsky (con N. Slogotskaya y V. Shevchenko). Calle Ivana Mazepy 11B,",
        "junto a la plaza/parque de la Gloria. Volumenes del edificio construido (segun las fuentes):",
        "  - Cuerpo de habitaciones en forma de 'barril', de planta ELIPTICA, volado sobre la plaza.",
        "  - 6 plantas de habitaciones colgadas en voladizo de un nucleo central de hormigon (tubo) que",
        "    contiene ascensores, instalaciones y una rampa/escalera en espiral.",
        "  - 19 muros de hormigon armado radiales entre habitaciones (no hay cables de acero).",
        "  - Balcones corridos alrededor de cada planta de habitaciones.",
        "  - Planta tecnica bajo las habitaciones, zocalo/vestibulo, y una pequena sobreconstruccion en",
        "    cubierta (sala de conferencias; tuvo cupula de cristal, hoy desaparecida).",
        "  - Estilobato (cuerpo bajo) alargado hacia el ESTE, en direccion al Dnipro.",
        "  - Total: unas 7-8 plantas segun como se cuenten (planta tecnica + 6 de habitaciones + sala).",
        "",
        "**QUE NO SE REPRESENTA: EL PROYECTO ORIGINAL (no construido)",
        "  - Torre de 18 plantas (recortada a menos de la mitad por las autoridades del Partido).",
        "  - Estilobato unas 3 veces mas corto que el construido.",
        "  Si encuentras fotos de un 'Salut' alto y esbelto, son dibujos del proyecto original.",
        "",
        "**FIABILIDAD DE LAS MEDIDAS",
        "No existen planos ni cotas publicadas. Lo documentado es la composicion (lista anterior).",
        "Las dimensiones son ESTIMACIONES a partir de: altura de planta ~3 m, 88-100 habitaciones en",
        "6 plantas (~16-19 por planta, una por cada hueco entre los 19 muros) y proporciones de fotos.",
        "Tamano real estimado: barril de ~25 x 22 m, altura total ~31 m, estilobato ~40 x 16 m.",
        "La orientacion del eje largo de la elipse respecto al estilobato tambien es estimada.",
        "Si tienes fotos propias o una medida real, se reescala todo facilmente.",
        "",
        "**CONTENIDO",
        "  Hoja 2  Alzado y seccion a escala 1:300        Hoja 3  Planta a escala 1:300",
        "  Hoja 4  Tabla de piezas y medidas              Hojas 5-7  Plantillas a tamano real (1:1)",
        "  Hoja 8  Caja-encofrado del estilobato          Hoja 9  Instrucciones de vaciado y tallado",
    ], size=9)
    y -= 4
    y = parrafo(c, 15, y, [
        "**FUENTES (consultadas en noviembre de 2026)",
        "architectuul.com/architecture/hotel-salut  -  pragmatika.media (Macrocosm and microcosm of the Salyut Hotel)",
        "go2.kiev.ua/en/salut-hotel  -  urbexhub.com/hotel-salute-kyiv  -  uk.wikipedia.org (Saliut, hotel)",
        "hmarochos.kiev.ua (Monstri modernizmu, 2016)  -  news.telegraf.com.ua (2025)  -  apostrophe.ua (2023)",
    ], size=7.5, lead=4)
    barra_control(c, 15, 22)
    pie(c, 1, W / MM)


# ---------------------------------------------------------------- HOJA 2
def hoja_alzado(c):
    W, H = landscape(A4)
    texto(c, 15, 197, "Alzado (izquierda) y seccion por el eje (derecha) - escala 1:300", 13, "Helvetica-Bold")
    texto(c, 15, 191, "Medidas: real estimada = maqueta. Oeste a la izquierda, estilobato hacia el este (Dnipro).", 8)

    def dibujar(ox, oy, seccion):
        c.setLineWidth(0.6)
        X = lambda m: ox + mm(m)
        Y = lambda m: oy + mm(m)
        # suelo
        c.setLineWidth(0.8)
        c.line(X(-16) * MM, Y(0) * MM, X(48) * MM, Y(0) * MM)
        c.setLineWidth(0.5)
        # estilobato
        c.rect(X(ESTI_X0) * MM, Y(0) * MM, mm(ESTI_X1 - ESTI_X0) * MM, mm(ESTI_H) * MM)
        # base / nucleo
        if seccion:
            c.setFillColor(colors.Color(0.8, 0.8, 0.8))
            c.rect(X(-NUCLEO_R) * MM, Y(0) * MM, mm(2 * NUCLEO_R) * MM, mm(SUP_Z0) * MM, fill=1)
            c.setFillColor(colors.black)
            texto(c, X(-1.6), Y(16), "nucleo", 5.5)
        c.rect(X(-BASE_R) * MM, Y(BASE_Z0) * MM, mm(2 * BASE_R) * MM, mm(BASE_Z1) * MM)
        # planta tecnica
        c.rect(X(-TEC_A) * MM, Y(TEC_Z0) * MM, mm(2 * TEC_A) * MM, mm(TEC_Z1 - TEC_Z0) * MM)
        # plantas
        for p in PLANTAS:
            # losa-balcon
            c.rect(X(-p["a"]) * MM, Y(p["z0"]) * MM, mm(2 * p["a"]) * MM, mm(LOSA) * MM)
            # fachada retranqueada
            c.rect(X(-p["fa"]) * MM, Y(p["z0"] + LOSA) * MM, mm(2 * p["fa"]) * MM,
                   mm(H_PLANTA - LOSA) * MM)
            if not seccion:
                # aletas (muros radiales vistos) - vista desde el sur
                for k in range(N_MUROS):
                    th = 2 * math.pi * k / N_MUROS
                    if math.sin(th) < 0:  # solo los de la cara visible
                        x = p["a"] * math.cos(th)
                        c.setLineWidth(0.35)
                        c.line(X(x) * MM, Y(p["z0"] + LOSA) * MM, X(x) * MM, Y(p["z1"]) * MM)
                        c.setLineWidth(0.5)
                # banda de ventanas
                c.setStrokeColor(GRIS)
                c.setLineWidth(0.2)
                c.line(X(-p["fa"]) * MM, Y(p["z0"] + 1.0) * MM, X(p["fa"]) * MM, Y(p["z0"] + 1.0) * MM)
                c.setStrokeColor(colors.black)
                c.setLineWidth(0.5)
        # cubierta
        pu = PLANTAS[-1]
        c.rect(X(-pu["a"]) * MM, Y(TECHO_Z) * MM, mm(2 * pu["a"]) * MM, mm(CUBIERTA) * MM)
        # sobreconstruccion
        c.rect(X(-SUP_A) * MM, Y(SUP_Z0) * MM, mm(2 * SUP_A) * MM, mm(SUP_Z1 - SUP_Z0) * MM)
        return X, Y

    X, Y = dibujar(70, 55, False)
    # cotas del alzado
    cota_v(c, X(-17.5), Y(0), Y(ALTURA_TOTAL), f"total {f(ALTURA_TOTAL)}")
    cota_v(c, X(-14.5), Y(HAB_Z0), Y(TECHO_Z), f"6 plantas hab. {f(TECHO_Z - HAB_Z0)}", 5.5)
    cota_h(c, X(-PLANTAS[2]["a"]), X(PLANTAS[2]["a"]), Y(ALTURA_TOTAL) + 6,
           f"barril maximo {f(2 * PLANTAS[2]['a'])}")
    cota_h(c, X(ESTI_X0), X(ESTI_X1), Y(0) - 6, f"estilobato {f(ESTI_X1 - ESTI_X0)}")
    cota_h(c, X(-BASE_R), X(BASE_R), Y(0) - 11, f"base {f(2 * BASE_R)}", 5.5)
    texto(c, X(30), Y(ESTI_H) + 1.5, f"estilobato h {f(ESTI_H)}", 5.5)

    X2, Y2 = dibujar(190, 55, True)
    niveles = [("suelo", 0), ("planta tecnica", TEC_Z0), ("hab. 1", HAB_Z0), ("hab. 6", HAB_Z0 + 15),
               ("cubierta", TECHO_Z), ("remate", SUP_Z1)]
    for nom, z in niveles:
        c.setStrokeColor(GRIS)
        c.setLineWidth(0.15)
        c.setDash(1, 1)
        c.line(X2(13.5) * MM, Y2(z) * MM, X2(17) * MM, Y2(z) * MM)
        c.setDash()
        c.setStrokeColor(colors.black)
        texto(c, X2(17.3), Y2(z) - 0.8, f"+{z:.1f} m / {mm(z):.1f} mm  {nom}".replace(".", ","), 5.5)
    texto(c, X2(-12), Y2(PLANTAS[2]["z0"]) - 3, f"balcones de {BALCON:.1f} m".replace(".", ","), 5)

    parrafo(c, 15, 26, [
        "Losas-balcon dibujadas con 0,45 m de canto (1,5 mm en maqueta) en vez de ~0,25 m reales: mas finas se rompen en yeso.",
        "Lineas verticales del alzado = cantos de los 19 muros radiales que asoman entre balcones. Linea gris = antepecho/ventanas.",
    ], size=7, lead=3.8)
    pie(c, 2, W / MM)


# ---------------------------------------------------------------- HOJA 3
def hoja_planta(c):
    W, H = landscape(A4)
    texto(c, 15, 197, "Planta de conjunto - escala 1:300 (norte arriba, orientacion estimada)", 13, "Helvetica-Bold")
    cx, cy = 75, 105
    X = lambda m: cx + mm(m)
    Y = lambda m: cy + mm(m)
    # estilobato
    c.setLineWidth(0.6)
    c.rect(X(ESTI_X0) * MM, Y(-ESTI_ANCHO / 2) * MM, mm(ESTI_X1 - ESTI_X0) * MM, mm(ESTI_ANCHO) * MM)
    texto(c, X(28), Y(-1), "ESTILOBATO (2 plantas)", 7)
    texto(c, X(30), Y(-3.5), "hacia el Dnipro  ->", 7)
    p = PLANTAS[2]
    elipse(c, cx, cy, mm(p["a"]), mm(p["b"]), width=0.8)
    elipse(c, cx, cy, mm(p["fa"]), mm(p["fb"]), dash=(2, 1))
    elipse(c, cx, cy, mm(TEC_A), mm(TEC_B), dash=(0.6, 1), color=GRIS)
    elipse(c, cx, cy, mm(SUP_A), mm(SUP_B), dash=(3, 1.5), color=AZUL)
    c.circle(cx * MM, cy * MM, mm(BASE_R) * MM, stroke=1)
    c.setFillColor(colors.Color(0.8, 0.8, 0.8))
    c.circle(cx * MM, cy * MM, mm(NUCLEO_R) * MM, stroke=1, fill=1)
    c.setFillColor(colors.black)
    c.setLineWidth(0.4)
    for k in range(N_MUROS):
        th = 2 * math.pi * k / N_MUROS
        x0, y0 = NUCLEO_R * math.cos(th), NUCLEO_R * math.sin(th)
        x1, y1 = p["a"] * math.cos(th), p["b"] * math.sin(th)
        c.line(X(x0) * MM, Y(y0) * MM, X(x1) * MM, Y(y1) * MM)
    cota_h(c, X(-p["a"]), X(p["a"]), Y(p["b"]) + 5, f"eje mayor {f(2 * p['a'])}")
    cota_v(c, X(-p["a"]) - 5, Y(-p["b"]), Y(p["b"]), f"eje menor {f(2 * p['b'])}")
    cota_h(c, X(ESTI_X0), X(ESTI_X1), Y(-ESTI_ANCHO / 2) - 6, f"{f(ESTI_X1 - ESTI_X0)}")
    cota_v(c, X(ESTI_X1) + 5, Y(-ESTI_ANCHO / 2), Y(ESTI_ANCHO / 2), f"{f(ESTI_ANCHO)}")
    # norte
    c.line(270 * MM, 170 * MM, 270 * MM, 182 * MM)
    c.line(268 * MM, 179 * MM, 270 * MM, 182 * MM)
    c.line(272 * MM, 179 * MM, 270 * MM, 182 * MM)
    texto(c, 268.8, 184, "N", 9, "Helvetica-Bold")
    parrafo(c, 195, 60, [
        "**Leyenda",
        "Linea gruesa: borde de balcones (planta 3, la mas ancha)",
        "Discontinua: fachada de habitaciones",
        "Gris punteada: planta tecnica",
        "Azul: sobreconstruccion de cubierta (sala)",
        "Circulo: base/vestibulo  -  relleno gris: nucleo",
        "19 lineas radiales: muros de hormigon",
    ], size=7.5, lead=4)
    pie(c, 3, W / MM)


# ---------------------------------------------------------------- HOJA 4
def hoja_tabla(c):
    W, H = A4
    texto(c, 15, 280, "Tabla de piezas (medidas de MAQUETA en mm, escala 1:300)", 14, "Helvetica-Bold")
    texto(c, 15, 274, "La 'banda' es la tira de acetato/cartulina que forma la pared del molde (perimetro + 10 mm de solape).", 8)
    cols = [15, 30, 82, 112, 140, 165, 190]
    cab = ["Pieza", "Descripcion", "Largo/eje X", "Ancho/eje Y", "Alto", "Banda", "Nivel base"]
    y = 264
    for x, t in zip(cols, cab):
        texto(c, x, y, t, 8, "Helvetica-Bold")
    c.line(15 * MM, (y - 1.5) * MM, 200 * MM, (y - 1.5) * MM)
    filas = [("A", "Estilobato (caja, hoja 8)", mm(ESTI_X1 - ESTI_X0), mm(ESTI_ANCHO), mm(ESTI_H), None, 0),
             ("B", "Base/vestibulo, cilindro", mm(2 * BASE_R), mm(2 * BASE_R), mm(BASE_Z1),
              math.pi * mm(2 * BASE_R) + 10, 0),
             ("C", "Planta tecnica, elipse", mm(2 * TEC_A), mm(2 * TEC_B), mm(TEC_Z1 - TEC_Z0),
              perimetro_elipse(mm(TEC_A), mm(TEC_B)) + 10, mm(TEC_Z0))]
    for p in PLANTAS:
        alto = mm(H_PLANTA) + (mm(CUBIERTA) if p["i"] == N_HAB - 1 else 0)
        filas.append((f"D{p['i'] + 1}", f"Planta hab. {p['i'] + 1} (balcon)", mm(2 * p["a"]), mm(2 * p["b"]),
                      alto, perimetro_elipse(mm(p["a"]), mm(p["b"])) + 10, mm(p["z0"])))
        filas.append(("", "   fachada a tallar", mm(2 * p["fa"]), mm(2 * p["fb"]), None, None, None))
    filas.append(("E", "Sala de cubierta, elipse", mm(2 * SUP_A), mm(2 * SUP_B), mm(SUP_Z1 - SUP_Z0),
                  perimetro_elipse(mm(SUP_A), mm(SUP_B)) + 10, mm(SUP_Z0)))
    y -= 7
    for fila in filas:
        for x, v in zip(cols, fila):
            s = "" if v is None else (v if isinstance(v, str) else f"{v:.1f}".replace(".", ","))
            texto(c, x, y, s, 8, "Helvetica" if fila[0] else "Helvetica-Oblique",
                  colors.black if fila[0] else GRIS)
        y -= 5.5
    c.line(15 * MM, (y + 3) * MM, 200 * MM, (y + 3) * MM)
    y -= 4
    parrafo(c, 15, y, [
        f"Altura total montada: {mm(ALTURA_TOTAL):.1f} mm.  Solape de la base: el estilobato A mide lo mismo de alto que la base B,".replace(".", ","),
        "de modo que la planta tecnica C apoya sobre ambos y los une.",
        "D6 incluye 1,3 mm extra de losa de cubierta (va pegada en una sola pieza).",
        "",
        "**Detalle de las plantas D1-D6 (cada disco de 10 mm de alto):",
        "  - El labio de 1,5 mm va ABAJO (es la losa-balcon de esa planta).",
        "  - Encima del labio se rebaja 4 mm hacia dentro (balcon de 1,2 m) hasta la linea 'fachada a tallar'.",
        "  - En ese rebaje se dejan 19 'dientes' de 1 mm de ancho (los muros radiales) en las marcas de la plantilla.",
        "  Si prefieres algo mas sencillo: discos lisos y solo una ranura fina marcada con cuchilla.",
        "",
        "**Material recomendado",
        "  Yeso de alta dureza (tipo dental IV o alabastrino fino) para que los labios de 1,5 mm no se desmoronen.",
        "  Acetato de 0,3-0,5 mm o cartulina plastificada para bandas; base de vidrio/metacrilato o melamina lisa;",
        "  plastilina para sellar; desmoldeante (vaselina o jabon liquido diluido); cuchilla, limas y lija 400-800.",
    ], size=8, lead=4.4)
    pie(c, 4, W / MM)


# ---------------------------------------------------------------- HOJAS 5-7
def plantilla_elipse(c, cx, cy, nombre, a, b, fa=None, fb=None, radiales=False, nota=""):
    elipse(c, cx, cy, a, b, width=0.6)
    if fa:
        elipse(c, cx, cy, fa, fb, dash=(1.5, 1), width=0.35, color=ROJO)
    c.setLineWidth(0.2)
    c.line((cx - 3) * MM, cy * MM, (cx + 3) * MM, cy * MM)
    c.line(cx * MM, (cy - 3) * MM, cx * MM, (cy + 3) * MM)
    # marca eje X (hacia el estilobato)
    c.setDash(0.5, 1)
    c.line((cx - a - 4) * MM, cy * MM, (cx + a + 4) * MM, cy * MM)
    c.setDash()
    texto(c, cx + a + 1, cy + 1, "E >", 6)
    if radiales:
        c.setStrokeColor(ROJO)
        c.setLineWidth(0.3)
        for k in range(N_MUROS):
            th = 2 * math.pi * k / N_MUROS
            c.line((cx + fa * math.cos(th)) * MM, (cy + fb * math.sin(th)) * MM,
                   (cx + (a + 2.5) * math.cos(th)) * MM, (cy + (b + 2.5) * math.sin(th)) * MM)
        c.setStrokeColor(colors.black)
    texto(c, cx - 14, cy - b - 6, nombre, 9, "Helvetica-Bold")
    texto(c, cx - 14, cy - b - 10, f"{2 * a:.1f} x {2 * b:.1f} mm  {nota}".replace(".", ","), 6.5)


def hojas_plantillas(c, n0):
    W, H = A4
    items = [("B  base Ø", mm(BASE_R), mm(BASE_R), None, None, False, f"alto {mm(BASE_Z1):.0f} mm"),
             ("C  planta tecnica", mm(TEC_A), mm(TEC_B), None, None, False, f"alto {mm(3):.0f} mm"),
             ("E  sala cubierta", mm(SUP_A), mm(SUP_B), None, None, False, f"alto {mm(3.6):.0f} mm")]
    for p in PLANTAS:
        items.append((f"D{p['i'] + 1}  planta hab. {p['i'] + 1}", mm(p["a"]), mm(p["b"]),
                      mm(p["fa"]), mm(p["fb"]), True, "alto 10 mm"))
    # 2 columnas x 2 filas por hoja (elipses de hasta 85 mm)
    huecos = [(55, 215), (155, 215), (55, 120), (155, 120)]
    n = n0
    # hoja 5: B, C, E + D1 ; hoja 6: D2-D5 ; hoja 7: D6
    paginas = [items[0:4], items[4:8], items[8:9]]
    for pag in paginas:
        texto(c, 15, 280, "Plantillas a TAMANO REAL (1:1) - imprimir al 100 %", 13, "Helvetica-Bold")
        texto(c, 15, 274, "Negro: contorno de la pieza / base del molde.  Rojo discontinuo: linea de fachada a tallar.  "
                          "Rojo radial: los 19 muros.", 7.5)
        texto(c, 15, 270, "Linea de puntos con 'E >': eje mayor, apunta hacia el estilobato (este). Alinea todas las piezas con ella.", 7.5)
        for (cx, cy), it in zip(huecos, pag):
            nombre, a, b, fa, fb, rad, nota = it
            plantilla_elipse(c, cx, cy, nombre, a, b, fa, fb, rad, nota)
        if len(pag) == 1:
            parrafo(c, 115, 245, [
                "**Uso de las plantillas",
                "1. Recorta la plantilla por la linea negra.",
                "2. Pegala con cinta en la base lisa del molde",
                "   (bajo un vidrio/metacrilato) como guia.",
                "3. Ciñe la banda de acetato a la linea y",
                "   sella por fuera con plastilina.",
                "4. Una vez fraguado y desmoldado, pega encima",
                "   una copia en papel y pica con un alfiler las",
                "   marcas rojas para transferirlas al yeso.",
                "5. Tienes 6 plantas iguales en forma pero de",
                "   tamano distinto: rotula cada disco al",
                "   desmoldarlo (D1 abajo ... D6 arriba).",
            ], size=8, lead=4.4)
        barra_control(c, 15, 22)
        pie(c, n, W / MM)
        c.showPage()
        n += 1
    return n


# ---------------------------------------------------------------- HOJA 8
def hoja_caja(c, n):
    W, H = A4
    texto(c, 15, 280, "A - Caja-encofrado del estilobato (desarrollo a tamano real)", 13, "Helvetica-Bold")
    texto(c, 15, 274, "Imprime sobre cartulina, corta por el contorno, dobla por las lineas de puntos, pega las solapas por FUERA,", 8)
    texto(c, 15, 270, "y forra el interior con cinta de embalar o barniz para que el yeso no se pegue. Vierte con la caja abierta arriba.", 8)
    L, A, Hh = mm(ESTI_X1 - ESTI_X0), mm(ESTI_ANCHO), mm(ESTI_H)
    ox, oy = (210 - (L + 2 * Hh)) / 2, 120
    c.setLineWidth(0.6)
    # fondo
    fx, fy = ox + Hh, oy
    c.setDash(1, 1)
    c.rect(fx * MM, fy * MM, L * MM, A * MM)
    c.setDash()
    # contorno exterior (cruz)
    pts = [(fx, fy - Hh), (fx + L, fy - Hh), (fx + L, fy), (fx + L + Hh, fy), (fx + L + Hh, fy + A),
           (fx + L, fy + A), (fx + L, fy + A + Hh), (fx, fy + A + Hh), (fx, fy + A), (fx - Hh, fy + A),
           (fx - Hh, fy), (fx, fy)]
    p = c.beginPath()
    p.moveTo(pts[0][0] * MM, pts[0][1] * MM)
    for x, y in pts[1:]:
        p.lineTo(x * MM, y * MM)
    p.close()
    c.drawPath(p)
    # solapas (en los laterales largos)
    c.setLineWidth(0.3)
    for (x0, y0, dx) in [(fx, fy - Hh, -1), (fx + L, fy - Hh, 1), (fx, fy + A, -1), (fx + L, fy + A, 1)]:
        s = 6
        c.line(x0 * MM, y0 * MM, (x0 + dx * s) * MM, (y0 + 1) * MM)
        c.line((x0 + dx * s) * MM, (y0 + 1) * MM, (x0 + dx * s) * MM, (y0 + Hh - 1) * MM)
        c.line((x0 + dx * s) * MM, (y0 + Hh - 1) * MM, x0 * MM, (y0 + Hh) * MM)
    texto(c, fx + L / 2 - 18, fy + A / 2, f"FONDO {L:.1f} x {A:.1f} mm".replace(".", ","), 8, "Helvetica-Bold")
    texto(c, fx + L / 2 - 20, fy - Hh / 2, f"pared {Hh:.1f} mm (= altura de la pieza)".replace(".", ","), 7)
    texto(c, fx - Hh + 1, fy + A / 2, "OESTE", 6)
    texto(c, fx + L + 2, fy + A / 2, "ESTE", 6)
    parrafo(c, 15, 80, [
        "**Truco: rellena solo hasta la marca de altura (pinta una raya en la pared interior a %.1f mm)." % Hh,
        "El extremo OESTE es el que va contra la base cilindrica B y bajo el voladizo del barril.",
        "Opcional: antes de que fragüe del todo, marca con regla las lineas de las ventanas (bandas horizontales).",
    ], size=8)
    barra_control(c, 15, 22)
    pie(c, n, W / MM)


# ---------------------------------------------------------------- HOJA 9
def hoja_instrucciones(c, n):
    W, H = A4
    texto(c, 15, 280, "Instrucciones de vaciado, tallado y montaje", 14, "Helvetica-Bold")
    parrafo(c, 15, 270, [
        "**1. Preparacion",
        "  Imprime TODO al 100 % y comprueba la barra de 100 mm. Trabaja sobre vidrio o metacrilato liso.",
        "  Untar todas las superficies de molde con desmoldeante (vaselina muy fina o jabon diluido).",
        "",
        "**2. Moldes de las piezas redondas (B, C, D1-D6, E)",
        "  Corta una banda de acetato del largo de la tabla (hoja 4) y unos 5 mm mas alta que la pieza.",
        "  Coloca la plantilla de papel bajo el vidrio, ciñe la banda a la linea negra, une el solape con cinta",
        "  y sella el pie por fuera con un cordon de plastilina. Marca la altura en el interior.",
        "  Truco para las 6 plantas: puedes verter un unico bloque de ~62 mm con la elipse de D3 y luego",
        "  tallarlo con forma de barril usando las demas plantillas como galgas. Es mas dificil pero sin juntas.",
        "",
        "**3. Vertido",
        "  Proporcion orientativa yeso:agua ~ 100:30-40 (sigue la del fabricante). Espolvorea el yeso sobre el agua,",
        "  deja reposar 1-2 min, mezcla sin batir aire. Vierte despacio, golpea suavemente la base para que suban",
        "  las burbujas y enrasa con una regla. Desmolda tras el fraguado inicial (~30-60 min), aun algo humedo:",
        "  es el MEJOR momento para tallar.",
        "",
        "**4. Tallado de cada planta D (aun humeda)",
        "  Transfiere con alfiler las marcas rojas. Con cuchilla y lima, rebaja la fachada 4 mm hacia dentro, dejando",
        "  abajo el labio-balcon de 1,5 mm y los 19 dientes de 1 mm (muros). Con una aguja marca la banda de ventanas.",
        "",
        "**5. Montaje (de abajo arriba, alineando el eje 'E >' de todas las piezas)",
        "  B (base) + A (estilobato, extremo oeste tocando B) sobre una peana  ->  C encima, centrada en B",
        "  ->  D1 ... D6  ->  E centrada en la cubierta. Pega con papilla de yeso fresco (o cola blanca en yeso seco).",
        "  Comprueba la vertical con una escuadra en cada paso. Altura final esperada: %.0f mm." % mm(ALTURA_TOTAL),
        "",
        "**6. Acabado",
        "  Seca 24-48 h. Lija 400-800, rellena juntas con yeso fino, y si quieres, sella con goma laca diluida.",
        "  El edificio real es blanco/gris claro de hormigon; los huecos de ventana pueden oscurecerse con grafito.",
        "",
        "**7. Siguiente paso",
        "  El modelo 3D (STL) con esta misma geometria permitira imprimir un original para un molde de silicona,",
        "  o los moldes directamente. Si consigues una cota real (p. ej. la altura), se reescala todo a la vez.",
    ], size=8.5, lead=4.6)
    pie(c, n, W / MM)


def main():
    c = canvas.Canvas(OUT, pagesize=A4)
    c.setTitle("Hotel Salut Kyiv - maqueta 1:300")
    hoja_portada(c); c.showPage()
    c.setPageSize(landscape(A4)); hoja_alzado(c); c.showPage()
    hoja_planta(c); c.showPage()
    c.setPageSize(A4); hoja_tabla(c); c.showPage()
    n = hojas_plantillas(c, 5)
    hoja_caja(c, n); c.showPage()
    hoja_instrucciones(c, n + 1); c.showPage()
    c.save()
    print("ok", OUT)


if __name__ == "__main__":
    main()
