"""Calibracion de camaras y superposicion de aristas usando la definicion edificio.py (no el modelo antiguo).
Observaciones de una foto: cilindros conocidos -> (clave, x_izq, x_der, y) en pixeles."""
import math, numpy as np
from scipy.optimize import least_squares
from PIL import Image
import edificio as E

T = np.array(E.T)
CIL = {   # clave: (centro, radio, cota)
    "barril_sup": (T, E.R_AL, E.Z_B1 + E._v["FOR_C"]), "barril_inf": (T, E.R_AL, E.Z_ALETA0),
    "tambor": (T, E.R_T, (E.Z_B1 + E.Z_T1) / 2), "visera": (np.array(E.P(*E.OFF_V)), E.R_V, (E.Z_G1 + E.Z_V1) / 2),
    "remate": (np.array(E.P(*E.OFF_R)), E.R_R, (E.Z_V1 + E.Z_R1) / 2), "columna": (T, E.R_COL, 5.6),
    "columna_pie": (T, E.R_COL, 0.5), "cuello": (T, E.R_CU, (E.Z_CU0 + E.Z_CU1) / 2),
}


def cam(x, W, H):
    az, el, dist, tx, ty, tz, fov, roll = x
    a, e = math.radians(az), math.radians(el); tgt = np.array([tx, ty, tz])
    c = tgt + dist * np.array([math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)])
    d = tgt - c; d /= np.linalg.norm(d); r = np.cross(d, [0, 0, 1]); r /= np.linalg.norm(r); u = np.cross(r, d)
    rr = math.radians(roll); r, u = r * math.cos(rr) + u * math.sin(rr), -r * math.sin(rr) + u * math.cos(rr)
    return c, r, u, d, (W / 2) / math.tan(math.radians(fov) / 2), W, H


def proj(K, P):
    c, r, u, d, f, W, H = K; v = np.atleast_2d(P) - c
    return np.c_[W / 2 + f * (v @ r) / (v @ d), H / 2 - f * (v @ u) / (v @ d)]


def silueta(K, c, R, z):
    P = np.array([c[0], c[1], z]); v = P - K[0]; h = np.array([v[0], v[1], 0]); h /= np.linalg.norm(h)
    l = np.array([-h[1], h[0], 0]); q = proj(K, np.array([P + R * l, P - R * l])); return q[np.argsort(q[:, 0])]


HCAM = None   # (altura de camara, peso px/m) para fotos a pie de calle


def residuos(x, obs, W, H):
    K = cam(x, W, H); out = []
    if HCAM is not None:
        out.append((K[0][2] - HCAM[0]) * HCAM[1])
    for o in obs:
        if o[0] == "forj":                      # dinteles de las 6 plantas (de arriba a abajo), en la vertical frontal
            Tz = np.array([T[0], T[1], 0.0]); v = K[0] - Tz; v[2] = 0; v /= np.linalg.norm(v)
            for j, yf in enumerate(o[1]):
                z = E.Z_B0 + (6 - j) * E.F
                out.append(proj(K, Tz + v * E.R_B + np.array([0, 0, z]))[0, 1] - yf)
            continue
        k, xl, xr, y = o
        c, R, z = CIL[k]; q = silueta(K, c, R, z)
        out += [q[0, 0] - xl, q[1, 0] - xr, (q[0, 1] + q[1, 1]) / 2 - y]
    return np.array(out)


def calibrar(foto, obs, az_rango, el_rango=(-5, 60), fov_rango=(3, 70), hcam=None):
    global HCAM
    HCAM = hcam
    W, H = Image.open(foto).size
    best = None
    for az in np.arange(az_rango[0], az_rango[1] + 1, 10):
        for el in (el_rango[0] + 2, (el_rango[0] + el_rango[1]) / 2):
            for fv in (fov_rango[0] + 2, (fov_rango[0] + fov_rango[1]) / 2):
                x0 = [az, el, 200, T[0], T[1], 25, fv, 0]
                lo = [az_rango[0], el_rango[0], 30, T[0] - 40, T[1] - 40, -5, fov_rango[0], -8]
                hi = [az_rango[1], el_rango[1], 3000, T[0] + 40, T[1] + 40, 60, fov_rango[1], 8]
                try:
                    r = least_squares(residuos, x0, args=(obs, W, H), bounds=(lo, hi))
                except Exception:
                    continue
                e = float(np.sqrt(np.mean(r.fun ** 2)))
                if best is None or e < best[0]:
                    best = (e, r.x, r.fun)
    HCAM = None
    return best, (W, H)


# ------------------------------------------------------------------ render de aristas del modelo
def _malla(m):
    me = m.to_mesh(); return np.asarray(me.vert_properties)[:, :3].astype(float), np.asarray(me.tri_verts).astype(int)


def aristas(m, K):
    c, r, u, d, f, W, H = K
    V, F = _malla(m); v = V - c
    X, Y, Zd = v @ r, v @ u, v @ d
    px, py = W / 2 + f * X / Zd, H / 2 - f * Y / Zd
    tri = V[F]; nrm = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    ln = np.linalg.norm(nrm, axis=1); ok = ln > 1e-12; nrm[ok] /= ln[ok, None]
    cen = tri.mean(axis=1) - c
    vis = ok & (np.einsum("ij,ij->i", nrm, cen) < 0)
    zb = np.full((H, W), np.inf); fid = np.full((H, W), -1)
    for fi in np.nonzero(vis)[0]:
        a = F[fi]; x, y, z = px[a], py[a], Zd[a]
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
        sub = zb[y0:y1 + 1, x0:x1 + 1]; msk &= ZZ < sub
        sub[msk] = ZZ[msk]; fid[y0:y1 + 1, x0:x1 + 1][msk] = fi
    occ = fid >= 0; N = np.zeros((H, W, 3)); N[occ] = nrm[fid[occ]]; D = np.where(occ, zb, 1e6)
    e = np.zeros((H, W), bool)
    for ax in (0, 1):
        o2 = np.roll(occ, -1, axis=ax); D2 = np.roll(D, -1, axis=ax); N2 = np.roll(N, -1, axis=ax)
        e |= occ ^ o2
        both = occ & o2
        e |= both & (np.abs(D - D2) / np.maximum(D, 1) > 0.006)
        e |= both & (np.sum(N * N2, axis=2) < 0.8)
    return e, occ
