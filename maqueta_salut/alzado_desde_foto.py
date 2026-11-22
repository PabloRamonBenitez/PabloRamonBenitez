"""ALZADO DEL CHAFLAN dibujado SOLO con medidas tomadas en la foto F09 (no del modelo 3D).
Escala de la foto: puntas de aletas del barril = 30,6 m -> 12,97 px/m; suelo y=795 px; eje torre x=303,5 px."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
I='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'
PX, Y0, X0 = 397/30.6, 795, 303.5
m = lambda px_y: (Y0-px_y)/PX          # px vertical -> m
mx = lambda px_x: (px_x-X0)/PX         # px horizontal -> m respecto al eje
# medidas leidas en F09 (px) -> metros
E = dict(
  rest=(mx(80), mx(246)), col=(mx(246), mx(330)), hotel=(mx(330), mx(455)), relieve=(mx(455), mx(640)),
  pb_top=m(745), p1_top=m(700),
  barril=(mx(105), mx(502), m(598), m(372)),
  cuello=(mx(205), mx(400), m(660), m(598)),
  tambor=(mx(133), mx(485), m(370), m(300)),
  banda=(mx(150), mx(432), m(300), m(270)),
  visera=(mx(110), mx(442), m(270), m(228)),
  remate=(mx(240), mx(385), m(228), m(158)),
)
fig, (a, b) = plt.subplots(1, 2, figsize=(22, 12))
def caja(ax, x0, x1, z0, z1, **kw): ax.add_patch(Rectangle((x0, z0), x1-x0, z1-z0, fill=False, lw=1.4, **kw))
def cota_h(ax, x0, x1, z, t):
    ax.annotate("", (x0, z), (x1, z), arrowprops=dict(arrowstyle="<->", lw=0.7, color="crimson"))
    ax.text((x0+x1)/2, z+0.3, f"{t} {x1-x0:.1f}".replace(".", ","), color="crimson", fontsize=7, ha="center")
def cota_v(ax, x, z0, z1, t):
    ax.annotate("", (x, z0), (x, z1), arrowprops=dict(arrowstyle="<->", lw=0.7, color="crimson"))
    ax.text(x+0.3, (z0+z1)/2, f"{t} {z1-z0:.1f}".replace(".", ","), color="crimson", fontsize=7, va="center")
for ax in (a, b):
    ax.axhline(0, color="k", lw=1.5)
# --- dibujo ---
r0, r1 = E["rest"]; c0, c1 = E["col"]; h0, h1 = E["hotel"]; v0, v1 = E["relieve"]
caja(a, r0, r1, 0, E["pb_top"], ls="--"); caja(a, r0, r1, E["pb_top"], E["p1_top"])
caja(a, h0, h1, 0, E["pb_top"], ls="--"); caja(a, h0, h1, E["pb_top"], E["p1_top"])
caja(a, v0, v1, 0, E["pb_top"], ls="--"); caja(a, v0, v1, E["pb_top"], E["p1_top"])
caja(a, c0, c1, 0, E["cuello"][2])
for k in ("barril", "cuello", "tambor", "banda", "visera", "remate"):
    x0, x1, z0, z1 = E[k]; caja(a, x0, x1, z0, z1)
    cota_h(a, x0, x1, z1 + 0.4, k); cota_v(a, x1 + 1.0, z0, z1, "")
cota_h(a, r0, r1, -1.5, "restaurante"); cota_h(a, c0, c1, -3.0, "columna"); cota_h(a, h0, h1, -1.5, "hotel"); cota_h(a, v0, v1, -3.0, "muro relieve")
cota_v(a, r0 - 1.5, 0, E["pb_top"], "PB"); cota_v(a, r0 - 1.5, E["pb_top"], E["p1_top"], "P1")
cota_v(a, v1 + 2, 0, E["remate"][3], "total")
a.set_xlim(-26, 30); a.set_ylim(-5, 54); a.set_aspect("equal"); a.grid(True, lw=0.2)
a.set_title("ALZADO DEL CHAFLÁN dibujado con medidas de F09 (m). Discontinuo = planta baja hundida", fontsize=10, loc="left")
# --- foto escalada a metros con las mismas lineas ---
im = np.asarray(Image.open(I+"9.webp").convert("L")); H, W = im.shape
b.imshow(im, cmap="gray", extent=(mx(0), mx(W), m(H), m(0)))
for k in ("barril", "cuello", "tambor", "banda", "visera", "remate"):
    x0, x1, z0, z1 = E[k]; caja(b, x0, x1, z0, z1, color="red")
for (x0, x1) in (E["rest"], E["hotel"], E["relieve"]):
    caja(b, x0, x1, E["pb_top"], E["p1_top"], color="red")
b.set_xlim(-26, 30); b.set_ylim(-5, 54); b.set_aspect("equal"); b.grid(True, lw=0.2)
b.set_title("F09 escalada a metros con el alzado encima (rojo): comprobación", fontsize=10, loc="left")
fig.savefig("ALZADO_01_chaflan_desde_F09.png", dpi=85)
for k, v in E.items(): print(k, np.round(v, 1))
