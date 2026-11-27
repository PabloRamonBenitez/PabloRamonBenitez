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
    bb = t.get_window_extent(r)
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
        elif ax is not None and ax.get_aspect() == 1.0:              # dibujo a escala: ningún rótulo se sale de su dibujo
            from shapely.geometry import box
            A = box(*ax.bbox.extents)
            if A.intersection(P).area < 0.97 * P.area:
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
