"""Dibujo arquitectonico por lineas a partir de la definicion 'edificio':
- lo VISTO: aristas (siluetas gruesas, pliegues finos) obtenidas de un render ortogonal con z-buffer;
- lo CORTADO: poligonos de corte con trama y contorno grueso;
- lo de ENCIMA (en plantas): proyeccion en discontinua."""
import math
import numpy as np
from manifold3d import Manifold

RES = 0.04          # m por pixel del render de aristas


def _malla(m):
    me = m.to_mesh()
    V = np.asarray(me.vert_properties)[:, :3].astype(float)
    F = np.asarray(me.tri_verts).astype(int)
    return V, F


def vista(m, res=RES):
    """render ortogonal mirando hacia -z de 'm' (ya orientado). Devuelve (imagen de lineas RGBA, extent)."""
    V, F = _malla(m)
    if len(F) == 0:
        return None, None
    tri = V[F]
    nrm = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    ln = np.linalg.norm(nrm, axis=1); ok = ln > 1e-12
    nrm[ok] /= ln[ok, None]
    vis = ok & (nrm[:, 2] > 1e-6)
    x0, y0 = V[:, 0].min() - 0.5, V[:, 1].min() - 0.5
    x1, y1 = V[:, 0].max() + 0.5, V[:, 1].max() + 0.5
    W, H = int((x1 - x0) / res) + 1, int((y1 - y0) / res) + 1
    zb = np.full((H, W), -np.inf); fid = np.full((H, W), -1)
    px = (V[:, 0] - x0) / res; py = (y1 - V[:, 1]) / res; pz = V[:, 2]
    for f in np.nonzero(vis)[0]:
        a, b, c = F[f]
        x = px[[a, b, c]]; y = py[[a, b, c]]; z = pz[[a, b, c]]
        xa, xb = max(int(x.min()), 0), min(int(x.max()) + 1, W - 1)
        ya, yb = max(int(y.min()), 0), min(int(y.max()) + 1, H - 1)
        if xb < xa or yb < ya:
            continue
        XX, YY = np.meshgrid(np.arange(xa, xb + 1) + 0.5, np.arange(ya, yb + 1) + 0.5)
        den = (y[1] - y[2]) * (x[0] - x[2]) + (x[2] - x[1]) * (y[0] - y[2])
        if abs(den) < 1e-12:
            continue
        l0 = ((y[1] - y[2]) * (XX - x[2]) + (x[2] - x[1]) * (YY - y[2])) / den
        l1 = ((y[2] - y[0]) * (XX - x[2]) + (x[0] - x[2]) * (YY - y[2])) / den
        l2 = 1 - l0 - l1
        msk = (l0 >= -1e-6) & (l1 >= -1e-6) & (l2 >= -1e-6)
        ZZ = l0 * z[0] + l1 * z[1] + l2 * z[2]
        sub = zb[ya:yb + 1, xa:xb + 1]
        msk &= ZZ > sub
        sub[msk] = ZZ[msk]
        fid[ya:yb + 1, xa:xb + 1][msk] = f
    occ = fid >= 0
    N = np.zeros((H, W, 3)); N[occ] = nrm[fid[occ]]
    D = np.where(occ, zb, -1e6)
    sil = np.zeros((H, W), bool); cre = np.zeros((H, W), bool)
    for ax in (0, 1):
        o2 = np.roll(occ, -1, axis=ax); D2 = np.roll(D, -1, axis=ax); N2 = np.roll(N, -1, axis=ax)
        sil |= occ ^ o2
        both = occ & o2
        sil |= both & (np.abs(D - D2) > 0.6)                     # salto de profundidad grande: contorno
        cre |= both & (np.abs(D - D2) > 0.08)                    # escalon (poyetes, entrantes)
        cre |= both & (np.sum(N * N2, axis=2) < 0.94)            # pliegue (> ~20 grados)
    img = np.zeros((H, W, 4))
    img[cre] = (0.25, 0.25, 0.25, 0.85)
    sil2 = sil | np.roll(sil, 1, axis=0) | np.roll(sil, 1, axis=1)
    img[sil2] = (0, 0, 0, 1)
    img[:, :, 3][~(cre | sil2)] = 0
    return img, (x0, x1, y0, y1)


def dibujar_vista(ax, m, res=RES, z=0):
    img, ext = vista(m, res)
    if img is not None:
        ax.imshow(img, extent=ext, interpolation="antialiased", zorder=z)


def corte(ax, cs, z=5):
    """poligonos de corte con trama y contorno grueso"""
    from matplotlib.patches import Polygon
    for P in cs.to_polygons():
        P = np.array(P)
        ax.add_patch(Polygon(P, closed=True, fc="#d9d9d9", ec="none", hatch="////", lw=0, zorder=z))
        ax.add_patch(Polygon(P, closed=True, fc="none", ec="k", lw=1.8, zorder=z + 1))


def encima(ax, m, z=4):
    from matplotlib.patches import Polygon
    for P in m.project().to_polygons():
        ax.add_patch(Polygon(np.array(P), closed=True, fc="none", ec="0.35", lw=0.6, ls=(0, (4, 3)), zorder=z))


def nivel(ax, x, z, txt):
    ax.plot([x, x + 1.2], [z, z], color="k", lw=0.6)
    ax.plot([x + 0.3, x + 0.6, x + 0.9, x + 0.3], [z + 0.6, z, z + 0.6, z + 0.6], color="k", lw=0.6)
    ax.text(x + 1.5, z + 0.1, f"+{z:.2f} {txt}".replace(".", ","), fontsize=6.5, va="bottom")


def cota(ax, p0, p1, off, txt="", fs=6.5, color="k"):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = p1 - p0; L = np.linalg.norm(d)
    if L < 1e-6:
        return
    t = d / L; n = np.array([-t[1], t[0]])
    a, b = p0 + n * off, p1 + n * off
    ax.plot(*zip(a, b), color=color, lw=0.5)
    for p, q in ((p0, a), (p1, b)):
        ax.plot(*zip(p + n * 0.3 * np.sign(off), q + n * 0.4 * np.sign(off)), color=color, lw=0.35)
        ax.plot(*zip(q - (t + n) * 0.35, q + (t + n) * 0.35), color=color, lw=0.8)
    ang = math.degrees(math.atan2(t[1], t[0]))
    if ang > 90: ang -= 180
    if ang <= -90: ang += 180
    mid = (a + b) / 2 + n * 0.25 * np.sign(off if off else 1)
    ax.text(*mid, (txt + " " if txt else "") + f"{L:.2f}".replace(".", ","), fontsize=fs, ha="center",
            va="bottom" if off >= 0 else "top", rotation=ang, rotation_mode="anchor", color=color)
