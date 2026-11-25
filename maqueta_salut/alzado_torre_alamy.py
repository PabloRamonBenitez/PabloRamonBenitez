"""ALZADO DE LA TORRE – código de la verdad: foto de Alamy medida por MGF.

Cada cilindro se mide en su generatriz frontal (rojo remate, amarillo visera, azul banda, verde tambor) y el barril
en la vertical de medida del usuario (celeste, x ≈ 1186 px). Referencia: cara inferior de la losa de cubierta del barril
(y = 1337) = +32,50. Escala vertical 56,53 px/m (5 forjados, paso 175,25 px); horizontal 64,4 px/m.
Salidas: ALZADO_TORRE_ALAMY.png (lámina) y, en la carpeta de imágenes de los planos, alamy_torre.png / alamy_alto.png /
alamy_barril.png (la foto con sus líneas de medida, para sustituir a las fotos antiguas)."""
import math, sys, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import edificio as E
import laminas as LM
import vista_alamy as VA

V = E._v
FOTO = sys.argv[1] if len(sys.argv) > 1 else "/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/scratchpad/alamy.jpg"
PV, PH = 175.25 / 3.10, 64.4
Y0 = 887                      # recorte de trabajo: y = Y_foto − 887
Y_REF, XT = 1337, 1078
z = lambda y: E.Z_B1 + (Y_REF - y) / PV
yv = lambda zz: Y_REF - (zz - E.Z_B1) * PV
s = lambda x: (x - XT) / PH

GEN = [  # (nombre, color, x generatriz px, [(y px, etiqueta)])
    ("remate", "#d43c3c", 1064, [(733, "visera sup."), (302, "remate")]),
    ("visera", "#e0a000", 1365, [(840, "visera inf."), (733, "visera sup.")]),
    ("banda", "#2a6fdb", 1255, [(985, "tambor"), (840, "visera inf.")]),
    ("tambor", "#1a9b4b", 1100, [(1306, "canto cub."), (985, "tambor")]),
]
X_BAR = 1186                  # vertical de medida del barril (usuario)
BAR = [1337, 1421, 1464, 1481, 1515, 1595, 1640, 1655, 1688, 1770, 1815, 1827, 1864, 1945, 1989, 2005, 2038]

im = Image.open(FOTO).convert("RGB"); W, H = im.size
crop = im.crop((0, Y0 + 150, W, Y0 + 2200))
ext = (s(0), s(W), z(2200), z(150))
XTm = VA.x_eje_alzado()


def lineas(ax, dx=0.0, foto=True):
    for nm, col, xg, pts in GEN:
        xs = s(xg) + dx
        ys = sorted(p[0] for p in pts)
        ax.plot([xs, xs], [z(ys[-1]), z(ys[0])], color=col, lw=2.2, zorder=30)
        for y, et in pts:
            ax.plot([xs - 0.5, xs + 0.5], [z(y)] * 2, color=col, lw=2.2, zorder=30)
        h = z(ys[0]) - z(ys[-1])
        ax.text(xs + 0.6, (z(ys[0]) + z(ys[-1])) / 2, f"{h:.2f}".replace(".", ","), color=col, fontsize=8, weight="bold",
                va="center", zorder=31, bbox=dict(fc="white", ec="none", alpha=0.75, pad=0.4))
    xb = s(X_BAR) + dx
    ax.plot([xb, xb], [z(BAR[-1]), z(1306)], color="#16b5e8", lw=2.2, zorder=30)
    for y in BAR + [1306]:
        ax.plot([xb - 0.35, xb + 0.35], [z(y)] * 2, color="#16b5e8", lw=1.6, zorder=30)
    for ya, yb, t in ((1306, 1337, "canto"), (1337, 1421, "hueco"), (1421, 1464, "poyete"), (1464, 1481, "ranura")):
        ax.text(xb + 0.5, (z(ya) + z(yb)) / 2, f"{t} {(yb - ya) / PV:.2f}".replace(".", ","), color="#0b7fa6", fontsize=6.5, va="center", zorder=31,
                bbox=dict(fc="white", ec="none", alpha=0.7, pad=0.2))


fig, (a1, a2) = plt.subplots(1, 2, figsize=(22, 13), sharey=True, gridspec_kw=dict(wspace=0.03))
LM.alzado(a1, VA.MIRA, "")
lineas(a1, dx=XTm)
a1.set_xlim(XTm - 20, XTm + 24)
a1.set_title("MODELO – alzado de la torre en la dirección de Alamy (179,7°), sin perspectiva", fontsize=10, loc="left", weight="bold")
a2.imshow(crop, extent=ext, aspect="auto")
lineas(a2)
a2.set_xlim(-20, 24)
a2.set_title("ALAMY – medida por generatrices (código de la verdad)", fontsize=10, loc="left", weight="bold")
niveles = [(E.Z_R1, "remate"), (E.Z_V1, "visera sup."), (E.Z_G1, "visera inf. / banda"), (E.Z_T1, "tambor"), (V["OJO_Z"], "centro ojos"),
           (E.Z_B1 + V["FOR_C"], "canto cubierta"), (E.Z_B1, "cubierta barril")] + [(E.Z_B1 - i * E.F, f"forjado {6 - i}") for i in range(1, 5)]
for ax in (a1, a2):
    ax.set_ylim(z(2200), z(150)); ax.set_aspect("equal")
    for zz, t in niveles:
        ax.axhline(zz, color="0.35", lw=0.5, ls=":", zorder=25)
a2.yaxis.set_tick_params(labelleft=True)
for zz, t in niveles:
    a2.text(24.3, zz, f"+{zz:.2f} {t}".replace(".", ","), fontsize=7, va="center")
fig.text(0.02, 0.012,
         ("Referencia: cara inferior de la losa de cubierta del barril (y = 1337 px) = +32,50 · 56,53 px/m vertical (5 forjados, paso 175,25 px) · 64,4 px/m horizontal\n"
          f"Barril (vertical celeste): canto {V['FOR_C']:.2f} · hueco 1,45 · poyete {V['FOR_P']:.2f} · ranura {V['FOR_R']:.2f} · forjados +32,50 / 29,35 / 26,29 / 23,17 / 20,09 (modelo 32,5 / 29,4 / 26,3 / 23,2 / 20,1)\n"
          f"Vista {V['VISTA_ALAMY']}° (cuña de la escalera en el borde izquierdo) · ojos {sum(1 for h in __import__('ventanas').catalogo() if h['grupo'] == 'tambor ojos')} (lado ciego {V['OJO_C0']:.0f}°–{V['OJO_C1']:.0f}°), Ø {V['OJO_D']:.2f}, tubo {V['OJO_V']:.2f}, centro +{V['OJO_Z']:.2f} · 19 muros, giro {V['FASE_AL']}°, hueco de escalera {V['ESC_SEC']}° (2 módulos)").replace(".", ","),
         fontsize=9, va="bottom")
fig.suptitle("ALZADO DE LA TORRE – medido sobre Alamy por generatrices frontales (MGF)", fontsize=13, x=0.02, ha="left", weight="bold")
fig.subplots_adjust(bottom=0.08, top=0.95, left=0.03, right=0.95)
fig.savefig("ALZADO_TORRE_ALAMY.png", dpi=75)

# ---- imágenes de comprobación para las láminas (sustituyen a las fotos antiguas)
for nombre, (ya, yb) in (("alamy_torre.png", (150, 2200)), ("alamy_alto.png", (150, 1400)), ("alamy_barril.png", (1250, 2200))):
    f, ax = plt.subplots(figsize=(8, 8 * (yb - ya) / W * 1.0 * PH / PV + 0.3))
    c = im.crop((0, Y0 + ya, W, Y0 + yb))
    ax.imshow(c, extent=(s(0), s(W), z(yb), z(ya)), aspect="auto")
    lineas(ax)
    ax.set_xlim(s(0), s(W)); ax.set_ylim(z(yb), z(ya)); ax.set_aspect("equal"); ax.axis("off")
    f.savefig(os.path.join(LM.IMG, nombre), dpi=110, bbox_inches="tight", pad_inches=0.02); plt.close(f)
print("ok")
