"""Tres lecturas de A–B (7,3 m) para el bloque alto del ala corta, dibujadas en planta y en sección transversal."""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
import edificio as E
import lineas as L

V = E._v
sw = lambda x, y: np.array(E.SWP(x, y))
x0 = -E.L_C; WC = E.W_C; VV = V["VOL_V"]; VL = V["VOL_L"]
d = np.array([0.7071, 0.7071])                       # diagonal paralela al chaflán (coordenadas de L recta)
P1 = np.array([x0 + VL, -VV])
AB = 7.3


def huella(prof):
    """bloque alto con fondo 'prof' desde la cara del vuelo: vuelo 6 m + diagonal hasta la línea A"""
    yA = -VV + prof
    t = (yA - P1[1]) / d[1]; C = P1 + t * d
    return [(x0, -VV), tuple(P1), tuple(C), (x0, yA)], C


def base(ax):
    pl = E.plantas_base()
    ax.add_patch(Polygon(pl["P1"], closed=True, fc="none", ec="0.3", lw=0.9))
    ax.add_patch(Circle(E.T, E.R_AL, fill=False, ec="0.6", lw=0.5, ls="--"))
    ax.add_patch(Circle(E.T, E.R_COL, fc="0.8", ec="k", lw=0.6))
    ax.plot(*zip(sw(x0 - 3, 0), sw(x0 + 26, 0)), color="0.6", lw=0.5, ls="-.")
    ax.text(*sw(x0 + 12, -4.2), "CALLE", fontsize=6, color="0.4", ha="center")
    ax.add_patch(Polygon([sw(x0 - 4, -2), sw(x0, -2), sw(x0, WC + 2), sw(x0 - 4, WC + 2)], closed=True, fc="none", ec="0.5", hatch="////", lw=0.4))
    ax.text(*sw(x0 - 2, WC / 2), "colindante", fontsize=5, rotation=90, ha="center", va="center", color="0.4")


def poly(ax, pts, **k):
    ax.add_patch(Polygon([sw(*p) for p in pts], closed=True, **k))


def puntos(ax, A, B, C):
    for n, p in (("A", A), ("B", B), ("C", C)):
        q = sw(*p); ax.plot(*q, "o", color="crimson", ms=4, zorder=9)
        ax.text(q[0] + 0.5, q[1] + 0.5, n, color="crimson", fontsize=9, weight="bold", zorder=9)
    L.cota(ax, sw(*A), sw(*B), -1.5, "A–B", fs=6, color="crimson")
    L.cota(ax, sw(*B), sw(*C), 1.5, "B–C", fs=6, color="crimson")


def seccion(ax, perfiles, titulo):
    """sección perpendicular a la calle por la mitad del vuelo: lista de (y0, y1, z1, estilo)"""
    ax.plot([-4, 16], [0, 0], color="k", lw=1.2)
    ax.add_patch(Polygon([(-VV + VV, 0), (WC, 0), (WC, E.Z_P1), (0, E.Z_P1)], closed=True, fc="0.9", ec="k", lw=0.6))
    for y0, y1, z1, st in perfiles:
        z0 = V["Z_VOL0"] if y0 < 0 else E.Z_P1
        ax.add_patch(Polygon([(y0, z0), (y1, z0), (y1, z1), (y0, z1)], closed=True, **st))
    ax.text(-3.5, 0.5, "calle", fontsize=6); ax.text(WC - 0.3, 0.5, "patio", fontsize=6, ha="right")
    ax.set_xlim(-4, 16); ax.set_ylim(-1, 15); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(titulo, fontsize=7, loc="left")


fig = plt.figure(figsize=(16.5, 11.7))
fig.text(0.01, 0.98, "Bloque alto del ala corta: tres lecturas de la triangulación A–B = 7,3 m · B–C = 14,98 m (A–B perpendicular al colindante)",
         fontsize=12, weight="bold", va="top")
LAD = dict(fc="#f1e4dc", ec="k", lw=1.2, hatch="---")
ALT = dict(fc="#d8c0b0", ec="k", lw=1.2, hatch="---")
ops = []
# 1) todo el bloque alto con 7,3 de fondo
h1, C1 = huella(AB)
ops.append(("1 · Todo el bloque alto tiene 7,3 m de fondo",
            [(h1, LAD)], ((x0, -VV + AB), (x0, -VV), tuple(C1)),
            [(-VV, -VV + AB, E.Z_ALTO, LAD)],
            "La línea A queda a 7,3 m de la cara del vuelo (6,1 m de la fachada).\nB–C = %.1f m por la línea A (triangulación 14,98).\nDetrás, el ala corta es cubierta a +7,20 con las claraboyas." % np.linalg.norm(C1 - np.array((x0, -VV + AB)))))
# 2) parte más alta 7,3 de fondo + resto del bloque hasta el fondo del ala corta
ba_full = [tuple(np.array(p)) for p in E.bloque_alto_poligono()]
h2, C2 = huella(AB)
ops.append(("2 · Solo la parte más alta (escalón del peto) tiene 7,3 m",
            [("REAL", ba_full, LAD), (h2, ALT)], ((x0, -VV + AB), (x0, -VV), tuple(C2)),
            [(-VV, WC, E.Z_ALTO, LAD), (-VV, -VV + AB, E.Z_ALTO + 0.6, ALT)],
            "Bloque alto hasta el fondo del ala corta (línea A del croquis) a +11,50,\ny encima del vuelo un cuerpo más alto (+12,10, peto blanco de la foto frontal)\nde 7,3 m de fondo: ahí están A, B y C."))
# 3) modelo actual
ops.append(("3 · Modelo actual (fondo 13,9 m): A–B no encaja",
            [("REAL", ba_full, LAD)], ((x0, WC), (x0, -VV), None),
            [(-VV, WC, E.Z_ALTO, LAD)],
            "El bloque alto llega desde el vuelo hasta el fondo del ala corta.\nLa línea A mide 15,6 m (≈ B–C 14,98) pero el fondo es 13,9 m, no 7,3:\nhabría que explicar A–B con otra arista."))
for i, (tit, huellas, (A, B, C), perf, txt) in enumerate(ops):
    ax = fig.add_axes([0.01 + i * 0.33, 0.30, 0.32, 0.62])
    base(ax)
    for h in huellas:
        if h[0] == "REAL":
            ax.add_patch(Polygon(h[1], closed=True, **h[2]))
        else:
            poly(ax, h[0], **h[1])
    if C is not None:
        puntos(ax, A, B, C)
    else:
        q = [np.array(p) for p in E.bloque_alto_poligono()]
        L.cota(ax, q[0], q[-1], -1.5, "fondo", fs=6, color="crimson")
    ax.set_xlim(x0 - 6, x0 + 30); ax.set_ylim(-8, 26); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(tit, fontsize=9, loc="left", weight="bold")
    axs = fig.add_axes([0.03 + i * 0.33, 0.03, 0.28, 0.19])
    seccion(axs, perf, "")
    fig.text(0.02 + i * 0.33, 0.29, txt, fontsize=7, va="top")
fig.savefig("OPCIONES_AB.png", dpi=90)
print("ok")
