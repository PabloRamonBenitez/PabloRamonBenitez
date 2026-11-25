"""INTERIORES Y ESTRUCTURA – solo en los planos (el volumen no se toca).

Propuesta de distribución coherente con el uso de cada pieza (hotel, restaurante, bar, oficinas) y con la estructura
que se ve desde fuera (aletas = muros de carga radiales del barril, módulo de 3,40 m de los huecos del ala larga).
Estándar de representación: tabiques con trama, puertas con hoja y barrido, mobiliario en línea fina, ejes
estructurales en trazo y punto con burbuja, nombre y superficie de cada estancia.
Todo se recorta contra el interior real del corte (lo que no cabe, no se dibuja)."""
import math
import numpy as np
from shapely.geometry import Polygon as SP, LineString, Point, box
from shapely.ops import unary_union
from shapely import affinity
from matplotlib.patches import Polygon, Arc, Circle
import edificio as E

V = E._v
TAB = 0.12                                   # tabique
FINO = dict(color="0.25", lw=0.35)
T = np.array(E.T)


# ------------------------------------------------------------------ utilidades
def _interior(cs, muro=0.30):
    out = []
    for P in cs.to_polygons():
        P = np.array(P)
        if len(P) < 3: continue
        sp = SP(P).buffer(0)
        if sp.is_empty: continue
        h = sp.buffer(-muro)
        if not h.is_empty: out.append(h)
    return unary_union(out) if out else None


def _dib(ax, g, z, **st):
    for gg in getattr(g, "geoms", [g]):
        if gg.is_empty: continue
        if gg.geom_type == "Polygon":
            ax.add_patch(Polygon(np.array(gg.exterior.coords), closed=True, zorder=z, **st))
        elif gg.geom_type in ("LineString", "LinearRing"):
            ax.plot(*np.array(gg.coords).T, zorder=z, color=st.get("ec", "0.25"), lw=st.get("lw", 0.35))


def tabique(ax, INT, p0, p1, e=TAB, z=6.6):
    g = LineString([p0, p1]).buffer(e / 2, cap_style=2)
    if INT is not None: g = g.intersection(INT)
    _dib(ax, g, z, fc="#c8c8c8", ec="k", lw=0.5, hatch="////")
    return g


def mueble(ax, INT, poly, z=6.5, lw=0.35):
    g = SP(poly)
    if INT is not None:
        if not INT.contains(g.centroid): return
        g = g.intersection(INT)
    _dib(ax, g, z, fc="none", ec="0.3", lw=lw)


def puerta(ax, bis, dir_hoja, dir_paso, w=0.85, z=6.8, INT=None):
    """bisagra en 'bis', hoja abierta en 'dir_hoja' (perpendicular al muro), cierra hacia 'dir_paso' (a lo largo del muro)"""
    bis, dh, dp = np.array(bis, float), np.array(dir_hoja, float), np.array(dir_paso, float)
    dh, dp = dh / np.linalg.norm(dh), dp / np.linalg.norm(dp)
    if INT is not None and not INT.buffer(0.2).contains(Point(*(bis + dh * w * 0.5))): return
    ax.plot(*zip(bis, bis + dh * w), color="k", lw=0.8, zorder=z)
    a0, a1 = math.degrees(math.atan2(dh[1], dh[0])), math.degrees(math.atan2(dp[1], dp[0]))
    d = (a1 - a0) % 360
    lo, hi = (a0, a0 + d) if d <= 180 else (a1, a1 + 360 - d)
    ax.add_patch(Arc(bis, 2 * w, 2 * w, theta1=lo, theta2=hi, lw=0.35, color="k", zorder=z))


_INT = [None]


def rotulo(ax, p, nombre, sup=None, rot=0, fs=4.8, z=9):
    if _INT[0] is not None and not _INT[0].contains(Point(float(p[0]), float(p[1]))): return
    t = nombre + (f"\n{sup:.1f} m²".replace(".", ",") if sup else "")
    ax.text(p[0], p[1], t, fontsize=fs, ha="center", va="center", rotation=rot, zorder=z, color="0.1", clip_on=True,
            bbox=dict(fc="white", ec="none", alpha=0.75, pad=0.4))


def pilar(ax, p, a=0.40, z=7.0):
    ax.add_patch(Polygon([(p[0] - a / 2, p[1] - a / 2), (p[0] + a / 2, p[1] - a / 2), (p[0] + a / 2, p[1] + a / 2), (p[0] - a / 2, p[1] + a / 2)],
                         closed=True, fc="k", ec="k", lw=0.5, zorder=z))


def eje(ax, p0, p1, nombre, z=3.5):
    ax.plot(*zip(p0, p1), color="0.45", lw=0.35, ls=(0, (8, 2, 1, 2)), zorder=z)
    d = np.array(p1, float) - np.array(p0, float); d /= np.linalg.norm(d)
    q = np.array(p0) - d * 0.9
    ax.add_patch(Circle(q, 0.75, fc="white", ec="0.3", lw=0.5, zorder=z + 0.1))
    ax.text(*q, nombre, fontsize=4.5, ha="center", va="center", zorder=z + 0.2, clip_on=True)


def mesa(ax, INT, c, n=4, r=0.45):
    if INT is not None and not INT.contains(Point(*c)): return
    ax.add_patch(Circle(c, r, fc="none", ec="0.3", lw=0.35, zorder=6.5))
    for k in range(n):
        a = 2 * math.pi * k / n + math.pi / 4
        q = (c[0] + (r + 0.3) * math.cos(a), c[1] + (r + 0.3) * math.sin(a))
        ax.add_patch(Circle(q, 0.2, fc="none", ec="0.4", lw=0.3, zorder=6.5))


# ------------------------------------------------------------------ estancias por partición del interior real
def partir(region, cortes, e=TAB):
    """divide 'region' (shapely) por los tabiques 'cortes' [(p0,p1)] → (estancias, tabiques recortados)"""
    tabs = unary_union([LineString([p0, p1]).buffer(e / 2, cap_style=2) for p0, p1 in cortes]).intersection(region)
    rest = region.difference(tabs)
    rooms = [g for g in getattr(rest, "geoms", [rest]) if g.geom_type == "Polygon" and g.area > 1.0]
    return rooms, tabs


def dib_tabiques(ax, tabs, z=6.6):
    _dib(ax, tabs, z, fc="0.9", ec="k", lw=0.45, hatch="//////")


def cotas_estancia(ax, g, fs=3.6):
    """cotas interiores de la estancia: ancho y fondo del rectángulo mínimo que la contiene"""
    from lineas import cota
    r = np.array(g.minimum_rotated_rectangle.exterior.coords)[:4]
    for i in (0, 1):
        a, b = r[i], r[i + 1]
        if np.linalg.norm(b - a) < 1.5: continue
        m = (a + b) / 2; c = np.array(g.centroid.coords[0]); d = c - m; d /= np.linalg.norm(d)
        cota(ax, a + d * 0.45, b + d * 0.45, 0.0, "", fs=fs, color="0.25")


def puerta_hacia(ax, room, otro, w=0.85):
    """puerta en el tabique común entre 'room' y 'otro' (pasillo): bisagra a 0,25 del extremo, hoja hacia la estancia"""
    lim = room.buffer(TAB).intersection(otro.buffer(TAB))
    if lim.is_empty or lim.area < 0.05: return
    r = np.array(lim.minimum_rotated_rectangle.exterior.coords)[:4]
    ls = [(np.linalg.norm(r[(i + 1) % 4] - r[i]), i) for i in range(4)]
    Lm, i = max(ls)
    if Lm < w + 0.6: return
    a, b = r[i], r[(i + 1) % 4]; t = (b - a) / Lm
    bis = (r[i] + r[(i + 3) % 4]) / 2 + t * 0.25
    c = np.array(room.centroid.coords[0]); n = np.array([-t[1], t[0]]); n = n if (c - bis) @ n > 0 else -n
    puerta(ax, bis, n, t, w=w)


def estancias(ax, rooms, nombres, pasillo=None, mueble_fn=None):
    for i, g in enumerate(sorted(rooms, key=lambda g: (g.centroid.x, g.centroid.y))):
        nm = nombres[i] if i < len(nombres) else ""
        p = g.representative_point()
        rotulo(ax, (p.x, p.y), nm, g.area, fs=4.2)
        cotas_estancia(ax, g)
        if pasillo is not None and nm and not nm.startswith("PASILLO"): puerta_hacia(ax, g, pasillo)
        if mueble_fn: mueble_fn(ax, g, nm)


def _escritorio(ax, g, nm):
    if not nm.startswith("OFICINA") and not nm.startswith("DESPACHO"): return
    c = np.array(g.representative_point().coords[0])
    mueble(ax, _INT[0], [c + (-0.8, -0.35), c + (0.8, -0.35), c + (0.8, 0.35), c + (-0.8, 0.35)])
    ax.add_patch(Circle(c + (0, -0.75), 0.25, fc="none", ec="0.35", lw=0.3, zorder=6.5))


# ------------------------------------------------------------------ piezas
def ala_larga(ax, zc, INT):
    W, L = V["W_P"], V["L_L"]; y0 = E.plantas_base()["IC"][1] + 1.0
    reg = INT.intersection(box(-0.5, y0, W + 0.5, L + 0.5))
    if reg.is_empty: return
    pas = 2 * V["S_VEN"]                                           # retícula 6,80 = 2 módulos de hueco (fachada)
    ys = [y for y in np.arange(L - V["VEN_FIN"] - V["VEN_W"] / 2 - V["S_VEN"] / 2, y0, -pas)][::-1]
    xs = (W / 3, 2 * W / 3)
    if zc < E.Z_P1:
        for i, x in enumerate(xs): eje(ax, (x, y0 - 2), (x, L + 2), "AB"[i])
        for j, y in enumerate(ys): eje(ax, (-3, y), (W + 3, y), str(j + 1))
        for x in xs:
            for y in ys:
                if reg.contains(Point(x, y)): pilar(ax, (x, y))
    if zc < E.Z_PB:                                                # PB: cocina y servicios del restaurante (bajo el comedor)
        y1, y2 = ys[len(ys) // 2], ys[-2]
        rooms, tabs = partir(reg, [((0, y1), (W, y1)), ((0, y2), (W, y2)), ((W - 2.4, y2), (W - 2.4, L))])
        dib_tabiques(ax, tabs)
        estancias(ax, rooms, ["COCINA", "CÁMARAS Y ALMACÉN", "VESTUARIOS", "INSTAL."])
        for k in range(5):                                         # bancos de trabajo contra la fachada del patio
            yb = y0 + 2 + 3.2 * k
            if yb + 2.4 < y1: mueble(ax, reg, [(0.35, yb), (1.0, yb), (1.0, yb + 2.4), (0.35, yb + 2.4)])
        mueble(ax, reg, [(4.5, y0 + 6), (8.2, y0 + 6), (8.2, y0 + 7.4), (4.5, y0 + 7.4)])
    elif zc < E.Z_P1:                                              # planta 1: comedor del restaurante + aseos y office al fondo
        yc = ys[-1]
        rooms, tabs = partir(reg, [((0, yc), (W, yc)), ((W / 2, yc), (W / 2, L))])
        dib_tabiques(ax, tabs)
        estancias(ax, rooms, ["COMEDOR DEL RESTAURANTE", "ASEOS", "OFFICE"])
        for y in np.arange(y0 + 3, yc - 1.5, 3.4):
            for x in (2.6, 6.4, 10.0): mesa(ax, reg, (x, y))
    else:                                                          # planta 2: bar (cubierto) y terraza
        WB = V["W_BAR"] + V["V_BAR"]; yb0 = L - V["L_FIN"] - 22
        mueble(ax, reg, [(0.5, yb0 + 4), (1.3, yb0 + 4), (1.3, yb0 + 14), (0.5, yb0 + 14)], lw=0.6)
        for y in np.arange(yb0 + 3, L - V["L_FIN"] - 2, 3.0): mesa(ax, reg, (WB / 2 + 0.6, y), n=2, r=0.35)
        rotulo(ax, (WB / 2, yb0 + 9), "BAR")



def celdas(ax, reg, cel, nombres, pasillo_idx=None, mueble_fn=None):
    """cel: lista de polígonos (celdas); estancia = celda ∩ interior real; tabiques = fronteras comunes"""
    rooms = []
    for c in cel:
        g = reg.intersection(c).buffer(-TAB / 2)
        g = max(getattr(g, "geoms", [g]), key=lambda q: q.area) if not g.is_empty else g
        rooms.append(g)
    fr = []
    for a in range(len(cel)):
        for b in range(a + 1, len(cel)):
            ln = cel[a].boundary.intersection(cel[b].boundary)
            if not ln.is_empty and ln.length > 0.3: fr.append(ln.buffer(TAB / 2, cap_style=2))
    if fr: dib_tabiques(ax, unary_union(fr).intersection(reg.buffer(-0.01)))
    pas = rooms[pasillo_idx] if pasillo_idx is not None else None
    for k, (g, nm) in enumerate(zip(rooms, nombres)):
        if g.is_empty or g.area < 2: continue
        p = g.representative_point(); rotulo(ax, (p.x, p.y), nm, g.area if not nm.startswith(("PASILLO", "DISTRIB")) else None, fs=4.2 if g.area > 8 else 3.6)
        if k == pasillo_idx: continue
        cotas_estancia(ax, g)
        if pas is not None: puerta_hacia(ax, g, pas)
        if mueble_fn: mueble_fn(ax, g, nm)
    return rooms


def ala_corta(ax, zc, INT):
    """ala corta con estructura deducida de la logia: el muro de medianera, el pilar (LOG_PX) y el muro final (LOG_X1)
    son portantes y siguen de la calle a la fachada del patio en todas las plantas (sostienen el cuerpo volado).
    Crujías: estancias a la calle + pasillo paralelo (atraviesa los muros portantes) + servicios contra el patio."""
    sw = lambda x, y: tuple(np.array(E.SWP(x, y)))
    q = lambda xa, xb, ya, yb: SP([sw(xa, ya), sw(xb, ya), sw(xb, yb), sw(xa, yb)])
    x0, Lc = -V["L_C"], V["L_C"]
    xe = x0 + Lc - 3.5
    reg = INT.intersection(q(x0 - 1, xe, -3, 45))
    if reg.is_empty: return
    xa, xb = x0 + V["LOG_PX"], x0 + V["LOG_X1"]                    # ejes de los muros portantes (pilar y muro final de la logia)
    def portantes(yc, y1):
        """muros portantes de 0,30 (y 0,70 el del pilar en su arranque) con paso en el pasillo"""
        g = unary_union([q(xa - 0.15, xa + 0.15, -3, 45), q(xb - 0.15, xb + 0.15, -3, 45)])
        g = g.difference(q(x0 - 1, xe, yc + 0.05, y1 - 0.05)).intersection(reg.buffer(0.02))
        _dib(ax, g, 6.9, fc="0.72", ec="k", lw=0.9, hatch="......")
        for k, x in enumerate((xa, xb)):
            eje(ax, sw(x, -6), sw(x, 30), "L" + str(k + 1))
    def plan(yc, xs_c, xs_p, n_c, n_p):
        y1 = yc + 1.8
        bc = [x0 - 1] + sorted(set([xa, xb] + list(xs_c))) + [xe]; bp = [x0 - 1] + sorted(set([xa, xb] + list(xs_p))) + [xe]
        cel = [q(x0 - 1, xe, yc, y1)] + [q(bc[i], bc[i + 1], -3, yc) for i in range(len(bc) - 1)] + [q(bp[i], bp[i + 1], y1, 45) for i in range(len(bp) - 1)]
        celdas(ax, reg, cel, ["PASILLO"] + n_c + n_p, pasillo_idx=0, mueble_fn=_escritorio)
        portantes(yc, y1)
    if zc < E.Z_PB:                                                # PB: locales a la calle entre muros portantes; almacenes y aseos al patio
        plan(8.0, [xb + k * (xe - xb) / 3 for k in range(1, 3)], [xb + (xe - xb) * 0.5],
             ["LOCAL 1", "LOCAL 2", "LOCAL 3", "LOCAL 4", "LOCAL 5"], ["ALMACÉN", "ASEOS", "INSTALACIONES", "ALMACÉN 2"])
    elif zc < E.Z_P1:                                              # P1: dos salas tras los dos paños de la logia, despachos
        plan(6.5, [xb + k * (xe - xb) / 4 for k in range(1, 4)], [xb + (xe - xb) * f for f in (0.35, 0.65)],
             ["SALA 1\n(tras la logia)", "SALA 2\n(tras la logia)"] + [f"DESPACHO {k + 1}" for k in range(4)],
             ["SALA DE JUNTAS", "ARCHIVO", "ASEOS", "OFFICE", "INSTAL."])
    elif zc < E.Z_ALTO:                                            # bloque alto (planta 2): dirección sobre las mismas crujías
        plan(5.0, [], [], ["SALA DE REUNIONES", "DIRECCIÓN", "ADMINISTRACIÓN"], ["ARCHIVO", "ASEOS", "ESTAR"])


def base_torre(ax, zc, INT):
    """núcleo de comunicaciones (2 ascensores + montacargas) y vestíbulo del hotel en planta baja"""
    if zc < E.Z_CU0:
        for k, a in enumerate((200, 240, 280)):
            u = np.array([math.cos(math.radians(a)), math.sin(math.radians(a))]); v = np.array([-u[1], u[0]])
            c = T + u * 1.7
            pts = [c - v * 0.75 - u * 0.7, c + v * 0.75 - u * 0.7, c + v * 0.75 + u * 0.7, c - v * 0.75 + u * 0.7]
            ax.add_patch(Polygon(pts, closed=True, fc="none", ec="k", lw=0.5, zorder=8))
            ax.plot(*zip(pts[0], pts[2]), color="k", lw=0.3, zorder=8); ax.plot(*zip(pts[1], pts[3]), color="k", lw=0.3, zorder=8)
    if zc < E.Z_PB:
        p = np.array(E.P(0, 5.5))
        arco = [tuple(np.array(E.P(3.5 * math.cos(t), 5.5 + 1.2 * math.sin(t)))) for t in np.linspace(math.pi * 0.15, math.pi * 0.85, 12)]
        ax.plot(*np.array(arco).T, color="k", lw=0.9, zorder=8)
        rotulo(ax, E.P(0, 7.5), "RECEPCIÓN", fs=4.5)
        rotulo(ax, E.P(0, 2.2), "VESTÍBULO DEL HOTEL", fs=4.5)


def habitaciones(ax, zc, INT):
    """plantas del barril: una habitación por módulo entre muros de carga (aletas); baño junto al pasillo, cama, escritorio"""
    if not (E.Z_B0 < zc < E.Z_B1): return
    rf = E.R_B - 1.8; rc = E.R_COL + 2.2 + 0.12
    da_esc = E.ESC_HA + 0.02
    for k in range(V["N_AL"]):
        am = 2 * math.pi * (k + 0.5) / V["N_AL"] + E.FASE_AL
        if abs((am - E.ESC_ANG + math.pi) % (2 * math.pi) - math.pi) < da_esc: continue
        u = np.array([math.cos(am), math.sin(am)]); v = np.array([-u[1], u[0]])
        hw = lambda r: r * math.tan(math.pi / V["N_AL"]) - 0.15          # medio ancho útil del módulo a radio r
        # baño: de rc a rc+2,1, pegado a un lado
        r0, r1 = rc + 0.05, rc + 2.1
        b = [T + u * r0 - v * hw(r0), T + u * r0 - v * (hw(r0) - 1.6), T + u * r1 - v * (hw(r1) - 1.6), T + u * r1 - v * hw(r1)]
        ax.add_patch(Polygon(b, closed=True, fc="#eeeeee", ec="k", lw=0.5, zorder=6.6, hatch="...."))
        # puerta de la habitación desde el pasillo
        puerta(ax, T + u * rc + v * (hw(rc) - 0.05), u, -v, w=0.8)
        # cama doble 1,60 × 2,00 con el cabecero en el muro de carga
        c0 = rc + 3.0
        cama = [T + u * c0 + v * (hw(c0) - 0.05), T + u * c0 + v * (hw(c0) - 2.05), T + u * (c0 + 1.6) + v * (hw(c0 + 1.6) - 2.05), T + u * (c0 + 1.6) + v * (hw(c0 + 1.6) - 0.05)]
        ax.add_patch(Polygon(cama, closed=True, fc="none", ec="0.3", lw=0.4, zorder=6.5))
        # escritorio junto a la ventana
        d0 = rf - 0.9
        ax.add_patch(Polygon([T + u * d0 - v * 0.8, T + u * d0 + v * 0.8, T + u * (d0 + 0.5) + v * 0.8, T + u * (d0 + 0.5) - v * 0.8], closed=True, fc="none", ec="0.3", lw=0.35, zorder=6.5))
        if k % 3 == 0:
            ax.text(*(T + u * (rc + 4.6)), f"HAB.\n{0.5 * (rf ** 2 - rc ** 2) * 2 * math.pi / V['N_AL']:.0f} m²", fontsize=3.6, ha="center", va="center",
                    rotation=math.degrees(am) - 90, zorder=9, color="0.15", clip_on=True)
    ax.text(*(T + np.array([0, -(E.R_COL + 1.1)])), "PASILLO", fontsize=3.8, ha="center", va="center", zorder=9, clip_on=True)


def dibujar(ax, zc, cs):
    """capa de interiores y estructura para la planta cortada a zc (cs = sección del 3D a esa cota)"""
    if zc is None: return
    INT = _interior(cs)
    if INT is None: return
    _INT[0] = INT
    ala_larga(ax, zc, INT)
    ala_corta(ax, zc, INT)
    base_torre(ax, zc, INT)
    habitaciones(ax, zc, INT)
