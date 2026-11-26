"""DUDA 7: la coronación inclinada de la escalera, proyectada en F09 (vista 320°, chaflán de frente, 12,9 px/m),
asoma a la derecha de la visera; en la foto hay cielo. Hipótesis A/B/C con planta."""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Polygon
from PIL import Image
import edificio as E, laminas as LM

V = E._v; T = np.array(E.T); R = "#d00000"
e = lambda d: np.array([math.cos(math.radians(d)), math.sin(math.radians(d))])
K, Y17, XT = 12.9, 571.5, 307.0
m = E.edificio()


def puntos_corona(m, az_min=60, az_max=120):
    out = []
    for zc in np.arange(38.9, 41.65, 0.15):
        for poly in m.slice(zc).to_polygons():
            for p in poly:
                q = np.array(p) - T; r = np.hypot(*q); az = math.degrees(math.atan2(q[1], q[0])) % 360
                if r > E.R_T + 0.3 and az_min <= az <= az_max: out.append((q, zc))
    return out


pc = puntos_corona(m)
fig = plt.figure(figsize=(24, 12))
fig.suptitle("DUDA 7 – la coronación de la escalera vista desde F09: el modelo la hace asomar a la derecha de la visera, la foto muestra cielo",
             fontsize=14, x=0.02, ha="left", weight="bold")
im = Image.open(LM.IMG + "9.webp").convert("RGB")
ax = fig.add_axes([0.02, 0.06, 0.40, 0.84]); box = (230, 150, 520, 380)
ax.imshow(im.crop(box), extent=(box[0], box[2], box[3], box[1])); ax.axis("off")
xs = [XT + (q @ e(50)) * K for q, z in pc]; ys = [Y17 - (z - 17.0) * K for q, z in pc]
ax.scatter(xs, ys, s=4, color=R, alpha=0.6, label="coronación del modelo proyectada (az 80–100°)")
for nom, r_, off, z0, z1, col in (("visera", E.R_V, (V["OV_X"], V["OV_Y"]), E.Z_G1, E.Z_V1, "#1a6fdb"),
                                  ("banda", E.R_G, (V["OB_X"], V["OB_Y"]), E.Z_T1 - V["H_PT"], E.Z_G1, "#1a9b4b")):
    c = np.array(E.P(*off)) - T; u0 = c @ e(50)
    for s_ in (-1, 1):
        ax.plot([XT + (u0 + s_ * r_) * K] * 2, [Y17 - (z0 - 17) * K, Y17 - (z1 - 17) * K], color=col, lw=2)
    ax.text(XT + (u0 + r_) * K + 3, Y17 - (z1 - 17) * K, nom + " (modelo)", color=col, fontsize=9, weight="bold")
ax.set_xlim(box[0], box[2]); ax.set_ylim(box[3], box[1]); ax.legend(loc="lower left", fontsize=9)
ax.set_title("F09 con el modelo proyectado (misma escala y eje que el collage): los puntos rojos caen sobre el cielo", fontsize=10, loc="left", weight="bold")
# planta
a2 = fig.add_axes([0.44, 0.06, 0.28, 0.84]); a2.set_aspect("equal"); a2.axis("off")
a2.add_patch(Circle((0, 0), E.R_T, fill=False, ec="k", lw=1.2)); a2.add_patch(Circle((0, 0), E.R_B, fill=False, ec="k", lw=0.5, ls="--"))
cv = np.array(E.P(V["OV_X"], V["OV_Y"])) - T; a2.add_patch(Circle(cv, E.R_V, fill=False, ec="#1a6fdb", lw=1))
q = np.array([p for p, z in pc]); a2.scatter(q[:, 0], q[:, 1], s=2, color=R)
for az, nom in ((320, "F09 (320°)"), (V["VISTA_ALAMY"], "Alamy (179,7°)")):
    p = e(az) * 24; a2.annotate(nom, (0, 0), p, arrowprops=dict(arrowstyle="<-", lw=1), fontsize=9, ha="center")
    rr = e(az + 90); a2.plot([-rr[0] * 20, rr[0] * 20], [-rr[1] * 20, rr[1] * 20], color="0.6", lw=0.6, ls=":")
a2.add_patch(Wedge((0, 0), 17.5, 95, 101, fc="none", ec="#e08000", lw=2, hatch="////"))
a2.text(-9, 19, "B: muro de coronación en el lado\nque mira a la plaza (az ≈ 98°)", color="#e08000", fontsize=9)
a2.text(9, 13, "modelo: muro en el lado izq.\n(az 80–82°, mirando la escalera)", color=R, fontsize=9)
a2.set_xlim(-22, 24); a2.set_ylim(-22, 24)
a2.set_title("Planta (eje de la torre en el origen)", fontsize=10, loc="left", weight="bold")
a3 = fig.add_axes([0.74, 0.06, 0.25, 0.84]); a3.axis("off")
a3.text(0, 1, "DUDA 7 · ¿DÓNDE ESTÁ EL MURO INCLINADO DE LA CORONACIÓN?\n\n"
        "Alamy ve la coronación en el borde izquierdo (lateral −15,3,\n+40,6 → +41,7): eso fija UNA coordenada, no la planta.\n"
        "F09 (chaflán de frente, 320°) es la segunda vista:\nallí, a la derecha de la visera, hay cielo.\n\n"
        "A · El muro está donde está (az 80–82°) y F09 no mira\n     desde 320° sino desde ≈ 300°.\n"
        "     → habría que recalcular los desplazamientos de\n     visera, banda y remate (todos salen de F09 = U).\n"
        "     En contra: en F09 el chaflán se ve de frente.\n\n"
        "B · El muro está en el otro lado de la cuña (az ≈ 98°,\n     el que mira a la plaza). Alamy lo ve igual (lateral −15,3)\n"
        "     y F09 lo tapa la visera.\n     En contra: en la foto de frente de la escalera lo\n     marcaste en el lado izquierdo.\n\n"
        "C · La coronación es más baja o más corta de lo que\n     sale de Alamy (no llega a r 16 por encima de +40,6).\n\n"
        "PREGUNTA: ¿A, B o C? Con B no cambia nada más.\n"
        "Probable: B (dos vistas lo cumplen sin tocar el resto).", fontsize=10.5, va="top")
fig.savefig("DUDA7_ESCALERA_F09.png", dpi=75)
print("ok", len(pc))
