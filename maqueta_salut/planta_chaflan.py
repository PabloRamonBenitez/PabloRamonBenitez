"""Detalle en planta del chaflan: planta baja (rojo, corte a +1,5) y planta primera (verde, corte a +6)."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import planos as P
fig, ax = plt.subplots(figsize=(10, 10))
for z, col, lw, nom in ((1.5, "red", 1.6, "planta baja (+1,5)"), (6.0, "green", 1.6, "planta primera (+6,0)")):
    for poly in P.Ms.slice(z).to_polygons():
        ax.add_patch(Polygon(poly, closed=True, fc="none", ec=col, lw=lw))
    ax.plot([], [], color=col, label=nom)
for poly in P.Ms.slice(17.0).to_polygons():
    ax.add_patch(Polygon(poly, closed=True, fc="none", ec="0.7", lw=0.6, ls="--"))
ax.plot([], [], color="0.7", ls="--", label="barril (proyeccion)")
ax.set_xlim(-25, 30); ax.set_ylim(-12, 40); ax.set_aspect("equal"); ax.grid(True, lw=0.3)
ax.legend(loc="upper left"); ax.set_title("Detalle del chaflan en planta (m)")
fig.savefig("Hotel_Salut_planta_chaflan.png", dpi=110)
