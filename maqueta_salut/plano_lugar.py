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

    # --- 2. lado exterior del ala larga: césped junto al edificio, camino de coches que la rodea, sendero al parque, parque
    xr = E.W_P + 9.0
    cx, cy, rl = xr - 13.5, E.L_L + 2.0, 13.5                       # vuelta por detrás del testero (fuera del ala) [F73, usuario]
    camino = [tuple(E.P(20, yf - 6)), (xr, 18.0), (xr, cy)] + \
             [(cx + rl * math.cos(a), cy + rl * math.sin(a)) for a in np.linspace(0, math.pi, 24)] + [(cx - rl, 70.0)]
    b_cam = via(ax, camino, 5.0, z=2)
    ax.plot(*zip((cx - rl, 70.0), (cx - rl, 50.0)), color="k", lw=0.5, ls=(0, (4, 3)), zorder=2.2)
    sendero = [(xr, 40.0), (xr + 6, 44.0), (xr + 14, 52.0), (xr + 20, 64.0), (xr + 24, 80.0), (xr + 30, 94.0)]
    b_sen = via(ax, sendero, 2.5, z=2, eje=False)
    cesped_ala = SP([(E.W_P, E.Y_CUNA - 30), (xr - 2.5, E.Y_CUNA - 30), (xr - 2.5, cy), (E.W_P, cy)])
    parque = SP([(xr + 2.5, 20), (XL[1], 20), (XL[1], YL[1]), (xr + 2.5, YL[1])]).union(SP([(XL[0] + 25, cy), (XL[1], cy), (XL[1], YL[1]), (XL[0] + 25, YL[1])])).difference(Point(cx, cy).buffer(rl + 2.5))
    testero = Point(cx, cy).buffer(rl - 2.5).intersection(SP([(cx - rl, E.L_L + 0.3), (cx + rl, E.L_L + 0.3), (cx + rl, cy + rl), (cx - rl, cy + rl)]))
    for g in (cesped_ala, parque, testero):
        punteado(ax, g.difference(b_cam).difference(b_sen).intersection(marco), dens=0.5, z=0.8)
    for c, r in (((xr + 8, 30), 4.5), ((xr + 16, 40), 4.0), ((xr + 26, 34), 5.0), ((xr + 9, 58), 3.5), ((xr + 30, 56), 4.5),
                 ((xr + 14, 74), 5.0), ((xr + 36, 74), 5.5), ((xr + 22, 92), 4.5), ((xr + 44, 96), 5.5), ((xr + 6, 104), 4.0),
                 ((-14, 112), 4.5), ((xr + 40, 40), 5.0), ((xr + 46, 62), 4.5), ((xr + 30, 108), 5.0), ((xr + 3, 88), 3.5)):
        arbol(ax, c, r)

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
    rot((xr + 1.2, 70), "camino de coches: rodea el ala por detrás (F47, F73)", fontsize=6.5, rotation=90, va="center")
    rot((E.W_P + 2.5, 82), "césped (F47, F73)", fontsize=6.5, rotation=90, va="center")
    rot((xr + 26, 47), "sendero al parque (F47)", fontsize=6.5, rotation=55)
    rot((48, 84), "PARQUE\n(arbolado, F01, F23, F47)", fontsize=9, weight="bold", ha="center")
    rot((-8, 30), "patio de la L\n(sin foto)", fontsize=7, ha="center", style="italic")
    rot((cx - rl - 0.8, 58), "continúa (sin foto)", fontsize=5.5, rotation=90, va="center", style="italic")
    ax.annotate("fuente en media luna (1984)", tuple(T - N * 5.0), tuple(E.P(-22, -12)), fontsize=6.5, zorder=10,
                arrowprops=dict(arrowstyle="-", lw=0.5))
    ax.annotate("medianera (linde)", tuple(SW(x0, 4.0)), tuple(SW(x0 - 12, -2.5) + np.array([0, -1])), fontsize=6, zorder=10, arrowprops=dict(arrowstyle="-", lw=0.5))
    ax.text(*E.P(8, yf - 3.5), "entrada", fontsize=6, ha="center", zorder=10)
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
    ley = fig.add_axes([xl0 / w, 200 / h, 70 / w, 66 / h]); ley.set_xlim(0, 70); ley.set_ylim(0, 66); ley.axis("off")
    items = [("edificio (cubiertas)", lambda a, y: a.plot([2, 12], [y, y], color="k", lw=1.3)),
             ("linde / medianera", lambda a, y: a.plot([2, 12], [y, y], color="k", lw=0.8, ls=(0, (12, 2, 1, 2, 1, 2)))),
             ("vial: bordillo y eje", lambda a, y: (a.plot([2, 12], [y + 1, y + 1], color="k", lw=0.7), a.plot([2, 12], [y - 1, y - 1], color="k", lw=0.7),
                                                    a.plot([2, 12], [y, y], color="k", lw=0.3, ls=(0, (6, 4))))),
             ("césped (punteado)", lambda a, y: a.plot(rng.uniform(2, 12, 40), rng.uniform(y - 1.5, y + 1.5, 40), ",", color="k")),
             ("árbol (copa y tronco)", lambda a, y: a.add_patch(Circle((7, y), 2.5, fc="white", ec="k", lw=0.5))),
             ("pavimento de la plaza", lambda a, y: [a.plot([x, x], [y - 2, y + 2], color="k", lw=0.15) for x in range(2, 13, 2)]),
             ("edificio colindante", lambda a, y: a.add_patch(plt.Rectangle((2, y - 2), 10, 4, fc="white", ec="k", hatch="////", lw=0.5)))]
    for i, (t, f) in enumerate(items):
        y = 60 - i * 8.5; f(ley, y); ley.text(15, y, t, fontsize=6.5, va="center")
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
