"""AJUSTE CONJUNTO (tipo 'bundle adjustment'): se resuelven A LA VEZ
  - los parametros del edificio (alturas, radios, desplazamientos, angulos de la planta),
  - la camara de cada foto (posicion, orientacion, focal y una deformacion vertical para escaneos),
con TODAS las observaciones de las fotos + las medidas de planta (Bing/Google) + las reglas de coherencia de
plantas y secciones (como ecuaciones suaves). Perdida robusta: una foto o un punto mal leido pesa poco y
queda señalado por su residuo grande.
Coordenadas de torre: eje de la torre en el origen; X a lo largo del chaflan; Y hacia dentro."""
import math, json, numpy as np
from scipy.optimize import least_squares

# ------------------------------------------------------------------ parametros del edificio (valor inicial, nombre)
GP = [
 ("F", 3.10), ("ZB0", 13.9), ("RAL", 15.3), ("RT", 13.55), ("ZT1", 38.2), ("RG", 10.85), ("ZG1", 40.5),
 ("RV", 12.8), ("ZV1", 43.7), ("OVX", -2.4), ("OVY", -0.4), ("RR", 5.6), ("ZR1", 49.1), ("RCOL", 3.25),
 ("ZP1", 7.3), ("ACH", 57.0), ("THL", 102.0),
]
GI = {k: i for i, (k, _) in enumerate(GP)}
# medidas fijas de planta (Bing/Google, F09) que no se ajustan aqui
W_P, W_EXT, L_L, REST, COL, HOT, RET = 12.74, 15.7, 94.8, 12.8, 6.5, 9.6, 1.5
PRIOR = [  # (expresion, valor, sigma m o grados)
 ("2*RV", 24.35, 1.0),          # Google: disco de la visera
 ("2*RAL", 30.6, 2.0),          # escala de referencia blanda
 ("ZP1", 7.3, 0.5),             # F50 con personas
 ("THL", 102.0, 8.0),           # F35/F58
]

IMG = '/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'
FOTOS = {   # obs: ("cil", clave, xl, xr, y) | ("forj", [y...]) | ("lin", clave, (x0,y0), (x1,y1)) | ("pt", clave, (x,y))
 "C04": dict(f="9.webp", WH=(874, 890), hcam=2.0, aspect=False, x0=[83, -1, 1270, 0, 0, 27, 3.0, 1.6],
   obs=[("cil", "barril_sup", 105, 502, 366), ("cil", "barril_inf", 108, 500, 598), ("cil", "columna", 246, 330, 720),
        ("forj", [373, 413, 453, 493, 533, 575]), ("cil", "tambor", 133, 485, 335), ("cil", "visera", 110, 442, 245),
        ("cil", "remate", 240, 385, 190)]),
 "C01": dict(f="1.webp", WH=(828, 762), hcam=None, aspect=True, x0=[-70, 25, 240, 0, 0, 22, 16, 0.5],
   obs=[("cil", "barril_sup", 170, 550, 262), ("cil", "barril_inf", 187, 532, 476), ("cil", "columna_pie", 322, 388, 652),
        ("forj", [281.7, 320, 358.3, 396.7, 435, 473]), ("cil", "tambor", 190, 525, 232), ("cil", "remate", 293, 417, 45),
        ("lin", "banda_rest", (170, 567), (320, 562)), ("lin", "peto_ala", (552, 425), (727, 352)), ("pt", "fin_ala", (727, 352))]),
 "C03": dict(f="2.webp", WH=(1794, 1170), hcam=1.6, aspect=True, x0=[80, -2, 340, 0, 0, 24, 16, -0.3],
   obs=[("cil", "barril_sup", 780, 1365, 410), ("cil", "barril_inf", 795, 1350, 760),
        ("forj", [427.5, 482.5, 537.5, 592.5, 647.5, 702.5]), ("cil", "tambor", 805, 1332, 385),
        ("cil", "visera", 785, 1252, 305), ("cil", "remate", 975, 1198, 180)]),
}


def geo(g):
    """primitivas en coordenadas de torre a partir de los parametros"""
    G = {k: g[i] for k, i in GI.items()}
    a, th = math.radians(G["ACH"]), math.radians(G["THL"])
    # planta (como edificio.py): esquina exterior KC=(W_EXT,0); calle con direccion US; chaflan A1->C
    LCH = REST + COL + HOT
    angC = math.pi - th - a
    A = L_aux = None
    _a = LCH * math.sin(angC) / math.sin(th); _c = LCH * math.sin(a) / math.sin(th)
    US = np.array([math.cos(math.pi / 2 + th), math.sin(math.pi / 2 + th)])
    KC = np.array([W_EXT, 0.0]); A1 = KC + _a * US; C = KC + np.array([0, _c])
    U = (C - A1) / LCH; N = np.array([-U[1], U[0]])
    T = A1 + (REST + COL / 2) * U + (G["RCOL"] - RET) * N
    def a_torre(p):
        q = np.asarray(p, float) - T; return np.array([q @ U, q @ N])
    yf = -(G["RCOL"] - RET)
    zb1 = G["ZB0"] + 6 * G["F"]
    cil = {"barril_sup": ((0, 0), G["RAL"], zb1 + 0.65), "barril_inf": ((0, 0), G["RAL"], 15.2),
           "tambor": ((0, 0), G["RT"], (zb1 + G["ZT1"]) / 2), "visera": ((G["OVX"], G["OVY"]), G["RV"], (G["ZG1"] + G["ZV1"]) / 2),
           "remate": ((0.6, 0.0), G["RR"], (G["ZV1"] + G["ZR1"]) / 2), "columna": ((0, 0), G["RCOL"], 5.6),
           "columna_pie": ((0, 0), G["RCOL"], 0.5)}
    lin = {"banda_rest": (np.array([-14, yf, G["ZP1"]]), np.array([-4, yf, G["ZP1"]])),
           "peto_ala": (np.append(a_torre((W_P, C[1] + 5)), G["ZP1"] + 1), np.append(a_torre((W_P, L_L)), G["ZP1"] + 1))}
    pts = {"fin_ala": np.append(a_torre((W_P, L_L)), G["ZP1"] + 1)}
    return G, cil, lin, pts, zb1


def cam(x, WH, asp):
    az, el, dist, tx, ty, tz, fov, roll = x[:8]
    W, H = WH
    a, e = math.radians(az), math.radians(el); tgt = np.array([tx, ty, tz])
    c = tgt + dist * np.array([math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)])
    d = tgt - c; d /= np.linalg.norm(d); r = np.cross(d, [0, 0, 1]); r /= np.linalg.norm(r); u = np.cross(r, d)
    rr = math.radians(roll); r, u = r * math.cos(rr) + u * math.sin(rr), -r * math.sin(rr) + u * math.cos(rr)
    return c, r, u, d, (W / 2) / math.tan(math.radians(fov) / 2), W, H, asp


def proj(K, P):
    c, r, u, d, f, W, H, asp = K; v = np.atleast_2d(P) - c
    return np.c_[W / 2 + f * (v @ r) / (v @ d), H / 2 - asp * f * (v @ u) / (v @ d)]


def sil(K, c, R, z):
    P = np.array([c[0], c[1], z]); v = P - K[0]; h = np.array([v[0], v[1], 0]); h /= np.linalg.norm(h)
    l = np.array([-h[1], h[0], 0]); q = proj(K, np.array([P + R * l, P - R * l])); return q[np.argsort(q[:, 0])]


def dist_lin(K, A, B, q):
    s = np.linspace(-0.3, 1.3, 161); P = A[None] * (1 - s[:, None]) + B[None] * s[:, None]
    pr = proj(K, P); return float(np.min(np.hypot(pr[:, 0] - q[0], pr[:, 1] - q[1])))


ORDEN = list(FOTOS)
NC = 9


def desempaqueta(x):
    g = x[:len(GP)]; cams = {}
    for i, k in enumerate(ORDEN):
        v = x[len(GP) + i * NC: len(GP) + (i + 1) * NC]; cams[k] = (v[:8], v[8] if FOTOS[k]["aspect"] else 1.0)
    return g, cams


def residuos(x, etiquetas=None):
    g, cams = desempaqueta(x)
    G, cil, lin, pts, zb1 = geo(g)
    out = []; lab = []
    for k in ORDEN:
        d = FOTOS[k]; K = cam(cams[k][0], d["WH"], cams[k][1])
        if d["hcam"] is not None:
            out.append((K[0][2] - d["hcam"]) * 3.0); lab.append((k, "altura cámara"))
        for o in d["obs"]:
            if o[0] == "cil":
                c, R, z = cil[o[1]]; q = sil(K, c, R, z)
                out += [q[0, 0] - o[2], q[1, 0] - o[3], (q[0, 1] + q[1, 1]) / 2 - o[4]]; lab += [(k, o[1])] * 3
            elif o[0] == "forj":
                v = K[0].copy(); v[2] = 0; v /= np.linalg.norm(v)
                for j, yf in enumerate(o[1]):
                    z = G["ZB0"] + (6 - j) * G["F"]
                    out.append(proj(K, v * (G["RAL"] - 0.9) + np.array([0, 0, z]))[0, 1] - yf); lab.append((k, "forjados"))
            elif o[0] == "lin":
                A, B = lin[o[1]]; out += [dist_lin(K, A, B, o[2]), dist_lin(K, A, B, o[3])]; lab += [(k, o[1])] * 2
            elif o[0] == "pt":
                q = proj(K, pts[o[1]])[0]; out += [q[0] - o[2][0], q[1] - o[2][1]]; lab += [(k, o[1])] * 2
    # medidas y reglas como ecuaciones suaves (convertidas a "pixeles equivalentes": 1 sigma = 5 px)
    Gd = G
    for expr, val, sg in PRIOR:
        out.append((eval(expr, {}, Gd) - val) / sg * 5.0); lab.append(("planos", f"{expr} = {val}"))
    if etiquetas is not None:
        etiquetas.extend(lab)
    return np.array(out)


def resolver():
    x0 = [v for _, v in GP]
    for k in ORDEN:
        x0 += FOTOS[k]["x0"] + [1.0]
    lo = [1.5, 10, 12, 10, 34, 8, 37, 9, 40, -6, -4, 4, 46, 2.5, 5.5, 25, 80]
    hi = [3.6, 17, 18, 16, 42, 13, 44, 15, 47, 4, 4, 7, 52, 4.5, 9.5, 80, 125]
    for k in ORDEN:
        lo += [-180, -10, 30, -60, -60, -10, 2, -10, 0.85]; hi += [180, 85, 3000, 60, 60, 70, 80, 10, 1.15]
    x0 = np.clip(x0, np.array(lo) + 1e-6, np.array(hi) - 1e-6)
    r = least_squares(residuos, x0, bounds=(lo, hi), loss="soft_l1", f_scale=6.0, max_nfev=4000)
    return r


if __name__ == "__main__":
    r = resolver()
    lab = []; res = residuos(r.x, lab)
    g, cams = desempaqueta(r.x)
    print("PARÁMETROS DEL EDIFICIO")
    for (k, v0), v in zip(GP, g):
        print(f"  {k:5s} {v0:8.2f} -> {v:8.2f}")
    print("CÁMARAS (az, el, dist, ..., fov, roll | deformación vertical)")
    for k, (c, a) in cams.items():
        print(f"  {k}: {np.round(c, 1)} | {a:.3f}")
    print("RESIDUOS POR GRUPO (px; 'planos' en px equivalentes)")
    grupos = {}
    for (k, n), v in zip(lab, res):
        grupos.setdefault((k, n), []).append(v)
    for (k, n), vs in grupos.items():
        print(f"  {k:7s} {n:22s} max {np.max(np.abs(vs)):6.1f}  {np.round(vs, 1)}")
    json.dump(dict(geometria={k: float(v) for (k, _), v in zip(GP, g)},
                   camaras={k: dict(cam=list(map(float, c)), deformacion=float(a)) for k, (c, a) in cams.items()},
                   residuos={f"{k}|{n}": list(map(float, vs)) for (k, n), vs in grupos.items()}),
              open("AJUSTE_CONJUNTO.json", "w"), indent=1, ensure_ascii=False)
