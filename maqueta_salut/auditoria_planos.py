"""AUDITORÍA GRÁFICA DE LA PLANIMETRÍA (antes de dar nada por bueno).
Corta el modelo en TODAS las plantas y secciones de los planos y busca, sin mirar a ojo:
  A · astillas macizas: trozos cortados delgados (< 0,09 m) y largos (> 0,6 m) que no son barandillas ni lamas
  B · rendijas: huecos de menos de 0,20 m entre dos macizos (cierre morfológico) que no son juntas de lamas
  C · nudos: vértices muy próximos (< 0,15 m) de contornos distintos (encuentros mal resueltos, como el de la escalera)
  D · reglas del usuario: sin ángulo de 90° en la parte de atrás de la L; triangulación A–B–C–D; testero sin tacón;
      base de la torre en ángulo recto; ningún plano entregado más antiguo que el cuadro de cotas
Escribe AUDITORIA_PLANOS.md y AUDITORIA_PLANOS.png (recorte de cada defecto)."""
import math, os, glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from shapely.geometry import Polygon as SP, MultiPolygon, Point, box
from shapely.ops import unary_union
from manifold3d import Manifold
import edificio as E, laminas as LM

V = E._v; M = LM.M
CORTES = [("planta baja", 1.8), ("planta 1", 5.6), ("planta 2", 9.2), ("planta 3", 13.0), ("planta tipo", E.Z_B0 + 3 * E.F + 2.0),
          ("tambor", E.Z_B1 + 2.0), ("banda", E.Z_T1 + 1.0)]
ZONA_LAMAS = []  # zonas donde las rendijas son juntas de lamas (intencionadas)
for r0, r1 in ((V["ESC_RR"] - 0.5, E.ESC_R1 + 0.6),):
    pts = [E.esc_ang_pt(r1, -E.ESC_HA - 0.05 + (2 * E.ESC_HA + 0.1) * k / 24) for k in range(25)] + \
          [E.esc_ang_pt(r0, E.ESC_HA + 0.05 - (2 * E.ESC_HA + 0.1) * k / 24) for k in range(25)]
    ZONA_LAMAS.append(SP(pts).buffer(0))
ZONA_LAMAS = unary_union(ZONA_LAMAS)


def geom(cs):
    ps = [SP(np.array(P)).buffer(0) for P in cs.to_polygons() if len(P) > 2]
    return unary_union(ps) if ps else SP()


def seccion_cs(p0, p1):
    """corte vertical por la recta p0→p1: se gira el modelo para que el plano de corte sea horizontal"""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float); d = (p1 - p0) / np.linalg.norm(p1 - p0)
    a = math.degrees(math.atan2(d[1], d[0]))
    m = M.translate((-p0[0], -p0[1], 0)).rotate((0, 0, -a)).rotate((-90, 0, 0))   # x = a lo largo, y = z, z = −n
    return m.slice(0.0)


def auditar(nombre, g, excl=None):
    out = []
    parts = list(getattr(g, "geoms", [g]))
    for p in parts:                                                # A · astillas
        if p.is_empty: continue
        mr = p.minimum_rotated_rectangle; xy = np.array(mr.exterior.coords)
        l1, l2 = np.linalg.norm(xy[1] - xy[0]), np.linalg.norm(xy[2] - xy[1]); w, L_ = min(l1, l2), max(l1, l2)
        if w < 0.09 and L_ > 0.6 and p.area / max(mr.area, 1e-9) > 0.6:
            if excl is not None and excl.contains(p.centroid): continue
            out.append(("A astilla", p.centroid.coords[0], f"{w:.2f} × {L_:.2f} m"))
    cerr = g.buffer(0.10, join_style=2).buffer(-0.10, join_style=2)  # B · rendijas < 0,20
    rend = cerr.difference(g)
    for r in getattr(rend, "geoms", [rend]):
        if r.is_empty or r.area < 0.03: continue
        if excl is not None and excl.intersects(r): continue
        mr = r.minimum_rotated_rectangle; xy = np.array(mr.exterior.coords)
        L_ = max(np.linalg.norm(xy[1] - xy[0]), np.linalg.norm(xy[2] - xy[1]))
        if L_ < 0.4: continue
        out.append(("B rendija", r.centroid.coords[0], f"{r.area:.2f} m², {L_:.2f} m de largo"))
    vs = []                                                          # C · nudos entre contornos distintos
    for i, p in enumerate(parts):
        if p.is_empty or p.area < 0.3: continue
        for c in np.array(p.exterior.coords)[:-1]: vs.append((i, c))
    if len(vs) < 20000:
        arr = np.array([c for _, c in vs]); ids = np.array([i for i, _ in vs])
        for k in range(len(arr)):
            dd = np.linalg.norm(arr - arr[k], axis=1)
            j = np.where((dd < 0.15) & (dd > 0.0) & (ids != ids[k]))[0]
            if len(j) and (excl is None or not excl.contains(Point(arr[k]))):
                out.append(("C nudo", tuple(arr[k]), f"{len(j)} vértices de otro contorno a < 0,15 m"))
    for p in parts:                                                  # E · dientes: escalones de < 0,35 m en un contorno grande
        if p.is_empty or p.area < 5: continue
        for ring in [p.exterior] + list(p.interiors):
            xy = np.array(ring.coords)[:-1]; n = len(xy)
            if n < 4: continue
            for k in range(n):
                a, b, c = xy[k - 1], xy[k], xy[(k + 1) % n]
                l1, l2 = np.linalg.norm(b - a), np.linalg.norm(c - b)
                if l1 < 1e-3 or l2 < 1e-3: continue
                cosg = np.clip((a - b) @ (c - b) / l1 / l2, -1, 1); ang = math.degrees(math.acos(cosg))
                if 60 < ang < 120 and min(l1, l2) < 0.06 and max(l1, l2) > 0.15:   # microescalón: dos piezas desalineadas
                    if excl is not None and excl.contains(Point(b)): continue
                    out.append(("E diente", tuple(b), f"escalón de {min(l1, l2):.2f} m ({ang:.0f}°)"))
    out = [o for o in out if o[0] != "E diente"] + [("e microescalón (faceta < 6 cm, invisible a 1:400)",) + o[1:] for o in out if o[0] == "E diente"]
    ded = []
    for t, c, n in out:                                              # quita repetidos (radio 0,5 m)
        if not any(t == t2 and math.dist(c, c2) < 0.5 for t2, c2, _ in ded): ded.append((t, c, n))
    return [(nombre, t, c, n) for t, c, n in ded]


def reglas():
    import cotas as K
    r = []
    g = K.planta()
    P1 = [np.array(p) for p in g["P1"]]
    # sin 90° en la parte de atrás de la L (entre la medianera y el ala larga)
    for i in range(len(P1)):
        a, b, c = P1[i - 1], P1[i], P1[(i + 1) % len(P1)]
        v1, v2 = a - b, c - b
        if min(np.linalg.norm(v1), np.linalg.norm(v2)) < 1.0: continue
        ang = math.degrees(math.acos(np.clip(v1 @ v2 / np.linalg.norm(v1) / np.linalg.norm(v2), -1, 1)))
        if abs(ang - 90) < 3 and b[0] < 0.5 and 5 < b[1] < 50:              # rincón de la L (no el testero)
            r.append(("D 90° atrás", tuple(b), f"esquina a {ang:.0f}° en la parte de atrás"))
    IC, F1 = np.array(g["IC"]), np.array(E.SWP(-V["L_C"], V["W_C"]))
    d = (IC - F1) / np.linalg.norm(IC - F1); u = np.array(E.U)
    if abs(abs(d @ u) - 1) > 0.002: r.append(("D línea posterior", tuple(IC), f"no es paralela al chaflán ({math.degrees(math.acos(abs(d @ u))):.1f}°)"))
    P = [np.array(p) for p in E.bloque_alto_poligono()]; A, B, C = P[0], P[1], P[2]; D = np.array([V["W_EXT"], V["L_L"]])
    for nom, x, ref, tol in (("A–B", np.linalg.norm(B - A), 7.3, 0.05), ("A–C", np.linalg.norm(C - A), 16.66, 0.05),
                             ("A–D", np.linalg.norm(D - A), 106.69, 0.1)):
        if abs(x - ref) > tol: r.append(("D triangulación", tuple(A), f"{nom} = {x:.2f} (debe ser {ref})"))
    if abs(np.linalg.norm(D - C) / 95.17 - 1) > 0.015: r.append(("D triangulación", tuple(C), f"D–C fuera del 1,5 %"))
    if V["ESQ_D"] > 0: r.append(("D testero", (V["W_P"], V["L_L"]), "muro de esquina (tacón) en el testero"))
    if abs(V["Z_CU1"] - V["Z_BI"]) > 0.01: r.append(("D base torre", tuple(E.T), "fondo del barril no plano"))
    t0 = os.path.getmtime("cotas.py")
    for f in ["SALUT_planos_A3_presentacion.pdf", "SALUT_planos_A4.pdf", "SALUT_planos_definitivos.pdf", "SALUT_planos_2D.pdf",
              "PLANO_LUGAR_1984.pdf", "Hotel_Salut_15cm_v3.stl", "DIBUJOS_EXPLICATIVOS/DIBUJOS_EXPLICATIVOS.pdf"]:
        if os.path.exists(f) and os.path.getmtime(f) < t0:
            r.append(("D entregable antiguo", (0, 0), f"{f} es anterior al cuadro de cotas"))
    return [("reglas",) + x for x in r]


def escalera_vs_forjados():
    """Ningún rellano de planta puede quedar a otra cota que su forjado: dibuja cada sección que corta la escalera y compara la
    cara superior de cada rellano cortado (losa de 0,20) con E.niveles_suelo() y con el rellano intermedio [usuario 27/11]."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    out = []
    NS = E.niveles_suelo(); mid = [(a + b) / 2 for a, b in zip(NS[:-1], NS[1:])]
    for k, p0, p1, _ in LM.SECC:
        if LM.hueco_escalera(p0, p1) is None: continue
        fig = plt.figure(figsize=(4, 4)); ax = fig.add_axes([0, 0, 1, 1])
        LM.tramos_escalera(ax, p0, p1)
        tops = sorted({round(p.get_y() + p.get_height(), 3) for p in ax.patches if isinstance(p, Rectangle) and abs(p.get_height() - 0.20) < 0.01})
        plt.close(fig)
        if not tops: continue
        for zt in tops:
            d = min(abs(zt - z) for z in NS + mid)
            if d > 0.02: out.append(("reglas", "D escalera ≠ forjado", (0, zt), f"sección {k}: rellano a +{zt:.2f}, el forjado más próximo está a {d:.2f} m"))
        for z in NS[1:]:
            if not any(abs(zt - z) < 0.02 for zt in tops):
                out.append(("reglas", "D escalera ≠ forjado", (0, z), f"sección {k}: el forjado +{z:.2f} no tiene rellano de planta"))
    return out


if __name__ == "__main__":
    res = []
    import ventanas as VT
    for nom, z in CORTES:
        hz = [SP([tuple(np.array(h["p"]) + np.array(h["t"]) * s1 * (h["w"] / 2 + 0.35) + np.array(h["n"]) * s2 * 0.6)
                  for s1, s2 in ((-1, -1), (1, -1), (1, 1), (-1, 1))]) for h in VT.catalogo() if h["z0"] - 0.5 <= z <= h["z1"] + 0.5]
        ex = unary_union([ZONA_LAMAS] + hz)                        # huecos del catálogo: sus mochetas y marcos son intencionados
        res += auditar(f"{nom} (+{z:.2f})", geom(M.slice(z)), ex)
    for k, p0, p1, _ in LM.SECC:
        g = geom(seccion_cs(p0, p1))
        exs = unary_union([box(-500, -1, 500, 0.25), box(-500, V["SIG_Z0"] - 0.1, 500, V["SIG_Z1"] + 0.1)])   # rasante y letras
        res += auditar(f"sección {k}", g, exs)
    res += reglas()
    res += escalera_vs_forjados()
    graves = [x for x in res if not x[1].startswith("e ")]
    lines = ["# Auditoría gráfica de la planimetría", "", f"Cortes: {', '.join(n for n, _ in CORTES)} · secciones {', '.join(k for k, *_ in LM.SECC)}",
             "", f"**Defectos: {len(graves)}** (A astillas · B rendijas · C nudos · D reglas del usuario) · "
             f"{len(res) - len(graves)} microescalones de faceta (< 6 cm, invisibles a 1:400, no se corrigen)", "",
             "| corte | tipo | x, y (o u, z) | detalle |", "|---|---|---|---|"]
    for n, t, c, d in graves:
        lines.append(f"| {n} | {t} | {c[0]:.1f}, {c[1]:.1f} | {d} |")
    open("AUDITORIA_PLANOS.md", "w").write("\n".join(lines) + "\n")
    print(len(graves), "defectos graves ·", len(res) - len(graves), "microescalones")
    for x in graves: print(x[0], "|", x[1], "|", np.round(x[2], 1), "|", x[3])
    # HOJA DE NUDOS: los encuentros más complejos de cada planta, ampliados, para revisarlos uno a uno
    import matplotlib.pyplot as plt
    crops = []
    for nom, z in CORTES[:5]:
        g = geom(M.slice(z)); pts = []
        for p in getattr(g, "geoms", [g]):
            for ring in [p.exterior] + list(p.interiors):
                xy = np.array(ring.coords)[:-1]; n = len(xy)
                for k in range(n):
                    a, b, c = xy[k - 1], xy[k], xy[(k + 1) % n]
                    v1, v2 = a - b, c - b
                    if min(np.linalg.norm(v1), np.linalg.norm(v2)) < 0.02: continue
                    ang = math.degrees(math.acos(np.clip(v1 @ v2 / np.linalg.norm(v1) / np.linalg.norm(v2), -1, 1)))
                    if ang < 155 and not ZONA_LAMAS.contains(Point(b)): pts.append(b)
        pts = np.array(pts); celdas = {}
        for q in pts: celdas.setdefault((int(q[0] // 3), int(q[1] // 3)), []).append(q)
        top = sorted(celdas.items(), key=lambda kv: -len(kv[1]))[:6]
        crops += [(nom, z, np.mean(v, axis=0)) for _, v in top]
    nc = 6; nr = math.ceil(len(crops) / nc)
    fig = plt.figure(figsize=(4 * nc, 4.2 * nr))
    for i, (nom, z, c) in enumerate(crops):
        ax = fig.add_axes([(i % nc) / nc + 0.005, 1 - (i // nc + 1) / nr + 0.01, 1 / nc - 0.01, 1 / nr - 0.03])
        LM.planta(ax, z, ""); ax.set_xlim(c[0] - 3, c[0] + 3); ax.set_ylim(c[1] - 3, c[1] + 3); ax.set_aspect("equal")
        ax.set_xticks([]); ax.set_yticks([]); ax.set_title(f"{nom} · ({c[0]:.1f}, {c[1]:.1f})", fontsize=8, loc="left")
    fig.savefig("AUDITORIA_NUDOS.png", dpi=60)
