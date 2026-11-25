"""Planta de comprobación de la torre: 19 muros radiales con su ángulo, hueco de escalera, ojos, lado ciego,
desplazamientos de banda / visera / remate / lucernario y dirección de la cámara de Alamy (VISTA_ALAMY)."""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge
import edificio as E, ventanas as VE, vista_alamy as VA

V = E._v; T = np.array(E.T)
fig, ax = plt.subplots(figsize=(13, 13))
for r, c, lw in ((V["R_AL"], "0.6", 0.6), (V["R_B"], "k", 1.0), (V["R_T"], "#1a9b4b", 1.4)):
    ax.add_patch(Circle(T, r, fill=False, ec=c, lw=lw))
for nm, (ox, oy), R, col in (("banda", (V["OB_X"], V["OB_Y"]), V["R_G"], "#2a6fdb"), ("visera", (V["OV_X"], V["OV_Y"]), V["R_V"], "#e0a000"),
                             ("remate", (V["OR_X"], V["OR_Y"]), V["R_R"], "#d43c3c"), ("lucernario", (V["LUC_X"], V["LUC_Y"]), V["LUC_R"], "purple")):
    p = np.array(E.P(ox, oy)); ax.add_patch(Circle(p, R, fill=False, ec=col, lw=1.6, ls="--" if nm == "visera" else "-"))
    ax.plot(*p, "+", color=col, ms=10); ax.text(p[0] + 0.3, p[1] + 0.3, nm, color=col, fontsize=8)
a0, a1 = math.degrees(E.ESC_ANG - E.ESC_HA), math.degrees(E.ESC_ANG + E.ESC_HA)
ax.add_patch(Wedge(T, V["ESC_R1"], a0, a1, width=V["ESC_R1"] - V["ESC_R0"], fc="#f2d7b6", ec="#a0522d", lw=1))
ax.text(*E.esc_ang_pt(V["ESC_R1"] + 1.5, 0), f"escalera\nhueco {V['ESC_SEC']}° = 2 módulos", ha="center", fontsize=8, color="#a0522d")
ax.add_patch(Wedge(T, V["R_T"] + 2.5, V["OJO_C0"], V["OJO_C1"], width=1.0, fc="0.8", ec="none"))
m = np.array([math.cos(math.radians((V["OJO_C0"] + V["OJO_C1"]) / 2)), math.sin(math.radians((V["OJO_C0"] + V["OJO_C1"]) / 2))])
ax.text(*(T + (V["R_T"] + 4) * m), f"lado ciego\n{V['OJO_C0']:.0f}°–{V['OJO_C1']:.0f}°", ha="center", fontsize=8, color="0.3")
for k in range(V["N_AL"]):
    a = 2 * math.pi * k / V["N_AL"] + E.FASE_AL; u = np.array([math.cos(a), math.sin(a)])
    ax.plot(*zip(T + (E.R_B - 1.8) * u, T + V["R_AL"] * u), color="k", lw=2)
    ax.text(*(T + (V["R_AL"] + 0.9) * u), f"M{k}\n{math.degrees(a) % 360:.1f}°", ha="center", va="center", fontsize=6.5)
for h in VE.catalogo():
    if h["grupo"] == "tambor ojos":
        ax.plot(*h["p"], "o", ms=9, mfc="white", mec="#1a9b4b", mew=1.5)
cam = VA.HACIA_CAMARA
ax.annotate("", T + 26 * cam, T + 19 * cam, arrowprops=dict(arrowstyle="<-", lw=2, color="crimson"))
ax.text(*(T + 27 * cam), f"cámara Alamy\n{V['VISTA_ALAMY']}°", color="crimson", ha="center", fontsize=9)
ax.plot(*zip(T - 18 * VA.DERECHA, T + 18 * VA.DERECHA), color="crimson", lw=0.6, ls=":")
ax.text(*(T + 18.5 * VA.DERECHA), "derecha de la foto", color="crimson", fontsize=7)
ax.set_aspect("equal"); ax.set_xlim(T[0] - 31, T[0] + 31); ax.set_ylim(T[1] - 31, T[1] + 31); ax.axis("off")
n_oj = sum(1 for h in VE.catalogo() if h["grupo"] == "tambor ojos")
ax.set_title(f"TORRE EN PLANTA – 19 muros (giro {V['FASE_AL']}°), {n_oj} ojos, escalera entre M3 y M5, dirección de la foto de Alamy", fontsize=11, loc="left", weight="bold")
fig.text(0.02, 0.02, "Dirección de Alamy fijada con la cuña de la escalera (borde izquierdo de la silueta, s −15,8…−16,2) y con 5 aletas (dispersión 0,8°).\n"
         "Descartadas 160,8° (la escalera taparía los balcones de la izquierda) y 198,7° (quedaría oculta). Muros M3 y M5 = bordes del hueco de escalera.", fontsize=8)
fig.savefig("PLANTA_ORIENTACION_ALAMY.png", dpi=80, bbox_inches="tight")
print("ok", n_oj)
