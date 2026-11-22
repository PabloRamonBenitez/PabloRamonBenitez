"""Levantamiento por geometria descriptiva sobre F01: camara + posicion de la torre en el marco D-E,
con puntos de satelite (A,B,C en el plano de cubierta del bloque alto; D,E en el plano de la terraza)
y siluetas de la torre. Despues F y G se obtienen cortando sus rayos con el plano de la terraza."""
import math, numpy as np
from scipy.optimize import least_squares
import cotas as K
V = K.V; W, H = 828, 762
# ---------------- planta de satelite (marco D: D=(0,0), E=(17,0), ala hacia -y)
def tri(P, Q, dp, dq, s):
    d = np.linalg.norm(Q - P); a = (dp**2 - dq**2 + d**2) / (2 * d); h = math.sqrt(max(dp**2 - a**2, 0))
    u = (Q - P) / d; n = np.array([-u[1], u[0]]); return P + a * u + s * h * n
D = np.array([0., 0.]); E = np.array([17., 0.])
A = tri(D, E, 106.69, 102.96, -1); C = tri(D, A, 95.17, 16.66, -1)
ca = A - C; th = math.atan2(7.3, math.sqrt(ca @ ca - 7.3**2))
R = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]]); ub = R @ ca / np.linalg.norm(ca)
B = C + ub * math.sqrt(ca @ ca - 7.3**2)
PX = {"A": (0, 515), "B": (54, 524), "C": (206, 500), "D": (722, 353), "E": (598, 344)}
PT = {"A": A, "B": B, "C": C, "D": D, "E": E}
PIX_F, PIX_G, PIX_X = (153, 575), (551, 520), (464, 604)
ZB1 = V["Z_B0"] + V["N_PL"] * V["F"]
TOR = [("barril_sup", V["R_AL"], ZB1 + 0.65, (170, 550, 262)), ("barril_inf", V["R_AL"], V["Z_ALE"], (187, 532, 476)),
       ("tambor", V["R_T"], (ZB1 + V["Z_T1"]) / 2, (190, 525, 232)), ("columna", V["R_COL"], 0.5, (322, 388, 652))]
FORJ = [281.7, 320, 358.3, 396.7, 435, 473]
def cam(x):
    az, el, dist, tx, ty, tz, fov, roll = x[:8]
    a, e = math.radians(az), math.radians(el); tgt = np.array([tx, ty, tz])
    c = tgt + dist * np.array([math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)])
    d = tgt - c; d /= np.linalg.norm(d); r = np.cross(d, [0, 0, 1]); r /= np.linalg.norm(r); u = np.cross(r, d)
    rr = math.radians(roll); r, u = r * math.cos(rr) + u * math.sin(rr), -r * math.sin(rr) + u * math.cos(rr)
    return c, r, u, d, (W / 2) / math.tan(math.radians(fov) / 2)
def proj(k, P):
    c, r, u, d, f = k; v = np.atleast_2d(P) - c
    return np.c_[W / 2 + f * (v @ r) / (v @ d), H / 2 - f * (v @ u) / (v @ d)]
def sil(k, c, Rr, z):
    P = np.array([c[0], c[1], z]); v = P - k[0]; h = np.array([v[0], v[1], 0]); h /= np.linalg.norm(h)
    l = np.array([-h[1], h[0], 0]); q = proj(k, np.array([P + Rr * l, P - Rr * l])); return q[np.argsort(q[:, 0])]
def res(x, h1, h2, peso_pts=1.0):
    k = cam(x); T = np.array([x[8], x[9]]); r = []
    for _, Rr, z, (xl, xr, y) in TOR:
        q = sil(k, T, Rr, z); r += [q[0, 0] - xl, q[1, 0] - xr, (q[0, 1] + q[1, 1]) / 2 - y]
    v = k[0][:2] - T; v /= np.linalg.norm(v)
    for j, yf in enumerate(FORJ):
        z = V["Z_B0"] + (6 - j) * V["F"]; r.append(proj(k, np.array([*(T + v * (V["R_AL"] - 0.9)), z]))[0, 1] - yf)
    for n_, p in PT.items():
        z = h1 if n_ in "ABC" else h2
        q = proj(k, np.array([p[0], p[1], z]))[0]; r += [peso_pts * (q[0] - PX[n_][0]), peso_pts * (q[1] - PX[n_][1])]
    return np.array(r)
def ray_plane(k, px, z):
    c, r, u, d, f = k; dirv = d + r * (px[0] - W / 2) / f - u * (px[1] - H / 2) / f
    t = (z - c[2]) / dirv[2]; return c + t * dirv
if __name__ == "__main__":
    print("planta satélite (marco D): A", A.round(2), "B", B.round(2), "C", C.round(2))
    best = None
    for h1 in (11.5,):
        for az in range(-180, 180, 20):
            for tyy in (-80, -60):
                x0 = [az, 30, 200, 20, tyy, 20, 25, 0, 20, tyy]
                try:
                    rr = least_squares(res, x0, args=(h1, V["Z_P1"]), bounds=([-200, 5, 50, -80, -160, -10, 8, -10, -40, -140], [200, 85, 1500, 120, 40, 60, 70, 10, 80, 0]), loss="soft_l1", f_scale=6)
                except Exception:
                    continue
                e = float(np.sqrt(np.mean(rr.fun ** 2)))
                if best is None or e < best[0]: best = (e, rr.x, rr.fun, h1)
    e, x, f, h1 = best; k = cam(x); T = np.array(x[8:10])
    print("error total %.1f px · torre en el marco D: T = (%.2f, %.2f)" % (e, *T))
    nT = 4 * 3 + 6
    print(" residuos torre (px):", np.round(f[:nT], 1))
    for i, n_ in enumerate(PT): print("  punto %s: residuo (%.1f, %.1f) px" % (n_, f[nT + 2 * i], f[nT + 2 * i + 1]))
    for nm, px in (("F", PIX_F), ("G", PIX_G), ("X (sin nombre)", PIX_X)):
        P = ray_plane(k, px, V["Z_P1"]); print("  %s en el plano +%.1f -> planta (%.2f, %.2f)" % (nm, V["Z_P1"], P[0], P[1]))
    np.save("levantamiento.npy", dict(x=x, T=T, A=A, B=B, C=C, D=D, E=E), allow_pickle=True)
