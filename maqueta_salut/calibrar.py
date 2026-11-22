"""Calibracion de camara por correspondencias: cilindros verticales conocidos (centro en planta, radio, cota)
cuyo contorno izquierdo/derecho se lee en la foto. Ajuste por minimos cuadrados de az, el, dist, objetivo, fov, roll."""
import math, sys, json
import numpy as np
from scipy.optimize import least_squares
import salut_v2 as s
import superponer as sp


def solar_off(off):
    """desplazamiento en coords de torre -> punto solar"""
    return s.solar(off[0], off[1])


def cilindros():
    return {
        "barril_sup": (s.CEN, s.R_B, s.Z_HAB1),
        "barril_inf": (s.CEN, s.R_B, s.Z_HAB0 + 0.5),
        "tambor_ojos": (s.CEN, s.R_OJOS, s.Z_OJOS0 + 2.6),
        "visera": (solar_off(s.OFF_VIS), s.R_VIS, s.Z_VIS1),
        "tambor_sup": (solar_off(s.OFF_TOP), s.R_TOP, s.Z_TOP1),
        "columna_pie": (s.CEN, s.R_COL, 0.5),
        "cuello": (s.CEN, s.R_CUELLO, s.Z_CUELLO1 - 0.5),
    }


def proyectar(cam, p):
    c, r, up, d, f = cam
    v = np.asarray(p, float) - c
    return np.array([v @ r, v @ up, v @ d])


def residuos(x, obs, W, H):
    az, el, dist, tx, ty, tz, fov, roll = x
    cam = sp.camara(az, el, dist, (tx, ty, tz), fov, roll, W, H)
    c, r, up, d, f = cam
    res = []
    cil = cilindros()
    for k, (xl, xr, y) in obs.items():
        cc, R, z = cil[k]
        P = np.array([cc[0], cc[1], z])
        # extremos de silueta: perpendiculares al rayo en planta
        v = P - c; h = np.array([v[0], v[1], 0]); h /= np.linalg.norm(h)
        lat = np.array([-h[1], h[0], 0])
        pts = []
        for sgn in (1, -1):
            X, Y, Z = proyectar(cam, P + sgn * R * lat)
            pts.append((W / 2 + f * X / Z, H / 2 - f * Y / Z))
        pts.sort()
        res += [pts[0][0] - xl, pts[1][0] - xr, (pts[0][1] + pts[1][1]) / 2 - y]
    for (p3a, p3b, q0, q1, peso) in LINEAS:
        q0, q1 = np.array(q0, float), np.array(q1, float)
        t = (q1 - q0) / np.linalg.norm(q1 - q0); nn = np.array([-t[1], t[0]])
        for a in np.linspace(0, 1, 5):
            P = np.array(p3a) * (1 - a) + np.array(p3b) * a
            X, Y, Z = proyectar(cam, P)
            u = np.array([W / 2 + f * X / Z, H / 2 - f * Y / Z])
            res.append(peso * float((u - q0) @ nn))
    return np.array(res)


LINEAS = []


def calibrar(foto, obs, x0):
    from PIL import Image
    W, H = Image.open(foto).size
    lo = [-180, -10, 30, -60, -60, -5, 3, -10]; hi = [180, 89, 3000, 80, 120, 60, 80, 10]
    r = least_squares(residuos, x0, args=(obs, W, H), bounds=(lo, hi))
    return r.x, residuos(r.x, obs, W, H)


if __name__ == "__main__":
    foto, sal = sys.argv[1], sys.argv[2]
    obs = json.loads(sys.argv[3]); x0 = json.loads(sys.argv[4])
    if len(sys.argv) > 5:
        LINEAS.extend(json.loads(sys.argv[5]))
    x, res = calibrar(foto, obs, x0)
    print("camara:", ",".join(f"{v:.2f}" for v in x))
    print("residuos px:", np.round(res, 1), " rms:", round(float(np.sqrt(np.mean(res ** 2))), 1))
    sp.superponer(foto, *x[:3], tuple(x[3:6]), x[6], x[7], sal)
