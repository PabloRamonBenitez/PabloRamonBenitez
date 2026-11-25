"""MGF en F09 (frontal desde la calle): alzado completo de la torre comprobado por proporciones.

1. Ajuste proyectivo 1D  z = (a·y + b)/(c·y + 1)  con las caras inferiores de los 7 forjados del barril (+13,90 … +32,50),
   leídas sobre el eje de la torre: da la cota de cualquier punto que esté en el plano del frente de balcones (R_B).
2. Lo que está más atrás (e > 0) o más delante (e < 0) de ese plano se ve más bajo o más alto:
   z_aparente = h + (z − h)·D / (D + e),  con h = 1,6 m (cámara a pie de calle) y D = distancia de la cámara (ajustada).
3. Con D ajustada en las piezas altas ya fijadas por Alamy (tambor, visera, remate) se leen las piezas bajas."""
import math, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
from scipy.optimize import least_squares
import edificio as E
import laminas as LM

V = E._v
IMG = sys.argv[1] if len(sys.argv) > 1 else LM.IMG + "9.webp"
H_CAM = 1.6
# caras inferiores de los forjados (y px, sobre el eje de la torre x≈300–330) [perfil vertical de F09]
Y_FOR = np.array([369, 409, 449, 490, 530, 571, 611.])
Z_FOR = np.array([E.Z_B0 + i * E.F for i in range(7)])[::-1]
r = least_squares(lambda p: (p[0] * Y_FOR + p[1]) / (p[2] * Y_FOR + 1) - Z_FOR, [-0.077, 61, 0.0])
a, b, c = r.x
zplano = lambda y: (a * y + b) / (c * y + 1)
yplano = lambda z: (b - z) / (c * z - a)
rms_for = float(np.sqrt((r.fun ** 2).mean()))

# profundidad respecto al frente de balcones (cámara del lado −N; e > 0 = más atrás)
dfront = lambda off_u, off_n, R: -off_n + math.sqrt(max(R * R - off_u * off_u, 0))
e_t = V["R_B"] - V["R_T"]
e_v = V["R_B"] - dfront(V["OV_X"], V["OV_Y"], V["R_V"])
e_r = V["R_B"] - dfront(V["OR_X"], V["OR_Y"], V["R_R"])
e_c = V["R_B"] - (V["R_CU"] + 0.6)
apar = lambda z, e, D: H_CAM + (z - H_CAM) * D / (D + e)
real = lambda za, e, D: H_CAM + (za - H_CAM) * (D + e) / D

LEC = [  # (nombre, y medida, e, cota del modelo)
    ("tambor: coronación", 290, e_t, E.Z_T1),
    ("visera: cara inferior", 251, e_v, E.Z_G1),
    ("remate: coronación", 156, e_r, E.Z_R1),
]
D = least_squares(lambda p: [apar(zm, e, p[0]) - zplano(y) for _, y, e, zm in LEC], [200.0], bounds=(20, 2000)).x[0]
filas = [(n, y, e, zplano(y), real(zplano(y), e, D), zm) for n, y, e, zm in LEC]
y_cu = 677                                                   # borde inferior del cuello (losa volada)
filas.append(("cuello: base (losa volada)", y_cu, e_c, zplano(y_cu), real(zplano(y_cu), e_c, D), V["Z_CU0"]))
filas.append(("visera: cara superior", 222, e_v, zplano(222), real(zplano(222), e_v, D), E.Z_V1))

# ---- lámina: alzado del modelo desde −N  |  F09 rectificada a cotas del plano de balcones
fig, (a1, a2) = plt.subplots(1, 2, figsize=(21, 12), gridspec_kw=dict(width_ratios=[1.15, 1], wspace=0.05))
LM.alzado(a1, tuple(E.N), "")
_ang = math.radians(-(math.degrees(math.atan2(E.N[1], E.N[0])) - 90))
XT = math.cos(_ang) * E.T[0] - math.sin(_ang) * E.T[1]
a1.set_xlim(XT - 24, XT + 30); a1.set_ylim(-1, 53); a1.set_aspect("equal")
a1.set_title("MODELO corregido – alzado de la torre desde la plaza (−N)", fontsize=10, loc="left", weight="bold")
im = Image.open(IMG).convert("RGB"); W, Hh = im.size
y_top, y_bot = 60, 860
zs = np.linspace(zplano(y_bot), zplano(y_top), 900)
ys = np.clip(yplano(zs), 0, Hh - 1).astype(int)
arr = np.asarray(im)[ys[::-1]]
PHx = 13.4
a2.imshow(arr, extent=((0 - 305) / PHx, (W - 305) / PHx, zs[0], zs[-1]), aspect="auto")
a2.set_xlim(-24, 30); a2.set_ylim(-1, 53); a2.set_aspect("equal")
a2.set_title("F09 rectificada: cotas sobre el plano del frente de balcones (ajuste con los 7 forjados)", fontsize=10, loc="left", weight="bold")
cols = ["#1a9b4b", "#e0a000", "#d43c3c", "#7b4bb5", "#c07000"]
for (n, y, e, zap, zr, zm), col in zip(filas, cols):
    zmod_ap = apar(zm, e, D)
    a2.plot([-22, 22], [zplano(y)] * 2, color=col, lw=1.6)
    a2.plot([-22, 22], [zmod_ap] * 2, color=col, lw=1.0, ls="--")
    a2.text(22.3, zplano(y), f"{n}: foto +{zr:.2f} / modelo +{zm:.2f}".replace(".", ","), color=col, fontsize=7.5, va="center")
    a1.plot([XT - 22, XT + 22], [zm] * 2, color=col, lw=0.8, ls="--")
for zf in Z_FOR:
    a2.plot([-16, -14], [zf, zf], color="crimson", lw=2)
a2.text(-23.5, Z_FOR.mean(), f"7 forjados\najuste rms {rms_for:.2f} m".replace(".", ","), color="crimson", fontsize=7.5, va="center", rotation=90)
txt = [f"F09 – ajuste proyectivo con 7 forjados (rms {rms_for:.3f} m); cámara a {H_CAM} m, distancia ajustada D = {D:.0f} m (con tambor, visera y remate)",
       "pieza                       e (m)   aparente   real (foto)   modelo    dif"]
for n, y, e, zap, zr, zm in filas:
    txt.append(f"{n:27s} {e:+5.1f}   +{zap:5.2f}    +{zr:5.2f}      +{zm:5.2f}   {zr - zm:+.2f}")
txt.append("línea continua = borde medido en F09 · discontinua = cota del modelo llevada a F09 con su profundidad")
fig.text(0.02, 0.01, "\n".join(txt).replace(".", ","), family="monospace", fontsize=9, va="bottom")
fig.suptitle("Alzado completo de la torre comprobado por proporciones (MGF sobre F09)", fontsize=12, x=0.02, ha="left", weight="bold")
fig.subplots_adjust(bottom=0.17, top=0.94, left=0.03, right=0.99)
fig.savefig("MGF_F09_TORRE.png", dpi=75)
print("\n".join(txt))
