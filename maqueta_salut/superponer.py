"""Comprobacion objetiva: renderiza el modelo con una camara en perspectiva y superpone sus aristas (rojo)
sobre una foto. Camara definida en coordenadas de solar (m): posicion por azimut/elevacion/distancia respecto a
un punto objetivo, campo de vision horizontal y giro (roll).
Uso: python3 superponer.py FOTO az el dist tx ty tz fov [roll] [salida]"""
import math
import sys
import numpy as np
import trimesh
from PIL import Image, ImageDraw
import salut_v2 as s

_M = s.construir(escalar=False)
_ANG = math.degrees(math.atan2(s._U[1], s._U[0]))
_Ms = _M.rotate((0, 0, _ANG)).translate((s.CEN[0], s.CEN[1], 0))
_m = _Ms.to_mesh()
T = trimesh.Trimesh(np.asarray(_m.vert_properties)[:, :3], np.asarray(_m.tri_verts), process=False)


def camara(az, el, dist, tgt, fov, roll, W, H):
    a, e = math.radians(az), math.radians(el)
    tgt = np.array(tgt, float)
    c = tgt + dist * np.array([math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)])
    d = tgt - c; d /= np.linalg.norm(d)
    r = np.cross(d, [0, 0, 1]); r /= np.linalg.norm(r)
    up = np.cross(r, d)
    rr = math.radians(roll)
    r, up = r * math.cos(rr) + up * math.sin(rr), -r * math.sin(rr) + up * math.cos(rr)
    f = (W / 2) / math.tan(math.radians(fov) / 2)
    return c, r, up, d, f


def render(cam, W, H):
    c, r, up, d, f = cam
    v = T.vertices - c
    X, Y, Z = v @ r, v @ up, v @ d
    px, py = W / 2 + f * X / Z, H / 2 - f * Y / Z
    zb = np.full((H, W), np.inf); nid = np.zeros((H, W), int) - 1
    cen = T.triangles_center - c
    vis = np.einsum("ij,ij->i", T.face_normals, cen) < 0
    for fi in np.nonzero(vis)[0]:
        fc = T.faces[fi]
        x, y, z = px[fc], py[fc], Z[fc]
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
        m = (l0 >= -1e-6) & (l1 >= -1e-6) & (l2 >= -1e-6)
        ZZ = l0 * z[0] + l1 * z[1] + l2 * z[2]
        sub = zb[y0:y1 + 1, x0:x1 + 1]; m &= ZZ < sub
        sub[m] = ZZ[m]; nid[y0:y1 + 1, x0:x1 + 1][m] = fi
    return zb, nid


def aristas(zb, nid):
    ok = nid >= 0
    D = np.where(ok, zb, 1e6)
    nrm = np.zeros(nid.shape + (3,)); nrm[ok] = T.face_normals[nid[ok]]
    e = np.zeros(zb.shape, bool)
    for ax in (0, 1):
        D2 = np.roll(D, -1, axis=ax); ok2 = np.roll(ok, -1, axis=ax); n2 = np.roll(nrm, -1, axis=ax)
        borde = ok ^ ok2                                             # silueta
        salto = ok & ok2 & (np.abs(D - D2) / np.maximum(D, 1) > 0.004)
        pliegue = ok & ok2 & (np.sum(nrm * n2, axis=2) < 0.7)
        e |= borde | salto | pliegue
    return e


def superponer(foto, az, el, dist, tgt, fov, roll=0.0, salida=None, alfa=0.55):
    im = Image.open(foto).convert("RGB")
    W, H = im.size
    zb, nid = render(camara(az, el, dist, tgt, fov, roll, W, H), W, H)
    e = aristas(zb, nid)
    a = np.asarray(im).astype(float)
    gris = a.mean(axis=2, keepdims=True) * 0.85 + 30
    a = gris.repeat(3, axis=2)
    msk = np.isfinite(zb)
    a[msk] = a[msk] * (1 - 0.18) + np.array([90, 140, 255]) * 0.18        # volumen del modelo: velo azul
    a[e] = np.array([255, 0, 0])                                            # aristas del modelo: rojo
    out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    if salida:
        out.save(salida)
    return out


if __name__ == "__main__":
    f = sys.argv[1]
    az, el, dist, tx, ty, tz, fov = map(float, sys.argv[2:9])
    roll = float(sys.argv[9]) if len(sys.argv) > 9 else 0.0
    sal = sys.argv[10] if len(sys.argv) > 10 else "superpuesta.png"
    superponer(f, az, el, dist, (tx, ty, tz), fov, roll, sal)
    print("ok", sal)
