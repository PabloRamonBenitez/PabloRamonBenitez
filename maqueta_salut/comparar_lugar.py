"""PLANO DE LUGAR frente a la vista cenital (F35, Google): el plano se dibuja encima de la foto al 50 % con una semejanza
(escala, giro, traslación) ajustada a referencias del propio edificio. Sirve para comparar lo nuevo con la foto, no para medir."""
import math, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import laminas as LM, edificio as E

IMG = LM.IMG + "35.webp"
im = Image.open(IMG).convert("RGB"); W, H = im.size
# referencias foto ↔ modelo (px de la foto, m del modelo)
# AJUSTE MEDIDO sobre F35 (no a ojo): dirección del ala larga por sus dos bordes rectos (−34,9° en la imagen), escala por su ancho
# (borde del patio → peto de la terraza = 155 px para 12,74 m → 12,17 px/m; la banda oscura de la cubierta del bar, 88 px = 7,2 m,
# lo confirma) y posición por el centro de la silueta del barril (465, 640) = eje de la torre.
ANG = math.radians(-34.9); S = 155.0 / 12.74
def semejanza(_=None):
    d = np.array([math.cos(ANG), math.sin(ANG)])               # +y del modelo → a lo largo del ala, en la imagen (y hacia abajo)
    n = np.array([-d[1], d[0]]) * -1                           # +x del modelo → hacia fuera del ala (abajo a la derecha)
    n = np.array([0.572, 0.821])
    A = np.c_[n, d] * S                                        # columnas: imagen de +x y de +y del modelo (px, y hacia abajo)
    A = np.diag([1, -1]) @ A                                    # a imagen con y hacia arriba
    t = np.array([465.0, -640.0]) - A @ np.array(E.T)
    return A, t
if __name__ == "__main__":
    import plano_lugar as PL
    R, t = semejanza()
    fig = PL.hoja_lugar()
    ax = fig.axes[0]
    Ri = np.linalg.inv(R)
    corners = [Ri @ (np.array([x, -y]) - t) for x, y in ((0, 0), (W, 0), (W, H), (0, H))]
    # imagen colocada en coordenadas del modelo con transformación afín
    import matplotlib.transforms as mt
    A = np.eye(3); A[:2, :2] = Ri @ np.diag([1, -1]); A[:2, 2] = -Ri @ t
    tr = mt.Affine2D(A) + ax.transData
    ax.imshow(im, extent=(0, W, H, 0), transform=tr, alpha=0.5, zorder=50)
    fig.savefig("COMPARAR_LUGAR_F35.png", dpi=90)
    print("escala", round(np.linalg.norm(R[:, 0]), 2), "px/m")
