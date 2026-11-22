"""Comparacion en serie: alzados del modelo (metros) superpuestos sobre fotos casi frontales escaladas a metros,
y planta del modelo superpuesta sobre la vista de Bing. Cada hoja lleva una tabla de cotas medidas en la foto."""
import math, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image
import planimetria as PL
import salut_v2 as s

I = '/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'

# --- calibracion metrica de cada foto (lectura de rejilla): eje de la torre (px x), suelo (px y), px por metro ---
#     escala: puntas de aletas del barril = 2*(R_B+0.9) m
D_ALETAS = 2 * (s.R_B + 0.9)
FOTOS = {
    "F09": dict(f="9.webp", x_eje=303.5, y_suelo=795, px_m=397 / D_ALETAS, titulo="F09 frontal (teleobjetivo)"),
    "F14": dict(f="14.webp", x_eje=584, y_suelo=700, px_m=432 / D_ALETAS, titulo="F14 epoca, desde la plaza"),
}


def alzado_sobre_foto(ax, k, d, titulo):
    c = FOTOS[k]
    im = np.asarray(Image.open(I + c["f"]).convert("L"))
    H, W = im.shape
    x0 = (0 - c["x_eje"]) / c["px_m"]; x1 = (W - c["x_eje"]) / c["px_m"]
    z1 = (c["y_suelo"] - 0) / c["px_m"]; z0 = (c["y_suelo"] - H) / c["px_m"]
    ax.imshow(im, cmap="gray", extent=(x0, x1, z0, z1), alpha=0.9)
    # modelo: siluetas/aristas del alzado ortogonal, en rojo, eje horizontal centrado en el eje de la torre
    PL.alzado_lineas(ax, d)
    for z, nom in PL.NIVELES:
        ax.axhline(z, color="tab:blue", lw=0.4, ls=":")
        ax.text(x1 + 0.3, z, f"+{z:.1f} {nom}".replace(".", ","), fontsize=6, color="tab:blue", va="center")
    ax.set_xlim(x0, x1 + 9); ax.set_ylim(max(z0, -3), z1)
    ax.set_aspect("equal"); ax.grid(True, lw=0.2)
    ax.set_title(titulo, fontsize=9, loc="left")


if __name__ == "__main__":
    import sys
    fig, axs = plt.subplots(1, 2, figsize=(22, 12))
    dch = (s._N[0], s._N[1])
    alzado_sobre_foto(axs[0], "F09", dch, "ALZADO DEL CHAFLAN (rojo, modelo) sobre F09 escalada a metros")
    alzado_sobre_foto(axs[1], "F14", dch, "ALZADO DEL CHAFLAN (rojo, modelo) sobre F14 escalada a metros")
    fig.savefig(sys.argv[1] if len(sys.argv) > 1 else "cmp_alzado_chaflan.png", dpi=85)
