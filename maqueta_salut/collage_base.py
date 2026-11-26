"""COLLAGE DE LA BASE DE LA TORRE: el alzado del modelo bajo cada foto frontal que la muestra (foto al 50 %), con la misma
escala (paso de forjados = 3,10 m) y la misma referencia (+17,00 = cara inferior del canto de la 2.ª planta del barril).
Sirve para comprobar, foto a foto, la 1.ª planta (pavés, banda), el escalón de las aletas, el fondo plano, las vigas y el cuello."""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import edificio as E, laminas as LM

FOTOS = [  # (archivo, rótulo, azimut cámara, px/m, y de +17,00, x del eje)
    ("9.webp", "F09 (teleobjetivo)", 320.0, 12.9, 571.5, 307.0),
    ("14.webp", "F14 (1984)", 327.0, 41.2 / 3.10, 443.0, 581.5),
]
fig = plt.figure(figsize=(26, 9))
for i, (img, tit, az, K, y17, xt) in enumerate(FOTOS):
    mira = (-math.cos(math.radians(az)), -math.sin(math.radians(az)))
    d = np.array(mira); a = math.radians(-(math.degrees(math.atan2(d[1], d[0])) - 90))
    xT = math.cos(a) * E.T[0] - math.sin(a) * E.T[1]
    im = Image.open(LM.IMG + img).convert("RGB"); W, H = im.size
    z = lambda y: E.Z_B0 + E.F + (y17 - y) / K
    ax = fig.add_axes([0.01 + i * 0.495, 0.04, 0.48, 0.86])
    LM.alzado(ax, mira, "")
    ax.imshow(im, extent=(xT - xt / K, xT + (W - xt) / K, z(H), z(0)), aspect="auto", alpha=0.5, zorder=100)
    ax.set_xlim(xT - 17, xT + 17); ax.set_ylim(8.5, 19.5); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(f"{tit}: foto al 50 % sobre el modelo · {K:.1f} px/m · +17,00".replace(".", ","), fontsize=11, loc="left", weight="bold")
fig.suptitle("BASE DE LA TORRE – modelo corregido (fondo plano, vigas rectas, aletas con escalón, 1.ª planta enrasada, cuello sin losa volada) bajo cada foto",
             fontsize=13, x=0.01, ha="left", weight="bold")
fig.savefig("COLLAGE_BASE.png", dpi=90)
print("ok")
