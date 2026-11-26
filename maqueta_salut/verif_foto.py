"""VERIFICACIÓN POR PUNTOS (método, pasada 10).

Para una foto:
 1. calibra la cámara SOLO con la torre (siluetas + forjados) y las bandas del chaflán: lo que se verifica
    (ala larga, bar, rampa, ventanas, escalera) NO entra en la calibración -> la prueba es independiente;
 2. proyecta los 610 puntos del catálogo (puntos_ref.py) y decide cuáles se ven (z-buffer del modelo);
 3. mide para cada punto visible la distancia a la arista más cercana de la FOTO (Canny + transformada de
    distancia) y la pasa a metros con la escala local;
 4. escribe la fila de la matriz (punto × foto) y una lámina con el modelo superpuesto y los puntos coloreados.
No modifica el modelo ni el cuadro."""
import sys, json, math, csv
import numpy as np, cv2, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from PIL import Image
import edificio as E, calib_e as C, puntos_ref as PR

I = '/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'
yf = -(E.R_COL - E.RET)


def P3(X, Y, z):
    p = E.P(X, Y); return np.array([p[0], p[1], z])


GEO = {"banda_rest": (P3(-14, yf, E.Z_P1), P3(-4, yf, E.Z_P1)),
       "banda_hotel": (P3(4, yf, E.Z_P1), P3(E.R_COL + E._v["HOT_L"], yf, E.Z_P1))}


def dlin(K, A, B, q):
    s = np.linspace(-0.3, 1.3, 161); Pm = A[None] * (1 - s[:, None]) + B[None] * s[:, None]; pr = C.proj(K, Pm)
    return float(np.min(np.hypot(pr[:, 0] - q[0], pr[:, 1] - q[1])))


def calibrar(foto, tor, lin, hcam=None, az=(-180, 180), el=(-10, 85), fov=(3, 100), pts=()):
    W, H = Image.open(I + foto).size; T = np.array(E.T)
    def res(x):
        K = C.cam(x, W, H); r = list(C.residuos(x, tor, W, H))
        if hcam: r.append((K[0][2] - hcam) * 5)
        for k, q0, q1 in lin:
            A, B = GEO[k]; r += [dlin(K, A, B, q0), dlin(K, A, B, q1)]
        for P, q in pts:
            pp = C.proj(K, np.array(P))[0]; r += [pp[0] - q[0], pp[1] - q[1]]
        return np.array(r)
    best = None
    for a in np.arange(az[0], az[1], 15):
        for e in (el[0] + 3, (el[0] + el[1]) / 2):
            for f in (fov[0] + 3, (fov[0] + fov[1]) / 2):
                try:
                    rr = least_squares(res, [a, e, 250, T[0], T[1], 20, f, 0],
                                       bounds=([az[0], el[0], 15, T[0] - 60, T[1] - 60, -10, fov[0], -15],
                                               [az[1], el[1], 3000, T[0] + 60, T[1] + 60, 70, fov[1], 15]),
                                       loss="soft_l1", f_scale=6)
                except Exception:
                    continue
                ee = float(np.sqrt(np.mean(rr.fun ** 2)))
                if best is None or ee < best[0]:
                    best = (ee, rr.x, rr.fun)
    return best, (W, H)


def zbuffer(m, K):
    c, r, u, d, f, W, H = K
    V, F = C._malla(m); v = V - c
    X, Y, Zd = v @ r, v @ u, v @ d
    px, py = W / 2 + f * X / Zd, H / 2 - f * Y / Zd
    zb = np.full((H, W), np.inf)
    for a in F:
        x, y, z = px[a], py[a], Zd[a]
        if (z <= 1).any(): continue
        x0, x1 = max(int(x.min()), 0), min(int(x.max()) + 1, W - 1)
        y0, y1 = max(int(y.min()), 0), min(int(y.max()) + 1, H - 1)
        if x1 < x0 or y1 < y0: continue
        XX, YY = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        den = (y[1] - y[2]) * (x[0] - x[2]) + (x[2] - x[1]) * (y[0] - y[2])
        if abs(den) < 1e-12: continue
        l0 = ((y[1] - y[2]) * (XX - x[2]) + (x[2] - x[1]) * (YY - y[2])) / den
        l1 = ((y[2] - y[0]) * (XX - x[2]) + (x[0] - x[2]) * (YY - y[2])) / den
        l2 = 1 - l0 - l1
        msk = (l0 >= -1e-6) & (l1 >= -1e-6) & (l2 >= -1e-6)
        ZZ = l0 * z[0] + l1 * z[1] + l2 * z[2]
        sub = zb[y0:y1 + 1, x0:x1 + 1]; msk &= ZZ < sub; sub[msk] = ZZ[msk]
    return zb


def verificar(nombre, foto, x, umbral_m=0.6):
    W, H = Image.open(I + foto).size; K = C.cam(x, W, H)
    c, r, u, d, f = K[:5]
    m = E.edificio()
    zb = zbuffer(m, K)
    g = cv2.cvtColor(np.asarray(Image.open(I + foto).convert("RGB")), cv2.COLOR_RGB2GRAY)
    ed = cv2.Canny(cv2.GaussianBlur(g, (3, 3), 0), 40, 110)
    dt = cv2.distanceTransform(255 - ed, cv2.DIST_L2, 3)
    filas = []
    for pid, zona, desc, X, Y, Z in PR.generar():
        P = np.array([X, Y, Z]); q = C.proj(K, P)[0]; dep = float((P - c) @ d)
        ix, iy = int(q[0]), int(q[1])
        if not (0 <= ix < W and 0 <= iy < H) or dep <= 1:
            filas.append((pid, zona, "fuera", None, None, None)); continue
        vis = dep <= zb[max(iy - 1, 0):iy + 2, max(ix - 1, 0):ix + 2].min() + 0.6
        if not vis:
            filas.append((pid, zona, "oculto", q[0], q[1], None)); continue
        mpp = dep / f                                     # metros por píxel a esa profundidad
        dist_m = float(dt[iy, ix]) * mpp
        filas.append((pid, zona, "OK" if dist_m <= umbral_m else "NO", q[0], q[1], round(dist_m, 2)))
    # lámina
    e, _ = C.aristas(m, K)
    a = np.asarray(Image.open(I + foto).convert("RGB")).astype(float) * 0.75 + 50
    a[e] = (255, 40, 40)
    fig = plt.figure(figsize=(14, 14 * H / W + 1.2))
    ax = fig.add_axes([0, 0.06, 1, 0.9]); ax.imshow(a.astype(np.uint8)); ax.axis("off")
    for pid, zona, est, qx, qy, dm in filas:
        if est in ("OK", "NO"):
            ax.plot(qx, qy, "o", ms=3.5, mfc="lime" if est == "OK" else "magenta", mec="k", mew=0.3)
    ok = sum(1 for t in filas if t[2] == "OK"); no = sum(1 for t in filas if t[2] == "NO")
    ax.set_title(f"{nombre} ({foto}): modelo del cuadro proyectado (rojo). Puntos visibles: verde = cae sobre una arista de la foto "
                 f"(≤ {umbral_m} m), magenta = no ({ok} OK / {no} NO)", fontsize=9, loc="left")
    fig.savefig(f"VERIF_{nombre}.png", dpi=80); plt.close(fig)
    with open(f"VERIF_{nombre}.csv", "w", newline="") as fh:
        wr = csv.writer(fh); wr.writerow(["id", "zona", "estado", "u_px", "v_px", "dist_m"])
        for t in filas:
            wr.writerow([t[0], t[1], t[2], None if t[3] is None else round(t[3], 1), None if t[4] is None else round(t[4], 1), t[5]])
    return filas


# ------------------------------------------------------------------ prueba por SEGMENTOS (orientada)
import re
from collections import defaultdict


def series():
    """agrupa el catálogo en polilíneas: (nombre, zona, [ids], cerrada)"""
    pts = PR.generar(); por = defaultdict(list); zona = {}
    for pid, z, *_ in pts:
        if pid.startswith("VEN-"):
            k = pid[:-2]; cerr = True
        elif pid.startswith("TOR-ALS-") or pid.startswith("TOR-ALI-"):
            continue
        elif pid.startswith("TOR-FOR-"):
            k = "-".join(pid.split("-")[:3]); cerr = True
        elif re.match(r"(TOR-(VIS-S|VIS-I|BAN|TAM|REM|COL|CUE))", pid):
            k = re.match(r"(TOR-(VIS-S|VIS-I|BAN|TAM|REM|COL|CUE))", pid).group(1); cerr = True
        elif re.match(r"(ALA-(PET|PIE|INT)|RAM-(PET|ARC)|BAR-BOR)", pid):
            k = re.match(r"(ALA-(PET|PIE|INT)|RAM-(PET|ARC)|BAR-BOR)", pid).group(1); cerr = False
        else:
            continue
        por[(k, cerr)].append(pid); zona[k] = z
    out = [(k, zona[k], ids, c) for (k, c), ids in por.items()]
    for k in range(E._v["N_AL"]):                       # aletas: segmento vertical
        out.append((f"TOR-AL-{k:02d}", "TORRE aletas", [f"TOR-ALS-{k:02d}", f"TOR-ALI-{k:02d}"], False))
    return out


def soporte(nombre, foto, x, radio_m=0.35, ang_tol=20):
    W, H = Image.open(I + foto).size; K = C.cam(x, W, H); c, r, u, d, f = K[:5]
    m = E.edificio(); zb = zbuffer(m, K)
    g = cv2.cvtColor(np.asarray(Image.open(I + foto).convert("RGB")), cv2.COLOR_RGB2GRAY).astype(np.float32)
    g = cv2.GaussianBlur(g, (3, 3), 0)
    gx, gy = cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3), cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3)
    mag = np.hypot(gx, gy); edge = cv2.Canny(g.astype(np.uint8), 30, 90) > 0
    P3D = {p[0]: np.array(p[3:6]) for p in PR.generar()}
    res = []
    for k, zona, ids, cerr in series():
        seq = ids + ([ids[0]] if cerr else [])
        tot = sop = 0
        for a, b in zip(seq, seq[1:]):
            A, B = P3D[a], P3D[b]
            for t in np.linspace(0.04, 0.96, 12):
                P = A * (1 - t) + B * t; dep = float((P - c) @ d)
                if dep <= 1: continue
                q = C.proj(K, P)[0]; ix, iy = int(q[0]), int(q[1])
                if not (2 <= ix < W - 2 and 2 <= iy < H - 2): continue
                if dep > zb[iy - 1:iy + 2, ix - 1:ix + 2].min() + 0.6: continue      # oculto
                qa, qb = C.proj(K, A)[0], C.proj(K, B)[0]; dv = qb - qa
                if np.hypot(*dv) < 1e-6: continue
                nrm = np.array([-dv[1], dv[0]]) / np.hypot(*dv)                     # normal a la línea en la imagen
                R = max(2, int(round(radio_m * f / dep)))
                y0, y1, x0, x1 = max(iy - R, 0), min(iy + R + 1, H), max(ix - R, 0), min(ix + R + 1, W)
                E_ = edge[y0:y1, x0:x1]; GX, GY, M = gx[y0:y1, x0:x1], gy[y0:y1, x0:x1], mag[y0:y1, x0:x1] + 1e-6
                cosang = np.abs(GX * nrm[0] + GY * nrm[1]) / M
                tot += 1
                if (E_ & (cosang > math.cos(math.radians(ang_tol)))).any():
                    sop += 1
        if tot:
            res.append((k, zona, tot, sop, sop / tot))
    with open(f"SOPORTE_{nombre}.csv", "w", newline="") as fh:
        wr = csv.writer(fh); wr.writerow(["linea", "zona", "muestras_visibles", "apoyadas", "fraccion"])
        for t in res: wr.writerow([t[0], t[1], t[2], t[3], round(t[4], 2)])
    # lámina: cada línea del cuadro coloreada por su apoyo en la foto
    a = np.asarray(Image.open(I + foto).convert("RGB")).astype(float) * 0.7 + 60
    fig = plt.figure(figsize=(14, 14 * H / W + 1.2)); ax = fig.add_axes([0, 0.06, 1, 0.9])
    ax.imshow(a.astype(np.uint8)); ax.axis("off")
    frac = {t[0]: t[4] for t in res}
    for k, zona, ids, cerr in series():
        if k not in frac: continue
        seq = ids + ([ids[0]] if cerr else [])
        Q = np.array([C.proj(K, P3D[i])[0] for i in seq if float((P3D[i] - c) @ d) > 1])
        if len(Q) < 2: continue
        fr = frac[k]; col = "lime" if fr >= 0.7 else ("orange" if fr >= 0.4 else "magenta")
        ax.plot(Q[:, 0], Q[:, 1], "-", color=col, lw=1.1)
    ax.set_title(f"{nombre}: líneas del cuadro proyectadas. Verde ≥70 % de su longitud visible coincide con una arista de la foto "
                 f"con su misma orientación; naranja 40–70 %; magenta < 40 % (NO está donde dice el plano)", fontsize=8.5, loc="left")
    fig.savefig(f"SOPORTE_{nombre}.png", dpi=80); plt.close(fig)
    return res
