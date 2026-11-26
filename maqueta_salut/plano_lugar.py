"""PLANO DE LUGAR (situación) 1984 – Ching, Manual de dibujo arquitectónico, «Dibujar la planta de situación»:
el edificio como FIGURA CLARA (su planta de cubiertas, del modelo verificado) sobre un FONDO con valor tonal dado por el
paisaje (césped punteado, arbolado, pavimentos, viales); linde con trazo largo y dos puntos; norte y escala gráfica;
misma orientación que el resto de las plantas. Solo líneas (sin colores).
Entorno según las fotos de 1984 (antes de las vallas posteriores):
  plaza ante el chaflán con autobuses ......... F14, F15, F70, F01
  calle Ivana Mazepy a lo largo del ala corta .. F09 (rótulos), F19, F72
  fuente en media luna al pie de la columna ..... F01, F14, F15 (modelo)
  césped junto al ala larga y camino de coches que la rodea por detrás ... F47 y F73 (marcas del usuario 26/11)
  parque arbolado hacia el Dniéper ............. F01, F23, F47
  colindante al otro lado de la medianera ....... F01, F72
Las posiciones del arbolado y el trazado de los caminos son APROXIMADAS (fotos oblicuas): se dibujan con su forma."""
import traduccion  # textos de los planos en ucraniano (usuario 26/11)
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, PathPatch
from matplotlib.path import Path
from PIL import Image
from shapely.geometry import Polygon as SP, Point, LineString
from shapely.ops import unary_union
import edificio as E, laminas as LM, imprimir as IA

V = E._v; T = np.array(E.T); U = np.array(E.U); N = np.array(E.N)
SW = lambda x, y: np.array(E.SWP(x, y))
rng = np.random.default_rng(1984)
DEN = 750
XL, YL = (-58, 62), (-44, 120)
A3L = (420, 297)

M = LM.M
huella = unary_union([SP(np.array(P)).buffer(0) for P in M.project().to_polygons() if len(P) > 2]).buffer(0.05)


def _polys(g):
    """solo las partes poligonales (una intersección puede dejar líneas o puntos sueltos)"""
    if g is None or g.is_empty: return []
    out = []
    for x in getattr(g, "geoms", [g]):
        if x.geom_type == "Polygon" and not x.is_empty: out.append(x)
        elif x.geom_type in ("MultiPolygon", "GeometryCollection"): out += _polys(x)
    return out


def poly(ax, pts, **k):
    ax.add_patch(Polygon(np.asarray(pts), closed=True, **k))


def punteado(ax, geom, dens=0.55, ms=0.35, z=1):
    """césped: punteado aleatorio (Ching: textura del suelo) dentro de geom, fuera del edificio"""
    g = geom.difference(huella)
    if g.is_empty: return
    x0, y0, x1, y1 = g.bounds
    n = int(g.area * dens)
    pts = np.c_[rng.uniform(x0, x1, n * 2), rng.uniform(y0, y1, n * 2)]
    from shapely import contains_xy
    pts = pts[contains_xy(g, pts[:, 0], pts[:, 1])][:n]
    ax.plot(pts[:, 0], pts[:, 1], ",", color="k", ms=ms, zorder=z)
    for gg in _polys(g):
        ax.plot(*gg.exterior.xy, color="k", lw=0.35, zorder=z + 0.1)


def arbol(ax, c, r, z=5):
    """símbolo de árbol en planta (copa festoneada + tronco), Ching"""
    t = np.linspace(0, 2 * math.pi, 60)
    rr = r * (1 + 0.07 * np.sin(9 * t + rng.uniform(0, 6)))
    sh = SP(np.c_[c[0] + rr * np.cos(t), c[1] + rr * np.sin(t)]).difference(huella)
    for g in _polys(sh):
        if g.area < 1: continue
        ax.add_patch(Polygon(np.c_[g.exterior.xy], closed=True, fc="white", ec="k", lw=0.45, zorder=z))
    if not huella.contains(Point(c)):
        ax.add_patch(Circle(c, 0.25, fc="k", ec="none", zorder=z + 0.1))
        for a in np.linspace(0, 2 * math.pi, 7)[:-1] + rng.uniform(0, 1):
            ax.plot([c[0], c[0] + 0.55 * r * math.cos(a)], [c[1], c[1] + 0.55 * r * math.sin(a)], color="k", lw=0.2, zorder=z + 0.05)


def via(ax, linea, ancho, z=2, eje=True):
    """vial: bordillos a ±ancho/2 (línea media) y eje a trazos"""
    ls = LineString(linea); b = ls.buffer(ancho / 2, cap_style=2, join_style=1).difference(huella)
    for g in _polys(b):
        ax.add_patch(Polygon(np.c_[g.exterior.xy], closed=True, fc="white", ec="k", lw=0.7, zorder=z))
    if eje:
        l2 = ls.difference(huella)
        for g in getattr(l2, "geoms", [l2]):
            ax.plot(*g.xy, color="k", lw=0.3, ls=(0, (6, 4)), zorder=z + 0.1)
    return b


def senda(ax, linea, ancho, z=2.0):
    """camino peatonal (Ching): bordes finos y despiece de losas cada 1,0 m (línea superficial)"""
    ls = LineString(linea); b = ls.buffer(ancho / 2, cap_style=2, join_style=2).difference(huella)
    for g in _polys(b):
        ax.add_patch(Polygon(np.c_[g.exterior.xy], closed=True, fc="white", ec="k", lw=0.45, zorder=z))
    L_ = ls.length
    for d in np.arange(0.5, L_, 1.0):
        p = np.array(ls.interpolate(d).coords[0]); q = np.array(ls.interpolate(min(d + 0.01, L_)).coords[0]) - p
        if np.linalg.norm(q) < 1e-6: continue
        q = q / np.linalg.norm(q); n = np.array([-q[1], q[0]]) * ancho / 2
        seg = LineString([p - n, p + n]).difference(huella)
        for g in getattr(seg, "geoms", [seg]):
            if g.length > 0.1: ax.plot(*g.xy, color="k", lw=0.12, zorder=z + 0.05)
    return b


def calzada(ax, linea, ancho, z=2.2):
    """vial de servicio: doble línea de bordillo (0,15) y eje a trazos"""
    ls = LineString(linea); b = ls.buffer(ancho / 2, cap_style=2, join_style=1).difference(huella)
    bi = ls.buffer(ancho / 2 - 0.15, cap_style=2, join_style=1)
    for g in _polys(b):
        ax.add_patch(Polygon(np.c_[g.exterior.xy], closed=True, fc="white", ec="k", lw=0.75, zorder=z))
    for g in _polys(bi.difference(huella)):
        ax.plot(*g.exterior.xy, color="k", lw=0.3, zorder=z + 0.05)
    l2 = ls.difference(huella)
    for g in getattr(l2, "geoms", [l2]):
        ax.plot(*g.xy, color="k", lw=0.3, ls=(0, (6, 4)), zorder=z + 0.1)
    return b


def camion(ax, p, d, L=9.0, W=2.5, z=9):
    """silueta de camión rígido de servicio en planta (cabina + caja), centrado en p y orientado según d"""
    d = np.asarray(d, float) / np.linalg.norm(d); n = np.array([-d[1], d[0]])
    p = np.asarray(p, float)
    caja = [p - d * L / 2 - n * W / 2, p + d * (L / 2 - 2.2) - n * W / 2, p + d * (L / 2 - 2.2) + n * W / 2, p - d * L / 2 + n * W / 2]
    cab = [p + d * (L / 2 - 2.1) - n * (W / 2 - 0.05), p + d * (L / 2) - n * (W / 2 - 0.25), p + d * (L / 2) + n * (W / 2 - 0.25),
           p + d * (L / 2 - 2.1) + n * (W / 2 - 0.05)]
    ax.add_patch(Polygon(caja, closed=True, fc="white", ec="k", lw=0.6, zorder=z))
    ax.add_patch(Polygon(cab, closed=True, fc="white", ec="k", lw=0.6, zorder=z))
    for t_ in (-L / 2 + 1.3, L / 2 - 1.6):                       # ejes
        for s_ in (-1, 1):
            c = p + d * t_ + n * s_ * (W / 2 - 0.15)
            ax.add_patch(Polygon([c - d * 0.5 - n * 0.15, c + d * 0.5 - n * 0.15, c + d * 0.5 + n * 0.15, c - d * 0.5 + n * 0.15],
                                 closed=True, fc="k", ec="k", lw=0.2, zorder=z + 0.1))


def hoja_lugar():
    fig = IA.pagina(A3L, "PLANO DE LUGAR 1984 – situación del hotel y entorno según las fotos de la época")
    ax, (aw, ah) = IA.eje_escala(fig, (14, 36), XL, YL, DEN)
    ax.set_xlim(*XL); ax.set_ylim(*YL); ax.set_aspect("equal"); ax.axis("off")
    marco = SP([(XL[0], YL[0]), (XL[1], YL[0]), (XL[1], YL[1]), (XL[0], YL[1])])

    # --- 1. calle Ivana Mazepy (a lo largo del ala corta) y plaza ante el chaflán
    yf = -(E.R_COL - E.RET) - V["RETR"]
    x0 = -V["L_C"]
    calle = SP([SW(x0 - 60, -4.0), SW(40, -4.0), SW(40, -18.0), SW(x0 - 60, -18.0)])
    acera = SP([SW(x0 - 60, -0.0), SW(10, -0.0), SW(10, -4.0), SW(x0 - 60, -4.0)])
    plaza = SP([E.P(-30, yf - 0.5), E.P(48, yf - 0.5), E.P(48, -42), E.P(-30, -42)]).union(
            SP([SW(-2, -4.0), SW(40, -4.0), SW(40, -18), SW(-2, -18)])).difference(calle).difference(huella).intersection(
            SP([SW(x0 - 60, -4.0), SW(120, -4.0), SW(120, 200), SW(x0 - 60, 200)]))                        # solo del lado del hotel
    plaza = plaza.difference(SP([(E.W_P + 6.5, 18.0), (200, 18.0), (200, 200), (E.W_P + 6.5, 200)]))                # hasta el camino y el parque
    for g in _polys(plaza):
        poly(ax, np.c_[g.exterior.xy], fc="white", ec="k", lw=0.6, zorder=1)
    for s in np.arange(-30, 49, 4.0):                                # despiece del pavimento de la plaza (línea superficial)
        l = LineString([E.P(s, yf - 0.5), E.P(s, -42)]).intersection(plaza)
        for g in getattr(l, "geoms", [l]):
            if g.length > 0.5: ax.plot(*g.xy, color="k", lw=0.12, zorder=1.1)
    for s in np.arange(yf - 4.5, -42, -4.0):
        l = LineString([E.P(-30, s), E.P(48, s)]).intersection(plaza)
        for g in getattr(l, "geoms", [l]):
            if g.length > 0.5: ax.plot(*g.xy, color="k", lw=0.12, zorder=1.1)
    c_ = calle.intersection(marco)
    poly(ax, np.c_[c_.exterior.xy], fc="white", ec="k", lw=0.9, zorder=1.5)
    ax.plot(*zip(SW(x0 - 60, -11.0), SW(40, -11.0)), color="k", lw=0.35, ls=(0, (10, 6)), zorder=1.6)
    a_ = acera.intersection(marco).difference(huella)
    for g in _polys(a_): poly(ax, np.c_[g.exterior.xy], fc="white", ec="k", lw=0.5, zorder=1.4)
    for i in range(5):                                               # autobuses en fila ante el chaflán (F14, F15, F70)
        c = np.array(E.P(8 + i * 3.6, -24))
        poly(ax, [c - U * 1.25 - N * 5.6, c + U * 1.25 - N * 5.6, c + U * 1.25 + N * 5.6, c - U * 1.25 + N * 5.6], fc="white", ec="k", lw=0.5, zorder=3)

    # --- 2. lado exterior del ala larga: VIARIO DE SERVICIO (camión rígido de 9 m) y caminos peatonales (marcas del usuario)
    #  · calzada de servicio de 5,0 m (doble sentido) paralela al ala: lo que aún se ve en Google Maps (F35) y en F47/F73
    #  · entra y sale por la plaza con una curva de radio ≥ 12 m
    #  · al final, junto al testero, GLORIETA DE GIRO: bordillo exterior R 10,0 e isleta R 4,0 → el camión da la vuelta sin maniobras
    #  · peatonales (trazado verde del usuario): ramal en diagonal a la plaza, enlace y camino pegado al césped que rodea el testero
    xr = E.W_P + 9.0; yh = E.L_L - 15.0; xc = E.W_P + 2.2; yt = E.L_L + 4.0
    Cg = np.array([xr + 1.5, E.L_L + 3.5]); Rg, Ri = 10.0, 4.0
    ypz = 17.5                                                    # borde de la plaza (pavimento por el que entran los vehículos)
    A = [(xr, Cg[1] - Rg + 0.5), (xr, ypz - 1.0)]
    b_veh = calzada(ax, A, 5.0)
    for sg in (-1, 1):                                            # embocadura en la plaza: acuerdos de R 4,0 a cada lado
        cc = np.array([xr + sg * (2.5 + 4.0), ypz + 4.0])
        arc = [tuple(cc + 4.0 * np.array([math.cos(a), math.sin(a)])) for a in (np.linspace(math.pi, 1.5 * math.pi, 10) if sg > 0 else np.linspace(1.5 * math.pi, 2 * math.pi, 10))]
        ax.plot(*zip(*arc), color="k", lw=0.75, zorder=2.3)
        fil = SP([(xr + sg * 2.5, ypz + 4.0)] + arc + [(xr + sg * 2.5, ypz)]).buffer(0)
        if not fil.is_empty:
            ax.add_patch(Polygon(np.c_[fil.exterior.xy], closed=True, fc="white", ec="none", zorder=2.21))
            b_veh = b_veh.union(fil)
    glorieta = Point(*Cg).buffer(Rg).difference(huella)
    for g in _polys(glorieta):
        ax.add_patch(Polygon(np.c_[g.exterior.xy], closed=True, fc="white", ec="k", lw=0.75, zorder=2.25))
    ax.add_patch(Circle(tuple(Cg), Rg - 0.15, fill=False, ec="k", lw=0.3, zorder=2.3))
    isleta = Point(*Cg).buffer(Ri)
    ax.add_patch(Circle(tuple(Cg), Ri, fc="white", ec="k", lw=0.75, zorder=2.4))
    b_veh = b_veh.union(glorieta)
    # peatonales (trazado verde del usuario): 2,5 m, losas
    B2 = [(xr + 2.6, 42.0), (xr + 6.0, 34.0), (xr + 13.0, 22.0)]
    H = [(xr - 2.6, yh), (xc, yh)]
    C = [(xc, yh), (xc, E.L_L + 1.5)] + [(xc - 2.5 + 2.5 * math.cos(a), E.L_L + 1.5 + 2.5 * math.sin(a)) for a in np.linspace(0, math.pi / 2, 8)][1:] + \
        [(E.W_P / 2, yt), (1.5, yt)] + [(1.5 - 2.5 + 2.5 * math.cos(a), yt - 2.5 + 2.5 * math.sin(a)) for a in np.linspace(math.pi / 2, math.pi, 8)][1:] + [(-1.0, E.L_L + 0.6)]
    b_pea = unary_union([senda(ax, B2, 2.5), senda(ax, H, 2.5), senda(ax, C, 2.5)]).difference(b_veh)
    b_cam = b_veh.union(b_pea).union(isleta)
    # RECORRIDO DEL CAMIÓN: eje (trazo y punto) y envolvente de barrido (discontinuas); sube por el carril este, gira en la glorieta
    # en sentido antihorario y baja por el carril oeste
    rc = (Rg + Ri) / 2
    ida = [(xr + 1.25, ypz - 1.0), (xr + 1.25, Cg[1] - math.sqrt(rc ** 2 - (xr + 1.25 - Cg[0]) ** 2))]
    a0 = math.atan2(ida[-1][1] - Cg[1], ida[-1][0] - Cg[0]); xv = xr - 1.25
    a1 = math.atan2(-math.sqrt(rc ** 2 - (xv - Cg[0]) ** 2), xv - Cg[0]) + 2 * math.pi
    giro = [tuple(Cg + rc * np.array([math.cos(a), math.sin(a)])) for a in np.linspace(a0, a1, 60)]
    vuelta = [giro[-1], (xv, ypz - 1.0)]
    eje = LineString(ida + giro[1:] + vuelta[1:])
    ax.plot(*eje.xy, color="k", lw=0.5, ls=(0, (10, 2, 1, 2)), zorder=8.5)
    for off, lw in ((1.25 + 0.5, 0.35), (-(1.25 + 0.8), 0.35)):       # barrido: vuelo exterior y rueda trasera interior
        env = eje.parallel_offset(abs(off), "right" if off > 0 else "left", join_style=1)
        for g in getattr(env, "geoms", [env]):
            ax.plot(*g.xy, color="k", lw=lw, ls=(0, (4, 2)), zorder=8.4)
    for dd in (8.0, 40.0, eje.length - 30.0, eje.length - 8.0):        # flechas de sentido
        p = np.array(eje.interpolate(dd).coords[0]); q = np.array(eje.interpolate(dd + 1.5).coords[0])
        ax.annotate("", tuple(q), tuple(p), arrowprops=dict(arrowstyle="-|>,head_width=0.35,head_length=0.8", lw=0.6, color="k"), zorder=8.6)
    camion(ax, (xr + 1.25, 62.0), (0, 1))
    ag = (a0 + a1) / 2; pg = Cg + rc * np.array([math.cos(ag), math.sin(ag)])
    camion(ax, pg, (-math.sin(ag), math.cos(ag)))
    # césped y parque (el resto del lado exterior)
    cy = E.L_L + 6.0
    cesped_ala = SP([(E.W_P, E.Y_CUNA - 30), (xr - 2.5, E.Y_CUNA - 30), (xr - 2.5, cy), (E.W_P, cy)])
    parque = SP([(xr + 2.5, 20), (XL[1], 20), (XL[1], YL[1]), (xr + 2.5, YL[1])]).union(SP([(XL[0] + 25, cy), (XL[1], cy), (XL[1], YL[1]), (XL[0] + 25, YL[1])]))
    testero = SP([(-3.0, E.L_L + 0.3), (xr - 2.5, E.L_L + 0.3), (xr - 2.5, cy), (-3.0, cy)])
    for g in (cesped_ala, parque, testero):
        punteado(ax, g.difference(b_cam).intersection(marco), dens=0.5, z=0.8)
    punteado(ax, isleta, dens=0.9, z=2.45)
    arbol(ax, tuple(Cg), 2.8, z=5)
    for c, r in (((xr + 8, 30), 4.5), ((xr + 16, 40), 4.0), ((xr + 26, 34), 5.0), ((xr + 9, 58), 3.5), ((xr + 30, 56), 4.5),
                 ((xr + 14, 74), 5.0), ((xr + 36, 74), 5.5), ((xr + 22, 112), 4.5), ((xr + 44, 96), 5.5), ((xr + 6, 112), 4.0),
                 ((-14, 112), 4.5), ((xr + 40, 40), 5.0), ((xr + 46, 62), 4.5), ((xr + 30, 108), 5.0), ((xr + 6, 86), 3.5)):
        if b_cam.distance(Point(c)) > r * 0.8: arbol(ax, c, r)

    # --- 3. colindante al otro lado de la medianera y linde
    col = SP([SW(x0 - 30, 0.0), SW(x0, 0.0), SW(x0, V["W_C"] + 8), SW(x0 - 30, V["W_C"] + 8)]).intersection(marco)
    poly(ax, np.c_[col.exterior.xy], fc="white", ec="k", lw=0.8, hatch="////", zorder=2)
    ax.text(*SW(x0 - 14, 9.0), "EDIFICIO COLINDANTE\n(F01, F72)", fontsize=6.5, ha="center", va="center", zorder=9,
            bbox=dict(fc="white", ec="none", pad=1.5))
    ax.plot(*zip(SW(x0, -0.5), SW(x0, V["W_C"] + 8)), color="k", lw=0.8, ls=(0, (12, 2, 1, 2, 1, 2)), zorder=8)

    # --- 4. EL HOTEL: figura clara = planta de cubiertas del modelo (vectorial)
    for g in _polys(huella):
        poly(ax, np.c_[g.exterior.xy], fc="white", ec="none", zorder=3.9)
    LM.L.vista_vectorial(ax, M, z=4)
    import grafismo as GR
    _ax_z = ax                                                          # rampa: contorno + flecha (Ching), sin curvas de nivel
    from matplotlib.patches import Rectangle as _R
    LM.mascara_rampas(ax, None, zb=4.5)
    for a_ in ax.patches[-1:]: pass
    GR.rampas(ax, None)
    for g in _polys(huella):
        ax.plot(*g.exterior.xy, color="k", lw=1.3, zorder=7)
    # patio interior de la L (sin foto que lo muestre)
    pat = SP([SW(x0 + V["L_LAD"], V["W_C"]), (0.0, V["W_C"]), (0.0, 45.0), (x0 + 6, 45.0)]).difference(huella)

    # --- 5. rótulos
    rot = lambda p, s, **k: ax.text(*p, s, zorder=10, **k)
    rot((50.0, 6.0), "PLAZA\n(pavimento)", fontsize=9, weight="bold", ha="center")
    rot(SW(x0 - 30, -11.0) + np.array([0, 1.2]), "calle Ivana Mazepy", fontsize=8, ha="center", rotation=math.degrees(E.PHI))
    rot(E.P(16, -31.5), "autobuses (F14, F15, F70)", fontsize=6, ha="center")
    rot((xr + 3.4, 72), "vial de servicio 5,0 m (F47, F73, Google Maps)", fontsize=6.3, rotation=90, va="center")
    rot(tuple(Cg + np.array([Rg + 1.0, 2.0])), "glorieta de giro\nR 10,0 · isleta R 4,0", fontsize=6, va="center")
    rot((xr + 3.4, 50.0), "camión rígido 9 m:\nrecorrido y barrido", fontsize=5.5, ha="left", va="center", style="italic")
    rot((xc - 1.6, yh + 6), "senda peatonal", fontsize=5.3, rotation=90, va="center")
    rot((E.W_P + 5.6, 62), "césped (F47, F73)", fontsize=6.5, rotation=90, va="center")
    rot((xr + 9.6, 30.5), "senda a la plaza", fontsize=5.3, rotation=-60)
    rot((48, 84), "PARQUE\n(arbolado, F01, F23, F47)", fontsize=9, weight="bold", ha="center")
    rot((-8, 30), "patio de la L\n(sin foto)", fontsize=7, ha="center", style="italic")
    ax.annotate("fuente en media luna (1984)", tuple(T - N * 5.4), tuple(E.P(-4, -15)), fontsize=6.3, zorder=10,
                arrowprops=dict(arrowstyle="-", lw=0.5), bbox=dict(fc="white", ec="none", pad=0.8))
    for p_, d_, t_ in ((E.P(7.0, yf - 2.2), N, "entrada hotel"), (E.P(-9.0, yf - 2.2), N, "entrada restaurante"),
                       ((E.W_P + 1.4, E.Y_CUNA + 2.6), (0, -1), "rampa")):            # entradas (Ching: flecha llena)
        p_ = np.array(p_, float); d_ = np.array(d_, float); n_ = np.array([-d_[1], d_[0]])
        ax.add_patch(Polygon([p_ + d_ * 0.9, p_ - d_ * 0.6 + n_ * 0.6, p_ - d_ * 0.6 - n_ * 0.6], closed=True, fc="k", ec="k", zorder=10))
    ax.annotate("medianera (linde)", tuple(SW(x0, 4.0)), tuple(SW(x0 - 12, -2.5) + np.array([0, -1])), fontsize=6, zorder=10, arrowprops=dict(arrowstyle="-", lw=0.5))
    ax.text(*(np.array([6.4, 72.0])), "HOTEL SALUT", fontsize=8, weight="bold", rotation=90, ha="center", va="center", zorder=10)
    nc = np.array([XL[0] + 9, YL[1] - 10]); nd = np.array([-0.914, 0.407])    # norte (mismo que en todas las plantas)
    ax.add_patch(Circle(nc, 5.0, fill=False, ec="k", lw=0.8, zorder=10))
    ax.annotate("", tuple(nc + nd * 6.5), tuple(nc - nd * 4.0), arrowprops=dict(arrowstyle="-|>,head_width=0.6,head_length=1.2", lw=1.6, color="k"), zorder=10.1)
    ax.text(*(nc + nd * 9.0), "N", fontsize=12, weight="bold", ha="center", va="center", zorder=10)

    # --- 6. leyenda, fotos, escala y cajetín
    w, h = fig._mm
    xl0 = 14 + aw + 10
    fig.text(xl0 / w, 283 / h, "PLANO DE LUGAR – 1984", fontsize=11, weight="bold", va="top")
    fig.text(xl0 / w, 276 / h,
             "El edificio es la planta de cubiertas del modelo (figura clara). El entorno, según las fotos de 1984,\n"
             "antes de las vallas posteriores. Caminos y árboles: trazado y posición aproximados (fotos oblicuas).",
             fontsize=6.3, va="top")
    ley = fig.add_axes([xl0 / w, 196 / h, 70 / w, 74 / h]); ley.set_xlim(0, 70); ley.set_ylim(0, 92); ley.axis("off")
    items = [("edificio (cubiertas)", lambda a, y: a.plot([2, 12], [y, y], color="k", lw=1.3)),
             ("linde / medianera", lambda a, y: a.plot([2, 12], [y, y], color="k", lw=0.8, ls=(0, (12, 2, 1, 2, 1, 2)))),
             ("vial de servicio: bordillo y eje", lambda a, y: (a.plot([2, 12], [y + 1.2, y + 1.2], color="k", lw=0.75), a.plot([2, 12], [y + 0.9, y + 0.9], color="k", lw=0.3),
                                                    a.plot([2, 12], [y - 1.2, y - 1.2], color="k", lw=0.75), a.plot([2, 12], [y - 0.9, y - 0.9], color="k", lw=0.3),
                                                    a.plot([2, 12], [y, y], color="k", lw=0.3, ls=(0, (6, 4))))),
             ("senda peatonal (losas)", lambda a, y: (a.plot([2, 12], [y + 0.8, y + 0.8], color="k", lw=0.45), a.plot([2, 12], [y - 0.8, y - 0.8], color="k", lw=0.45),
                                                     [a.plot([x, x], [y - 0.8, y + 0.8], color="k", lw=0.12) for x in range(3, 12)])),
             ("recorrido y barrido del camión", lambda a, y: (a.plot([2, 12], [y, y], color="k", lw=0.5, ls=(0, (10, 2, 1, 2))),
                                                             a.plot([2, 12], [y + 1.0, y + 1.0], color="k", lw=0.35, ls=(0, (4, 2))),
                                                             a.plot([2, 12], [y - 1.0, y - 1.0], color="k", lw=0.35, ls=(0, (4, 2))))),
             ("entrada", lambda a, y: a.add_patch(Polygon([(8, y), (5.5, y + 1.3), (5.5, y - 1.3)], closed=True, fc="k"))),
             ("césped (punteado)", lambda a, y: a.plot(rng.uniform(2, 12, 40), rng.uniform(y - 1.5, y + 1.5, 40), ",", color="k")),
             ("árbol (copa y tronco)", lambda a, y: a.add_patch(Circle((7, y), 2.5, fc="white", ec="k", lw=0.5))),
             ("pavimento de la plaza", lambda a, y: [a.plot([x, x], [y - 2, y + 2], color="k", lw=0.15) for x in range(2, 13, 2)]),
             ("edificio colindante", lambda a, y: a.add_patch(plt.Rectangle((2, y - 2), 10, 4, fc="white", ec="k", hatch="////", lw=0.5)))]
    for i, (t, f) in enumerate(items):
        y = 88 - i * 8.5; f(ley, y); ley.text(15, y, t, fontsize=6.3, va="center")
    for i, (img, t) in enumerate((("47.webp", "F47 (1984): césped y camino junto al ala larga"),
                                  ("1.webp", "F01 (1984): plaza, fuente, colindante y parque"),
                                  ("73.webp", "F73: camino y césped ante el testero"))):
        a = fig.add_axes([(xl0 + i * 72) / w, 112 / h, 68 / w, 80 / h]); im = Image.open(LM.IMG + img).convert("RGB"); im.thumbnail((700, 700))
        a.imshow(im); a.axis("off"); a.set_title(t, fontsize=5.8, loc="left")
    fig.text(xl0 / w, 100 / h, "Fuentes: F01, F14, F15, F23, F47, F70, F72, F73 (1984) y marcas del usuario (26/11).\n"
             "Mismo norte y orientación que todas las plantas del juego.", fontsize=6, va="top")
    IA.barra(fig, 14, 24, DEN, 40)
    IA.cajetin(fig, f"1:{DEN}")
    return fig


if __name__ == "__main__":
    fig = hoja_lugar()
    fig.savefig("PLANO_LUGAR_1984.pdf"); fig.savefig("PLANO_LUGAR_1984.png", dpi=110)
print("ok")
