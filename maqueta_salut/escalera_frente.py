"""Escalera vista de frente: foto (usuario, 25/11) junto al alzado del modelo en la misma dirección (mirando hacia el eje de la torre)."""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import edificio as E, laminas as LM

V = E._v
mira = (-math.cos(E.ESC_ANG), -math.sin(E.ESC_ANG))           # de frente a la escalera, hacia la torre
fig = plt.figure(figsize=(22, 13))
a1 = fig.add_axes([0.01, 0.05, 0.27, 0.88]); a1.imshow(Image.open(LM.IMG + "esc_frente.png").convert("RGB")); a1.axis("off")
a1.set_title("Foto: frente de la escalera (lamas en los bordes del corte del barril)", fontsize=10, loc="left", weight="bold")
a2 = fig.add_axes([0.29, 0.05, 0.27, 0.88]); a2.imshow(Image.open(LM.IMG + "esc_frente_alta.png").convert("RGB")); a2.axis("off")
a2.set_title("Foto: remate (verde), fin de lamas (amarillo), puerta ~2 m (rojo)", fontsize=10, loc="left", weight="bold")
a3 = fig.add_axes([0.58, 0.12, 0.41, 0.80])
LM.alzado(a3, mira, "")
a = math.radians(-(math.degrees(math.atan2(mira[1], mira[0])) - 90)); xe = math.cos(a) * E.T[0] - math.sin(a) * E.T[1]
a3.set_xlim(xe - 14, xe + 14); a3.set_ylim(12, 46); a3.set_aspect("equal")
for zz, t, col in ((V["ESC_Z1"], "remate +%.2f (fuera)" % V["ESC_Z1"], "green"), (V["ESC_ZL"], "fin de lamas +%.2f" % V["ESC_ZL"], "#d4a000"), (E.Z_T1, "tambor +%.2f" % E.Z_T1, "crimson")):
    a3.axhline(zz, color=col, lw=0.8, ls="--"); a3.text(xe + 9, zz + 0.2, t.replace(".", ","), color=col, fontsize=8)
w = 2 * V["ESC_R1"] * math.sin(math.radians(V["ESC_SECB"] / 2)); g = 13 * math.sin(math.radians((V["ESC_SEC"] - V["ESC_SECB"]) / 2))
a3.set_title("MODELO de frente a la escalera", fontsize=10, loc="left", weight="bold")
fig.text(0.58, 0.03, (f"cuña {V['ESC_SECB']}° → frente de lamas {w:.1f} m con {int(V['LAMA_N'])} lamas · hueco del barril {V['ESC_SEC']}° (2 módulos) → {g:.1f} m entre el corte y la cuña (una puerta)\n"
                      f"bordes del corte del barril cerrados con lamas de +{E.Z_B0:.2f} a +{E.Z_T1:.2f} · lamas del cuerpo hasta +{V['ESC_ZL']:.2f}; remate inclinado +{V['ESC_ZI']:.2f} → +{V['ESC_Z1']:.2f}").replace(".", ","), fontsize=9)
fig.suptitle("ESCALERA DE FRENTE – fotos del usuario frente al modelo", fontsize=13, x=0.01, ha="left", weight="bold")
fig.savefig("ESCALERA_FRENTE.png", dpi=75)
print("ok", round(w, 2), round(g, 2))
