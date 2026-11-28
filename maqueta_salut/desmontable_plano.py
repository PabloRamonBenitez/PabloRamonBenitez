"""MAQUETA DESMONTABLE – PLANO DE LA DIVISIÓN (propuesta para revisar ANTES de generar los modelos; usuario 28/11).
El tambor (toda la torre redonda) es una pieza con un cilindro que baja; la otra pieza (columna, cuello, alas, concha, restaurante)
lleva un hueco circular donde entra ese cilindro. Hoja de trabajo en español (no es del juego de planos).
Todo sale de las cotas del modelo (cotas.py / edificio.py): la altura del corte es el fondo de las vigas, bajo el forjado plano del barril."""
import traduccion
traduccion.ACTIVO = False
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
import edificio as E, laminas as LM, lineas as L

V = E._v; T = np.array(E.T)
ZC = V["Z_BI"] - V["VIG_H"]                     # plano de corte: fondo de las vigas (13,71)
RP, HP = 4.5, 3.0                            # cilindro de encaje: radio y largo (m reales)
HOLG, PROF_EXTRA = 0.15, 0.20                # holgura radial y fondo extra del hueco
KW, KP = 1.2, 0.9                            # llave (nervio vertical del cilindro): ancho y saliente
CH_W = KW + 2 * HOLG                         # ancho del canal del hueco
CH_R = RP + KP + HOLG                        # el canal llega hasta este radio (holgura HOLG en la punta de la llave)
K = 150.0 / E.Z_R1                           # mm de maqueta por metro real (1:339)
d_esc = np.array(E.esc_pt(1.0, 0)) - T; d_esc /= np.linalg.norm(d_esc)     # dirección de la escalera desde el eje

fig = plt.figure(figsize=(16.5, 11.7))
fig.suptitle("MAQUETA DESMONTABLE – cómo se divide (propuesta para revisar)", fontsize=15, weight="bold", x=0.02, ha="left", y=0.985)
fig.text(0.02, 0.953, f"El TAMBOR (barril de habitaciones, tambor, banda, visera, remate y letras) es una pieza con un cilindro que baja. La BASE (columna, cuello, escalera inferior, alas, concha y restaurante) "
         f"lleva un hueco circular.  Corte a z = {ZC:.2f} m (fondo de las vigas).", fontsize=8.5, va="top")

# ---------------------------------------------------------------- 1) SECCIÓN POR EL EJE DE LA ESCALERA
ax = fig.add_axes([0.03, 0.06, 0.40, 0.85])
p0, p1 = E.esc_pt(22.0, 0), E.esc_pt(-22.0, 0)
from shapely.geometry import Polygon as SP, box as SB
from shapely.ops import unary_union
a_ = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
cs = LM.orientar(LM.M, p0, a_).slice(0.0)                                 # corte real del modelo por el eje de la escalera
corte = unary_union([SP(np.array(q)).buffer(0) for q in cs.to_polygons() if len(q) > 2])
uT = 22.0                                                                 # el eje de la torre está a 22 m del extremo de la sección
canal = SB(uT - CH_R, ZC - HP - PROF_EXTRA, uT - RP - HOLG, ZC)           # surco de entrada + canal de la llave: abierto por arriba, lado de la escalera (izquierda)
socket = unary_union([SB(uT - RP - HOLG, ZC - HP - PROF_EXTRA, uT + RP + HOLG, ZC), canal])    # hueco de la base
plug = unary_union([SB(uT - RP, ZC - HP, uT + RP, ZC), SB(uT - RP - KP, ZC - HP, uT - RP, ZC)])   # cilindro del tambor con su llave (nervio de todo el largo)
pieza1 = unary_union([corte.intersection(SB(-100, ZC, 200, 100)), plug])
pieza2 = corte.intersection(SB(-100, -10, 200, ZC)).difference(socket)
def pinta(g, hatch, lw, z):
    for q in getattr(g, "geoms", [g]):
        if q.geom_type == "Polygon" and not q.is_empty:
            ax.add_patch(Polygon(np.c_[q.exterior.xy], closed=True, fc="white", ec="k", lw=lw, hatch=hatch, zorder=z))
            for h in q.interiors:
                ax.add_patch(Polygon(np.c_[h.xy], closed=True, fc="white", ec="k", lw=lw, zorder=z + 0.1))
pinta(pieza2, "\\\\\\", 0.9, 5.0); pinta(pieza1, "//////", 0.9, 6.0)             # la pieza 1 (con su cilindro) por encima de la base
ax.axhline(0, color="k", lw=1.8)
ax.set_xlim(uT - 17.5, uT + 17.5); ax.set_ylim(-2.0, 54.0); ax.set_aspect("equal"); ax.axis("off")
ax.axhline(ZC, color="k", lw=1.1, ls=(0, (10, 2, 2, 2)), zorder=70)
ax.text(uT - 17.3, ZC + 0.5, f"plano de corte  z = {ZC:.2f}", fontsize=8, weight="bold", va="bottom", zorder=71, bbox=dict(fc="white", ec="none", pad=1))
ax.add_patch(Polygon(np.c_[socket.exterior.xy], closed=True, fc="none", ec="k", lw=0.8, ls=(0, (3, 2)), zorder=67))
ax.text(uT, ZC - HP / 2, "cilindro", fontsize=7, ha="center", va="center", zorder=68, bbox=dict(fc="white", ec="none", pad=0.6))
ax.annotate("hueco circular\nen la base", (uT + RP + HOLG, ZC - HP + 0.3), (uT + 9.5, ZC - 6.5), fontsize=7.5, zorder=72,
            arrowprops=dict(arrowstyle="-", lw=0.5), bbox=dict(fc="white", ec="none", pad=0.8))
ax.annotate("llave: nervio vertical del cilindro,\nentra por el surco y baja por el canal", (uT - RP - KP / 2, ZC - HP / 2), (uT - 15.2, ZC - 5.4), fontsize=7.5, zorder=72,
            arrowprops=dict(arrowstyle="-", lw=0.5), bbox=dict(fc="white", ec="none", pad=0.8))
# llaves de pieza: corchetes laterales
xb = uT - 16.8
for z0, z1, txt in ((ZC, E.Z_R1, "PIEZA 1 · TAMBOR"), (0.0, ZC, "PIEZA 2 · BASE")):
    ax.plot([xb, xb + 0.5, xb + 0.5, xb], [z0 + 0.15, z0 + 0.15, z1 - 0.15, z1 - 0.15], color="k", lw=1.0, zorder=72)
    ax.text(xb - 0.5, (z0 + z1) / 2, f"{txt}\n{z1 - z0:.1f} m", fontsize=8, weight="bold", rotation=90, ha="right", va="center", zorder=72)
L.cota(ax, (uT + 15.3, ZC), (uT + 15.3, E.Z_R1), 0.0, "", fs=6.5)
ax.set_title(f"Corte por el eje de la escalera · trama / = pieza 1 (tambor) · trama \\ = pieza 2 (base) · cuello Ø {2 * E.R_CU:.0f} m, barril Ø {2 * E.R_B:.1f} m", fontsize=8.5, loc="left")

# ---------------------------------------------------------------- 2) PLANTA EN EL CORTE
axp = fig.add_axes([0.47, 0.50, 0.24, 0.41])
LM.planta(axp, ZC - 0.6, "")                 # lo que queda por debajo del corte: el cuello con el hueco
for t in list(axp.texts):
    t.set_visible(False)
axp.set_xlim(T[0] - 19.5, T[0] + 19.5); axp.set_ylim(T[1] - 19.5, T[1] + 19.5); axp.set_aspect("equal"); axp.axis("off")
axp.add_patch(Circle(T, E.R_CU, fill=False, ec="k", lw=1.2, zorder=60))
axp.add_patch(Circle(T, RP + HOLG, fill=False, ec="k", lw=1.2, ls=(0, (3, 2)), zorder=61))
axp.add_patch(Circle(T, RP, fill=False, ec="k", lw=0.5, zorder=61))
n_ = np.array([-d_esc[1], d_esc[0]]); c_ = T + d_esc * (RP + KP / 2)
axp.add_patch(Polygon([c_ + d_esc * KP / 2 + n_ * KW / 2, c_ + d_esc * KP / 2 - n_ * KW / 2, c_ - d_esc * KP / 2 - n_ * KW / 2, c_ - d_esc * KP / 2 + n_ * KW / 2],
                      closed=True, fc="white", ec="k", lw=1.0, zorder=62))
cc_ = T + d_esc * ((RP + HOLG + CH_R) / 2); hl, hw = (CH_R - RP - HOLG) / 2, CH_W / 2
axp.add_patch(Polygon([cc_ + d_esc * hl + n_ * hw, cc_ + d_esc * hl - n_ * hw, cc_ - d_esc * hl - n_ * hw, cc_ - d_esc * hl + n_ * hw], closed=True, fc="none", ec="k", lw=0.9, ls=(0, (3, 2)), zorder=61))
axp.annotate("llave (cilindro) y\nsurco + canal (hueco),\nlado de la escalera", tuple(c_), tuple(T + d_esc * 11.0 - n_ * 9.5), fontsize=7, zorder=72,
             arrowprops=dict(arrowstyle="-", lw=0.5), bbox=dict(fc="white", ec="none", pad=0.8), ha="left")
axp.annotate("hueco Ø %.2f" % (2 * (RP + HOLG)), tuple(T + np.array([-RP - HOLG, 0.0]) * 0.7), tuple(T + np.array([-16.0, -6.0])), fontsize=7, zorder=72,
             arrowprops=dict(arrowstyle="-", lw=0.5), bbox=dict(fc="white", ec="none", pad=0.8))
axp.annotate("cuello Ø %.0f" % (2 * E.R_CU), tuple(T + np.array([-E.R_CU * 0.72, E.R_CU * 0.72])), tuple(T + np.array([-17.0, 10.0])), fontsize=7, zorder=72,
             arrowprops=dict(arrowstyle="-", lw=0.5), bbox=dict(fc="white", ec="none", pad=0.8))
axp.set_title(f"Planta justo bajo el corte (z = {ZC - 0.6:.1f}): el cuello con su hueco", fontsize=8.5, loc="left")

# ---------------------------------------------------------------- 3) DETALLE DEL ENCAJE (separado para verlo)
axd = fig.add_axes([0.73, 0.50, 0.25, 0.41])
R9 = E.R_CU
sep = 5.0                                    # separación de las dos piezas para ver el encaje (m)
# BASE: cuello con el hueco
axd.add_patch(Polygon([(-R9, -7), (R9, -7), (R9, 0), (CH_R, 0), (CH_R, -HP - PROF_EXTRA), (-RP - HOLG, -HP - PROF_EXTRA), (-RP - HOLG, 0), (-R9, 0)],
                      closed=True, fc="white", ec="k", lw=1.3, hatch="\\\\\\\\", zorder=5))
axd.plot([RP + HOLG, RP + HOLG], [-HP - PROF_EXTRA, 0], color="k", lw=0.6, ls=(0, (3, 2)), zorder=6)      # pared del hueco, detrás del canal
axd.plot([-R9 - 0.8, R9 + 0.8], [-7, -7], color="k", lw=0.5)
for x_ in (-R9, R9): axd.plot([x_, x_], [-7, -7.9], color="k", lw=0.5, ls=(0, (6, 2)))
# TAMBOR: pie del cuello + vigas + cilindro con su llave
zt = sep                                     # fondo del tambor
axd.add_patch(Polygon([(-R9, zt), (R9, zt), (R9, zt + 6.5), (-R9, zt + 6.5)], closed=True, fc="white", ec="k", lw=1.3, hatch="////", zorder=5))
axd.add_patch(Rectangle((-RP, zt - HP), 2 * RP, HP, fc="white", ec="k", lw=1.3, hatch="////", zorder=6))
axd.add_patch(Rectangle((RP, zt - HP), KP, HP, fc="white", ec="k", lw=1.3, hatch="////", zorder=6))      # llave: nervio de todo el largo
axd.plot([-R9 - 0.8, R9 + 0.8], [zt + 6.5, zt + 6.5], color="k", lw=0.5, ls=(0, (2, 2)))
axd.text(0, zt + 3.2, "TAMBOR (sigue hasta z = %.2f)" % E.Z_R1, fontsize=7.5, ha="center", va="center", zorder=9, bbox=dict(fc="white", ec="none", pad=1))
axd.text(0, -4.3, "BASE", fontsize=8, weight="bold", ha="center", va="center", zorder=9, bbox=dict(fc="white", ec="none", pad=1))
for x_ in (-3.0, 3.0):                      # flechas de montaje
    axd.annotate("", (x_, 0.6), (x_, zt - 0.6), arrowprops=dict(arrowstyle="-|>", lw=0.9), zorder=10)
axd.text(-6.9, sep / 2 + 0.2, "se encaja", fontsize=7.5, ha="center", va="center", zorder=11, bbox=dict(fc="white", ec="none", pad=1))
# cotas del encaje
L.cota(axd, (-RP, zt - HP - 0.7), (RP, zt - HP - 0.7), 0.0, "", fs=6.5)
axd.text(0, zt - HP - 1.9, f"cilindro Ø {2 * RP:.1f} · largo {HP:.1f}", fontsize=7, ha="center", va="top", zorder=11)
L.cota(axd, (-RP - HOLG, -HP - PROF_EXTRA - 0.7), (RP + HOLG, -HP - PROF_EXTRA - 0.7), 0.0, "", fs=6.5)
axd.text(0, -HP - PROF_EXTRA - 1.9, f"hueco Ø {2 * (RP + HOLG):.2f} · fondo {HP + PROF_EXTRA:.1f}  (holgura {HOLG} por lado)", fontsize=7, ha="center", va="top", zorder=11)
axd.annotate(f"llave {KW} × {KP}\n(nervio de todo el largo)", (RP + KP / 2, zt - HP / 2), (RP + 3.3, zt + 0.2), fontsize=7, zorder=11,
             arrowprops=dict(arrowstyle="-", lw=0.5), bbox=dict(fc="white", ec="none", pad=0.8))
axd.annotate(f"surco de entrada\n(abierto por arriba)\ny canal {CH_W:.1f} × {KP + HOLG:.2f}", (RP + HOLG + KP / 2, -1.0), (RP + 1.2, -9.8), fontsize=7, zorder=11,
             arrowprops=dict(arrowstyle="-", lw=0.5), bbox=dict(fc="white", ec="none", pad=0.8))
axd.set_xlim(-R9 - 1.5, R9 + 7.5); axd.set_ylim(-11.0, zt + 7.2); axd.set_aspect("equal"); axd.axis("off")
axd.set_title("Detalle del encaje (m reales; maqueta Ø %.1f mm, largo %.1f mm)" % (2 * RP * K, HP * K), fontsize=8.5, loc="left")

# ---------------------------------------------------------------- 4) LOS CUATRO MODELOS
axt = fig.add_axes([0.47, 0.03, 0.51, 0.41]); axt.set_xlim(0, 100); axt.set_ylim(0, 46); axt.axis("off")
axt.set_title("Los cuatro modelos que saldrán, cuando apruebes la división", fontsize=9.5, loc="left", weight="bold")
filas = [("1", "ORIGINAL, todo el detalle", "una pieza", "Hotel_Salut_15cm_v3.stl (ya existe, copia)"),
         ("2", "MENOS DETALLE (para molde)", "una pieza", "Hotel_Salut_15cm_MOLDE.stl (ya existe, copia)"),
         ("3", "TODO EL DETALLE, DESMONTABLE", "2 piezas: tambor + base", "…_v3_DESMONTABLE_tambor.stl y …_base.stl"),
         ("4", "MENOS DETALLE, DESMONTABLE", "2 piezas: tambor + base", "…_MOLDE_DESMONTABLE_tambor.stl y …_base.stl")]
axt.plot([0, 100], [41, 41], color="k", lw=0.8)
for x_, t_ in ((1, "nº"), (6, "modelo"), (46, "piezas"), (66, "archivos")):
    axt.text(x_, 43, t_, fontsize=8.5, weight="bold", va="center")
for i, (a_, b_, c2, d2) in enumerate(filas):
    y_ = 37.5 - i * 6
    axt.plot([0, 100], [y_ - 3, y_ - 3], color="k", lw=0.3)
    for x_, t_ in ((1, a_), (6, b_), (46, c2), (66, d2)):
        axt.text(x_, y_, t_, fontsize=8, va="center")
axt.text(1, 14.0, "DECISIONES QUE TE PIDO CONFIRMAR", fontsize=8.5, weight="bold", va="center")
axt.text(1, 9.0, f"1. Corte a z = {ZC:.2f} (fondo de las vigas): el tambor lleva vigas, aletas, forjado plano y la escalera por encima del corte; la escalera por debajo queda en la base.\n"
         f"2. Cilindro Ø {2 * RP:.1f} m (maqueta {2 * RP * K:.0f} mm), largo {HP:.1f} m ({HP * K:.0f} mm), holgura {HOLG} m ({HOLG * K:.1f} mm) por lado.\n3. Llave, surco y canal: nervio vertical de {KW} × {KP} m en el cilindro (lado de la escalera) que entra por un surco abierto en el borde del hueco\n    y baja por un canal de {CH_W:.1f} × {KP + HOLG:.2f} m hasta el fondo: el tambor se baja recto y no gira.",
         fontsize=7.5, va="center", linespacing=1.6)
axt.text(1, 3.0, "En los dos desmontables, cada pieza tiene la misma geometría que el modelo entero: solo se corta por el plano, se añade el cilindro a una y se vacía el hueco en la otra.\n"
         "Pasan las mismas comprobaciones (estancas, sin aristas no manifold) y cada una tendrá su versión de baja resolución para los proveedores.", fontsize=7.5, va="center", linespacing=1.6)
fig._recolocado = True                                   # hoja con tabla y cotas: la colocación es a mano, sin recolocación automática
fig.savefig("DESMONTABLE_DIVISION.png", dpi=110); print("ok")
