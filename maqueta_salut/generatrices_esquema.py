"""Alturas de la parte alta leídas en la foto de Alamy SOBRE LA GENERATRIZ FRONTAL DE CADA CILINDRO.

En un cilindro visto casi en alzado, la única vertical en verdadera magnitud es la generatriz más cercana a la cámara,
que en la foto cae en el centro de su silueta. Como los cilindros no son coaxiales (banda, visera y remate están
desplazados), hay un «origen» por cilindro: cada altura se mide sobre la vertical de su propio cilindro.

Escalas (foto alamy.jpg, recorte desde y0 = 0,22·H):
  vertical   56,5 px/m  (paso de forjados del barril: 175 px = 3,10 m; bordes de losa 1306 → 1482)
  horizontal 64,4 px/m  (foto de pantalla deformada; diámetros: visera 23,4 · banda 18,9 · remate 9,5 m)
  referencia: cara superior del canto de la losa de cubierta del barril (y = 1306) = Z_B1 + 0,65 = +33,15 (la cara inferior, y = 1337, es +32,50);
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

V = E._v
FOTO = sys.argv[1] if len(sys.argv) > 1 else "/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/scratchpad/alamy.jpg"
PV, PH = 175 / 3.10, 64.4
Y_REF, Z_REF = 1306, E.Z_B1 + 0.65   # cara SUPERIOR del canto de la losa de cubierta del barril (canto 0,65; cara inferior y = 1337)
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
    "tambor": (0.0, E.Z_B1 + 0.65, E.Z_T1, V["R_T"]),
    "banda":  (-V["OB_Y"], E.Z_T1 - V["H_PT"], E.Z_G1, V["R_G"]),
    "visera": (-V["OV_Y"], E.Z_G1, E.Z_V1, V["R_V"]),
    "remate": (-V["OR_Y"], E.Z_V1, E.Z_R1, V["R_R"]),
}
foto_lat = {k: s(c["c"]) for k, c in CIL.items()}
im = Image.open(FOTO).convert("RGB"); W, H = im.size; y0 = int(H * 0.22)
crop = im.crop((0, y0 + 150, W, y0 + 1560))
ext = (s(0), s(W), z(1560), z(150))
fig, (a1, a2) = plt.subplots(1, 2, figsize=(19, 10.5), sharey=True, gridspec_kw=dict(wspace=0.04))
a1.imshow(crop, extent=ext, aspect="auto")
for k, (sl, z0, z1, r) in mod.items():
    col = CIL[k]["col"]
    a2.add_patch(Rectangle((sl - r, z0), 2 * r, z1 - z0, fc=col, alpha=0.12, ec=col, lw=1.2))
a2.add_patch(Rectangle((-V["R_B"], E.Z_B1 - 3 * E.F), 2 * V["R_B"], 3 * E.F, fc="0.92", ec="0.4", lw=0.8))
for i in range(4):
    a2.plot([-V["R_B"], V["R_B"]], [E.Z_B1 - i * E.F] * 2, color="0.4", lw=0.6)
a2.text(0, E.Z_B1 - 1.5, "barril (paso 3,10)", ha="center", fontsize=7, color="0.3")
rows = []
for k, cdat in CIL.items():
    col = cdat["col"]; xf = foto_lat[k]; xm = mod[k][0]
    zf0, zf1 = z(cdat["base"]), z(cdat["top"]); _, zm0, zm1, _ = mod[k]
    for ax, x, za, zb in ((a1, xf, zf0, zf1), (a2, xm, zm0, zm1)):
        ax.plot([x, x], [za, zb], color=col, lw=2.4, solid_capstyle="butt", zorder=5)
        for zz in (za, zb):
            ax.plot([x - 0.7, x + 0.7], [zz, zz], color=col, lw=2.4, zorder=5)
    a1.text(xf + 0.8, zf1 + 0.15, f"{k}\n+{zf1:.2f}".replace(".", ","), color=col, fontsize=8, weight="bold", va="bottom")
    a2.text(xm + 0.8, zm1 + 0.15, f"{k}\n+{zm1:.2f}".replace(".", ","), color=col, fontsize=8, weight="bold", va="bottom")
    for ax in (a1, a2):
        ax.axhline(zf1, color=col, lw=0.7, ls="--", alpha=0.8)
    rows.append((k, xf, xm, zf1 - zf0, zm1 - zm0, zf1, zm1))
zl0, zl1 = z(LUC["base"]), z(LUC["top"])
a1.plot([s(LUC["c"])] * 2, [zl0, zl1], color="purple", lw=2)
a1.text(s(LUC["c"]) + 0.5, zl1, f"lucernario +{zl1:.2f}".replace(".", ","), color="purple", fontsize=7)
for ax, t in ((a1, "FOTO (Alamy) – cada altura leída sobre la generatriz frontal de SU cilindro"),
              (a2, "MODELO actual – mismos orígenes: centro de cada cilindro en la vista")):
    ax.set_title(t, fontsize=10, loc="left", weight="bold")
    ax.axvline(0, color="0.5", lw=0.5, ls=":")
    ax.set_xlim(-17, 17); ax.set_ylim(29, 52); ax.set_aspect("equal")
    ax.set_xlabel("m en horizontal desde el eje del tambor (derecha de la foto = hacia la plaza, −N)", fontsize=8)
a1.set_ylabel("cota (m)")
txt = ["cilindro   desplaz. foto / modelo   altura foto / modelo   coronación foto / modelo"]
for k, xf, xm, hf, hm, zf, zm in rows:
    txt.append(f"{k:8s}   {xf:+5.1f} / {xm:+5.1f} m          {hf:4.2f} / {hm:4.2f} m          +{zf:5.2f} / +{zm:5.2f}")
txt.append(f"lucernario  altura {zl1 - zl0:.2f} / {V['LUC_H']:.2f} m · punta +{zl1:.2f}")
fig.text(0.06, 0.015, "\n".join(txt).replace(".", ","), family="monospace", fontsize=8.5, va="bottom")
fig.suptitle("Parte alta: un origen por cilindro (generatriz frontal = centro de la silueta). Escala vertical 56,5 px/m por el paso de forjados; "
             "referencia: cara superior del canto de la losa de cubierta del barril +33,15", fontsize=11, x=0.06, ha="left")
fig.subplots_adjust(bottom=0.2, top=0.92, left=0.05, right=0.99)
fig.savefig("GENERATRICES_ESQUEMA.png", dpi=80)
