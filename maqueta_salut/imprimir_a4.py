"""Juego de planos PARA IMPRIMIR en A4 (impresora normal), escala real (plantas 1:500, secciones y alzados 1:750, detalles 1:300), cajetín, escala gráfica, sin fotos.
Sale todo de la misma geometría que el resto de planos (edificio.py / cotas.py)."""
import math, datetime
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import edificio as E
import laminas as LM

A3P = (210, 297); A3L = (297, 210)          # mm (A4: se mantienen los nombres)
MM = 1 / 25.4
PAGS = []
INDICE = []
_VV = np.asarray(LM.M.to_mesh().vert_properties)[:, :3]


def rango_seccion(p0, p1):
    """encuadre: lo cortado ± 8 m (más los niveles a la derecha)"""
    a = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
    b = LM.orientar(LM.M, p0, a).slice(0.0).bounds()
    Lg = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    return (min(-2.0, max(b[0], -12.0) - 2), min(max(b[2], 0), Lg + 6) + 16)


def pagina(fmt, titulo):
    w, h = fmt
    fig = plt.figure(figsize=(w * MM, h * MM))
    fig._mm = (w, h)
    fig.add_artist(plt.Rectangle((10 / w, 10 / h), (w - 20) / w, (h - 20) / h, transform=fig.transFigure, fill=False, lw=0.8))
    INDICE.append(titulo)
    fig._titulo = titulo
    return fig


def cajetin(fig, escala):
    w, h = fig._mm
    n = len(INDICE)
    x0, y0, bw, bh = w - 10 - 90, 10, 90, 20
    fig.add_artist(plt.Rectangle((x0 / w, y0 / h), bw / w, bh / h, transform=fig.transFigure, fill=True, fc="white", ec="k", lw=0.8, zorder=50))
    t = lambda x, y, s, **k: fig.text((x0 + x) / w, (y0 + y) / h, s, zorder=51, **k)
    t(2, 15, "HOTEL SALUT · Kyiv, 1984 – levantamiento desde fotos", fontsize=6, weight="bold")
    t(2, 10.5, fig._titulo[:70], fontsize=5.2)
    t(2, 6, f"Escala {escala} (A4, imprimir al 100 %)  ·  cotas en m  ·  {datetime.date.today():%d/%m/%Y}", fontsize=5)
    t(2, 2, "Fuente única: cuadro de cotas. Medidas estimadas con margen.", fontsize=4.5, style="italic")
    t(bw - 11, 2, f"{n:02d}", fontsize=12, weight="bold")


def eje_escala(fig, rect_mm, xl, yl, den):
    """ejes con escala exacta 1:den colocados en rect_mm=(x, y) esquina inferior izquierda (mm de papel)"""
    w, h = fig._mm
    aw, ah = (xl[1] - xl[0]) * 1000 / den, (yl[1] - yl[0]) * 1000 / den
    ax = fig.add_axes([rect_mm[0] / w, rect_mm[1] / h, aw / w, ah / h])
    import cotas_rel as _CR, lineas as _L
    _CR.MM = den / 1000; _L.MM = den / 1000          # burbujas, cadenas y números de cota en mm de papel a esta escala
    return ax, (aw, ah)


def fijar(ax, xl, yl, titulo=""):
    ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect("equal"); ax.axis("off")
    if titulo:
        ax.set_title(titulo, fontsize=8, loc="left")


def barra(fig, x_mm, y_mm, den, largo_m=20):
    w, h = fig._mm
    seg = largo_m / 4 * 1000 / den
    for i in range(4):
        fig.add_artist(plt.Rectangle(((x_mm + i * seg) / w, y_mm / h), seg / w, 1.5 / h, transform=fig.transFigure,
                                     fc="k" if i % 2 == 0 else "white", ec="k", lw=0.5))
        fig.text((x_mm + i * seg) / w, (y_mm + 2.5) / h, f"{int(i * largo_m / 4)}", fontsize=5.5, ha="center")
    fig.text((x_mm + 4 * seg) / w, (y_mm + 2.5) / h, f"{largo_m} m", fontsize=5.5, ha="center")


def norte(ax, x, y):
    ax.annotate("N", xy=(x - 0.914 * 6, y + 0.407 * 6), xytext=(x, y), arrowprops=dict(arrowstyle="-|>", lw=0.8), fontsize=8, ha="center")


# ------------------------------------------------------------------------------------------------ hojas
def portada():
    fig = pagina(A3L, "Portada, índice y situación de secciones")
    fig.text(15 / 297, 188 / 210, "HOTEL SALUT (Kyiv, 1984)", fontsize=18, weight="bold")
    fig.text(15 / 297, 180 / 210, "Juego de planos para imprimir – A4 (imprimir al 100 %, sin ajustar)", fontsize=9.5)
    fig.text(15 / 297, 174 / 210, "Plantas 1:500 · secciones y alzados 1:750 (alzado 5 1:500) · detalles 1:300", fontsize=7.5)
    xl, yl = (-34, 42), (-10, 100)
    ax, _ = eje_escala(fig, (190, 50), xl, yl, 1000)
    LM.planta(ax, None, "", aerea=True)
    for k, p0, p1, _ in LM.SECC:
        ax.plot(*zip(p0, p1), "-.", color="crimson", lw=0.7)
        ax.text(*p0, k, color="crimson", fontsize=7, weight="bold"); ax.text(*p1, k, color="crimson", fontsize=7, weight="bold")
    norte(ax, 26, 88)
    fijar(ax, xl, yl, "situación de secciones (1:1000)")
    barra(fig, 190, 40, 1000, 40)
    cajetin(fig, "1:1000 (situación)")
    return fig


def hoja_planta(zc, titulo):
    fig = pagina(A3P, titulo)
    xl, yl = (-30, 34), (-10, 100)
    ax, (aw, ah) = eje_escala(fig, ((210 - 128) / 2, 42), xl, yl, 500)
    LM.planta(ax, zc, "", aerea=zc is None)
    LM.cotas_planta(ax)
    norte(ax, 28, 88)
    fijar(ax, xl, yl, titulo)
    barra(fig, 15, 34, 500, 20)
    cajetin(fig, "1:500")
    PAGS.append(fig)


def hoja_secciones(lista, titulo, den=750):
    fig = pagina(A3L, titulo)
    y = 210 - 14
    for k, p0, p1, t in lista:
        xl, yl = rango_seccion(p0, p1), (-2, 53)
        hgt = (yl[1] - yl[0]) * 1000 / den + 12
        y -= hgt
        ax, _ = eje_escala(fig, (15, y), xl, yl, den)
        LM.seccion(ax, p0, p1, f"SECCIÓN {k}: {t}")
        fijar(ax, xl, yl, f"SECCIÓN {k}: {t}")
    barra(fig, 15, 14, den, 20)
    cajetin(fig, f"1:{den}")
    PAGS.append(fig)


def hoja_secciones_cortas(lista, titulo):
    fig = pagina(A3L, titulo)
    pos = [(15, 117), (150, 117), (15, 34), (150, 34)]
    lista = sorted(lista, key=lambda q: -(rango_seccion(q[1], q[2])[1] - rango_seccion(q[1], q[2])[0]))
    for (k, p0, p1, t), (x, y) in zip(lista, pos):
        xl, yl = rango_seccion(p0, p1), (-2, 53)
        ax, _ = eje_escala(fig, (x, y), xl, yl, 750)
        LM.seccion(ax, p0, p1, "")
        fijar(ax, xl, yl, f"SECCIÓN {k}: {t[:45]}")
    barra(fig, 15, 14, 750, 20)
    cajetin(fig, "1:750")
    PAGS.append(fig)


def hoja_alzados(lista, titulo, den=750):
    fig = pagina(A3L, titulo)
    y = 210 - 14
    for d, t in lista:
        tmp = plt.figure(); a0 = tmp.add_subplot(); x0, x1 = LM.alzado(a0, d, t); plt.close(tmp)
        xl, yl = (x0 - 2, x1 + 13), (-2, 52)
        hgt = (yl[1] - yl[0]) * 1000 / den + 12
        y -= hgt
        ax, (aw, ah) = eje_escala(fig, (15, y), xl, yl, den)
        LM.alzado(ax, d, t)
        fijar(ax, xl, yl, t)
    barra(fig, 15, 14, den, 20)
    cajetin(fig, f"1:{den}")
    PAGS.append(fig)


def hoja_detalles():
    fig = pagina(A3L, "Detalles: planta tipo de la torre y encuentro escalera – rampa – bar")
    T = E.T
    xl, yl = (T[0] - 18, T[0] + 18), (T[1] - 17, T[1] + 19)
    ax, _ = eje_escala(fig, (15, 50), xl, yl, 300)
    LM.planta(ax, E.Z_B0 + 3 * E.F + 2.0, "")
    fijar(ax, xl, yl, f"planta tipo de habitaciones (+{E.Z_B0 + 3 * E.F + 2.0:.2f}) – núcleo, pasillo, 19 módulos, escalera en cuña")
    xl2, yl2 = (-3, 15), (12, 48)
    ax2, _ = eje_escala(fig, (160, 50), xl2, yl2, 300)
    LM.planta(ax2, 9.2, "")
    fijar(ax2, xl2, yl2, "planta +9,20: escalera, bar, rampa 2, meseta")
    barra(fig, 15, 40, 300, 10)
    cajetin(fig, "1:300")
    PAGS.append(fig)


if __name__ == "__main__":
    plt.rcParams["figure.max_open_warning"] = 0
    p = portada(); PAGS.append(p)
    for zc, t in [(1.8, "Planta baja (suelo ±0,00) – corte a +1,80"), (5.6, "Planta 1 (suelo +3,20) – corte a +5,60"),
                  (9.2, "Planta 2 – corte a +9,20 (terraza, bar, bloque alto)"), (13.0, "Planta 3 – corte a +13,00 (cuello)"),
                  (E.Z_B0 + 3 * E.F + 2.0, f"Planta tipo de habitaciones – corte a +{E.Z_B0 + 3 * E.F + 2.0:.2f}"),
                  (E.Z_B1 + 2.5, f"Planta última – tambor – corte a +{E.Z_B1 + 2.5:.2f}"), (None, "Planta de cubiertas")]:
        hoja_planta(zc, t.replace(".", ","))
    S = {k: (k, p0, p1, t) for k, p0, p1, t in LM.SECC}
    hoja_secciones([S["L1"], S["L2"]], "Secciones longitudinales L1 y L2")
    hoja_secciones([S["L3"], S["S1"]], "Sección longitudinal L3 y sección S1 por el eje de la torre")
    hoja_secciones_cortas([S["S2"], S["S3"], S["S4"], S["S5"]], "Secciones transversales S2, S3, S4 y S5")
    hoja_alzados([((-1, 0), "ALZADO 2 – fachada exterior del ala larga"), ((E.N[0], E.N[1]), "ALZADO 1 – chaflán")], "Alzados 2 y 1")
    hoja_alzados([((0, 1), "ALZADO 3 – calle (ala corta)"), ((1, 0), "ALZADO 4 – patio interior de la L")], "Alzados 3 y 4")
    hoja_alzados([((0, -1), "ALZADO 5 – testero del ala larga")], "Alzado 5", den=500)
    hoja_detalles()
    # índice en la portada
    p.text(15 / 297, 163 / 210, "Índice", fontsize=9, weight="bold")
    for i, t in enumerate(INDICE):
        p.text(15 / 297, (156 - i * 6.6) / 210, f"{i + 1:02d}   {t}", fontsize=6.5)
    cajetin_p = INDICE[0]
    p._titulo = INDICE[0]
    INDICE_tmp = INDICE[:]
    with PdfPages("SALUT_planos_IMPRIMIR_A4.pdf") as pdf:
        for i, f in enumerate(PAGS):
            pdf.savefig(f)
            if i in (0, 1, 8, 12, 14):
                f.savefig(f"imp4_{i + 1:02d}.png", dpi=70)
    print("páginas:", len(PAGS))
