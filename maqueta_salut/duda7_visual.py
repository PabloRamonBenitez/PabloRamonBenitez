"""DUDA 7 en visual: cada opción (actual, A, B, C) proyectada sobre F09, sobre Alamy y comparada con la foto de frente de la
escalera; planta de cada opción. Rojo = coronación de la escalera según la opción. ✔/✘ = la foto lo admite o no."""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Rectangle, FancyArrow
from PIL import Image
import edificio as E, laminas as LM

V = E._v; T = np.array(E.T); R = "#d00000"; VE = "#1a9b4b"; AZ = "#1a6fdb"; NA = "#e08000"
e = lambda d: np.array([math.cos(math.radians(d)), math.sin(math.radians(d))])
SCR = "/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/scratchpad/"
m = E.edificio()
pc = []
for zc in np.arange(38.9, 41.65, 0.12):
    for poly in m.slice(zc).to_polygons():
        for p in poly:
            q = np.array(p) - T; r = np.hypot(*q); az = math.degrees(math.atan2(q[1], q[0])) % 360
            if r > E.R_T + 0.3 and 60 <= az <= 120: pc.append((q, zc))
espejo = lambda q: np.array([-q[0], q[1]])                 # simetría respecto al eje de la cuña (az 90° = +y)
OPC = [
 ("ACTUAL", "muro inclinado a la izquierda (az 80–82°), F09 desde 320°", 320, pc, "izq",
  "Así está hoy el modelo.\nF09: la coronación asoma sobre el cielo ✘"),
 ("A", "muro donde está (izquierda); F09 tomada desde ≈ 300° (no de frente al chaflán)", 300, pc, "izq",
  "Cumple las 4 fotos.\nCoste: se rehace lo que salía de F09 =\n· chaflán: X 12,8 → 13,6 · Y 10,1 → 10,8 (+6 %)\n· visera (−3,5, −2,7) · banda (−2,2, −1,6)\n  (hoy (−2,4, −4,1) y (−1,7, −2,3))"),
 ("B", "muro al otro lado de la cuña (az 98–100°, mirando a la plaza); F09 desde 320°", 320, [(espejo(q), z) for q, z in pc], "dcha",
  "F09 y Alamy bien.\nPero en la foto de frente el bloque\nestá a la IZQUIERDA (tus marcas) ✘"),
 ("C", "coronación más baja: no sube por encima del peto del tambor (+39,0)", 320, [(q, z) for q, z in pc if z <= 39.0], "izq",
  "F09 bien.\nPero Alamy mide la coronación de\n+40,6 a +41,7 (inclinada) ✘"),
]
VER = {"ACTUAL": ("✘", "✔", "✔"), "A": ("✔", "✔", "✔"), "B": ("✔", "✔", "✘"), "C": ("✔", "✘", "✔")}
f09 = Image.open(LM.IMG + "9.webp").convert("RGB")
ala = Image.open(SCR + "alamy.jpg").convert("RGB")
fte = Image.open(LM.IMG + "esc_frente_alta.png").convert("RGB")
BF, BA, BE = (330, 190, 520, 320), (0, 1600, 620, 1900), (250, 380, 1050, 950)
OFF_F09 = {320: {"visera": -2.37, "banda": -1.55}, 300: {"visera": -2.37, "banda": -1.55}}   # laterales medidos en F09


def marca(ax, ok, box):
    ax.text(box[2] - 8, box[1] + 8, ok, fontsize=34, ha="right", va="top", color=VE if ok == "✔" else R, weight="bold",
            bbox=dict(fc="white", ec="none", alpha=0.85, pad=2), zorder=50)


fig = plt.figure(figsize=(26, 25))
fig.suptitle("DUDA 7 – ¿dónde está la coronación inclinada de la escalera? Cada fila es una opción; rojo = la parte de la coronación que sale por fuera del tambor, según esa opción",
             fontsize=17, x=0.01, ha="left", weight="bold", y=0.995)
for j, t in enumerate(("F09 (teleobjetivo): ¿asoma algo a la\nderecha de la visera? En la foto: cielo",
                       "ALAMY: el extremo exterior de la coronación\nen el borde izquierdo (+40,6 → +41,7)",
                       "FOTO DE FRENTE DE LA ESCALERA (tus marcas):\n¿en qué lado está el bloque inclinado?", "PLANTA (eje de la torre)", "QUÉ IMPLICA")):
    fig.text(0.01 + j * 0.2, 0.962, t, fontsize=11.5, weight="bold", va="top")
H = 0.215
for i, (k, tit, beta, pts, lado, txt) in enumerate(OPC):
    y0 = 0.695 - i * 0.232
    fig.text(0.01, y0 + H + 0.005, f"{k} · {tit}", fontsize=13, weight="bold", color="k" if k != "ACTUAL" else R)
    vf, va, ve = VER[k]
    # F09
    ax = fig.add_axes([0.01, y0, 0.19, H]); ax.imshow(f09.crop(BF), extent=(BF[0], BF[2], BF[3], BF[1])); ax.axis("off")
    xs = [307 + (q @ e(beta + 90)) * 12.9 for q, z in pts]; ys = [571.5 - (z - 17.0) * 12.9 for q, z in pts]
    ax.scatter(xs, ys, s=5, color=R, alpha=0.7, zorder=10)
    for nom, r_, col in (("visera", E.R_V, AZ), ("banda", E.R_G, VE)):
        u = OFF_F09[beta][nom] + r_
        ax.axvline(307 + u * 12.9, color=col, lw=1.2, ls="--")
    ax.set_xlim(BF[0], BF[2]); ax.set_ylim(BF[3], BF[1]); marca(ax, vf, BF)
    # Alamy
    ax = fig.add_axes([0.205, y0, 0.19, H]); ax.imshow(ala.crop(BA), extent=(BA[0], BA[2], BA[3], BA[1])); ax.axis("off")
    D = e(V["VISTA_ALAMY"] + 90)
    xs = [1078 + (q @ D) * 64.4 for q, z in pts]; ys = [887 + 1337 - (z - 32.5) * 56.53 for q, z in pts]
    ax.scatter(xs, ys, s=5, color=R, alpha=0.6, zorder=10)
    ax.set_xlim(BA[0], BA[2]); ax.set_ylim(BA[3], BA[1]); marca(ax, va, BA)
    # frente
    ax = fig.add_axes([0.40, y0, 0.19, H]); ax.imshow(fte.crop(BE), extent=(BE[0], BE[2], BE[3], BE[1])); ax.axis("off")
    if lado == "izq": ax.add_patch(Rectangle((310, 470), 360, 260, fill=False, ec=R, lw=3, zorder=10))
    else: ax.add_patch(Rectangle((680, 470), 300, 260, fill=False, ec=R, lw=3, zorder=10))
    ax.text(310 if lado == "izq" else 680, 460, "muro según " + k, color=R, fontsize=10, weight="bold", va="bottom")
    ax.set_xlim(BE[0], BE[2]); ax.set_ylim(BE[3], BE[1]); marca(ax, ve, BE)
    # planta
    ax = fig.add_axes([0.60, y0, 0.17, H]); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Circle((0, 0), E.R_T, fill=False, ec="k", lw=1.2))
    ax.add_patch(Wedge((0, 0), E.ESC_R1, 90 - V["ESC_SECB"] / 2, 90 + V["ESC_SECB"] / 2, fc="0.88", ec="k", lw=0.6))
    q = np.array([p for p, z in pts]) if pts else np.zeros((0, 2))
    if len(q): ax.scatter(q[:, 0], q[:, 1], s=2, color=R)
    for az_, nom in ((beta, f"F09 ({beta}°)"), (V["VISTA_ALAMY"], "Alamy")):
        p = e(az_) * 21; ax.annotate(nom, (0, 0), p, arrowprops=dict(arrowstyle="<-", lw=1), fontsize=9, ha="center")
    ax.text(0, 17.5, "escalera", ha="center", fontsize=8)
    ax.set_xlim(-24, 24); ax.set_ylim(-20, 22)
    # texto
    fig.text(0.79, y0 + H - 0.01, txt, fontsize=11.5, va="top")
fig.text(0.01, 0.022, "RECUENTO: ACTUAL 2/3 · A 3/3 · B 2/3 · C 2/3. Solo A cumple todas las fotos; su coste es rehacer lo que se midió en F09 suponiéndola de frente al chaflán (+6 %).", fontsize=13, weight="bold")
fig.text(0.01, 0.006, "Escalas: F09 12,9 px/m y vista desde el ángulo de cada opción; Alamy 64,4 / 56,5 px/m (como el collage). "
         "Líneas a trazos en F09: borde derecho de visera (azul) y banda (verde) medidos en la foto.", fontsize=10)
fig.savefig("DUDA7_VISUAL.png", dpi=62)
print("ok")
