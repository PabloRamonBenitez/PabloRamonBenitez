"""MGF aplicado al tambor y al barril (foto de Alamy): aletas, ojos y balcones.

Un elemento a radio R y ángulo φ respecto al eje de la vista se proyecta en x = R·sen φ (vista casi ortogonal).
Se comparan con la foto la posición de las aletas (postes blancos de los balcones), la de los ojos (centros oscuros),
su tamaño y su cota, el paso de forjados y el radio del borde de balcones."""
import sys, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
from scipy.ndimage import gaussian_filter1d, label
from scipy.signal import find_peaks
import edificio as E, ventanas as VE

V = E._v
FOTO = sys.argv[1] if len(sys.argv) > 1 else "/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/scratchpad/alamy.jpg"
PV, PH, XT, Y_REF = 175 / 3.10, 64.4, 1078, 1306
z = lambda y: E.Z_B1 + 0.65 + (Y_REF - y) / PV     # y = 1306: cara superior del canto de la losa de cubierta
T, U, N = np.array(E.T), np.array(E.U), np.array(E.N)
xpx = lambda p: XT - ((np.asarray(p) - T) @ N) * PH          # derecha de la foto = −N
delante = lambda p: (np.asarray(p) - T) @ U < 0               # cámara del lado −U

im = Image.open(FOTO).convert("RGB"); W, H = im.size; y0 = int(H * 0.22)
g = np.asarray(im.convert("L")).astype(float)[y0:int(H * 0.62)]

# --- foto: postes (aletas) en la fila de balcones
p = gaussian_filter1d(g[1350:1420, :].mean(0), 3)
pk, pr = find_peaks(p, prominence=15, distance=60)
postes = np.array([x for x, h in zip(pk, p[pk]) if h > 150 and 400 < x < 2000], float)
# --- foto: ojos (núcleos oscuros dentro del tambor, a la derecha de la zona ciega)
lab, n = label(g[1090:1215, 850:2000] < 60)
ojos = []
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(xs) > 1500:
        ojos.append((xs.mean() + 850, ys.min() + 1090, ys.max() + 1090, xs.min() + 850, xs.max() + 850))
# --- modelo
alet = []
for k in range(V["N_AL"]):
    a = 2 * math.pi * k / V["N_AL"] + E.FASE_AL
    q = T + V["R_AL"] * np.array([math.cos(a), math.sin(a)])
    if delante(q): alet.append(xpx(q))
alet = np.array(sorted(alet))
ojm = sorted(xpx(T + (np.asarray(h["p"]) - T) * (E.R_T + V["OJO_V"]) / E.R_T) for h in VE.catalogo()
             if h["grupo"] == "tambor ojos" and delante(h["p"]))      # aro al final del tubo (vuelo OJO_V)

res_al = [postes_i - alet[np.argmin(abs(alet - postes_i))] for postes_i in postes]
res_oj = [o[0] - min(ojm, key=lambda m: abs(m - o[0])) for o in ojos]
d_oj = np.median([(o[2] - o[1]) / PV for o in ojos])
z_oj = np.median([z((o[1] + o[2]) / 2) for o in ojos])
# paso de forjados y borde de balcones
pf = gaussian_filter1d(g[1250:1612, 500:1700].mean(1), 1.5); d = np.diff(pf)
bordes = [i + 1250 for i in find_peaks(d, height=8, distance=40)[0]]

fig, ax = plt.subplots(figsize=(18, 8.5))
crop = im.crop((0, y0 + 950, W, y0 + 1620))
ax.imshow(crop, extent=(0, W, 1620, 950))
for x in alet: ax.axvline(x, ymin=0, ymax=0.48, color="red", lw=1.4)
for x in postes: ax.plot([x, x], [1440, 1470], color="lime", lw=4)
for x in ojm: ax.plot(x, Y_REF - (V["OJO_Z"] - (E.Z_B1 + 0.65)) * PV, "o", ms=22, mfc="none", mec="red", mew=1.5)
for o in ojos: ax.plot(o[0], (o[1] + o[2]) / 2, "+", color="lime", ms=18, mew=2)
ax.set_title("MGF tambor y barril: rojo = modelo proyectado; verde = medido en la foto (aletas en los balcones, ojos)", fontsize=10, loc="left")
ax.axis("off")
txt = [f"aletas: {len(postes)} medidas · residuo foto − modelo " + " ".join(f"{r:+.0f}" for r in res_al) + f" px  (medio {np.mean(res_al) / PH:+.2f} m, máx {max(map(abs, res_al)) / PH:.2f} m)",
       f"ojos: {len(ojos)} medidos · residuo " + " ".join(f"{r:+.0f}" for r in res_oj) + f" px · diámetro {d_oj:.2f} m (modelo {V['OJO_D']:.2f}) · centro +{z_oj:.2f} (modelo +{V['OJO_Z']:.2f})",
       f"forjados: bordes {bordes} → paso {np.median(np.diff(bordes[::2])) / PV if len(bordes) > 2 else float('nan'):.2f} m (modelo {E.F:.2f})",
       f"lado ciego: sin ojos entre {V['OJO_C0']:.0f}° y {V['OJO_C1']:.0f}° (lado interior de la L) → modelo con {sum(1 for h in VE.catalogo() if h['grupo'] == 'tambor ojos')} ojos"]
fig.text(0.01, 0.01, "\n".join(txt).replace(".", ","), fontsize=9, family="monospace", va="bottom")
fig.subplots_adjust(bottom=0.16, top=0.95, left=0.01, right=0.99)
fig.savefig("MGF_TAMBOR.png", dpi=80)
print("\n".join(txt))
ok = max(map(abs, res_al)) / PH < 0.35 and all(o[0] > 850 for o in ojos) and all(m > 850 for m in ojm)
print("MGF tambor:", "OK" if ok else "FALLA")
