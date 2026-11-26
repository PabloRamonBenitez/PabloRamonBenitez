"""PLANTA DE SITUACIÓN (1984) dibujada sobre la planta de cubiertas del MODELO (no sobre una foto):
cada elemento del entorno se refiere a líneas ya comprobadas del edificio:
  calle Ivana Mazepy  = paralela a la fachada del ala corta (SWP y = 0), por delante del vuelo
  plaza               = delante del chaflán (P, Y < fachada de planta baja)
  colindante          = al otro lado de la medianera (SWP x < −L_C), con su cuerpo a la calle y 10 lucernarios
                        en diente de sierra (F01, 1984)
  fuente              = vaso en media luna al pie de la columna (F01, F14)
  camino de coches    = entra desde la plaza junto al pie de la concha y rodea el ala larga por detrás (F47, F73)
  césped              = franja entre la fachada exterior del ala larga y el camino (F47, F73)"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Wedge, Circle
from PIL import Image
import edificio as E, laminas as LM

V = E._v; T = np.array(E.T); pl = E.plantas_base()
x0 = -V["L_C"]
SW = lambda x, y: tuple(np.array(E.SWP(x, y)))
fig = plt.figure(figsize=(23.4, 16.5))
ax = fig.add_axes([0.02, 0.05, 0.62, 0.88]); ax.set_aspect("equal"); ax.axis("off")
# 1) plaza delante del chaflán y calle paralela a la fachada del ala corta (fondos, debajo de todo)
yf = -(E.R_COL - E.RET) - V["RETR"]
ax.add_patch(Polygon([E.P(-60, yf), E.P(45, yf), E.P(45, -40), E.P(-60, -40)], closed=True, fc="0.94", ec="none", zorder=0))
ax.add_patch(Polygon([SW(x0 - 40, -1.4), SW(30, -1.4), SW(30, -16), SW(x0 - 40, -16)], closed=True, fc="0.88", ec="none", zorder=0.2))
ax.plot(*zip(SW(x0 - 40, -1.4), SW(6, -1.4)), color="0.5", lw=0.8, zorder=0.3)
ax.text(*SW(x0 - 14, -9), "calle Ivana Mazepy", fontsize=12, color="0.3", ha="center", rotation=math.degrees(E.PHI), zorder=0.4)
ax.text(*E.P(-2, -34), "PLAZA", fontsize=14, color="0.35", ha="center", zorder=0.4)
for i in range(5):                                         # autobuses aparcados en la plaza, en línea con el chaflán (F14, F15, F70)
    c = np.array(E.P(6 + i * 3.4, -20)); u, n = np.array(E.U), np.array(E.N)
    ax.add_patch(Polygon([c - u * 1.25 - n * 5.5, c + u * 1.25 - n * 5.5, c + u * 1.25, c - u * 1.25], closed=True, fc="white", ec="0.4", lw=0.6, zorder=1))
ax.text(*E.P(13, -28.5), "autobuses (F14, F15, F70)", fontsize=8, ha="center", color="0.3", zorder=1)
# 2) parque, césped y camino de coches por detrás del ala larga
ax.add_patch(Polygon([(E.W_EXT + 0.5, 15), (70, 15), (70, 112), (-20, 112), (-20, E.L_L + 1), (E.W_EXT + 0.5, E.L_L + 1)], closed=True, fc="#e6f1dc", ec="none", zorder=0.1))
ax.add_patch(Polygon([(E.W_EXT + 0.5, E.Y_CUNA), (E.W_EXT + 4.5, E.Y_CUNA), (E.W_EXT + 4.5, E.L_L - 1), (E.W_EXT + 0.5, E.L_L - 1)], closed=True, fc="#b9dca0", ec="none", zorder=0.6))
xr = E.W_EXT + 7.5
cx = np.r_[np.linspace(E.W_EXT + 3, xr, 15), np.full(30, xr), xr - (xr + 10) * np.sin(np.linspace(0, math.pi / 2, 20))]
cy = np.r_[np.linspace(22, 40, 15), np.linspace(40, E.L_L + 2, 30), E.L_L + 2 + 6 * (1 - np.cos(np.linspace(0, math.pi / 2, 20)))]
ax.plot(cx, cy, color="#cdbd9b", lw=16, solid_capstyle="round", zorder=0.7)
ax.plot(cx, cy, color="0.45", lw=0.6, ls=(0, (6, 4)), zorder=0.8)
ax.text(xr + 3.0, 70, "camino de coches: entra desde la plaza junto a la concha\ny rodea el edificio por detrás (F47, F73)", fontsize=9, rotation=90, va="center", zorder=2)
ax.text(E.W_EXT + 2.5, 78, "césped", fontsize=8, rotation=90, color="#3f6b2f", va="center", zorder=2)
ax.text(45, 70, "parque (F24, F47)", fontsize=11, color="#4b6b3a", ha="center", zorder=2)
# 3) edificio colindante al otro lado de la medianera, con su cuerpo a la calle y los lucernarios en diente de sierra
ax.add_patch(Polygon([SW(x0 - 30, 0), SW(x0, 0), SW(x0, V["W_C"] + 6), SW(x0 - 30, V["W_C"] + 6)], closed=True, fc="0.86", ec="0.4", lw=0.8, hatch="///", zorder=1))
cuerpo = [SW(x0 - 16, -1.2), SW(x0, -1.2), SW(x0, 9.5), SW(x0 - 16, 9.5)]
ax.add_patch(Polygon(cuerpo, closed=True, fc="0.8", ec="k", lw=0.9, zorder=1.2))
def diente(x, y):
    ax.add_patch(Polygon([SW(x - 0.8, y - 0.8), SW(x + 0.8, y - 0.8), SW(x + 0.8, y + 0.8), SW(x - 0.8, y + 0.8)], closed=True, fc="#dfe8ee", ec="k", lw=0.6, zorder=1.3))
    ax.plot(*zip(SW(x - 0.8, y + 0.8), SW(x + 0.8, y + 0.8)), color="k", lw=1.4, zorder=1.31)
for i in range(5): diente(x0 - 13.5 + 2.4 * i, 1.8)
for x, y in ((x0 - 13.0, 5.4), (x0 - 10.4, 6.8), (x0 - 7.8, 5.4), (x0 - 5.2, 6.8), (x0 - 2.6, 5.4)): diente(x, y)
ax.text(*SW(x0 - 8, 13.0), "edificio colindante: cuerpo a la calle\ncon 10 lucernarios en diente de sierra (F01, 1984)", fontsize=8, ha="center", zorder=3)
# 4) EL HOTEL: planta de cubiertas del modelo (vectorial, verificada)
LM.L.vista_vectorial(ax, LM.M, z=4)
ax.add_patch(Polygon(pl["P1"], closed=True, fc="white", ec="none", zorder=3.5))
LM.L.vista_vectorial(ax, LM.M, z=4)
# 5) fuente al pie de la columna (F01, F14)
ax.add_patch(Wedge(T, 5.6, 200, 345, width=2.3, fc="#bfe0f2", ec="k", lw=1.0, zorder=6))
ax.annotate("FUENTE (1984): vaso en media luna\nal pie de la columna (F01, F14)", tuple(T + 4.6 * np.array([0.3, -1])), tuple(E.P(-14, -12)),
            fontsize=9, color="#1a5fb4", weight="bold", arrowprops=dict(arrowstyle="->", color="#1a5fb4"), zorder=9)
ax.text(*E.P(8, -6.0), "entrada del hotel", fontsize=8, ha="center", color="0.2", zorder=9)
ax.text(*SW(x0 + 4, -0.6), "medianera", fontsize=7, rotation=math.degrees(E.PHI) + 90, zorder=9)
# norte y escala
ax.annotate("N", (-38 + 5 * 0.914 * 0 - 2.1, 104 + 4.6), (-38, 104), arrowprops=dict(arrowstyle="-|>"), fontsize=12, ha="center")
for k in range(3):
    ax.add_patch(Polygon([(-45 + 10 * k, -38), (-35 + 10 * k, -38), (-35 + 10 * k, -37.4), (-45 + 10 * k, -37.4)], closed=True, fc="k" if k % 2 == 0 else "white", ec="k", lw=0.5, zorder=9))
ax.text(-45, -36.6, "0        10        20        30 m", fontsize=8, zorder=9)
ax.set_xlim(-60, 72); ax.set_ylim(-40, 114)
ax.set_title("PLANTA DE SITUACIÓN 1984 – sobre la planta de cubiertas del modelo; entorno según F01, F14, F15, F24, F47, F70, F73",
             fontsize=13, loc="left", weight="bold")
for i, (f, t_) in enumerate((("1.webp", "F01 – fuente y colindante con dientes de sierra"), ("47.webp", "F47 – camino de coches y césped"), ("14.webp", "F14 – fuente y autobuses"))):
    a = fig.add_axes([0.66, 0.66 - i * 0.31, 0.33, 0.29]); a.imshow(Image.open(LM.IMG + f).convert("RGB")); a.axis("off"); a.set_title(t_, fontsize=10, loc="left")
fig.savefig("ENTORNO_1984.png", dpi=72); fig.savefig("ENTORNO_1984.pdf")
print("ok")
