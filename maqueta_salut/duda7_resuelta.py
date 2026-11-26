"""DUDA 7 RESUELTA con la foto de dron del usuario (26/11): el muro de coronación de la escalera está sobre la cubierta
del tambor, en el eje de la cuña, acaba en el borde del tambor (fuera solo lamas, más bajas) y vierte hacia dentro.
Se comprueba el modelo corregido en F09, Alamy y la foto de frente; planta antes/después."""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Polygon, Rectangle
from PIL import Image
import edificio as E, laminas as LM

V = E._v; T = np.array(E.T); R = "#d00000"; VE = "#1a9b4b"; AZ = "#1a6fdb"; NA = "#e08000"
e = lambda d: np.array([math.cos(math.radians(d)), math.sin(math.radians(d))])
SCR = "/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/scratchpad/"


def muro(r0, r1, z0i, z1o, az, n=14):
    """puntos del muro (radial, en az) entre r0 y r1, coronación de z0i (dentro) a z1o (fuera)"""
    out = []
    for r in np.linspace(r0, r1, n):
        zt = z0i + (r - r0) / (r1 - r0) * (z1o - z0i)
        for z in np.linspace(E.Z_T1, zt, 8): out.append((r * e(az), z))
    return out


ANT = muro(V["ESC_RS"], E.ESC_R1 + 0.3, V["ESC_ZI"], V["ESC_Z1"], math.degrees(E.ESC_ANG - E.ESC_HB) + 0.5)
NUE = muro(V["ESC_RS"], E.R_T + V["ESC_MO"], V["ESC_ZI"], V["ESC_Z1"], math.degrees(E.ESC_ANG))
fig = plt.figure(figsize=(26, 19))
fig.suptitle("DUDA 7 RESUELTA con tu foto de dron: el muro inclinado está SOBRE la cubierta del tambor, acaba en su borde y vierte hacia dentro",
             fontsize=16, x=0.01, ha="left", weight="bold", y=0.995)
# 1. dron anotado
dr = Image.open(LM.IMG + "dron_letras.png").convert("RGB")
ax = fig.add_axes([0.01, 0.36, 0.36, 0.6]); ax.imshow(dr); ax.axis("off")
ax.add_patch(Polygon([(763, 437), (958, 402), (958, 528), (763, 532)], closed=True, fill=False, ec=R, lw=3))
ax.annotate("", (775, 432), (950, 404), arrowprops=dict(arrowstyle="-|>", color=R, lw=2.5))
ax.text(760, 380, "vierte hacia dentro", color=R, fontsize=11, weight="bold", bbox=dict(fc="white", ec="none", alpha=0.85))
ax.text(700, 575, "muro sobre la terraza del tambor", color=R, fontsize=11, weight="bold", bbox=dict(fc="white", ec="none", alpha=0.8))
ax.annotate("acaba en el borde del tambor;\nfuera, solo lamas (más bajas)", (950, 500), (760, 690), color=R, fontsize=10.5, weight="bold",
            arrowprops=dict(arrowstyle="->", color=R, lw=1.5), bbox=dict(fc="white", ec="none", alpha=0.8))
ax.add_patch(Circle((167, 395), 100, fill=False, ec=AZ, lw=2.5)); ax.text(60, 520, "claraboya (lado plaza, az 320°)", color=AZ, fontsize=11, weight="bold",
                                                                         bbox=dict(fc="white", ec="none", alpha=0.8))
ax.text(330, 230, "САЛЮТ de frente = 2.ª palabra (az ≈ 30°)", color=VE, fontsize=11, weight="bold", bbox=dict(fc="white", ec="none", alpha=0.8))
ax.set_title("TU FOTO DE DRON (desde el patio, ≈ 7°): claraboya a la izquierda, letras de frente, escalera a la derecha", fontsize=11, loc="left", weight="bold")
# 2. F09 con el muro nuevo
f09 = Image.open(LM.IMG + "9.webp").convert("RGB"); BF = (330, 190, 520, 320)
ax = fig.add_axes([0.39, 0.66, 0.29, 0.3]); ax.imshow(f09.crop(BF), extent=(BF[0], BF[2], BF[3], BF[1])); ax.axis("off")
for pts, col, lab in ((ANT, "0.55", "antes (r hasta 16,2, lado izq.)"), (NUE, R, "ahora (sobre el tambor, eje)")):
    ax.scatter([307 + (q @ e(50)) * 12.9 for q, z in pts], [571.5 - (z - 17.0) * 12.9 for q, z in pts], s=6, color=col, label=lab, zorder=10)
ax.axvline(307 + (V["OV_X"] + E.R_V) * 12.9, color=AZ, ls="--", lw=1.2)
ax.set_xlim(BF[0], BF[2]); ax.set_ylim(BF[3], BF[1]); ax.legend(loc="lower left", fontsize=9)
ax.text(BF[2] - 6, BF[1] + 6, "✔", fontsize=30, color=VE, ha="right", va="top", weight="bold")
ax.set_title("F09: el muro nuevo queda detrás de la visera; ya no asoma sobre el cielo", fontsize=11, loc="left", weight="bold")
# 3. Alamy
ala = Image.open(SCR + "alamy.jpg").convert("RGB"); BA = (0, 1600, 620, 1900)
ax = fig.add_axes([0.70, 0.66, 0.29, 0.3]); ax.imshow(ala.crop(BA), extent=(BA[0], BA[2], BA[3], BA[1])); ax.axis("off")
D = e(V["VISTA_ALAMY"] + 90)
for pts, col in ((ANT, "0.55"), (NUE, R)):
    ax.scatter([1078 + (q @ D) * 64.4 for q, z in pts], [887 + 1337 - (z - 32.5) * 56.53 for q, z in pts], s=6, color=col, zorder=10)
ax.set_xlim(BA[0], BA[2]); ax.set_ylim(BA[3], BA[1])
ax.text(BA[2] - 6, BA[1] + 6, "≈", fontsize=30, color=NA, ha="right", va="top", weight="bold")
ax.set_title("Alamy: misma coronación inclinada (alturas de Alamy); su extremo\nqueda ≈ 1,5 m más dentro que en la foto (Alamy, otra vez, por encima del tambor)",
             fontsize=10.5, loc="left", weight="bold")
# 4. frente
fte = Image.open(LM.IMG + "esc_frente_alta.png").convert("RGB"); BE = (250, 380, 1050, 950)
ax = fig.add_axes([0.39, 0.33, 0.29, 0.3]); ax.imshow(fte.crop(BE), extent=(BE[0], BE[2], BE[3], BE[1])); ax.axis("off")
ax.annotate("", (600, 518), (330, 548), arrowprops=dict(arrowstyle="-|>", color=R, lw=2.5))
ax.text(300, 470, "el muro sube hacia fuera (marca verde)", color=R, fontsize=10.5, weight="bold", bbox=dict(fc="white", ec="none", alpha=0.8))
ax.text(690, 780, "lamas: empiezan\njusto donde acaba\nel muro", color=R, fontsize=10, weight="bold", bbox=dict(fc="white", ec="none", alpha=0.8))
ax.set_xlim(BE[0], BE[2]); ax.set_ylim(BE[3], BE[1])
ax.text(BE[2] - 6, BE[1] + 6, "✔", fontsize=30, color=VE, ha="right", va="top", weight="bold")
ax.set_title("Foto de frente (tomada algo desde el patio): mismo muro, visto en escorzo", fontsize=11, loc="left", weight="bold")
# 5. planta antes / después
ax = fig.add_axes([0.70, 0.33, 0.29, 0.3]); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(Circle((0, 0), E.R_T, fill=False, ec="k", lw=1.3)); ax.add_patch(Circle((0, 0), E.R_B, fill=False, ec="k", lw=0.5, ls="--"))
cb = np.array(E.P(V["OB_X"], V["OB_Y"])) - T; ax.add_patch(Circle(cb, E.R_G, fill=False, ec="0.4", lw=0.8))
ax.add_patch(Wedge((0, 0), E.ESC_R1, 90 - V["ESC_SECB"] / 2, 90 + V["ESC_SECB"] / 2, width=E.ESC_R1 - E.R_T, fc="0.9", ec="k", lw=0.6))
ax.text(0, E.ESC_R1 + 0.8, "lamas (fuera del tambor)", ha="center", fontsize=9)
a0 = E.ESC_ANG - E.ESC_HB
ax.plot([V["ESC_RS"] * math.cos(a0), (E.ESC_R1 + 0.3) * math.cos(a0)], [V["ESC_RS"] * math.sin(a0), (E.ESC_R1 + 0.3) * math.sin(a0)], color="0.55", lw=4, label="antes")
ax.plot([0, 0], [V["ESC_RS"], E.R_T + V["ESC_MO"]], color=R, lw=4, label="ahora")
cl = np.array(E.P(V["LUC_X"], V["LUC_Y"])) - T; ax.add_patch(Circle(cl, V["LUC_R"], fc="none", ec=AZ, lw=1.5)); ax.text(cl[0] + 2, cl[1], "claraboya", color=AZ, fontsize=9)
for az_, nom in ((320, "F09"), (V["VISTA_ALAMY"], "Alamy"), (7, "dron")):
    p = e(az_) * 20; ax.annotate(nom, (0, 0), p, arrowprops=dict(arrowstyle="<-", lw=0.9), fontsize=9, ha="center")
ax.legend(loc="lower left", fontsize=9); ax.set_xlim(-22, 22); ax.set_ylim(-20, 21)
ax.set_title("Planta: muro de coronación antes (gris) y ahora (rojo)", fontsize=11, loc="left", weight="bold")
fig.text(0.01, 0.3, "QUÉ CAMBIA EN EL MODELO\n"
         f"· El muro inclinado va en el eje de la cuña, apoyado en la cubierta del tambor (+{E.Z_T1:.2f}), de r {V['ESC_RS']:.1f} a r {E.R_T + V['ESC_MO']:.2f} "
         f"(antes llegaba a r {E.ESC_R1 + 0.3:.1f}, por encima de las lamas).\n"
         f"· Coronación inclinada que vierte hacia dentro: +{V['ESC_ZI']:.2f} junto a la banda → +{V['ESC_Z1']:.2f} en el borde del tambor (alturas de Alamy).\n"
         "· Fuera del tambor, solo las lamas (más bajas). Nada más cambia: visera, banda, remate y letras se quedan como estaban.\n\n"
         "TAMBIÉN CONFIRMAN LO QUE YA ESTABA (tus dos fotos)\n"
         "· Letras: desde el patio se lee САЛЮТ entero y de frente → la 2.ª palabra del arco (az 330°→90°), como en el modelo.\n"
         "· Claraboya hacia la plaza (az 320°), a unos 130° de la escalera: a la izquierda en el dron, con la escalera a la derecha.\n"
         "· Postal de 1984: la 1.ª planta es de pavés con la banda continua debajo y las ménsulas (P4), y la visera vuela por fuera del barril (H1)."
         .replace("+38.73", "+38,73").replace("+40.80", "+40,80").replace("+41.60", "+41,60").replace("r 10.2", "r 10,2")
         .replace("r 13.85", "r 13,85").replace("r 16.2", "r 16,2"), fontsize=12.5, va="top", linespacing=1.5)
fig.savefig("DUDA7_RESUELTA.png", dpi=62)
print("ok")
