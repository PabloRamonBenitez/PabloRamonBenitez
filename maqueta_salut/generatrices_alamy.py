"""Alturas de la parte alta leídas en la foto de Alamy SOBRE LA GENERATRIZ FRONTAL DE CADA CILINDRO.

En un cilindro visto casi en alzado, la única vertical en verdadera magnitud es la generatriz más cercana a la cámara,
que en la foto cae en el centro de su silueta. Como los cilindros no son coaxiales (banda, visera y remate están
desplazados), hay un «origen» por cilindro: cada altura se mide sobre la vertical de su propio cilindro.

Escalas (foto alamy.jpg, recorte desde y0 = 0,22·H):
  vertical   56,5 px/m  (paso de forjados del barril: 175 px = 3,10 m; bordes de losa 1306 → 1482)
  horizontal 64,4 px/m  (foto de pantalla deformada; diámetros: visera 23,4 · banda 18,9 · remate 9,5 m)
  referencia: cara superior del canto de la losa de cubierta del barril (y = 1306) = Z_B1 + 0,65 = +32,50 (cara inferior de la losa de cubierta) (la cara inferior, y = 1337, es +32,50);
              comprobación independiente: coronación del tambor 5,68 m más arriba = +38,18 (F09: +38,20).
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
from PIL import Image
import edificio as E
import vista_alamy as VA

V = E._v
FOTO = sys.argv[1] if len(sys.argv) > 1 else "/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/scratchpad/alamy.jpg"
PV, PH = 175.25 / 3.10, 64.4
Y_REF, Z_REF = 1337, E.Z_B1          # cara INFERIOR de la losa de cubierta del barril (+32,50)
X_T = 1078                            # centro del tambor (borde derecho 1950 − R_T·PH; borde izquierdo visible ≈ 210)

z = lambda y: Z_REF + (Y_REF - y) / PV
s = lambda x: (x - X_T) / PH          # + a la derecha de la foto = −N

# centros de silueta (px) y bordes leídos SOBRE la generatriz de cada cilindro (px)
CIL = {
    "tambor": dict(c=1078, col="#1a9b4b", base=1306, top=985),
    "banda":  dict(c=1255, col="#2a6fdb", base=985, top=840),     # base visible = coronación del tambor (peto)
    "visera": dict(c=1365, col="#e0a000", base=840, top=733),
    "remate": dict(c=1064, col="#d43c3c", base=733, top=302),
}
LUC = dict(c=1615, base=728, top=625)
mod = {  # modelo: (desplazamiento lateral en la vista = −N, z0, z1, radio)
    "tambor": (0.0, E.Z_B1 + V["FOR_C"], E.Z_T1, V["R_T"]),
    "banda":  (VA.lat(E.P(V["OB_X"], V["OB_Y"])), E.Z_T1 - V["H_PT"], E.Z_G1, V["R_G"]),
    "visera": (VA.lat(E.P(V["OV_X"], V["OV_Y"])), E.Z_G1, E.Z_V1, V["R_V"]),
    "remate": (VA.lat(E.P(V["OR_X"], V["OR_Y"])), E.Z_V1, E.Z_R1, V["R_R"]),
}
foto_lat = {k: s(c["c"]) for k, c in CIL.items()}
# bordes de silueta en la foto (px) → diámetros medidos a la altura de cada cilindro
SIL = {"tambor": (210, 1950, 1150), "banda": (647, 1864, 920), "visera": (612, 2118, 790), "remate": (757, 1371, 650)}

import math
import laminas as LM
XT = VA.x_eje_alzado()      # eje de la torre en el alzado del modelo (vista de Alamy)

im = Image.open(FOTO).convert("RGB"); W, H = im.size; y0 = int(H * 0.22)
crop = im.crop((0, y0 + 150, W, y0 + 1560))
ext = (XT + s(0), XT + s(W), z(1560), z(150))

fig, (a2, a1) = plt.subplots(1, 2, figsize=(22, 11), sharey=True, gridspec_kw=dict(wspace=0.03))
LM.alzado(a2, VA.MIRA, "")
a1.imshow(crop, extent=ext, aspect="auto")

def cota_v(ax, x, za, zb, col, lado=1):
    ax.plot([x, x], [za, zb], color=col, lw=2.2, zorder=20)
    for zz in (za, zb):
        ax.plot([x - 0.5, x + 0.5], [zz, zz], color=col, lw=2.2, zorder=20)
    ax.text(x + lado * 0.6, (za + zb) / 2, f"{zb - za:.2f}".replace(".", ","), color=col, fontsize=9, weight="bold",
            ha="left" if lado > 0 else "right", va="center", zorder=21,
            bbox=dict(fc="white", ec="none", alpha=0.75, pad=0.5))

def cota_h(ax, xa, xb, zz, col):
    ax.annotate("", (xa, zz), (xb, zz), arrowprops=dict(arrowstyle="<->", color=col, lw=1.1), zorder=20)
    ax.text((xa + xb) / 2, zz + 0.12, f"Ø {xb - xa:.1f}".replace(".", ","), color=col, fontsize=8, ha="center", va="bottom",
            zorder=21, bbox=dict(fc="white", ec="none", alpha=0.7, pad=0.3))

rows = []
for k, cdat in CIL.items():
    col = cdat["col"]
    sl, zm0, zm1, r = mod[k]
    xf, xm = XT + foto_lat[k], XT + sl
    zf0, zf1 = z(cdat["base"]), z(cdat["top"])
    l, rr, yy = SIL[k]; df = (rr - l) / PH
    lado = -1 if k == "remate" else 1
    # foto
    cota_v(a1, xf, zf0, zf1, col, lado)
    cota_h(a1, XT + s(l), XT + s(rr), z(yy), col)
    # modelo
    cota_v(a2, xm, zm0, zm1, col, lado)
    zh = (zm0 + zm1) / 2 if k != "tambor" else zm0 + 1.0
    cota_h(a2, xm - r, xm + r, z(yy) if k != "banda" else zh, col)
    for ax in (a1, a2):
        ax.plot([xf, xf] if ax is a1 else [xm, xm], [28, 52], color=col, lw=0.6, ls=":", zorder=19)
        ax.axhline(zf1, color=col, lw=0.8, ls="--", zorder=18)
        ax.text(23.5, zf1, f"foto +{zf1:.2f}".replace(".", ","), color=col, fontsize=7.5, va="bottom", ha="right")
    a2.text(23.5, zm1, f"modelo +{zm1:.2f}".replace(".", ","), color=col, fontsize=7.5, va="top", ha="right")
    rows.append((k, foto_lat[k], sl, zf1 - zf0, zm1 - zm0, zf1, zm1, df, 2 * r))
zl0, zl1 = z(LUC["base"]), z(LUC["top"])
cota_v(a1, XT + s(LUC["c"]), zl0, zl1, "purple")
for ax, t in ((a2, "MODELO – alzado desde −U (proyección sin perspectiva); verticales = centro de cada cilindro"),
              (a1, "ALAMY – cada altura sobre la generatriz frontal de SU cilindro (centro de su silueta)")):
    ax.set_title(t, fontsize=10, loc="left", weight="bold")
    ax.set_xlim(-20, 24); ax.set_ylim(29.5, 51.5); ax.set_aspect("equal")
a1.tick_params(labelleft=True)
hdr = "cilindro   eje (desde tambor)   altura visible        coronación           diámetro"
txt = [hdr, "           foto / modelo        foto / modelo         foto / modelo        foto / modelo"]
for k, xf, xm, hf, hm, zf, zm, df, dm in rows:
    txt.append(f"{k:8s}   {xf:+5.1f} / {xm:+5.1f}        {hf:4.2f} / {hm:4.2f}  ({hf - hm:+.2f})   +{zf:5.2f} / +{zm:5.2f}  ({zf - zm:+.2f})   {df:4.1f} / {dm:4.1f}")
txt.append(f"lucernario                      {zl1 - zl0:4.2f} / {V['LUC_H']:4.2f}")
txt.append("banda: en la foto solo se ve desde la coronación del tambor (peto); en el modelo arranca 1,0 m más abajo (pasillo).")
fig.text(0.05, 0.01, "\n".join(txt).replace(".", ","), family="monospace", fontsize=9, va="bottom")
fig.suptitle("Parte alta: un origen por cilindro. Foto a 56,5 px/m vertical (paso de forjados 175 px = 3,10 m) y 64,4 px/m horizontal; "
             "referencia: cara superior del canto de la losa de cubierta del barril +32,50 (cara inferior de la losa de cubierta) (comprobación independiente en F09, ajuste proyectivo con 7 forjados)", fontsize=11, x=0.05, ha="left")
fig.subplots_adjust(bottom=0.17, top=0.93, left=0.04, right=0.99)
fig.savefig("GENERATRICES_ALAMY.png", dpi=80)
for r in rows: print(r)
print("luc", zl0, zl1)

# ---- comprobación MGF: el modelo debe reproducir la foto (tolerancias: 0,10 m en cota, 0,15 m en eje y radio)
print("\nComprobación MGF (foto − modelo):")
ok = True
for k, xf, xm, hf, hm, zf, zm, df, dm in rows:
    r1, r2, r3 = zf - zm, xf - xm, (df - dm) / 2
    bien = abs(r1) <= 0.10 and abs(r2) <= 0.15 and abs(r3) <= 0.15
    ok &= bien
    print(f"  {k:7s} coronación {r1:+.2f}  eje {r2:+.2f}  radio {r3:+.2f}  {'OK' if bien else 'NO'}")
print("MGF:", "OK" if ok else "FALLA")
