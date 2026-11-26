"""Dibujo arquitectonico por lineas a partir de la definicion 'edificio':
- lo VISTO: aristas (siluetas gruesas, pliegues finos) obtenidas de un render ortogonal con z-buffer;
- lo CORTADO: poligonos de corte con trama y contorno grueso;
- lo de ENCIMA (en plantas): proyeccion en discontinua."""
import math
import numpy as np
import matplotlib as _mpl
_mpl.rcParams["hatch.color"] = "0.45"; _mpl.rcParams["hatch.linewidth"] = 0.35
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


def corte(ax, cs, z=5, muro=0.30, huecos=(), polys=None, hatch="......"):
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
        hueco = sp.buffer(-muro, join_style=2)
        if not hueco.is_empty: hueco = hueco.buffer(-0.25, join_style=2).buffer(0.25, join_style=2)   # sin rendijas en pilares
        if hueco.is_empty or hueco.area < 1.5:                                                       # pilares y muros cortos: macizos
            anillos.append(sp); continue
        anillos.append(sp.difference(hueco))
    if not anillos: return
    muros = unary_union(anillos)
    # orientación de cada hueco decidida AQUÍ, contra el muro dibujado: el símbolo siempre dentro del espesor [estándar de planos]
    from shapely.geometry import Point
    hs = []
    for h in huecos:
        h = dict(h); p, n, e = np.array(h["p"]), np.array(h["n"]), h.get("e", muro)
        den = lambda q: muros.distance(Point(*q)) < 0.02
        if not den(p - n * e / 2) and den(p + n * e / 2):
            h["n"] = tuple(-n)
        elif not den(p - n * e / 2) and not den(p + n * e / 2):
            for k in (0.5, 1.0, 1.5):                       # el muro real está algo desplazado: busca la cara más cercana
                if den(p - n * (e / 2 + k)): h["p"] = tuple(p - n * k); break
                if den(p + n * (e / 2 + k)): h["p"] = tuple(p + n * k); h["n"] = tuple(-n); break
        hs.append(h)
    huecos = hs
    aberturas = []
    for h in huecos:
        p, t, n, w, e = np.array(h["p"]), np.array(h["t"]), np.array(h["n"]), h["w"], h.get("e", muro)
        a0, a1 = p - t * w / 2, p + t * w / 2
        aberturas.append(SP([a0 + n * 0.4, a1 + n * 0.4, a1 - n * (e + 0.4), a0 - n * (e + 0.4)]))
    if aberturas:
        muros = muros.difference(unary_union(aberturas))
    for gm in getattr(muros, "geoms", [muros]):
        if gm.is_empty or gm.geom_type != "Polygon": continue
        ax.add_patch(Polygon(np.array(gm.exterior.coords), closed=True, fc="white", ec="k", lw=1.1, hatch=hatch, zorder=z))   # cortado: el valor de línea más grueso   # muro cortado: blanco con trama punteada (estándar)
        for it in gm.interiors:
            ax.add_patch(Polygon(np.array(it.coords), closed=True, fc="white", ec="k", lw=0.9, zorder=z + 0.5))
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
        # ventana (estándar de planos): jambas cerradas, cara exterior e interior finas, marco en doble línea fina,
        # vidrio en línea media y vierteaguas exterior
        for q in (a0, a1):
            ax.plot(*zip(q, q - n * e), color="k", lw=0.9, zorder=z + 2)
        for off, lw in ((0.0, 0.35), (e, 0.35), (0.40 * e, 0.3), (0.60 * e, 0.3), (0.5 * e, 0.6)):
            ax.plot(*zip(a0 - n * off, a1 - n * off), color="k", lw=lw, zorder=z + 2)
        ax.plot(*zip(a0 + n * 0.06 - t * 0.05, a1 + n * 0.06 + t * 0.05), color="k", lw=0.3, zorder=z + 2)


def encima(ax, m, z=4, muro=0.30):
    """lo que queda por encima del corte, proyectado: muro con dos líneas discontinuas"""
    from matplotlib.patches import Polygon
    from shapely.geometry import Polygon as SP
    for P in m.project().to_polygons():
        P = np.array(P)
        ax.add_patch(Polygon(P, closed=True, fc="none", ec="0.3", lw=0.7, ls=(0, (5, 3)), zorder=z))
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
    ax.plot(*zip(a, b), color=color, lw=0.3)
    for p, q in ((p0, a), (p1, b)):
        if abs(off) > 0.05:
            ax.plot(*zip(p + n * 0.3 * np.sign(off), q + n * 0.4 * np.sign(off)), color=color, lw=0.2)
        ax.plot(*zip(q - (t + n) * 0.3, q + (t + n) * 0.3), color=color, lw=0.6)
    ang = math.degrees(math.atan2(t[1], t[0]))
    if ang > 90: ang -= 180
    if ang <= -90: ang += 180
    mid = (a + b) / 2 + n * 0.25 * np.sign(off if off else 1)
    ax.text(*mid, (txt + " " if txt else "") + f"{L:.2f}".replace(".", ","), fontsize=fs, ha="center",
            va="bottom" if off >= 0 else "top", rotation=ang, rotation_mode="anchor", color=color)


def vista_vectorial(ax, m, ztop=None, z=1, lw_alto=0.7, lw_bajo=0.3):
    """planta vista desde arriba en VECTORES con líneas ocultas: se recorren los niveles de la malla de arriba abajo y en
    cada uno se dibuja solo el contorno que no tapa lo que hay encima (calidad de plano, sin raster)."""
    from shapely.geometry import Polygon as SP
    from shapely.ops import unary_union
    vz = np.asarray(m.to_mesh().vert_properties)[:, 2]
    if ztop is not None: vz = vz[vz < ztop - 0.01]
    if len(vz) == 0: return
    lev = np.unique(np.round(vz, 2))[::-1]
    if len(lev) > 160: lev = lev[np.linspace(0, len(lev) - 1, 160).astype(int)]
    cub = None; zmax = lev[0]
    for zz in lev:
        polys = [SP(np.array(P)).buffer(0) for P in m.slice(float(zz) - 0.015).to_polygons() if len(P) > 2]
        if not polys: continue
        g = unary_union(polys)
        vis = g.boundary if cub is None else g.boundary.difference(cub)
        lw = lw_bajo + (lw_alto - lw_bajo) * (zz - lev[-1]) / max(zmax - lev[-1], 1e-6)
        for ln in getattr(vis, "geoms", [vis]):
            if ln.is_empty or ln.length < 0.05: continue
            if ln.geom_type in ("LineString", "LinearRing"):
                ax.plot(*np.array(ln.coords).T, color="k", lw=lw, zorder=z, solid_capstyle="butt")
        cub = g if cub is None else unary_union([cub, g])


def terreno(ax, u0, u1, prof=1.2, z=6):
    """volumen de terreno cortado bajo la rasante: línea gruesa continua y trama de tierra (Ching, pp. 72-73, 86)"""
    from matplotlib.patches import Rectangle
    ax.add_patch(Rectangle((u0, -prof), u1 - u0, prof, fc="white", ec="none", hatch="\\\\..", zorder=z - 0.5))
    ax.plot([u0, u1], [0, 0], color="k", lw=1.8, zorder=z + 5, solid_capstyle="butt")


def figura(ax, u, z0=0.0, h=1.75, z=40):
    """figura humana esquemática para la escala (Ching, p. 71 y 78)"""
    from matplotlib.patches import Circle, Polygon
    ax.add_patch(Circle((u, z0 + h - 0.12), 0.12, fc="white", ec="k", lw=0.5, zorder=z))
    ax.add_patch(Polygon([(u - 0.2, z0 + h - 0.26), (u + 0.2, z0 + h - 0.26), (u + 0.15, z0 + 0.85), (u + 0.12, z0),
                          (u + 0.02, z0), (u, z0 + 0.8), (u - 0.02, z0), (u - 0.12, z0), (u - 0.15, z0 + 0.85)], closed=True,
                         fc="white", ec="k", lw=0.5, zorder=z))
