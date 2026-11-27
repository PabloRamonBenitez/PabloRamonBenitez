"""PUERTA 3b – CALIDAD GRÁFICA (usuario 27/11: «deberías tener una representación gráfica extraordinaria; no compruebas»).
Se ejecuta sola en cada hoja que se guarda (gancho en traduccion.py, justo después de traducir), así mide el texto final.
Detecta en TODAS las láminas:
  · rótulos que se pisan entre sí (rectángulo GIRADO real de cada texto, no su caja alineada)
  · rótulos cortados por el marco de su planta (texto recortado por los ejes)
  · rótulos que se salen de la hoja
Resultado: CALIDAD_GRAFICA.json (por archivo de salida y página) y CALIDAD_GRAFICA.md (resumen). Criterio: 0 en A3, A4 y lugar."""
import atexit, json, math, os
from matplotlib.text import Text

REG = {}                       # salida → lista de defectos
_PAG = {}


def _poligono(t, r):
    """rectángulo girado del texto en píxeles de pantalla (centro = centro de su caja alineada)"""
    from shapely.geometry import Polygon
    from matplotlib.text import Text as _T
    bb = _T.get_window_extent(t, r)                      # solo el texto (una Annotation sumaría su flecha)
    ang = t.get_rotation() % 360
    if abs(math.sin(math.radians(ang))) < 1e-3:
        return Polygon([(bb.x0, bb.y0), (bb.x1, bb.y0), (bb.x1, bb.y1), (bb.x0, bb.y1)]), bb
    rot = t.get_rotation(); t.set_rotation(0)
    b0 = t.get_window_extent(r); t.set_rotation(rot)
    w, h = b0.width, b0.height; cx, cy = (bb.x0 + bb.x1) / 2, (bb.y0 + bb.y1) / 2
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    pts = [(cx + dx * c - dy * s, cy + dx * s + dy * c) for dx, dy in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2))]
    return Polygon(pts), bb


def revisar(fig, salida):
    try:
        fig.canvas.draw()
        r = fig.canvas.get_renderer()
    except Exception:
        return
    _PAG[salida] = _PAG.get(salida, 0) + 1
    pag = _PAG[salida]
    W, H = fig.bbox.width, fig.bbox.height
    mm = 25.4 / fig.dpi
    items, out = [], []
    textos = list(fig.texts)
    for ax_ in fig.axes:
        if not ax_.get_visible(): continue
        textos += list(ax_.texts) + [ax_.title, ax_._left_title, ax_._right_title]
        if ax_.axison:
            textos += [x for x in ax_.get_xticklabels() + ax_.get_yticklabels()] + [ax_.xaxis.label, ax_.yaxis.label]
        lg = ax_.get_legend()
        if lg: textos += list(lg.get_texts())
    # fondo sin textos (para ver si un rótulo cae encima de líneas)
    vis = [(t, t.get_visible()) for t in textos]
    for t, _ in vis: t.set_visible(False)
    try:
        fig.canvas.draw()
        import numpy as np
        fondo = np.asarray(fig.canvas.get_renderer().buffer_rgba())[:, :, :3].mean(axis=2) < 110
    except Exception:
        fondo = None
    for t, v in vis: t.set_visible(v)
    fig.canvas.draw(); r = fig.canvas.get_renderer()
    for t in textos:
        s = t.get_text()
        if not t.get_visible() or not s.strip() or (t.get_alpha() is not None and t.get_alpha() == 0):
            continue
        try:
            P, bb = _poligono(t, r)
        except Exception:
            continue
        if P.area < 4:
            continue
        ax = t.axes
        if ax is not None and t.get_clip_on():
            from shapely.geometry import box
            A = box(*ax.bbox.extents)
            if not A.intersects(P):
                continue                                           # recortado entero: no se dibuja
            if A.intersection(P).area < 0.97 * P.area:
                out.append({"tipo": "cortado por el marco", "texto": s[:50], "x_mm": round(P.centroid.x * mm), "y_mm": round((H - P.centroid.y) * mm)})
                P = A.intersection(P)
        elif ax is not None and getattr(ax, "_marco", False):       # dibujo con marco visible: ningún rótulo lo cruza
            from shapely.geometry import box
            A = box(*ax.bbox.extents)
            if A.contains(P.centroid) and A.intersection(P).area < 0.97 * P.area:        # los rótulos de margen (niveles, cadenas) son legítimos
                out.append({"tipo": "se sale de su dibujo", "texto": s[:50], "x_mm": round(P.centroid.x * mm), "y_mm": round((H - P.centroid.y) * mm)})
        if P.bounds[0] < -1 or P.bounds[1] < -1 or P.bounds[2] > W + 1 or P.bounds[3] > H + 1:
            out.append({"tipo": "fuera de la hoja", "texto": s[:50], "x_mm": round(P.centroid.x * mm), "y_mm": round((H - P.centroid.y) * mm)})
        bp = t.get_bbox_patch()
        tapa = bp is not None and bp.get_facecolor()[:3] == (1.0, 1.0, 1.0) and bp.get_facecolor()[3] > 0.9
        if fondo is not None and len(s.strip()) > 2 and not tapa:
            from PIL import Image, ImageDraw
            import numpy as np
            x0, y0, x1, y1 = [int(v) for v in P.bounds]
            x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1 + 1, int(W)), min(y1 + 1, int(H))
            if x1 > x0 and y1 > y0:
                m = Image.new("L", (x1 - x0, y1 - y0), 0)
                ImageDraw.Draw(m).polygon([(x - x0, y1 - y) for x, y in P.exterior.coords], fill=1)       # fila = y1 − y (origen arriba)
                mk = np.asarray(m, bool); sub = fondo[int(H) - y1:int(H) - y0, x0:x1]
                if sub.shape == mk.shape and mk.sum() > 0:
                    fr = float(sub[mk].mean())
                    if fr > 0.12:                                  # con halo blanco, solo cuenta un fondo muy denso
                        out.append({"tipo": "rótulo sobre líneas", "texto": s[:50], "fraccion": round(fr, 3),
                                    "x_mm": round(P.centroid.x * mm), "y_mm": round((H - P.centroid.y) * mm)})
        items.append((t, s, P))
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i][2], items[j][2]
            if not a.intersects(b):
                continue
            inter = a.intersection(b).area
            if inter > 4 and inter > 0.10 * min(a.area, b.area):
                c = a.intersection(b).centroid
                out.append({"tipo": "rótulos que se pisan", "texto": items[i][1][:40] + "  ×  " + items[j][1][:40],
                            "x_mm": round(c.x * mm), "y_mm": round((H - c.y) * mm)})
    REG.setdefault(salida, []).extend(dict(d, pagina=pag) for d in out)


# ---------------------------------------------------------------------------------------------------------------------
# RECOLOCACIÓN AUTOMÁTICA (antes de comprobar): cada rótulo móvil que pisa a otro, cae sobre líneas o se sale de su dibujo
# prueba posiciones cercanas (escalonado perpendicular a su renglón, desplazado a lo largo, combinaciones) y se queda con la
# mejor; si se aleja más de 1,6 alturas, lleva una línea de referencia fina hasta su sitio (normas: rótulo con línea guía).
def _lista_textos(fig):
    textos = list(fig.texts)
    for ax_ in fig.axes:
        if not ax_.get_visible(): continue
        textos += list(ax_.texts) + [ax_.title, ax_._left_title, ax_._right_title]
        if ax_.axison:
            textos += [x for x in ax_.get_xticklabels() + ax_.get_yticklabels()] + [ax_.xaxis.label, ax_.yaxis.label]
        lg = ax_.get_legend()
        if lg: textos += list(lg.get_texts())
    return [t for t in textos if t.get_visible() and t.get_text().strip()]


def _mascara_lineas(fig, textos):
    import numpy as np
    vis = [(t, t.get_visible()) for t in textos]
    for t, _ in vis: t.set_visible(False)
    try:
        fig.canvas.draw()
        f = np.asarray(fig.canvas.get_renderer().buffer_rgba())[:, :, :3].mean(axis=2) < 110
    except Exception:
        f = None
    for t, v in vis: t.set_visible(v)
    return f


def _fraccion(P, fondo, W, H):
    import numpy as np
    from PIL import Image, ImageDraw
    if fondo is None: return 0.0
    x0, y0, x1, y1 = [int(v) for v in P.bounds]
    x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1 + 1, int(W)), min(y1 + 1, int(H))
    if x1 <= x0 or y1 <= y0: return 0.0
    m = Image.new("L", (x1 - x0, y1 - y0), 0)
    ImageDraw.Draw(m).polygon([(x - x0, y1 - y) for x, y in P.exterior.coords], fill=1)
    mk = np.asarray(m, bool); sub = fondo[int(H) - y1:int(H) - y0, x0:x1]
    return float(sub[mk].mean()) if sub.shape == mk.shape and mk.sum() else 0.0


def _movil(t):
    s = t.get_text().strip()
    if t.axes is None or t.get_gid() == "fijo" or t in (t.axes.title, t.axes._left_title, t.axes._right_title): return False
    import re
    if re.fullmatch(r"[LS]\d", s): return True
    if t.get_fontsize() > 7.5: return False
    if re.fullmatch(r"[LS]\d", s): return True                              # letras de los cortes: se pueden apartar un poco de su línea
    if len(s) <= 2 and not s.replace(",", "").isdigit(): return False        # burbujas de ejes
    bp = t.get_bbox_patch()
    if bp is not None and "Circle" in type(bp.get_boxstyle()).__name__: return False
    return True


def recolocar(fig):
    import numpy as np
    from shapely.geometry import box
    try:
        fig.canvas.draw()
    except Exception:
        return 0
    W, H = fig.bbox.width, fig.bbox.height
    textos = _lista_textos(fig)
    fondo = _mascara_lineas(fig, textos)
    fig.canvas.draw(); r = fig.canvas.get_renderer()
    fijos, moviles = [], []
    for t in textos:
        try:
            P, _ = _poligono(t, r)
        except Exception:
            continue
        if P.area < 4: continue
        if t.axes is not None and t.get_clip_on() and not box(*t.axes.bbox.extents).intersects(P):
            continue                                                     # recortado entero: no se dibuja, no se mueve
        (moviles if _movil(t) else fijos).append((t, P))
    colocados = [P for _, P in fijos]
    n_mov = 0

    def coste(t, P, d):
        c = 0.0
        for Q in colocados:
            if P.intersects(Q):
                c += 12.0 * P.intersection(Q).area / max(1.0, min(P.area, Q.area))
        ax = t.axes
        A = box(*ax.bbox.extents)
        fuera = 1.0 - A.intersection(P).area / P.area
        c += 8.0 * fuera
        if P.bounds[0] < 0 or P.bounds[1] < 0 or P.bounds[2] > W or P.bounds[3] > H: c += 20.0
        bp = t.get_bbox_patch()
        tapa = bp is not None and tuple(bp.get_facecolor()[:3]) == (1.0, 1.0, 1.0)
        fr = 0.0 if tapa else _fraccion(P, fondo, W, H)
        c += 8.0 * max(0.0, fr - 0.05)
        return c + 0.05 * d

    for t, P in moviles:
        rot = t.get_rotation(); t.set_rotation(0)
        b0 = __import__('matplotlib.text', fromlist=['Text']).Text.get_window_extent(t, r); t.set_rotation(rot)
        h_, w_ = max(b0.height, 1.0), max(b0.width, 1.0)
        a = np.radians(rot); tg = np.array([np.cos(a), np.sin(a)]); nr = np.array([-np.sin(a), np.cos(a)])
        c0 = coste(t, P, 0.0)
        if c0 < 0.12:
            colocados.append(P); continue
        tr = t.get_transform(); pos = np.array(tr.transform(t.get_position()), float)
        mejor = (c0, np.zeros(2), P)
        cand = [k * 1.15 * h_ * nr for k in (1, -1, 2, -2, 3, -3, 4, -4, 6, -6)] + [j * w_ * tg for j in (0.6, -0.6, 1.1, -1.1, 1.8, -1.8)] + \
               [k * 1.15 * h_ * nr + j * w_ * tg for k in (1, -1, 2, -2, 3, -3, 5, -5) for j in (0.5, -0.5, 1.0, -1.0, 1.6, -1.6)]
        for dv in cand:
            Pq = __import__("shapely.affinity", fromlist=["translate"]).translate(P, dv[0], dv[1])
            c = coste(t, Pq, float(np.hypot(*dv)) / h_)
            if c < mejor[0] - 1e-6: mejor = (c, dv, Pq)
        c, dv, Pn = mejor
        if c >= 8.0 and (Pn.bounds[0] < 0 or Pn.bounds[1] < 0 or Pn.bounds[2] > W or Pn.bounds[3] > H):
            t.set_visible(False); continue                                      # rótulo que queda fuera de la hoja: no se dibuja
        if np.hypot(*dv) > 0:
            t.set_position(tuple(tr.inverted().transform(pos + dv)))
            n_mov += 1
            if np.hypot(*dv) > 1.6 * h_:                                        # línea guía desde el sitio original
                from matplotlib.lines import Line2D
                from shapely.geometry import Point
                c0p = P.centroid; q = Pn.exterior.interpolate(Pn.exterior.project(Point(c0p.x, c0p.y)))
                ln = Line2D([c0p.x / W, q.x / W], [c0p.y / H, q.y / H], transform=fig.transFigure, lw=0.25, color="0.35", zorder=t.get_zorder() - 0.01)
                fig.add_artist(ln); ln.set_clip_box(t.axes.bbox); ln.set_clip_on(True)        # la guía no sale de su dibujo
        colocados.append(Pn)
    return n_mov


def _guardar():
    if not REG:
        return
    f = "CALIDAD_GRAFICA.json"
    try:
        old = json.load(open(f))
    except Exception:
        old = {}
    old.update(REG)
    json.dump(old, open(f, "w"), ensure_ascii=False, indent=1)
    L = ["# Calidad gráfica (puerta 3b): rótulos que se pisan, cortados o fuera de la hoja", "",
         "| Salida | Se pisan | Sobre líneas | Cortados | Se salen del dibujo | Fuera de la hoja | Total |", "|---|---|---|---|---|---|---|"]
    for k in sorted(old):
        v = old[k]; n = lambda t: sum(1 for d in v if d["tipo"] == t)
        L.append(f"| `{k}` | {n('rótulos que se pisan')} | {n('rótulo sobre líneas')} | {n('cortado por el marco')} | {n('se sale de su dibujo')} | {n('fuera de la hoja')} | {len(v)} |")
    open("CALIDAD_GRAFICA.md", "w").write("\n".join(L) + "\n")


atexit.register(_guardar)
