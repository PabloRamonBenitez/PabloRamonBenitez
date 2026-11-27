"""DUDA 8 – colocación de los 10 lucernarios piramidales del bloque alto (usuario 27/11: «los colocas como te sale del huevo; solo
se ven bien en la histórica, en perspectiva, y se ven distintos»). Solo se ven en F01, en escorzo y con ≈ 17 px por pirámide:
la forma (pirámides) es segura, la colocación no. Se presentan la foto ampliada con cada pirámide numerada y tres hipótesis en planta."""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
from PIL import Image, ImageEnhance
import edificio as E, laminas as LM
import traduccion
traduccion.ACTIVO = False                                  # hoja de trabajo: en español

V = E._v
B, S = V["PIR_B"], V["PIR_S"]
fig = plt.figure(figsize=(16.5, 11.7))
fig.suptitle("DUDA 8 – ¿Cómo están colocados los 10 lucernarios piramidales del bloque alto?  (solo se ven en F01, 1984)",
             fontsize=14, weight="bold", x=0.02, ha="left", y=0.975)
# 1) F01 ampliada (×5) con las pirámides numeradas
X0, Y0, X1, Y1, K = 0, 430, 260, 560, 5
im = Image.open(LM.IMG + "1.webp").convert("RGB").crop((X0, Y0, X1, Y1))
im = ImageEnhance.Contrast(im).enhance(1.4).resize(((X1 - X0) * K, (Y1 - Y0) * K), Image.BICUBIC)
a = fig.add_axes([0.02, 0.40, 0.56, 0.52]); a.imshow(im); a.axis("off")
a.set_title("F01 (1984) ampliada ×5. Puntos = vértices que se distinguen (aprox.): unas 10 pirámides de base cuadrada, alto ≈ ancho",
            fontsize=9, loc="left")
apices = [(31.7, 499.2), (40.8, 494.6), (50.0, 512.0), (54.2, 489.2), (65.8, 492.5), (66.7, 507.9), (78.3, 498.3), (90.0, 492.5),
          (99.2, 488.3), (109.2, 485.8)]                       # coordenadas en F01 (px), leídas en la ampliación ×12
for i, (x, y) in enumerate(apices, 1):
    px, py = (x - X0) * K, (y - Y0) * K
    a.plot(px, py, "o", ms=9, mfc="none", mec="red", mew=1.6)
    a.text(px + 6, py - 12, str(i), color="red", fontsize=10, weight="bold")
a.annotate("muro de ladrillo del colindante", (150, 120), (40, 30), color="white", fontsize=9, arrowprops=dict(arrowstyle="-", color="white"))
a.annotate("borde de la cubierta del bloque alto", (700, 462), (620, 600), color="black", fontsize=9, arrowprops=dict(arrowstyle="-", color="black"))
a.annotate("barandilla del fondo", (800, 222), (760, 120), color="white", fontsize=9, arrowprops=dict(arrowstyle="-", color="white"))
fig.text(0.02, 0.37, "Lo que es seguro: son PIRÁMIDES de base cuadrada (≈ 1,3 m de lado, ≈ 1,2 m de alto), unas 10, en una banda pegada al pie del muro\n"
         "del colindante. Lo que no se puede asegurar con 17 px por pirámide: si la banda va paralela a la medianera o a la calle, ni cómo se reparten\n"
         "las 5 + 5 («5 en línea y 5 en una distribución no aleatoria pero distinta», usuario 26/11). Por eso no la fijo: elige una de las tres.",
         fontsize=10, va="top")

# 2) tres hipótesis en planta (cubierta del bloque alto; x desde la medianera, y desde la calle)
poli = [(-V["L_C"], -V["VOL_V"]), (-V["L_C"] + V["VOL_L"], -V["VOL_V"]), (-8.0, 7.0), (-8.2, V["W_C"]), (-V["L_C"], V["W_C"])]
poli = [(x + V["L_C"], y) for x, y in poli]


def pir(ax, c):
    x, y = c; h = B / 2
    q = [(x - h, y - h), (x + h, y - h), (x + h, y + h), (x - h, y + h)]
    ax.add_patch(Polygon(q, closed=True, fc="white", ec="k", lw=0.9))
    ax.plot([q[0][0], q[2][0]], [q[0][1], q[2][1]], color="k", lw=0.5); ax.plot([q[1][0], q[3][0]], [q[1][1], q[3][1]], color="k", lw=0.5)


x1 = 0.6 + B / 2
H = {"H1 · 2 filas PARALELAS A LA MEDIANERA, a tresbolillo (provisional)":
         [(x1, 0.9 + S * i) for i in range(5)] + [(x1 + S, 0.9 + S / 2 + S * i) for i in range(5)],
     "H2 · banda en DIAGONAL desde la esquina medianera–calle":
         [(x1 + S * i * 0.55, 0.3 + S * i * 0.83) for i in range(5)] + [(x1 + S * 0.8 + S * (i + 0.5) * 0.55, 0.3 - S * 0.5 + S * (i + 0.5) * 0.83) for i in range(5)],
     "H3 · 2 filas PARALELAS A LA CALLE, junto al peto":
         [(x1 + 1.7 * i, 0.8) for i in range(5)] + [(x1 + 0.85 + 1.7 * i, 2.5) for i in range(5)]}
for k, (t, pts) in enumerate(H.items()):
    ax = fig.add_axes([0.60 + 0.0, 0.66 - k * 0.30, 0.38, 0.27]); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Polygon(poli, closed=True, fc="white", ec="k", lw=1.4))
    ax.add_patch(Rectangle((-6, -2.5), 6, V["W_C"] + 3.5, fc="white", ec="k", hatch="////", lw=0.6))
    ax.plot([-6, 18], [-2.5, -2.5], color="k", lw=0.6)
    ax.text(-3, 5.5, "COLINDANTE", rotation=90, ha="center", va="center", fontsize=7, bbox=dict(fc="white", ec="none", pad=1))
    ax.text(8, -3.8, "calle Ivana Mazepy", ha="center", fontsize=7)
    ax.text(0.2, V["W_C"] + 0.4, "medianera", fontsize=6.5)
    for c in pts: pir(ax, c)
    ax.set_xlim(-6.5, 17.5); ax.set_ylim(-5, V["W_C"] + 1.5)
    ax.set_title(t, fontsize=8.5, loc="left")
    ax.plot([13, 17], [-4.6] * 2, color="k", lw=1.2); ax.text(15, -4.4, "4 m", ha="center", va="bottom", fontsize=6.5)
fig.text(0.02, 0.22, "PREGUNTA: ¿cuál de las tres se parece a lo que ves en F01 (H1, H2, H3) o cómo es? Si conoces otra foto de esa cubierta, mándamela.\n"
         "Hasta que contestes, el modelo lleva H1 marcada como provisional (zona Z34 y ORDENES E14).", fontsize=11, weight="bold", va="top")
fig.savefig("DUDA8_LUCERNARIOS.png", dpi=110); print("ok")
