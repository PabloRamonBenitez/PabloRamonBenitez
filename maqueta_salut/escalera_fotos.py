"""Caja de escalera: medidas en la foto lateral (escala propia por las juntas de las lamas, 3,10 m), lectura del dron
y collage de Alamy, frente al modelo."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import edificio as E, laminas as LM, vista_alamy as VA

V = E._v; IMG = LM.IMG
fig = plt.figure(figsize=(22, 13))
# 1) foto lateral (coordenadas de la captura original 1080x2400)
a1 = fig.add_axes([0.01, 0.06, 0.25, 0.86]); im = Image.open(IMG + "esc_lateral.png").convert("RGB")
a1.imshow(im.crop((300, 650, 1000, 1900))); a1.axis("off")
ox, oy = 300, 650; px_m = 138 / 3.10
def cota(x, y0, y1, t, col="crimson"):
    a1.plot([x - ox] * 2, [y0 - oy, y1 - oy], color=col, lw=2.5); a1.text(x - ox + 8, (y0 + y1) / 2 - oy, t, color=col, fontsize=9, weight="bold", va="center", bbox=dict(fc="white", ec="none", alpha=0.8))
yc0, yl0 = 707, 842          # cubierta del remate y coronación de las lamas (px de la captura)
cota(860, yc0, yl0, f"remate de hormigón {(yl0 - yc0) / px_m:.2f} m")
for k in range(6):
    yy = 842 + 138 * k; a1.plot([680 - ox, 760 - ox], [yy - oy] * 2, color="#16b5e8", lw=1.5)
a1.text(690 - ox, 842 + 138 * 5.4 - oy, "juntas de lamas = forjados\n138 px = 3,10 m", color="#0b7fa6", fontsize=8, bbox=dict(fc="white", ec="none", alpha=0.8))
a1.annotate("", (462 - ox, 1000 - oy), (728 - ox, 1000 - oy), arrowprops=dict(arrowstyle="<->", color="crimson", lw=1.5))
a1.text(500 - ox, 985 - oy, f"frente de lamas {(728 - 462) / px_m:.1f} m", color="crimson", fontsize=9, bbox=dict(fc="white", ec="none", alpha=0.8))
a1.set_title("Foto lateral (de frente a la caja: la pendiente no se ve): remate ~3 m sin lamas", fontsize=10, loc="left", weight="bold")
# 2) dron
a2 = fig.add_axes([0.27, 0.06, 0.25, 0.86]); im2 = Image.open(IMG + "esc_dron.png").convert("RGB")
a2.imshow(im2.crop((300, 300, 1080, 1500))); a2.axis("off")
for (x, y, t) in ((640, 560, "muro / lucernario con la coronación\nINCLINADA (sube hacia fuera)"), (820, 900, "el peto del tambor\nse corta en la escalera"),
                  (830, 1250, "lamas por fuera\ndel barril"), (380, 700, "terraza del tambor")):
    a2.text(x - 300, y - 300, t, color="crimson", fontsize=9, weight="bold", bbox=dict(fc="white", ec="crimson", alpha=0.85))
a2.set_title("Dron: coronación inclinada sobre la terraza del tambor; lamas finas", fontsize=10, loc="left", weight="bold")
# 3) collage Alamy en la zona de la escalera
a3 = fig.add_axes([0.54, 0.30, 0.45, 0.62])
PV, PH, Y0, YR, XT = 175.25 / 3.10, 64.4, 887, 1337, 1078
z = lambda y: E.Z_B1 + (YR - y) / PV; s = lambda x: (x - XT) / PH
ima = Image.open("/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/scratchpad/alamy.jpg").convert("RGB")
W, H = ima.size; cr = ima.crop((0, Y0 + 150, W, Y0 + 2200)); XTm = VA.x_eje_alzado()
LM.alzado(a3, VA.MIRA, "")
a3.imshow(cr, extent=(XTm + s(0), XTm + s(W), z(2200), z(150)), aspect="auto", alpha=0.5, zorder=100)
a3.set_xlim(XTm - 18, XTm - 2); a3.set_ylim(33, 45); a3.set_aspect("equal")
a3.axhline(V["ESC_Z1"], color="crimson", lw=1, ls="--"); a3.text(XTm - 17.8, V["ESC_Z1"] + 0.15, f"coronación fuera +{V['ESC_Z1']:.2f} → dentro +{V['ESC_ZI']:.2f}".replace(".", ","), color="crimson", fontsize=8)
a3.axhline(V["ESC_ZL"], color="#a0522d", lw=1, ls="--"); a3.text(XTm - 17.8, V["ESC_ZL"] + 0.15, f"fin de lamas +{V['ESC_ZL']:.2f}".replace(".", ","), color="#a0522d", fontsize=8)
a3.set_title("Alamy al 50 % sobre el modelo – caja de escalera", fontsize=10, loc="left", weight="bold")
fig.text(0.54, 0.08, "\n".join([
    f"Modelo: hueco {V['ESC_SEC']}° (2 módulos), cuña {V['ESC_SECB']}°, caja por encima del tambor de r {V['ESC_RS']} a {V['ESC_R1']} (+ lamas 0,3)",
    f"coronación inclinada +{V['ESC_Z1']:.2f} fuera → +{V['ESC_ZI']:.2f} dentro (Alamy de perfil, dron) · lamas de {V['LAMA_E']:.2f} cada {V['LAMA_P']:.2f} hasta +{V['ESC_ZL']:.2f} (foto lateral: remate de 2,97 m)",
    "frente de lamas en la foto lateral 6,0 m (+ escalera de gato 0,7) · cuerda de la cuña a r 15,9: 6,9 m (vista algo oblicua)"]).replace(".", ","), fontsize=9, va="bottom")
fig.suptitle("CAJA DE ESCALERA – foto lateral, dron y Alamy frente al modelo", fontsize=13, x=0.01, ha="left", weight="bold")
fig.savefig("ESCALERA_FOTOS.png", dpi=75)
print("ok")
