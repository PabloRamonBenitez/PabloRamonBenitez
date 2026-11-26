"""JUEGO A3 DE PRESENTACIÓN: plantas 1:400 con cotas encadenadas (huecos / tramos / total) en todas las fachadas,
muros cortados rellenos, grafismo de rampas y escalera; secciones y alzados alineados a escala; fotos de
comprobación junto a cada dibujo; cajetín y escala gráfica. Todo sale de cotas.py / edificio.py."""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image
import edificio as E
import cotas as K
import laminas as LM
import lineas as L
import imprimir as IA

plt.rcParams["hatch.linewidth"] = 0.25
V = E._v
G = K.planta()
IMG = LM.IMG
FS = 4.6                                  # tamaño de texto de cotas
A3P, A3L = (297, 420), (420, 297)


# ------------------------------------------------------------------------------------------- cotas encadenadas
def cadena(ax, pts, off, fs=FS, total=True, paso=2.2):
    """pts: puntos (mundo) sobre una recta, en orden. Dibuja la cadena parcial a 'off' y el total a 'off+paso'."""
    pts = [np.array(p, float) for p in pts]
    for a, b in zip(pts, pts[1:]):
        if np.linalg.norm(b - a) > 0.05:
            L.cota(ax, a, b, off, "", fs=fs)
    if total and len(pts) > 2:
        L.cota(ax, pts[0], pts[-1], off + math.copysign(paso, off), "", fs=fs)


def cotas_completas(ax):
    WP, WX, LL = V["W_P"], V["W_EXT"], V["L_L"]
    C, E90, yS = G["C"], G["E90"], G["YS"]
    # fachada exterior del ala: huecos (fila alta) – tramos – total
    yh = [LL]
    for i in range(int(V["N_VEN"])):
        y1 = LL - V["VEN_FIN"] - i * V["S_VEN"]; yh += [y1, y1 - V["VEN_W"]]
    yh += [E.Y_CUNA]
    cadena(ax, [(WP, y) for y in yh], (WX - WP) + 2.5, total=False)
    ys = [LL, LL - V["L_FIN"], E.Y_CUNA, yS, C[1]]
    cadena(ax, [(WP, y) for y in ys], (WX - WP) + 5.5, paso=2.4)
    # fachada del patio
    yb0 = C[1] + 0.5
    cadena(ax, [(0, LL), (0, LL - V["L_FIN"]), (0, yb0 + V["R2_L"]), (0, G["IC"][1])], -3.0, paso=2.4)
    # testero: anchos
    cadena(ax, [(0, LL), (V["W_BAR"], LL), (WP, LL), (WX, LL)], 3.0, paso=2.2)
    # chaflán: X (restaurante) – columna – Y (hotel) – total
    A1, U = np.array(G["A1"]), np.array(G["U"]); k = V["REST_L"]
    cadena(ax, [A1, A1 + k * U, A1 + (k + 2 * V["R_COL"]) * U, np.array(E90)], -4.0, paso=2.4)
    # ala corta: calle y fondo
    SWP = G["SWP"]
    cadena(ax, [SWP(-V["L_C"], 0), SWP(-V["L_C"] + V["LOG_PX"], 0), SWP(-V["L_C"] + V["VOL_L"], 0), A1], -3.0, paso=2.4)
    L.cota(ax, SWP(-V["L_C"], 0), SWP(-V["L_C"], -V["VOL_V"]), -1.5, "vuelo", fs=FS)
    cadena(ax, [SWP(-V["L_C"], 0), SWP(-V["L_C"], V["W_C"])], 3.0, total=False)
    # rampa: ancho y radio de la curva
    L.cota(ax, (WP, 45), (WX, 45), 0.0, "", fs=FS)
    ax.text(E90[0] + 0.8, E90[1] - 0.6, f"R {V['R_RAMPA']:.1f}\n90°".replace(".", ","), fontsize=FS)


def norte(ax, x, y):
    ax.annotate("N", xy=(x - 0.914 * 6, y + 0.407 * 6), xytext=(x, y), arrowprops=dict(arrowstyle="-|>", lw=0.7), fontsize=7, ha="center")


def fotos(fig, x0, y0, w, h, lista):
    """columna de fotos de comprobación: lista de (archivo, pie)"""
    W, H = fig._mm
    n = len(lista); gap = 6; hh = (h - gap * (n - 1)) / n
    for i, (f, pie) in enumerate(lista):
        im = Image.open(IMG + f).convert("RGB")
        r = im.width / im.height
        bw, bh = (w, w / r) if w / r <= hh - 5 else ((hh - 5) * r, hh - 5)
        y = y0 + h - (i + 1) * hh - i * gap + 5
        ax = fig.add_axes([x0 / W, y / H, bw / W, bh / H]); ax.imshow(im); ax.axis("off")
        fig.text(x0 / W, (y - 3.5) / H, pie, fontsize=5.5, style="italic")


# ------------------------------------------------------------------------------------------- hojas
def hoja_planta(zc, titulo, lista_fotos, nota=""):
    fig = IA.pagina(A3P, titulo)
    xl, yl = (-32, 31), (-12, 102)
    ax, (aw, ah) = IA.eje_escala(fig, (12, 38), xl, yl, 400)
    LM.planta(ax, zc, "", aerea=zc is None)
    cotas_completas(ax)
    for k_, p0, p1, _ in LM.SECC:
        ax.plot(*zip(p0, p1), "-.", color="k", lw=0.45)
        for p in (p0, p1):
            ax.text(*p, k_, fontsize=6.5, weight="bold", ha="center", va="center", bbox=dict(boxstyle="circle,pad=0.15", fc="white", ec="k", lw=0.5))
    norte(ax, -26, 95)
    IA.fijar(ax, xl, yl)
    fig.text(14 / 297, 410 / 420, titulo, fontsize=10, weight="bold", va="top")
    fig.text(14 / 297, 404 / 420, "Cotas en m. Trazo grueso relleno: cortado · fino: visto · discontinuo: por encima. " + nota, fontsize=6, va="top")
    fotos(fig, 182, 60, 103, 340, lista_fotos)
    IA.barra(fig, 14, 30, 400, 20)
    IA.cajetin(fig, "1:400")
    IA.PAGS.append(fig)


def hoja_alz_secc(titulo, d_alz, t_alz, secc, e, u_rng, den, lista_fotos):
    """alzado (abajo) y sección (arriba) alineados en el mismo eje horizontal e"""
    fig = IA.pagina(A3L, titulo)
    W, H = fig._mm; k = 1000 / den
    ZL = (-6.0, 52.0)
    wd = (u_rng[1] - u_rng[0]) * k; hz = (ZL[1] - ZL[0]) * k
    x0 = 14; y_a = 26; y_s = y_a + hz + 14
    ax_a = fig.add_axes([x0 / W, y_a / H, wd / W, hz / H])
    LM.alzado(ax_a, d_alz, ""); ax_a.set_xlim(*u_rng); ax_a.set_ylim(*ZL); ax_a.set_aspect("equal"); ax_a.axis("off")
    fig.text(x0 / W, (y_a + hz + 2) / H, t_alz, fontsize=8, weight="bold")
    if secc is not None:
        kk, p0, p1, tx = secc
        p0, p1 = np.array(p0, float), np.array(p1, float)
        off = float(p0 @ np.array(e))
        ax_s = fig.add_axes([x0 / W, y_s / H, wd / W, hz / H])
        LM.seccion(ax_s, p0, p1, "")
        ax_s.set_xlim(u_rng[0] - off, u_rng[1] - off); ax_s.set_ylim(*ZL); ax_s.set_aspect("equal"); ax_s.axis("off")
        fig.text(x0 / W, (y_s + hz + 2) / H, f"SECCIÓN {kk} – {tx}", fontsize=8, weight="bold")
    fig.text(x0 / W, 289 / H, titulo, fontsize=10, weight="bold", va="top")
    xf = x0 + wd + 10
    fotos(fig, xf, 48, 408 - xf, 232, lista_fotos)
    IA.barra(fig, x0, 14, den, 20)
    IA.cajetin(fig, f"1:{den}")
    IA.PAGS.append(fig)


def hoja_detalle():
    fig = IA.pagina(A3L, "Detalle 1:200 – torre (planta tipo), escalera en cuña y encuentro con la rampa del techo")
    T = E.T
    xl, yl = (T[0] - 17, T[0] + 17), (T[1] - 17, T[1] + 18)
    ax, _ = IA.eje_escala(fig, (14, 50), xl, yl, 200)
    LM.planta(ax, E.Z_B0 + 3 * E.F + 2.0, ""); IA.fijar(ax, xl, yl, f"planta tipo de habitaciones (+{E.Z_B0 + 3 * E.F + 2.0:.2f})".replace(".", ","))
    xl2, yl2 = (-2, 22), (8, 42)
    ax2, _ = IA.eje_escala(fig, (195, 50), xl2, yl2, 200)
    LM.planta(ax2, 9.2, ""); cotas_completas(ax2); IA.fijar(ax2, xl2, yl2, "planta +9,20: esquina, meseta, techo-rampa y escalera")
    fotos(fig, 322, 60, 86, 220, [("8.webp", "F08 – escalera en cuña con lamas"), ("11.webp", "F11 – rellanos tras las lamas"), ("18.webp", "F18 – chaflán: restaurante, columna, hotel")])
    IA.barra(fig, 14, 40, 200, 10)
    IA.cajetin(fig, "1:200")
    IA.PAGS.append(fig)


if __name__ == "__main__":
    plt.rcParams["figure.max_open_warning"] = 0
    p = IA.portada(); IA.PAGS.append(p)
    hoja_planta(1.8, "PLANTA BAJA (suelo ±0,00) – corte a +1,80", [("18.webp", "F18 – planta baja del chaflán y entrada del hotel"), ("71.webp", "F71 – rampa de acceso y esquina"), ("73.webp", "F73 – testero y huecos del ala")])
    hoja_planta(5.6, "PLANTA PRIMERA (suelo +3,20) – corte a +5,60, por las ventanas", [("alamy_torre.png", "ALAMY – torre medida por MGF"), ("18.webp", "F18 – 5 y pico / 4 y pico paños"), ("47.webp", "F47 – huecos del ala y rampa")])
    hoja_planta(9.2, "PLANTA SEGUNDA (suelo +7,20) – corte a +9,20 (terraza, bar, bloque alto)", [("47.webp", "F47 – terraza-restaurante"), ("76.webp", "F76 – maqueta: curva de la rampa y techo en rampa"), ("1.webp", "F01 – vista aérea 1984")])
    hoja_planta(E.Z_B0 + 3 * E.F + 2.0, "PLANTA TIPO DE HABITACIONES", [("alamy_barril.png", "ALAMY – barril medido por MGF"), ("8.webp", "F08 – escalera y aletas"), ("58.webp", "F58 – cenital: encuentro barril – ala")])
    hoja_planta(None, "PLANTA DE CUBIERTAS", [("36.webp", "F36 – cenital"), ("62.webp", "F62 – cenital")])
    S = {k: (k, p0, p1, t) for k, p0, p1, t in LM.SECC}
    hoja_alz_secc("ALA LARGA – fachada exterior: sección L1 y alzado 2", (-1, 0), "ALZADO 2 – fachada exterior del ala larga",
                  S["L1"], (0, 1), (-16, 110), 500, [("73.webp", "F73 – desde el testero"), ("71.webp", "F71 – rampa de acceso"), ("47.webp", "F47 – 1984")])
    hoja_alz_secc("ALA LARGA – el bar: sección L4 (mirando al bar) y alzado 2", (-1, 0), "ALZADO 2 – fachada exterior del ala larga",
                  S["L4"], (0, 1), (-16, 110), 500, [("47.webp", "F47 – bar y terraza (1984)"), ("71.webp", "F71 – cubierta inclinada"), ("73.webp", "F73 – desde el testero")])
    hoja_alz_secc("ALA LARGA – patio: sección L5 y alzado 4", (1, 0), "ALZADO 4 – patio interior de la L",
                  ("L5", (3.1, 100.0), (3.1, -14.0), "por el bar, la escalera y la torre"), (0, -1), (-110, 16), 500,
                  [("75.png", "F75 – escalera desde el patio"), ("8.webp", "F08 – escalera y barril")])
    hoja_alz_secc("CHAFLÁN – sección L3 y alzado 1", tuple(E.N), "ALZADO 1 – chaflán (frontal)",
                  S["L3"], tuple(E.U), (np.array(E.T) @ np.array(E.U) - 40, np.array(E.T) @ np.array(E.U) + 40), 400,
                  [("alamy_torre.png", "ALAMY – torre medida por MGF"), ("alamy_alto.png", "ALAMY – parte alta"), ("18.webp", "F18 – actual")])
    hoja_alz_secc("ALA CORTA – alzado 3 a la calle", (0, 1), "ALZADO 3 – calle (ala corta)", None, (1, 0), (-38, 40), 400,
                  [("72.webp", "F72 – calle desde el ala corta"), ("alamy_torre.png", "ALAMY – torre medida por MGF")])
    hoja_alz_secc("TESTERO – alzado 5 y sección S4", (0, -1), "ALZADO 5 – testero del ala larga", S["S4"], (-1, 0), (-26, 22), 400,
                  [("73.webp", "F73 – testero, puerta y marquesina")])
    hoja_detalle()
    p.text(20 / 420, 235 / 297, "Índice", fontsize=11, weight="bold")
    for i, t in enumerate(IA.INDICE):
        p.text(20 / 420, (226 - i * 8) / 297, f"{i + 1:02d}   {t}", fontsize=8.5)
    with PdfPages("SALUT_planos_A3_presentacion.pdf") as pdf:
        for f in IA.PAGS:
            pdf.savefig(f)
    print("páginas:", len(IA.PAGS))
