"""Problema aislado: cómo termina arriba la rampa de acceso y cómo gira el coche hasta la rampa del techo del
restaurante (bajo la escalera), sin tocar la fachada del hotel en el chaflán. Tres hipótesis en la misma base."""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, FancyArrowPatch
from shapely.geometry import LineString, Polygon as SP
import edificio as E

V = E._v; T = np.array(E.T); U = np.array(E.U); N = np.array(E.N)
Q = np.array(E.plantas_base()["Q"]); A1 = np.array(E.A1)
WP, WEXT = E.W_P, E.W_EXT; WR = WEXT - WP; XM = (WP + WEXT) / 2
Y0 = Q[1] + V["D_HOTF"]; YPIE = E.Y_CUNA
WB = E.W_BAR + V["V_BAR"]; YR0 = Q[1] + 0.5; YR1 = YR0 + V["R2_L"]
AZ = "#1a5fb4"


def poly(ax, pts, **k):
    ax.add_patch(Polygon(np.array(pts), closed=True, **k))


def banda(linea, ancho):
    return LineString(linea).buffer(ancho / 2, cap_style=2, join_style=1)


def base(ax, titulo):
    # edificio existente (lo que ya estaba claro)
    ax.plot([WP, WP], [Q[1], 64], color="k", lw=1.6)                         # fachada exterior del ala
    ax.plot([0, 0], [11.7, 64], color="k", lw=1.6)                           # fachada patio
    ax.plot([Q[0], A1[0]], [Q[1], A1[1]], color="k", lw=2.2)                  # CHAFLÁN = entrada del hotel (intocable)
    m = (Q + A1) / 2 - N * 1.2
    ax.text(*m, "fachada del hotel (entrada)\n– no se toca –", fontsize=5.5, rotation=math.degrees(math.atan2(U[1], U[0])), ha="center", va="top")
    ax.add_patch(Circle(T, E.R_COL, fc="0.6", ec="k", lw=0.8))
    ax.add_patch(Circle(T, E.R_AL, fill=False, ec="0.4", lw=0.7, ls=(0, (5, 3))))
    ax.text(T[0] - 9, T[1] - 12.5, "vuelo del barril", fontsize=5, style="italic", color="0.4")
    poly(ax, [(WP - 0.4, Q[1]), (WP, Q[1]), (WP, Y0), (WP - 0.4, Y0)], fc="0.75", ec="k", lw=0.5)
    ax.text(WP - 0.8, (Q[1] + Y0) / 2, "banda hotel", fontsize=4.5, rotation=90, ha="right", va="center")
    n = 12
    esc = [E.esc_ang_pt(V["ESC_RC"], -E.ESC_HB + 2 * E.ESC_HB * k / n) for k in range(n + 1)] + \
          [E.esc_ang_pt(V["ESC_R0"], E.ESC_HB - 2 * E.ESC_HB * k / n) for k in range(n + 1)]
    poly(ax, esc, fill=False, ec="k", lw=0.8, ls=(0, (5, 3)))
    ax.text(*E.esc_ang_pt(10.5, 0), "escalera\n(por encima)", fontsize=4.5, ha="center", va="center", style="italic")
    poly(ax, [(0, YR0), (WB, YR0), (WB, YR1), (0, YR1)], fc="#e8e8e8", ec="k", lw=0.6)
    ax.add_patch(FancyArrowPatch((WB / 2, YR0 + 1), (WB / 2, YR1 - 1), arrowstyle="-|>", mutation_scale=7, lw=0.6))
    ax.text(WB / 2 + 0.5, (YR0 + YR1) / 2, "techo restaurante en rampa +7,20→+11,50", fontsize=4.5, rotation=90, va="center")
    poly(ax, [(0, YR1), (E.W_BAR, YR1), (E.W_BAR, 64), (0, 64)], fc="0.85", ec="k", lw=0.6)
    ax.text(3.1, 50, "bar", fontsize=5, ha="center")
    ax.text(9.9, 45, "terraza +7,20", fontsize=5, rotation=90, ha="center")
    ax.set_xlim(-8, 34); ax.set_ylim(-8, 62); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(titulo, fontsize=8.5, loc="left", weight="bold")


def rampa(ax, linea, ancho=WR, fc="#cfe0f5"):
    b = banda(linea, ancho)
    poly(ax, list(b.exterior.coords), fc=fc, ec="k", lw=0.9)
    return b


def camino(ax, pts):
    P = np.array(pts, float)
    ax.plot(P[:, 0], P[:, 1], color=AZ, lw=1.0, ls=(0, (6, 2, 1, 2)))
    ax.add_patch(FancyArrowPatch(tuple(P[-2]), tuple(P[-1]), arrowstyle="-|>", mutation_scale=8, color=AZ, lw=1.0))


def arco(c, r, a0, a1, n=30):
    return [(c[0] + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)), c[1] + r * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]


def h1(ax):
    base(ax, "H1 · la rampa se curva hacia fuera (izquierda) y\ndesemboca en un rellano; vuelta a la derecha por un puente")
    R = 9.0; c = (XM + R, 34.0)
    eje = [(XM, YPIE), (XM, 34.0)] + arco(c, R, 180, 240)[1:]
    d = np.array([math.sin(math.radians(240)) * -1, math.cos(math.radians(240))]); d = d / np.linalg.norm(d)
    fin = np.array(eje[-1]) + np.array([0.866, -0.5]) * 4.0
    rampa(ax, eje + [tuple(fin)])
    rell = [fin + np.array([-0.5, 3.5]), fin + np.array([6.5, 3.5]), fin + np.array([6.5, -7.5]), fin + np.array([-0.5, -7.5])]
    poly(ax, rell, fc="#cfe0f5", ec="k", lw=0.9)
    ax.text(*(fin + np.array([3.0, -2.0])), "rellano\n+7,20", fontsize=5, ha="center")
    pu = [(WP, Q[1] + 0.3), (fin[0] - 0.5, Q[1] + 0.3), (fin[0] - 0.5, Q[1] + 4.3), (WP, Q[1] + 4.3)]
    poly(ax, pu, fc="#cfe0f5", ec="k", lw=0.9)
    ax.text((WP + fin[0]) / 2, Q[1] + 2.3, "puente +7,20", fontsize=4.6, ha="center", va="center")
    ax.add_patch(Polygon([(WP + 0.2, 21), (XM - 1.5, 21), (XM + 1.2, 32), (WP + 0.2, 32)], closed=True, fill=False, ec="0.4", lw=0.6, ls=":"))
    ax.text(WP + 0.6, 26.5, "hueco / arco\nbajo la curva", fontsize=4.3, color="0.3")
    camino(ax, [(XM, 52), (XM, 36), (XM + 2.0, 29.5), (fin[0] + 1.0, fin[1] + 0.5), (fin[0] + 4.0, fin[1] - 2.5),
                (fin[0] + 2.0, Q[1] + 2.3), (WP - 1.0, Q[1] + 2.3), (WB / 2 + 1.5, Q[1] + 2.0), (WB / 2, YR0 + 3.0)])
    ax.text(fin[0] + 1.0, fin[1] + 4.2, "① izquierda", fontsize=5, color=AZ); ax.text(fin[0] + 3.5, Q[1] - 1.2, "② derecha", fontsize=5, color=AZ)


def h2(ax):
    base(ax, "H2 · rampa recta pegada a la fachada + plataforma\nde giro con esquinas redondeadas (lo que hay ahora)")
    rampa(ax, [(XM, YPIE), (XM, Y0 + V["R_ENT"])])
    pol, _ = E.curva_poligono()
    poly(ax, pol, fc="#cfe0f5", ec="k", lw=0.9)
    camino(ax, [(XM, 52), (XM, 22), (17.5, 19.5), (17.0, 15.6), (WP - 1.0, 15.7), (WB / 2 + 1.5, 15.2), (WB / 2, YR0 + 3.0)])


def h3(ax):
    base(ax, "H3 · rampa recta hasta la torre y giro en horquilla\nsobre la propia terraza (sin nada fuera)")
    rampa(ax, [(XM, YPIE), (XM, Q[1] + 0.5)])
    ax.add_patch(Circle((9.7, Q[1] + 3.5), 5.5, fill=False, ec="crimson", lw=0.8, ls="--"))
    ax.text(9.7, Q[1] + 9.5, "círculo de giro Ø 11 m:\nno cabe (choca con escalera\ny barandilla)", fontsize=4.6, color="crimson", ha="center")
    camino(ax, [(XM, 52), (XM, Q[1] + 2.0), (WP - 1.5, Q[1] + 1.0), (WB / 2 + 1.5, Q[1] + 1.2), (WB / 2, YR0 + 3.0)])


TXT = [
 ("Lo que enseña la maqueta (F76, recorte)",
  "1) la rampa sube pegada al ala y en su tramo alto su borde se CURVA hacia fuera (a la izquierda del que sube);\n"
  "2) debajo de la curva hay un ARCO con pilares y vidrio detrás (paso en planta baja);\n"
  "3) arriba termina en un BLOQUE plano y recto (rellano) junto a un foso ovalado, delante de la torre;\n"
  "4) entre ese bloque y la base de la torre hay una ranura oscura: el rellano está separado y se cruza para volver."),
 ("Otras pruebas",
  "• foto S. Glover: bajo el barril, cara CURVA de hormigón junto a la torre (borde de la curva de la rampa);\n"
  "• cenitales F36/F62: un elemento blanco alargado y diagonal sale de la base de la torre hacia la plaza (el rellano);\n"
  "• foto del hotel: la entrada (chaflán) queda libre, con la rampa subiendo a su derecha;\n"
  "• Bing: tramo recto de la rampa de 2,96 m de ancho y pie a ~35 m del testero."),
 ("Comparación", "              F76 curva+arco  Glover  cenital  hotel libre  giro de coche\n"
  "H1 curva fuera     sí              sí      sí       sí           sí (R 9 + rellano)\n"
  "H2 plataforma      no              ~       no       sí           justo (6 m)\n"
  "H3 horquilla       no              no      no       sí           NO (no cabe)"),
 ("Defiendo H1",
  "Es la única que explica a la vez la curva y el arco de la maqueta, la cara curva bajo el barril (Glover) y el\n"
  "elemento diagonal de las cenitales, deja intacta la entrada del hotel y da al coche un giro real: sube, se abre a\n"
  "la izquierda por la curva hasta el rellano, vuelve a la derecha por el puente sobre la banda del hotel, cruza la\n"
  "terraza y sube por el techo del restaurante bajo la escalera. Sin medir: radio de la curva (9 m), tamaño del\n"
  "rellano (7 × 11 m) y ancho del puente (4 m). H2 es un apaño sin apoyo en las fotos; H3 es geométricamente imposible."),
]

if __name__ == "__main__":
    fig = plt.figure(figsize=(16.5, 11.7))
    fig.text(0.01, 0.985, "HOTEL SALUT – giro en lo alto de la rampa de acceso: tres hipótesis (misma base, escala común)", fontsize=12, weight="bold", va="top")
    for i, f in enumerate((h1, h2, h3)):
        ax = fig.add_axes([0.01 + i * 0.22, 0.05, 0.215, 0.88]); f(ax)
    y = 0.93
    for t, b in TXT:
        fig.text(0.675, y, t, fontsize=8.5, weight="bold", va="top")
        fig.text(0.675, y - 0.022, b, fontsize=6.4, va="top", family="monospace" if t == "Comparación" else None)
        y -= 0.06 + 0.017 * b.count("\n")
    fig.savefig("GIRO_HIPOTESIS.png", dpi=90)
    fig.savefig("GIRO_HIPOTESIS.pdf")
    print("ok")
