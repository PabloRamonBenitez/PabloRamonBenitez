"""Laminas de zonas: axonometrias (2), plantas (0, 1, cubiertas) y secciones, con las mismas zonas y colores."""
import math, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MP
from matplotlib.backends.backend_pdf import PdfPages
from shapely.geometry import Polygon as SP, LineString
from manifold3d import Manifold
import edificio as E, lineas as L, zonas_def as Z

M = E.edificio()
cm = plt.cm.tab20(np.linspace(0, 1, 20)); cm2 = plt.cm.tab20b(np.linspace(0, 1, 20))
COL = {z[0]: (cm[i] if i < 20 else cm2[i - 20]) for i, z in enumerate(Z.ZONAS)}
OUT = []


def etq(ax, p, k, fs=8):
    c = COL[k]
    ax.text(p[0], p[1], k, color="white", fontsize=fs, weight="bold", ha="center", va="center", zorder=20,
            bbox=dict(fc=c, ec="none", pad=1.0))


def hoja(t, w=16.5, h=11.7):
    f = plt.figure(figsize=(w, h))
    f.text(0.01, 0.985, "HOTEL SALUT – ZONAS DE VERIFICACIÓN – " + t, fontsize=13, weight="bold", va="top")
    return f


def leyenda(fig, x=0.79):
    ax = fig.add_axes([x, 0.03, 0.2, 0.92]); ax.axis("off")
    y = 1.0; g0 = None
    for k, n, g, *_ in Z.ZONAS:
        if g != g0:
            ax.text(0, y, g.upper(), fontsize=8, weight="bold", va="top"); y -= 0.022; g0 = g
        ax.add_patch(plt.Rectangle((0, y - 0.016), 0.06, 0.016, color=COL[k], transform=ax.transAxes))
        ax.text(0.08, y, f"{k}  {n}", fontsize=6.6, va="top", transform=ax.transAxes); y -= 0.021


# ------------------------------------------------------------------ axonometrias
def matriz_axo(az, el):
    a, e = math.radians(az), math.radians(el)
    Rz = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, math.cos(e - math.pi / 2), -math.sin(e - math.pi / 2)], [0, math.sin(e - math.pi / 2), math.cos(e - math.pi / 2)]])
    return Rx @ Rz


def axo(ax, az, el, titulo):
    R = matriz_axo(az, el)
    m = M.transform(np.c_[R, np.zeros(3)].tolist())
    L.dibujar_vista(ax, m, res=0.08)
    def pr(P3): return (np.atleast_2d(P3) @ R.T)[:, :2]
    for z in Z.ZONAS:
        k, n, g, t, d = z; c = COL[k]
        if t == "cil":
            cc, r0, r1, z0, z1 = d; a = np.linspace(0, 2 * np.pi, 80)
            for zz in (z0, z1):
                q = pr(np.c_[cc[0] + r1 * np.cos(a), cc[1] + r1 * np.sin(a), np.full(80, zz)]); ax.plot(q[:, 0], q[:, 1], color=c, lw=1.6, zorder=10)
            q = pr([[cc[0] - r1 * 0.95, cc[1], z1]])[0]; etq(ax, q, k, 7)
        elif t == "pri":
            for p, z0, z1 in d:
                p = np.array(p); m_ = len(p)
                lo = pr(np.c_[p, np.full(m_, z0)]); hi = pr(np.c_[p, np.full(m_, z1)])
                for j in range(m_):
                    for A, B in ((lo[j], lo[(j + 1) % m_]), (hi[j], hi[(j + 1) % m_]), (lo[j], hi[j])):
                        ax.plot([A[0], B[0]], [A[1], B[1]], color=c, lw=1.4, zorder=10)
                etq(ax, hi.mean(axis=0), k, 7)
        else:
            ls, _ = Z.concha_lineas()
            for l3 in ls:
                q = pr(l3); ax.plot(q[:, 0], q[:, 1], color=c, lw=1.8, zorder=10)
            etq(ax, pr(ls[0][6])[0], k, 7)
    ax.set_aspect("equal"); ax.axis("off"); ax.set_title(titulo, fontsize=10, loc="left")


# ------------------------------------------------------------------ plantas
def planta(ax, zc, titulo, zmin, zmax):
    BIG = 400
    if zc is None:
        L.dibujar_vista(ax, M, res=0.06)
    else:
        L.dibujar_vista(ax, M ^ Manifold.cube((BIG, BIG, zc)).translate((-BIG / 2, -BIG / 2, -1)), res=0.06)
        L.encima(ax, M ^ Manifold.cube((BIG, BIG, 100)).translate((-BIG / 2, -BIG / 2, zc)))
        L.corte(ax, M.slice(zc))
    for z in Z.ZONAS:
        for p, z0, z1 in Z.huella(z):
            if z1 < zmin or z0 > zmax:
                continue
            ax.add_patch(MP(p, closed=True, fc=(*COL[z[0]][:3], 0.22), ec=COL[z[0]], lw=1.6, zorder=8))
            etq(ax, p.mean(axis=0), z[0], 7)
    ax.set_xlim(-28, 22); ax.set_ylim(-8, 98); ax.set_aspect("equal"); ax.tick_params(labelsize=6); ax.grid(True, lw=0.15)
    ax.set_title(titulo, fontsize=10, loc="left")


# ------------------------------------------------------------------ secciones
def seccion(ax, p0, p1, titulo, ylim=(-1, 52)):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = (p1 - p0) / np.linalg.norm(p1 - p0); Lg = np.linalg.norm(p1 - p0); a = math.degrees(math.atan2(d[1], d[0]))
    m = M.translate((-p0[0], -p0[1], 0)).rotate((0, 0, -a)).rotate((-90, 0, 0))
    L.dibujar_vista(ax, m ^ Manifold.cube((800, 100, 800)).translate((-400, -50, -800)), res=0.06)
    L.corte(ax, m.slice(0.0))
    linea = LineString([tuple(p0), tuple(p1)])
    for z in Z.ZONAS:
        for p, z0, z1 in Z.huella(z):
            inter = SP(p).intersection(linea)
            if inter.is_empty:
                continue
            ss = [(np.array(q) - p0) @ d for q in np.array(inter.coords if hasattr(inter, "coords") else [c for g in inter.geoms for c in g.coords])]
            s0, s1 = min(ss), max(ss)
            ax.add_patch(plt.Rectangle((s0, z0), s1 - s0, z1 - z0, fc=(*COL[z[0]][:3], 0.15), ec=COL[z[0]], lw=1.8, zorder=8))
            etq(ax, ((s0 + s1) / 2, (z0 + z1) / 2), z[0], 7)
    ax.axhline(0, color="k", lw=1.5)
    ax.set_xlim(-1, Lg + 1); ax.set_ylim(*ylim); ax.set_aspect("equal"); ax.tick_params(labelsize=6); ax.grid(True, lw=0.15)
    ax.set_title(titulo, fontsize=9, loc="left")


SECC = [("SA", Z.P(0, -16), Z.P(0, 30), "por el eje de la torre, perpendicular al chaflán (izq. = plaza)"),
        ("SB", Z.P(-10, -12), Z.P(-10, 14), "por la banda del restaurante, perpendicular al chaflán"),
        ("SC", Z.P(7.5, -12), Z.P(7.5, 14), "por la banda del hotel, perpendicular al chaflán"),
        ("SD", (-4, 40), (20, 40), "transversal del ala larga por el tramo ciego y la concha (izq. = patio)"),
        ("SE", (-4, 70), (20, 70), "transversal del ala larga por el bar, la terraza y las ventanas"),
        ("SF", (-4, 91), (20, 91), "transversal del ala larga por el tramo final"),
        ("SG", (-14, -6), (-14, 18), "transversal del ala corta (restaurante + bloque alto)"),
        ("LA", (3.1, -8), (3.1, 98), "LONGITUDINAL del ala larga por el bar"),
        ("LB", (11.5, -8), (11.5, 98), "LONGITUDINAL del ala larga por la terraza y la fachada exterior"),
        ("LC", (-28, 8.0), (25, 8.0), "LONGITUDINAL del ala corta")]

if __name__ == "__main__":
    fig = hoja("AXONOMETRÍAS")
    axo(fig.add_axes([0.0, 0.03, 0.39, 0.92]), -35, 30, "axonometría desde la plaza (chaflán)")
    axo(fig.add_axes([0.39, 0.03, 0.39, 0.92]), 135, 30, "axonometría desde el patio (ala larga y escalera)")
    leyenda(fig); OUT.append(fig)
    for zc, t, a, b in ((1.8, "PLANTA 0 (corte +1,80)", 0, 3.9), (5.6, "PLANTA 1 (corte +5,60)", 3.8, 7.4),
                        (None, "PLANTA DE CUBIERTAS Y TORRE", 7.2, 60)):
        fig = hoja(t); planta(fig.add_axes([0.03, 0.03, 0.74, 0.92]), zc, t, a, b); leyenda(fig); OUT.append(fig)
    fig = hoja("SITUACIÓN DE SECCIONES")
    ax = fig.add_axes([0.03, 0.03, 0.74, 0.92]); planta(ax, None, "situación", 99, 99)
    for k, p0, p1, _ in SECC:
        ax.plot(*zip(p0, p1), "-.", color="crimson", lw=1); ax.text(*p0, k, color="crimson", weight="bold"); ax.text(*p1, k, color="crimson", weight="bold")
    leyenda(fig); OUT.append(fig)
    for grupo in (SECC[0:3], SECC[3:6], SECC[6:7], SECC[7:8], SECC[8:9], SECC[9:10]):
        fig = hoja("SECCIONES " + " / ".join(g[0] for g in grupo))
        n = len(grupo)
        for i, (k, p0, p1, t) in enumerate(grupo):
            if n == 3:
                axg = fig.add_axes([0.03 + i * 0.255, 0.04, 0.25, 0.9])
            else:
                axg = fig.add_axes([0.03, 0.04, 0.74, 0.9])
            seccion(axg, p0, p1, f"{k}: {t}")
        leyenda(fig); OUT.append(fig)
    plt.rcParams["figure.max_open_warning"] = 0
    with PdfPages("ZONAS_laminas.pdf") as pdf:
        for i, f in enumerate(OUT):
            pdf.savefig(f); f.savefig(f"zon_{i + 1:02d}.png", dpi=75)
    print("laminas", len(OUT), "zonas", len(Z.ZONAS), "juntas", len(Z.JUNTAS))
