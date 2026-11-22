"""Render en perspectiva (z-buffer) para comparar con fotos: camara en (az, el, dist) mirando a un punto."""
import math, numpy as np
from PIL import Image

def render(t, az, el, dist, target, fov=30, W=732, H=650, roll=0.0):
    a, e = math.radians(az), math.radians(el)
    tgt = np.array(target, float)
    c = tgt + dist * np.array([math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)])
    d = tgt - c; d /= np.linalg.norm(d)
    right = np.cross(d, [0, 0, 1]); right /= np.linalg.norm(right)
    up = np.cross(right, d)
    v = t.vertices - c
    X, Y, Z = v @ right, v @ up, v @ d
    f = (W / 2) / math.tan(math.radians(fov) / 2)
    px = W / 2 + f * X / Z; py = H / 2 - f * Y / Z
    zb = np.full((H, W), np.inf); img = np.ones((H, W))
    luz = -d + np.array([-0.4, -0.3, 0.8]); luz /= np.linalg.norm(luz)
    sh = 0.35 + 0.65 * np.clip(t.face_normals @ luz, 0, 1)
    cen = t.triangles_center - c
    vis = np.einsum('ij,ij->i', t.face_normals, cen) < 0
    for fc, s in zip(t.faces[vis], sh[vis]):
        x, y, z = px[fc], py[fc], Z[fc]
        if (z <= 1).any(): continue
        x0, x1 = max(int(x.min()), 0), min(int(x.max()) + 1, W - 1)
        y0, y1 = max(int(y.min()), 0), min(int(y.max()) + 1, H - 1)
        if x1 < x0 or y1 < y0: continue
        XX, YY = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        den = (y[1] - y[2]) * (x[0] - x[2]) + (x[2] - x[1]) * (y[0] - y[2])
        if abs(den) < 1e-9: continue
        l0 = ((y[1] - y[2]) * (XX - x[2]) + (x[2] - x[1]) * (YY - y[2])) / den
        l1 = ((y[2] - y[0]) * (XX - x[2]) + (x[0] - x[2]) * (YY - y[2])) / den
        l2 = 1 - l0 - l1
        m = (l0 >= -1e-6) & (l1 >= -1e-6) & (l2 >= -1e-6)
        ZZ = l0 * z[0] + l1 * z[1] + l2 * z[2]
        sub = zb[y0:y1 + 1, x0:x1 + 1]; m &= ZZ < sub
        sub[m] = ZZ[m]; img[y0:y1 + 1, x0:x1 + 1][m] = s
    D = zb.copy(); fondo = ~np.isfinite(D); D[fondo] = np.nanmax(D[~fondo]) + 50
    gx = np.abs(np.diff(D, axis=1, prepend=D[:, :1])); gy = np.abs(np.diff(D, axis=0, prepend=D[:1]))
    img[np.maximum(gx, gy) > 3] *= 0.45
    img[fondo] = 1.0
    return Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))
