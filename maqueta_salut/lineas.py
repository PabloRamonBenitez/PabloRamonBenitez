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


def corte(ax, cs, z=5, muro=0.30, huecos=(), polys=None):
    """corte arquitectónico: muro de 'muro' m (trama + contorno grueso), interior hueco; los huecos del catálogo
    (en coordenadas del dibujo: dict p, t, n, w, e, tipo) abren el muro y llevan su símbolo."""
    from matplotlib.patches import Polygon, Arc
    from shapely.geometry import Polygon as SP
    from shapely.ops import unary_union
    anillos = []
    src = polys if polys is not None else [np.array(P) for P in cs.to_polygons()]
    for P in src:
        P = np.array(P)
        if len(P) < 3: continue
        sp = SP(P).buffer(0)
        if sp.is_empty: continue
        hueco = sp.buffer(-muro)
        anillos.append(sp.difference(hueco) if not hueco.is_empty else sp)
    if not anillos: return
    muros = unary_union(anillos)
    aberturas = []
    for h in huecos:
        p, t, n, w, e = np.array(h["p"]), np.array(h["t"]), np.array(h["n"]), h["w"], h.get("e", muro)
        a0, a1 = p - t * w / 2, p + t * w / 2
        aberturas.append(SP([a0 + n * 0.4, a1 + n * 0.4, a1 - n * (e + 0.4), a0 - n * (e + 0.4)]))
    if aberturas:
        muros = muros.difference(unary_union(aberturas))
    for gm in getattr(muros, "geoms", [muros]):
        if gm.is_empty or gm.geom_type != "Polygon": continue
        ax.add_patch(Polygon(np.array(gm.exterior.coords), closed=True, fc="#9a9a9a", ec="k", lw=1.3, zorder=z))
        for it in gm.interiors:
            ax.add_patch(Polygon(np.array(it.coords), closed=True, fc="white", ec="k", lw=1.3, zorder=z + 0.5))
    for h in huecos:                                     # símbolo
        p, t, n, w, e = np.array(h["p"]), np.array(h["t"]), np.array(h["n"]), h["w"], h.get("e", muro)
        a0, a1 = p - t * w / 2, p + t * w / 2
        if h["tipo"] == "puerta":
            ax.plot(*zip(a0, a1), color="k", lw=0.5, zorder=z + 2)
            q = a0 - n * e; ax.plot(*zip(q, q - n * w), color="k", lw=0.9, zorder=z + 2)
            ang0 = math.degrees(math.atan2(-n[1], -n[0])); ang1 = math.degrees(math.atan2(t[1], t[0]))
            d = (ang1 - ang0) % 360
            lo, hi = (ang0, ang0 + d) if d <= 180 else (ang1, ang1 + 360 - d)
            ax.add_patch(Arc(q, 2 * w, 2 * w, theta1=lo, theta2=hi, lw=0.5, color="k", zorder=z + 2))
            continue
        for off in (0.0, e):                                                             # caras del muro
            ax.plot(*zip(a0 - n * off, a1 - n * off), color="k", lw=0.5, zorder=z + 2)
        for off in (0.42 * e, 0.58 * e):                                                 # carpintería y vidrio: doble línea
            ax.plot(*zip(a0 - n * off, a1 - n * off), color="k", lw=0.9, zorder=z + 2)


def encima(ax, m, z=4, muro=0.30):
    """lo que queda por encima del corte, proyectado: muro con dos líneas discontinuas"""
    from matplotlib.patches import Polygon
    from shapely.geometry import Polygon as SP
    for P in m.project().to_polygons():
        P = np.array(P)
        ax.add_patch(Polygon(P, closed=True, fc="none", ec="0.35", lw=0.6, ls=(0, (4, 3)), zorder=z))
        sp = SP(P).buffer(0)
        if sp.is_empty or sp.area < 4: continue
        inn = sp.buffer(-muro)
        for gm in getattr(inn, "geoms", [inn]):
            if gm.geom_type == "Polygon" and not gm.is_empty:
                ax.add_patch(Polygon(np.array(gm.exterior.coords), closed=True, fc="none", ec="0.5", lw=0.4, ls=(0, (4, 3)), zorder=z))


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
