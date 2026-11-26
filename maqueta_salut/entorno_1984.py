"""Planta de situación histórica (1984): el hotel con su entorno según las fotos de época (F01, F14, F15, F23, F24, F47, F70).
Solo lo que se ve en las fotos; lo demás, en línea fina sin detalle."""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Wedge, FancyArrowPatch
from PIL import Image
import edificio as E, laminas as LM, lineas as L

V = E._v; T = np.array(E.T); pl = E.plantas_base()
fig = plt.figure(figsize=(23.4, 16.5))
ax = fig.add_axes([0.02, 0.05, 0.62, 0.88]); ax.set_aspect("equal"); ax.axis("off")
# calles y plaza
calle = [E.SWP(-45, -18), E.SWP(10, -18), E.SWP(10, -1.5), E.SWP(-45, -1.5)]
ax.add_patch(Polygon(calle, closed=True, fc="0.92", ec="none", zorder=0)); ax.text(*E.SWP(-30, -9), "calle Ivana Mazepy", fontsize=11, rotation=math.degrees(E.PHI) + 0, ha="center", color="0.3")
plaza = [E.P(-34, -2.5), E.P(30, -2.5), E.P(30, -32), E.P(-34, -32)]
ax.add_patch(Polygon(plaza, closed=True, fc="0.95", ec="none", zorder=0)); ax.text(*E.P(-12, -24), "PLAZA", fontsize=13, color="0.35", ha="center")
for i in range(5):                                         # autobuses aparcados delante del chaflán (F14, F15, F70)
    c = np.array(E.P(8 + i * 3.4, -19.5)); u = np.array(E.U); n = np.array(E.N)
    q = [c - u * 1.25 - n * 5.5, c + u * 1.25 - n * 5.5, c + u * 1.25 + n * 0.0, c - u * 1.25 + n * 0.0]
    ax.add_patch(Polygon(q, closed=True, fc="white", ec="0.4", lw=0.6, zorder=2))
ax.text(*E.P(15, -27), "aparcamiento de autobuses\n(F14, F15, F70)", fontsize=8, ha="center", color="0.3")
# parque detrás del ala larga: césped y caminos curvos (F24, F47)
park = [(E.W_EXT + 2, 20), (60, 20), (60, 100), (E.W_EXT + 2, 100)]
ax.add_patch(Polygon(park, closed=True, fc="#e3f0d8", ec="none", zorder=0))
t = np.linspace(0, 1, 60)
ax.text(40, 75, "parque con caminos curvos\n(F24, F47; trazado esquemático)", fontsize=10, color="#4b6b3a", ha="center")
for xy in ((25, 45), (32, 60), (44, 52), (50, 82), (28, 88), (20, 70)):
    ax.add_patch(Circle(xy, 2.2, fc="#b8d7a2", ec="#6f9a5a", lw=0.6, zorder=1))
# edificios vecinos (siluetas)
ax.add_patch(Polygon([E.SWP(-45, -1.5), E.SWP(-V["L_C"], -1.5), E.SWP(-V["L_C"], 24), E.SWP(-45, 24)], closed=True, fc="0.85", ec="0.5", hatch="///", zorder=1))
ax.text(*E.SWP(-36, 10), "edificio colindante", fontsize=9, rotation=90, ha="center")
# el hotel: huella de planta primera, torre y escalera
ax.add_patch(Polygon(pl["P1"], closed=True, fc="0.75", ec="k", lw=1.4, zorder=3))
ax.add_patch(Polygon(pl["PB"], closed=True, fill=False, ec="k", lw=0.6, ls="--", zorder=3))
ax.add_patch(Circle(T, E.R_AL, fc="0.88", ec="k", lw=1.2, zorder=4)); ax.add_patch(Circle(T, E.R_COL, fc="0.6", ec="k", lw=1.0, zorder=5))
ax.text(*T + np.array([0, 4]), "HOTEL SALUT\ntorre (+50,8)", fontsize=10, ha="center", weight="bold", zorder=6)
# fuente al pie de la columna (F01, F14): vaso en media luna hacia la plaza y el restaurante
a0, a1 = 200, 345
ax.add_patch(Wedge(T, 5.6, a0, a1, width=2.3, fc="#bfe0f2", ec="k", lw=1.0, zorder=6))
ax.add_patch(Wedge(T, 5.6, a0, a1, width=0.3, fc="0.6", ec="none", zorder=6.1))
fq = T + 7.5 * np.array([math.cos(math.radians(270)), math.sin(math.radians(270))])
ax.annotate("FUENTE (1984)\nvaso en media luna al pie de la columna\n(F01, F14)", T + 4.5 * np.array([0, -1]), fq + np.array([-14, -10]),
            fontsize=9, color="#1a5fb4", weight="bold", arrowprops=dict(arrowstyle="->", color="#1a5fb4"), zorder=9)
ax.text(*E.P(0, -4.0), "entrada del hotel", fontsize=8, ha="center", color="0.2", zorder=9)
ax.annotate("rampa de acceso (concha)", (E.W_EXT - 1, 45), (E.W_EXT + 8, 40), fontsize=8, arrowprops=dict(arrowstyle="->"), zorder=9)
ax.annotate("terraza de las sombrillas", (9.5, 70), (20, 95), fontsize=8, arrowprops=dict(arrowstyle="->"), zorder=9)
ax.annotate("N", (-30 + 3, 95 + 7), (-30, 95), arrowprops=dict(arrowstyle="-|>"), fontsize=12, ha="center")
for x in range(0, 30, 10):
    ax.add_patch(Polygon([(-35 + x, -30), (-25 + x, -30), (-25 + x, -29.4), (-35 + x, -29.4)], closed=True, fc="k" if x % 20 == 0 else "white", ec="k", lw=0.5))
ax.text(-35, -28.5, "0      10      20      30 m", fontsize=8)
ax.set_xlim(-48, 62); ax.set_ylim(-34, 102)
ax.set_title("ENTORNO HISTÓRICO (1984) – planta de situación según las fotos de época", fontsize=14, loc="left", weight="bold")
for i, (f, t_) in enumerate((("1.webp", "F01 – 1984: la fuente al pie de la columna"), ("14.webp", "F14 – 1984: fuente y autobuses"), ("24.webp", "F24 – 1984: parque y caminos"))):
    a = fig.add_axes([0.66, 0.66 - i * 0.31, 0.33, 0.29]); a.imshow(Image.open(LM.IMG + f).convert("RGB")); a.axis("off"); a.set_title(t_, fontsize=10, loc="left")
fig.savefig("ENTORNO_1984.png", dpi=72); fig.savefig("ENTORNO_1984.pdf")
print("ok")
