"""Propuesta de ZONAS de verificacion: areas 3D (no puntos), dibujadas sobre la foto F09 escalada a metros
y sobre la planta. Zonas vecinas comparten limites (juntas), que se comprueban desde las dos zonas."""
import math, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle
from PIL import Image
import edificio as E
I='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'
PX, Y0, X0 = 397/30.6, 795, 303.5
# zonas visibles en el alzado del chaflan: (id, nombre, x0, x1, z0, z1)   [m, x respecto al eje de la torre]
ALZ = [
 ("Z1", "Remate y letrero", -7, 8, 43.7, 50),
 ("Z2", "Visera", -16, 12, 40.5, 43.7),
 ("Z3", "Banda acristalada", -12.5, 11, 38.2, 40.5),
 ("Z4", "Tambor de ojos y terraza de servicio", -14.5, 15, 32.6, 38.2),
 ("Z5", "Barril: plantas tipo 2-6", -16, 16, 18.1, 32.6),
 ("Z6", "Barril: 1ª planta (pavés) y canto inferior", -16, 16, 15.2, 18.1),
 ("Z7", "Arranque de la torre: ménsulas, cuello y columna", -16, 16, 7.3, 15.2),
 ("Z8", "Chaflán: restaurante (banda + PB hundida)", -17.5, -4.4, 0, 7.3),
 ("Z9", "Chaflán: pie de columna y fuente", -4.4, 2.0, 0, 7.3),
 ("Z10", "Chaflán: hotel y esquina a 90°", 2.0, 12.0, 0, 7.3),
 ("Z11", "Concha y muro del relieve", 12.0, 26.5, 0, 7.3),
]
COL = plt.cm.tab20(np.linspace(0, 1, 20))
fig = plt.figure(figsize=(22, 12.5))
fig.suptitle("PROPUESTA DE ZONAS (filas de la matriz). Izquierda: zonas sobre F09 escalada a metros. Derecha: zonas en planta.", fontsize=13, weight="bold")
ax = fig.add_axes([0.02, 0.04, 0.44, 0.88])
im = np.asarray(Image.open(I + "9.webp").convert("L")); H, W = im.shape
ax.imshow(im, cmap="gray", extent=((0 - X0)/PX, (W - X0)/PX, (Y0 - H)/PX, Y0/PX), alpha=0.85)
for i, (k, n, x0, x1, z0, z1) in enumerate(ALZ):
    c = COL[i]
    ax.add_patch(Rectangle((x0, z0), x1 - x0, z1 - z0, fill=True, fc=(*c[:3], 0.18), ec=c, lw=2.2))
    ax.text(x0 + 0.3, z1 - 0.4, k, color="white", fontsize=10, weight="bold", va="top",
            bbox=dict(fc=c, ec="none", pad=1.5))
for z in (7.3, 15.2, 18.1, 32.6, 38.2, 40.5, 43.7):
    ax.text(27.2, z, f"junta +{z:.1f}".replace(".", ","), fontsize=7, va="center", color="crimson")
    ax.plot([26.6, 27.1], [z, z], color="crimson", lw=1)
ax.set_xlim(-24, 31); ax.set_ylim(-4, 53); ax.set_aspect("equal"); ax.tick_params(labelsize=6)
# leyenda con nombres
ax3 = fig.add_axes([0.47, 0.04, 0.17, 0.88]); ax3.axis("off")
txt = [f"{k}  {n}" for k, n, *_ in ALZ] + ["", "Zonas que no se ven de frente", "(se comprueban en otras fotos):",
       "Z12  Ala corta: bloque alto y lucernarios", "Z13  Ala corta: ladrillo sobre pilares",
       "Z14  Ala larga: tramo junto a la torre", "Z15  Ala larga: tramo central (bar, terraza, ventanas)",
       "Z16  Ala larga: tramo final y testero", "Z17  Escalera trasera y encuentro con el barril",
       "Z18  Patio interior de la L", "", "JUNTAS entre zonas (se comprueban desde las dos):",
       "Z6/Z7  +15,2: borde inferior del barril", "Z7/Z8-Z11  +7,3: coronación de las bandas",
       "Z7/Z9  columna que atraviesa la junta", "Z10/Z11  esquina a 90° y arranque de la concha",
       "Z11/Z14  concha a lo largo del ala", "Z5-Z7/Z17  escalera pegada al barril",
       "Z14/Z17  escalera entrando en el ala", "Z8/Z12  banda del restaurante y bloque alto",
       "Z4/Z5  +32,6 · Z3/Z4  +38,2 · Z2/Z3  +40,5 · Z1/Z2  +43,7"]
ax3.text(0, 1, "\n".join(txt), fontsize=8.5, va="top", family="DejaVu Sans")
# planta con zonas
ax2 = fig.add_axes([0.64, 0.04, 0.35, 0.88])
pl = E.plantas_base()
ax2.add_patch(Polygon(pl["P1"], closed=True, fc="0.9", ec="k", lw=1))
ax2.add_patch(Circle(E.T, E.R_AL, fc="none", ec="0.4", ls="--"))
def poly(pts, k, i):
    c = COL[i]; ax2.add_patch(Polygon(pts, closed=True, fc=(*c[:3], 0.25), ec=c, lw=2))
    cx, cy = np.mean(np.array(pts), axis=0); ax2.text(cx, cy, k, fontsize=9, weight="bold", ha="center", va="center",
                                                        bbox=dict(fc="white", ec=c, pad=1))
P = E.P
yf = -(E.R_COL - E.RET)
poly([P(-15.85, yf - 1), P(-E.R_COL, yf - 1), P(-E.R_COL, yf + 5), P(-15.85, yf + 5)], "Z8", 7)
poly([P(-E.R_COL, yf - 2), P(E.R_COL, yf - 2), P(E.R_COL, yf + 4), P(-E.R_COL, yf + 4)], "Z9", 8)
poly([P(E.R_COL, yf - 1), P(E.R_COL + E.HOT, yf - 1), P(E.R_COL + E.HOT, yf + 5), P(E.R_COL, yf + 5)], "Z10", 9)
poly([(E.W_P, pl["Q"][1]), (E.W_EXT + 1, pl["Q"][1]), (E.W_EXT + 1, E.Y_CUNA), (E.W_P, E.Y_CUNA)], "Z11", 10)
poly([(-E.L_C + E.L_LADR, 0), (-9, 0), (-9, E.W_C), (-E.L_C + E.L_LADR, E.W_C)], "Z12", 11)
poly([(-E.L_C, 0), (-E.L_C + E.L_LADR, 0), (-E.L_C + E.L_LADR, E.W_C), (-E.L_C, E.W_C)], "Z13", 12)
poly([(0, 22), (E.W_P, 22), (E.W_P, 45), (0, 45)], "Z14", 13)
poly([(0, 45), (E.W_P, 45), (E.W_P, 80), (0, 80)], "Z15", 14)
poly([(0, 80), (E.W_P, 80), (E.W_P, E.L_L), (0, E.L_L)], "Z16", 15)
xe = E.W_BAR / 2 + 0.5
poly([(xe - 5, E.ESC_Y0 - 2), (xe + 5, E.ESC_Y0 - 2), (xe + 5, E.ESC_Y1 + 1.5), (xe - 5, E.ESC_Y1 + 1.5)], "Z17", 16)
poly([(-16, E.W_C), (-0.2, E.W_C), (-0.2, 40), (-16, 40)], "Z18", 17)
ax2.text(*E.T, "Z1-Z7\n(torre)", ha="center", va="center", fontsize=9)
ax2.set_xlim(-28, 22); ax2.set_ylim(-8, 98); ax2.set_aspect("equal"); ax2.tick_params(labelsize=6)
ax2.set_title("zonas en planta (m)", fontsize=9, loc="left")
fig.savefig("ZONAS_propuesta.png", dpi=85)
