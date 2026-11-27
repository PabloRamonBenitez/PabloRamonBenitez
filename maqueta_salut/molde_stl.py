"""VERSIÓN MOLDE: STL a 15 cm con el detalle que admite un molde de silicona para colar maquetas de hormigón.
Construye el edificio con SALUT_MOLDE=1 (ver edificio.py: grosores ≥ 0,6 m, rendijas ≥ 0,35 m, relieves ≥ 0,25 m, sin barandillas
abiertas, lamas macizas, letras en relieve sobre el remate), exporta el STL y comprueba el resultado cortándolo:
  · en horizontal cada 0,25 m y en vertical (radiales por la torre cada 15° y transversales del ala larga)
  · grueso < 0,6 m  → «fino» (el hormigón se rompe al desmoldar)
  · rendija < 0,35 m → «rendija» (la silicona se rasga o el hormigón no entra)
Escribe Hotel_Salut_15cm_MOLDE.stl, MOLDE.md y MOLDE_COMPARACION.png (detalle frente a molde)."""
import os, math
os.environ["SALUT_MOLDE"] = "1"
import numpy as np
import trimesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from shapely.geometry import Polygon as SP
from shapely.ops import unary_union
import edificio as E, lineas as L

GM, GR = 0.55, 0.33                                   # umbral de aviso (m reales): por debajo de los mínimos de diseño 0,60 / 0,35 con tolerancia de facetado
m = E.edificio()
me = m.to_mesh(); Vv = np.asarray(me.vert_properties)[:, :3]; F = np.asarray(me.tri_verts)
k = 150.0 / E.Z_R1
tm = trimesh.Trimesh(Vv * k, F)
tm.export("Hotel_Salut_15cm_MOLDE.stl")


def geom(cs):
    ps = [SP(np.array(P)).buffer(0) for P in cs.to_polygons() if len(P) > 2]
    return unary_union(ps) if ps else SP()


def revisar(g):
    fino = g.difference(g.buffer(-GM / 2, join_style=2).buffer(GM / 2, join_style=2))
    rend = g.buffer(GR / 2, join_style=2).buffer(-GR / 2, join_style=2).difference(g)
    f = [p for p in getattr(fino, "geoms", [fino]) if not p.is_empty and p.area > 0.04]
    r = [p for p in getattr(rend, "geoms", [rend]) if not p.is_empty and p.area > 0.04]
    return f, r


hall = []
for z in np.arange(0.15, E.Z_R1, 0.25):
    f, r = revisar(geom(m.slice(float(z))))
    hall += [("planta", round(float(z), 2), "fino", p.centroid.x, p.centroid.y, p.area) for p in f]
    hall += [("planta", round(float(z), 2), "rendija", p.centroid.x, p.centroid.y, p.area) for p in r]
T = np.array(E.T)
def vertical(p0, d):
    a = math.degrees(math.atan2(d[1], d[0]))
    mm = m.translate((-p0[0], -p0[1], 0)).rotate((0, 0, -a)).rotate((-90, 0, 0))
    return geom(mm.slice(0.0))
for az in range(0, 360, 15):
    d = np.array([math.cos(math.radians(az)), math.sin(math.radians(az))])
    f, r = revisar(vertical(T, d))
    hall += [(f"radial {az}°", 0, t, p.centroid.x, p.centroid.y, p.area) for t, ps in (("fino", f), ("rendija", r)) for p in ps]
for y in (30, 50, 70, 90):
    f, r = revisar(vertical(np.array([-5.0, y]), np.array([1.0, 0.0])))
    hall += [(f"transversal y={y}", 0, t, p.centroid.x, p.centroid.y, p.area) for t, ps in (("fino", f), ("rendija", r)) for p in ps]

# agrupa hallazgos cercanos (misma pieza vista en varios cortes)
grupos = []
for h in hall:
    for g in grupos:
        if g[0][2] == h[2] and g[0][0].split()[0] == h[0].split()[0] and math.hypot(g[0][3] - h[3], g[0][4] - h[4]) < 1.5:
            g.append(h); break
    else:
        grupos.append([h])

fig = plt.figure(figsize=(22, 13))
import importlib
os.environ["SALUT_MOLDE"] = "0"
import edificio as E2
E2 = importlib.reload(E2)
md = E2.edificio()
def orientar(mm, az, el):
    a, e_ = math.radians(az), math.radians(el)
    v = np.array([math.cos(e_) * math.cos(a), math.cos(e_) * math.sin(a), math.sin(e_)])
    r = np.cross([0, 0, 1], v); r /= np.linalg.norm(r); u = np.cross(v, r)
    return mm.transform(np.hstack([np.vstack([r, u, v]), np.zeros((3, 1))]).tolist())
for i, (t, az, el) in enumerate((("frontal elevada (como F01)", -40, 25), ("desde el patio (como F08)", 125, 22), ("desde el testero (como F73)", 80, 6))):
    for j, (mm, tt) in enumerate(((md, "DETALLE (planos)"), (m, "MOLDE (hormigón 1:339)"))):
        ax = fig.add_axes([0.005 + i * 0.333, 0.5 - j * 0.48, 0.325, 0.45]); L.dibujar_vista(ax, orientar(mm, az, el), res=0.07)
        ax.set_aspect("equal"); ax.axis("off"); ax.set_title(f"{tt} – {t}", fontsize=10, loc="left", weight="bold")
fig.suptitle("VOLUMEN: versión de detalle (arriba) y versión para molde de silicona y colada de hormigón (abajo)", fontsize=14, x=0.01, ha="left", weight="bold")
fig.savefig("MOLDE_COMPARACION.png", dpi=70)

bb = tm.bounds
tm2 = trimesh.Trimesh(Vv * k, F, process=True); tm2.merge_vertices()
_u, _inv = trimesh.grouping.unique_rows(tm2.edges_sorted); _c = np.bincount(_inv)
nab, nnm = int((_c == 1).sum()), int((_c > 2).sum())
lines = ["# Versión molde – STL para molde de silicona y colada de hormigón", "",
         f"`Hotel_Salut_15cm_MOLDE.stl` · escala 1:{round(1000 / k)} · caja {bb[1][0] - bb[0][0]:.0f} × {bb[1][1] - bb[0][1]:.0f} × {bb[1][2] - bb[0][2]:.0f} mm · "
         f"volumen {tm.volume / 1000:.0f} cm³ · una sola pieza: {'sí' if tm.body_count == 1 else 'NO'} · aristas abiertas: {nab} · aristas no manifold: {nnm} · base plana a z = 0", "",
         "## Criterios (1 mm de maqueta = 0,34 m reales)",
         "| criterio | valor real | en la maqueta |", "|---|---|---|",
         f"| grosor mínimo de cualquier elemento | {GM} m | {GM * k:.1f} mm |",
         f"| rendija o hueco mínimo | {GR} m | {GR * k:.1f} mm |", f"| relieve mínimo | 0,25 m | {0.25 * k:.1f} mm |", "",
         "## Qué cambia respecto a la versión de detalle",
         "- Barandillas abiertas (cubierta del barril, visera, azoteas, terrazas): fuera. En hormigón no se pueden colar.",
         "- Balcones: canto, ranura de 0,27 (0,8 mm) y poyete en **una sola banda** de 1,64. El hueco de 1,46 entre bandas se mantiene, a 1,2 de fondo (3,5 mm).",
         "- Aletas y vigas radiales de 0,40 → 0,70 (2,1 mm).",
         "- Tambor macizo hasta la banda: sin el pasillo de servicio ni el peto de 0,25. Banda acristalada sin montantes.",
         "- Letrero САЛЮТ: letras en volumen de 0,6 de fondo (trazo engrosado 0,12), pegadas al remate. Separadas a 1,5 m, como en la versión de detalle, se romperían al desmoldar.",
         "- Escalera: la pantalla de lamas (0,08 cada 0,35) se cuela como volumen macizo. El muro de coronación, el peto y los forjados vistos pasan a 0,60.",
         "- Petos de la terraza, la rampa y la meseta: 0,25–0,30 → 0,60. Sin marcos de ventana (relieve de 0,08) ni montantes del chaflán.",
         "- Muro final de la fachada retranqueada del ala larga y fondo del barril, a 0,6–0,7. (La fuente ya no está en ninguna de las dos versiones: la quitó el usuario el 27/11.)",
         "- Se mantienen: forjados y huecos del barril, ojos (Ø 1,6, 4,7 mm), visera, remate, claraboya, rampa, concha, ventanas del ala larga, los 10 lucernarios piramidales del bloque alto (base 3,8 mm, alto 3,5 mm), los 6 lucernarios bajo el cuello, columna, cuello y vigas.",
         "", f"## Comprobación por cortes ({len(hall)} detecciones en {len(grupos)} piezas)",
         "| tipo | dónde | cortes | área máx. (m²) |", "|---|---|---|---|"]
for g in sorted(grupos, key=lambda g: -max(h[5] for h in g))[:60]:
    lines.append(f"| {g[0][2]} | {g[0][0]} ({g[0][3]:.1f}, {g[0][4]:.1f}) | {len(g)} | {max(h[5] for h in g):.2f} |")
open("MOLDE.md", "w").write("\n".join(lines) + "\n")
print("STL", round(1000 / k), "abiertas", nab, "no-manifold", nnm, "cuerpos", tm.body_count, round(tm.volume / 1000), "cm3 · hallazgos", len(hall), "piezas", len(grupos))
for g in sorted(grupos, key=lambda g: -max(h[5] for h in g))[:40]:
    print(g[0][2], g[0][0], round(g[0][3], 1), round(g[0][4], 1), len(g), round(max(h[5] for h in g), 2))
