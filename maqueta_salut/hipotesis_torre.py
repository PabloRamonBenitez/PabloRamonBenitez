"""HIPÓTESIS H1–H3 de la parte alta: diámetros y desplazamientos medidos en F09 (teleobjetivo, escala por forjados),
F14 (1984, frontal) y F23 (aérea 1984), frente a Alamy. Solo cocientes dentro de una misma fila de la foto."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import laminas as LM, edificio as E

V = E._v
# bordes medidos (px de la foto original): (izq, der, y) por elemento
M = {
 "F09": dict(img="9.webp", box=(40, 60, 560, 330), tambor=(132.1, 482.0, 300), banda=(153.3, 420.8, 280), visera=(110.6, 442.3, 255), remate=(242.4, 373.6, 210)),
 "F14": dict(img="14.webp", box=(330, 30, 800, 260), tambor=(400.0, 763.0, 200), banda=(428.0, 683.0, 150), visera=(370.0, 716.0, 140), remate=(510.0, 647.0, 75)),
 "F23": dict(img="23.webp", box=(180, 100, 560, 330), tambor=(241.9, 481.8, 260), banda=(277.7, 476.4, 240), visera=(259.5, 489.4, 220), remate=(313.0, 405.8, 165)),
}
COL = {"tambor": "#1a9b4b", "banda": "#2a6fdb", "visera": "#e0a000", "remate": "#d43c3c"}
mod = {"tambor": 2 * E.R_T, "banda": 2 * V["R_G"], "visera": 2 * V["R_V"], "remate": 2 * V["R_R"]}
ala = {"tambor": 27.02, "banda": 18.9, "visera": 23.39, "remate": 9.53}
fig = plt.figure(figsize=(24, 15))
rows = []
for i, (k, m) in enumerate(M.items()):
    ax = fig.add_axes([0.01 + i * 0.33, 0.42, 0.32, 0.52]); x0, y0, x1, y1 = m["box"]
    ax.imshow(Image.open(LM.IMG + m["img"]).convert("RGB").crop(m["box"]), extent=(x0, x1, y1, y0)); ax.axis("off")
    t = m["tambor"]; wt = t[1] - t[0]; ct = (t[0] + t[1]) / 2; esc = wt / (2 * E.R_T)
    for el in ("tambor", "banda", "visera", "remate"):
        a, b, y = m[el]; ax.plot([a, b], [y, y], color=COL[el], lw=2.5); ax.plot([a, a], [y - 6, y + 6], color=COL[el], lw=2); ax.plot([b, b], [y - 6, y + 6], color=COL[el], lw=2)
        ax.plot([(a + b) / 2] * 2, [y - 10, y + 10], color=COL[el], lw=1.5)
        rows.append((k, el, (b - a) / wt, (b - a) / esc, ((a + b) / 2 - ct) / esc))
    ax.plot([ct, ct], [y0, y1], color="#1a9b4b", lw=0.8, ls="--")
    ax.set_title(f"{k}: bordes medidos (escala: tambor = {2 * E.R_T:.1f} m)".replace(".", ","), fontsize=11, loc="left", weight="bold")
txt = ["               diámetro / diámetro del tambor                   diámetro (m)                desplazamiento lateral (m)",
       "               F09     F14     F23  | Alamy | modelo     F09    F14    F23  | modelo      F09     F14     F23"]
for el in ("tambor", "banda", "visera", "remate"):
    r = {k: (q, d, s) for k, e, q, d, s in rows if e == el}
    txt.append(f"{el:10s}   " + "  ".join(f"{r[k][0]:5.3f}" for k in M) + f"  | {ala[el] / ala['tambor']:5.3f} | {mod[el] / mod['tambor']:5.3f}     "
               + "  ".join(f"{r[k][1]:5.1f}" for k in M) + f"  | {mod[el]:5.1f}      " + "  ".join(f"{r[k][2]:+5.1f}" for k in M))
fig.text(0.01, 0.39, "\n".join(txt).replace(".", ","), family="monospace", fontsize=11, va="top")
fig.text(0.01, 0.17, "H1 · VISERA Y REMATE MÁS GRANDES. Tres fotos independientes (F09 teleobjetivo, F14 y F23 de 1984) dan visera/tambor ≈ 0,95 y remate/tambor ≈ 0,38;\n"
         "       Alamy da 0,866 y 0,352. Con la escala de F09 (forjados): visera Ø ≈ 25,7 (R 12,8) y remate Ø ≈ 10,2 (R 5,1) frente a 23,4 / 9,5 del modelo.\n"
         "       Posible causa: Alamy es una foto de pantalla; su escala horizontal puede no ser la misma en la fila del tambor y en la de la visera.\n"
         "H2 · BANDA MÁS DESPLAZADA HACIA −U: F09 −1,6 m, F14 −1,9 m (modelo −0,5).      H3 · REMATE CENTRADO EN U: F09 +0,1, F14 −0,2 (modelo +0,6).\n"
         "Las alturas (Alamy, MGF) no cambian: estas hipótesis solo tocan diámetros y desplazamientos en planta.", fontsize=12, va="top")
fig.suptitle("HIPÓTESIS DE LA PARTE ALTA – cocientes medidos en la misma fila de cada foto", fontsize=14, x=0.01, ha="left", weight="bold")
fig.savefig("HIPOTESIS_TORRE.png", dpi=65)
for r in rows: print(r)
