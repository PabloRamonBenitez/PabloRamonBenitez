"""COLLAGE F09 (teleobjetivo, 2.ª vista de la torre, mira según U): foto al 50 % sobre el alzado del modelo desde 320°.
Escala por el paso de forjados (40 px = 3,10 m → 12,9 px/m, igual en horizontal: foto normal); referencia: borde inferior
del canto de la 2.ª planta del barril (y 571,5 = +17,00); eje: centro del tambor (x 307)."""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import edificio as E, laminas as LM

AZ = 320.0                                   # torre → cámara (F09)
MIRA = (-math.cos(math.radians(AZ)), -math.sin(math.radians(AZ)))
K, Y17, XT = 12.9, 571.5, 307.0
z = lambda y: E.Z_B0 + E.F + (Y17 - y) / K
im = Image.open(LM.IMG + "9.webp").convert("RGB"); W, H = im.size
d = np.array(MIRA); a = math.radians(-(math.degrees(math.atan2(d[1], d[0])) - 90))
xT = math.cos(a) * E.T[0] - math.sin(a) * E.T[1]
ext = (xT - XT / K, xT + (W - XT) / K, z(H), z(0))
ZONAS = [("CONJUNTO", (-22, 22), (8, 52)), ("REMATE, LETRAS Y VISERA", (-16, 16), (38, 52)),
         ("TAMBOR, OJOS, BANDA", (-17, 17), (31, 44)), ("BASE DEL BARRIL: PAVÉS, BANDA, FONDO INCLINADO", (-17, 17), (10, 22))]
fig = plt.figure(figsize=(22, 24))
axs = [fig.add_axes([0.03, 0.52, 0.94, 0.45])] + [fig.add_axes([0.03 + (i % 2) * 0.48, 0.27 - (i // 2) * 0.25, 0.46, 0.22]) for i in range(3)]
for ax, (t, xl, zl) in zip(axs, ZONAS):
    LM.alzado(ax, MIRA, "")
    ax.imshow(im, extent=ext, aspect="auto", alpha=0.5, zorder=100)
    ax.set_xlim(xT + xl[0], xT + xl[1]); ax.set_ylim(*zl); ax.set_aspect("equal")
    ax.set_title(t + " – F09 al 50 % sobre el modelo", fontsize=10, loc="left", weight="bold")
fig.suptitle("COLLAGE F09 / MODELO – vista desde 320° (según U), 12,9 px/m en las dos direcciones, referencia +17,00", fontsize=13, x=0.03, ha="left", weight="bold")
fig.savefig("COLLAGE_F09.png", dpi=70)
print("ok")
