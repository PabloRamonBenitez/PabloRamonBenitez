"""COLLAGE: foto de Alamy semitransparente superpuesta al alzado del modelo (misma escala, mismo eje, misma cota).
Lo que no coincide es diferencia real o perspectiva; cada recuadro amplía una zona."""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import edificio as E, laminas as LM, vista_alamy as VA

FOTO = sys.argv[1] if len(sys.argv) > 1 else "/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/scratchpad/alamy.jpg"
PV, PH, Y0, Y_REF, XT = 175.25 / 3.10, 64.4, 887, 1337, 1078
z = lambda y: E.Z_B1 + (Y_REF - y) / PV
s = lambda x: (x - XT) / PH
im = Image.open(FOTO).convert("RGB"); W, H = im.size
crop = im.crop((0, Y0 + 150, W, Y0 + 2200))
XTm = VA.x_eje_alzado()
ext = (XTm + s(0), XTm + s(W), z(2200), z(150))
ZONAS = [("CONJUNTO", (-21, 24), (19, 52)), ("REMATE Y LETRAS", (-10, 10), (42, 52)),
         ("VISERA, BANDA Y CAJA DE ESCALERA", (-19, 18), (37, 45)), ("TAMBOR, OJOS Y CUBIERTA DEL BARRIL", (-17, 17), (31, 40)),
         ("BARRIL: FORJADOS, POYETES, ALETAS", (-17, 17), (19, 33))]
fig = plt.figure(figsize=(22, 26))
axs = [fig.add_axes([0.03, 0.52, 0.94, 0.45])] + [fig.add_axes([0.03 + (i % 2) * 0.48, 0.27 - (i // 2) * 0.25, 0.46, 0.22]) for i in range(4)]
for ax, (t, xl, zl) in zip(axs, ZONAS):
    LM.alzado(ax, VA.MIRA, "")
    ax.imshow(crop, extent=ext, aspect="auto", alpha=0.5, zorder=100)
    ax.set_xlim(XTm + xl[0], XTm + xl[1]); ax.set_ylim(*zl); ax.set_aspect("equal")
    ax.set_title(t + " – foto al 50 % sobre el modelo", fontsize=10, loc="left", weight="bold")
fig.suptitle("COLLAGE ALAMY / MODELO – misma escala (56,53 px/m vertical, 64,4 px/m horizontal), eje de la torre y referencia +32,50",
             fontsize=13, x=0.03, ha="left", weight="bold")
fig.savefig("COLLAGE_ALAMY.png", dpi=70)
print("ok")
