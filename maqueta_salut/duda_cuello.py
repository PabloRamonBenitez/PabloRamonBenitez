"""Duda 1 – base del cuello: medida en F70, F14 y F09 con el paso de forjados de cada foto."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import laminas as LM, edificio as E

FOTOS = [  # (archivo, x eje, y cubierta barril (+32,50), px por 3,10 m, y borde inferior del cuello, título)
    ("70.webp", 470, 318, 69.5, 844, "F70 (1984, postal frontal)"),
    ("14.webp", 600, 236, 41.2, 548, "F14 (1984, desde la plaza)"),
]
fig, axs = plt.subplots(1, 3, figsize=(20, 9))
for ax, (f, x, y0, p, yc, t) in zip(axs, FOTOS):
    im = Image.open(LM.IMG + f).convert("RGB"); ax.imshow(im); ax.axis("off")
    k = p / 3.10
    for i in range(7):
        ax.plot([x - 60, x + 60], [y0 + i * p] * 2, color="#16b5e8", lw=1)
    ax.plot([x - 140, x + 140], [yc, yc], color="crimson", lw=2)
    z = 32.5 - (yc - y0) / k
    ax.text(x + 150, yc, f"borde inferior del cuello\n+{z:.2f} aparente".replace(".", ","), color="crimson", fontsize=9, va="center",
            bbox=dict(fc="white", ec="crimson"))
    ax.text(x + 70, y0, "+32,50 cubierta del barril", color="#0b7fa6", fontsize=8, va="center")
    ax.set_title(f"{t}: paso de forjados {p} px = 3,10 m", fontsize=10, loc="left")
im = Image.open(LM.IMG + "9.webp").convert("RGB"); axs[2].imshow(im); axs[2].axis("off")
axs[2].plot([150, 450], [676, 676], color="crimson", lw=2)
axs[2].text(460, 676, "+9,03 (ajuste con 7 forjados\ny corrección de profundidad)", color="crimson", fontsize=9, va="center", bbox=dict(fc="white", ec="crimson"))
axs[2].set_title("F09 (frontal actual)", fontsize=10, loc="left")
fig.suptitle(f"DUDA 1 – base del cuello: tres fotos coinciden en +9,0 / +9,4 → modelo +{E._v['Z_CU0']:.2f} (antes +10,40)".replace(".", ","),
             fontsize=13, x=0.01, ha="left", weight="bold")
fig.savefig("DUDA1_BASE_CUELLO.png", dpi=80, bbox_inches="tight")
print("ok")
