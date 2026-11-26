"""PREGUNTAS P3–P5 + H4 con base gráfica: gárgolas, planta de pavés, letrero en arco y fuente.
Todo lo marcado sale de las fotos; las medidas de F09 con el paso de forjados (40 px = 3,10 m)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from PIL import Image
import laminas as LM, edificio as E

V = E._v
R = "#d00000"


def foto(ax, img, box, titulo):
    x0, y0, x1, y1 = box
    ax.imshow(Image.open(LM.IMG + img).convert("RGB").crop(box), extent=(x0, x1, y1, y0)); ax.axis("off")
    ax.set_title(titulo, fontsize=9.5, loc="left", weight="bold")


def circ(ax, pts, r=9, txt=None):
    for p in pts:
        ax.add_patch(Circle(p, r, fill=False, ec=R, lw=1.8))
    if txt:
        ax.annotate(txt, pts[0], (pts[0][0], pts[0][1] - 4 * r), color=R, fontsize=8.5, weight="bold", ha="center",
                    arrowprops=dict(arrowstyle="-", color=R, lw=0.8))


def marca(ax, y0, y1, x, txt, lado=1):
    ax.plot([x, x], [y0, y1], color=R, lw=2); ax.plot([x - 4, x + 4], [y0, y0], color=R, lw=1.5); ax.plot([x - 4, x + 4], [y1, y1], color=R, lw=1.5)
    ax.text(x + 6 * lado, (y0 + y1) / 2, txt, color=R, fontsize=8, weight="bold", va="center", ha="left" if lado > 0 else "right",
            bbox=dict(fc="white", ec="none", alpha=0.8, pad=1))


def seccion_planta(ax, pav, titulo):
    """sección radial esquemática de las dos plantas bajas del barril (líneas solo). pav: 'A' fondo / 'B' fachada"""
    FC, FR, FP, F, RB = V["FOR_C"], V["FOR_R"], V["FOR_P"], E.F, E.R_B
    rf = RB - 1.8; z0 = 0.0
    k = dict(color="k", lw=1.0)
    # planta 2 (habitaciones): forjado, ranura, poyete, ventana al fondo
    z = z0 + F
    ax.add_patch(Rectangle((rf - 0.6, z), RB - rf + 0.6, FC, fc="none", ec="k", lw=1.2, hatch="////"))
    ax.add_patch(Rectangle((RB - 0.25, z + FC + FR), 0.25, FP, fc="none", ec="k", lw=1.2, hatch="////"))
    ax.plot([rf, rf], [z + FC, z + F], **k); ax.plot([rf - 0.08, rf - 0.08], [z + FC, z + F], **k)
    ax.text(rf - 0.2, z + 1.9, "ventana", fontsize=7, ha="right")
    ax.text(RB + 0.15, z + FC + FR + FP / 2, "poyete 0,78", fontsize=7, va="center")
    ax.text(RB + 0.15, z + FC + FR / 2, "ranura 0,27", fontsize=7, va="center")
    ax.text(RB + 0.15, z + FC / 2, "canto 0,59", fontsize=7, va="center")
    ax.add_patch(Circle((RB + 0.06, z + FC - 0.12), 0.07, fc="k"))       # gárgola en el canto, bajo la ranura (F18)
    # planta 1 (pavés) medida en F09: pavés 1,40 hasta el canto de arriba; banda continua 1,09 sin ranura debajo;
    # su borde inferior queda a +Z_B0+0,61 (paso 3,10) y por debajo el fondo inclinado con ménsulas
    zb = z0 + F - 1.40 - 1.09
    ax.add_patch(Rectangle((RB - 0.25, zb), 0.25, 1.09, fc="none", ec="k", lw=1.2, hatch="////"))
    ax.plot([RB - 0.25, rf - 0.6], [zb + 0.3, zb + 0.3], color="k", lw=1.0)
    xp = rf if pav == "A" else RB - 0.45
    for dx in (0, -0.12):
        ax.plot([xp + dx, xp + dx], [zb + 1.09, z0 + F], color="k", lw=1.0)
    for zz in np.arange(zb + 1.09, z0 + F, 0.2):
        ax.plot([xp - 0.12, xp], [zz, zz], color="k", lw=0.4)
    ax.text(xp - 0.2, zb + 1.8, "pavés\n1,40", fontsize=7, ha="right")
    ax.text(RB + 0.15, zb + 0.55, "banda 1,09\nsin ranura", fontsize=7, va="center")
    ax.plot([RB, rf - 0.6], [zb, z0 - 0.9], color="k", lw=1.0)               # fondo inclinado / ménsula
    ax.text(RB + 0.15, zb - 0.1, "+%.2f borde (F09)" % (E.Z_B0 + zb), fontsize=6.5, va="top")
    ax.plot([rf - 1.2, RB + 0.2], [z0 + F, z0 + F], color="k", lw=0.25, ls=(0, (10, 2, 1, 2)))
    ax.text(rf - 1.2, z0 + F + 0.08, "+%.2f" % (E.Z_B0 + F), fontsize=6.5)
    ax.set_xlim(rf - 1.6, RB + 1.6); ax.set_ylim(-1.2, F + 2.0); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(titulo, fontsize=9, loc="left", weight="bold")


fig = plt.figure(figsize=(24, 22))
fig.suptitle("PREGUNTAS P3–P5 y H4 – lo que dicen las fotos (rojo = marcado sobre la foto)", fontsize=16, x=0.02, ha="left", weight="bold", y=0.995)
FILA = [0.725, 0.485, 0.25, 0.015]
H = 0.225

# ---------- P3 · gárgolas ----------
a = fig.add_axes([0.02, FILA[0], 0.27, H]); foto(a, "18.webp", (583, 482, 933, 782), "F18 – desde abajo: un puntito por módulo y por planta")
circ(a, [(693, 500), (700, 529), (836, 537), (700, 602), (841, 610)], 7, "gárgolas")
a = fig.add_axes([0.30, FILA[0], 0.36, H]); foto(a, "8.webp", (660, 560, 1320, 800), "F08 – cubierta del barril: el mismo puntito en el canto, centrado entre aletas")
circ(a, [(875, 695), (1020, 715), (1192, 721)], 8, "gárgola")
a = fig.add_axes([0.67, FILA[0] + 0.02, 0.31, H - 0.02]); a.axis("off")
a.text(0, 1, "P3 · LOS «PUNTITOS» (tu mensaje del 22/11)\n\n"
       "Lo que veo en F18 y F08:\n"
       " • uno por módulo, centrado entre dos aletas;\n"
       " • en TODAS las plantas, no solo en la cubierta;\n"
       " • en el canto del forjado, justo debajo de la ranura\n"
       "   → desagüe de cada balcón (gárgola o tubo corto).\n\n"
       "Hipótesis: tubo Ø ≈ 0,10, vuelo ≈ 0,15 m.\n"
       "En el molde de 15 cm (1:≈330) mide 0,3 mm: no sale.\n\n"
       "PREGUNTA: ¿los dibujo solo en alzados y secciones\n"
       "(símbolo, 19 × 6 plantas) y NO en el 3D?", fontsize=10.5, va="top", family="DejaVu Sans")

# ---------- P4 · planta de pavés ----------
a = fig.add_axes([0.02, FILA[1], 0.30, H]); foto(a, "9.webp", (95, 480, 515, 640), "F09 – la 1.ª planta del barril es distinta")
marca(a, 572, 589.5, 300, "pavés 1,40", 1); marca(a, 590, 603.5, 330, "banda 1,09 sin ranura", 1)
marca(a, 531, 549.5, 300, "ventana 1,47", 1); marca(a, 520, 523, 455, "ranura", 1)
a = fig.add_axes([0.33, FILA[1], 0.22, H]); foto(a, "18.webp", (583, 600, 933, 760), "F18 – se ve el techo sobre el pavés → está retranqueado")
a.annotate("techo sobre\nel pavés", (700, 620), (600, 610), color=R, fontsize=8, weight="bold", arrowprops=dict(arrowstyle="->", color=R))
a.annotate("banda continua", (760, 672), (850, 705), color=R, fontsize=8, weight="bold", arrowprops=dict(arrowstyle="->", color=R))
a.annotate("ménsulas", (655, 715), (690, 745), color=R, fontsize=8, weight="bold", arrowprops=dict(arrowstyle="->", color=R))
seccion_planta(fig.add_axes([0.56, FILA[1], 0.135, H]), "A", "A · pavés al fondo (probable)")
seccion_planta(fig.add_axes([0.70, FILA[1], 0.135, H]), "B", "B · pavés casi en fachada")
a = fig.add_axes([0.845, FILA[1], 0.15, H]); a.axis("off")
a.text(0, 1, "P4 · 1.ª PLANTA DEL BARRIL\n(«un poco distinta», 22/11)\n\n"
       "Medido en F09 (12,9 px/m):\n"
       " • pavés en vez de ventana;\n"
       " • delante, banda continua 1,09\n"
       "   SIN ranura (arriba: 0,59+0,27+0,78);\n"
       " • debajo, ménsulas.\n\n"
       "F18 ve el techo sobre el pavés:\n"
       "no está en fachada → A.\n\n"
       "Hoy el modelo la hace igual que\n"
       "las demás (ranura + poyete).\n\n"
       "PREGUNTA: ¿aplico A?", fontsize=9.5, va="top")

# ---------- H4 · letrero ----------
a = fig.add_axes([0.02, FILA[2], 0.22, H]); foto(a, "19.webp", (110, 130, 340, 290), "F19 (actual) – САЛЮТ sigue la curva del remate")
a.annotate("С de canto", (175, 238), (125, 270), color=R, fontsize=8, weight="bold", arrowprops=dict(arrowstyle="->", color=R))
a.annotate("Т girando", (300, 228), (315, 282), color=R, fontsize=8, weight="bold", arrowprops=dict(arrowstyle="->", color=R))
a.annotate("ГОТЕЛЬ: añadido\nreciente (no está en\nF09, F14, F70) → fuera", (250, 248), (190, 150), color=R, fontsize=7.5, weight="bold",
           arrowprops=dict(arrowstyle="->", color=R))
a = fig.add_axes([0.25, FILA[2], 0.33, H]); foto(a, "8.webp", (940, 100, 1480, 280), "F08 – …АЛЮТ y a la derecha otra С: la palabra se repite")
circ(a, [(1412, 180)], 30, "2.ª С")
a = fig.add_axes([0.59, FILA[2], 0.22, H]); foto(a, "70.webp", (80, 0, 600, 260), "F70 (1984) – СА… sobre bastidor, en el borde")
a = fig.add_axes([0.82, FILA[2] + 0.02, 0.17, H - 0.02]); a.axis("off")
a.text(0, 1, "H4 · LETRERO EN ARCO\n\n"
       "F19: las letras siguen la curva.\n"
       "F08: tras …АЛЮТ aparece otra С.\n"
       "F23: letras a los dos lados.\n"
       "→ САЛЮТ en arco y REPETIDO\n"
       "   alrededor del remate.\n\n"
       "Hoy: 1 plano frente a Alamy.\n\n"
       "PREGUNTA: ¿2 veces (cada\n"
       "palabra ≈ 150°) o 3 veces?\n"
       "Propongo 2, una hacia Alamy\n"
       "y otra opuesta.", fontsize=9.5, va="top")

# ---------- P5 · fuente ----------
a = fig.add_axes([0.02, FILA[3], 0.28, H]); foto(a, "1.webp", (300, 560, 560, 720), "F01 (1984) – vaso en media luna al pie de la columna")
a.annotate("vaso semicircular", (455, 690), (480, 715), color=R, fontsize=8, weight="bold", arrowprops=dict(arrowstyle="->", color=R))
a = fig.add_axes([0.31, FILA[3], 0.25, H]); foto(a, "14.webp", (330, 560, 640, 740), "F14 (1984) – chorros ante la cristalera de PB")
a.annotate("fuente", (470, 700), (430, 640), color=R, fontsize=8, weight="bold", arrowprops=dict(arrowstyle="->", color=R))
a = fig.add_axes([0.57, FILA[3], 0.25, H]); foto(a, "15.png", (150, 230, 450, 340), "F15 (1984) – chorros en abanico")
a = fig.add_axes([0.83, FILA[3] + 0.02, 0.16, H - 0.02]); a.axis("off")
a.text(0, 1, "P5 · FUENTE (26/11: «está\ndebajo del pilar, a la entrada»)\n\n"
       "F01, F14 y F15 (1984): vaso\n"
       "en media luna contra la base\n"
       "de la columna, bordillo bajo,\n"
       "chorros en abanico.\n"
       "Tamaño: Ø ≈ 6–7 m (F14, con\n"
       "los paños de 2,45; estimación).\n\n"
       "No está en el modelo.\n\n"
       "PREGUNTA: ¿la pongo en la\n"
       "planta baja y en el 3D\n"
       "(bordillo 0,4)?", fontsize=9.5, va="top")
fig.savefig("PREGUNTAS_P3_P5.png", dpi=75)
print("ok")
