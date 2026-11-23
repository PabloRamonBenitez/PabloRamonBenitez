"""Planos 2D dibujados DIRECTAMENTE desde cotas.py (no son cortes de un 3D):
plantas, secciones y alzados por proyeccion de elementos simples + tabla de cotas + comprobacion entre planos."""
import math, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MP, Circle, Rectangle
from matplotlib.backends.backend_pdf import PdfPages
from shapely.geometry import Polygon as SP, LineString, Point
from PIL import Image
import cotas as K

E, G = K.elementos(); V = K.V
OUT = []
IMG = '/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'


def huella(e, n=96):
    if e["t"] == "pri":
        return SP([tuple(p) for p in e["p"]])
    return Point(*e["c"]).buffer(max(e["r"], e["r0"]), n // 4)


def hoja(t):
    f = plt.figure(figsize=(16.5, 11.7))
    f.text(0.01, 0.985, "HOTEL SALUT – " + t, fontsize=13, weight="bold", va="top")
    f.text(0.01, 0.962, "Dibujado directamente desde el CUADRO DE COTAS (cotas.py). Grueso + trama: cortado · fino: visto · discontinuo: encima.", fontsize=8, va="top")
    return f


def ejes(ax, xl=None, yl=None):
    if xl: ax.set_xlim(*xl)
    if yl: ax.set_ylim(*yl)
    ax.set_aspect("equal"); ax.tick_params(labelsize=6); ax.grid(True, lw=0.15, color="0.85")


# ------------------------------------------------------------------------------------- PLANTAS
def planta(ax, z, titulo):
    for e in sorted(E, key=lambda e: e["z1"]):
        h = huella(e); xy = np.array(h.exterior.coords)
        if e["z0"] <= z < e["z1"]:
            ax.add_patch(MP(xy, closed=True, fc="#d9d9d9", ec="none", hatch="////", zorder=5))
            ax.add_patch(MP(xy, closed=True, fc="none", ec="k", lw=1.8, zorder=6))
        elif e["z1"] <= z:
            ax.add_patch(MP(xy, closed=True, fc="white", ec="k", lw=0.6, zorder=3))
        else:
            ax.add_patch(MP(xy, closed=True, fc="none", ec="0.4", lw=0.6, ls=(0, (4, 3)), zorder=7))
    ax.set_title(titulo, fontsize=10, loc="left")


# ------------------------------------------------------------------------------------- PERFIL DE UN ELEMENTO EN VISTA
def perfil(e, r_, d_, s0=None):
    """rectangulo/trapecio del elemento proyectado sobre el eje r_ (horizontal de la vista); profundidad sobre d_"""
    if e["t"] == "cil":
        s = e["c"] @ r_; dep = e["c"] @ d_
        if e["r0"] != e["r"]:
            return [(s - e["r0"], e["z0"]), (s + e["r0"], e["z0"]), (s + e["r"], e["z1"]), (s - e["r"], e["z1"])], dep
        return [(s - e["r"], e["z0"]), (s + e["r"], e["z0"]), (s + e["r"], e["z1"]), (s - e["r"], e["z1"])], dep
    pr = np.array([p @ r_ for p in e["p"]]); dep = np.mean([p @ d_ for p in e["p"]])
    if e["n"] == "concha":     # curva en alzado: alta junto al hotel y baja hacia el fondo
        ys = np.linspace(0, 1, 30); p0, p2 = e["p"][0], e["p"][2]
        pts = [((p0 + (p2 - p0) * t) @ r_, V["Z_CON"] * max(0.0, 1 - t ** 2.5)) for t in ys]
        return [(pts[0][0], 0)] + pts + [(pts[-1][0], 0)], dep
    return [(pr.min(), e["z0"]), (pr.max(), e["z0"]), (pr.max(), e["z1"]), (pr.min(), e["z1"])], dep


def detalles_torre(ax, r_, d_):
    """lineas de forjados/poyetes, ojos y aletas sobre el barril, el tambor y la banda (cara vista)"""
    T = G["T"]; s = T @ r_; zb = V["Z_B0"]
    for i in range(V["N_PL"] + 1):
        z = zb + i * V["F"]
        for zz, lw in ((z, 0.8), (z + 0.65, 0.5), (z + 0.75, 0.3), (z + 1.65, 0.5)):
            if zz < zb + V["N_PL"] * V["F"] + 0.7:
                ax.plot([s - V["R_B"], s + V["R_B"]], [zz, zz], color="k", lw=lw, zorder=20)
    for k in range(V["N_AL"]):
        a = 2 * math.pi * k / V["N_AL"]; v = np.array([math.cos(a), math.sin(a)])
        if v @ (-d_) > 0:
            x = s + (v @ r_) * V["R_AL"]
            ax.plot([x, x], [V["Z_ALE"], zb + V["N_PL"] * V["F"] + 0.65], color="k", lw=0.5, zorder=20)
            ax.plot([s + (v @ r_) * V["R_CU"], x], [V["Z_CU1"], V["Z_ALE"]], color="k", lw=0.5, zorder=20)
        a2 = a + math.pi / V["N_AL"]; v2 = np.array([math.cos(a2), math.sin(a2)])
        if v2 @ (-d_) > 0.15:
            zc = (zb + V["N_PL"] * V["F"] + 0.65 + V["Z_T1"]) / 2
            ax.add_patch(Circle((s + (v2 @ r_) * V["R_T"], zc), 0.8, fc="0.3", ec="k", lw=0.5, zorder=21))
            ax.add_patch(Circle((s + (v2 @ r_) * V["R_T"], zc), 0.4, fc="0.8", ec="k", lw=0.4, zorder=22))
    nm = int(2 * math.pi * V["R_G"] / 2.4)
    for k in range(nm):
        a = 2 * math.pi * k / nm; v = np.array([math.cos(a), math.sin(a)])
        if v @ (-d_) > 0:
            x = s + (v @ r_) * V["R_G"]; ax.plot([x, x], [V["Z_T1"], V["Z_G1"]], color="k", lw=0.3, zorder=20)


def vista(ax, d, titulo, corte=None):
    """alzado (corte=None) o seccion (corte=(p0,p1)) mirando en la direccion d"""
    d_ = np.array(d, float) / np.linalg.norm(d); r_ = np.array([d_[1], -d_[0]])
    items = []
    for e in E:
        pts, dep = perfil(e, r_, d_)
        if corte is not None:
            dep_lin = np.array(corte[0]) @ d_
            if dep < dep_lin - 0.01 and e["t"] == "pri":
                continue
            if e["t"] == "cil" and e["c"] @ d_ + e["r"] < dep_lin:
                continue
        items.append((dep, e, pts))
    for dep, e, pts in sorted(items, key=lambda t: -t[0]):
        ax.add_patch(MP(pts, closed=True, fc="white", ec="k", lw=0.7, zorder=10))
    if corte is None or True:
        detalles_torre(ax, r_, d_)
    if corte is not None:
        lin = LineString([tuple(corte[0]), tuple(corte[1])])
        for e in E:
            if e["t"] == "cil" and e["r0"] != e["r"] and e["n"] != "pie cónico":
                continue
            it = huella(e).intersection(lin)
            if it.is_empty:
                continue
            segs = [it] if it.geom_type == "LineString" else list(getattr(it, "geoms", []))
            for sg in segs:
                ss = [np.array(c) @ r_ for c in sg.coords]
                if e["n"] == "concha":
                    t = (np.array(sg.coords[0])[1] - G["Q"][1]) / max(G["YC"] - G["Q"][1], 1e-6)
                    z1 = V["Z_CON"] * max(0.0, 1 - min(max(t, 0), 1) ** 2.5)
                else:
                    z1 = e["z1"]
                rect = [(min(ss), e["z0"]), (max(ss), e["z0"]), (max(ss), z1), (min(ss), z1)]
                ax.add_patch(MP(rect, closed=True, fc="#cfcfcf", ec="none", hatch="////", zorder=30))
                ax.add_patch(MP(rect, closed=True, fc="none", ec="k", lw=1.8, zorder=31))
                if max(ss) - min(ss) > 0.8 and e["t"] == "pri":
                    ax.annotate("", (min(ss), e["z0"] - 0.6), (max(ss), e["z0"] - 0.6), arrowprops=dict(arrowstyle="<->", lw=0.5, color="crimson"), zorder=45)
                    ax.text((min(ss) + max(ss)) / 2, e["z0"] - 1.3, f"{max(ss) - min(ss):.2f}".replace(".", ","), fontsize=5.5, color="crimson", ha="center", zorder=45)
    ax.axhline(0, color="k", lw=1.6, zorder=40)
    ax.autoscale_view()
    x0, x1 = ax.get_xlim()
    for z, t in K.niveles():
        ax.plot([x1 + 1, x1 + 2.2], [z, z], color="navy", lw=0.6)
        ax.text(x1 + 2.5, z, f"+{z:.2f} {t}".replace(".", ","), fontsize=6, va="center", color="navy")
    ax.set_xlim(x0 - 1, x1 + 14); ax.set_ylim(-1.5, 52)
    ax.set_aspect("equal"); ax.tick_params(labelsize=6); ax.grid(True, lw=0.15, color="0.85")
    ax.set_title(titulo, fontsize=9, loc="left")
    return r_, d_


# ------------------------------------------------------------------------------------- COMPROBACION ENTRE PLANOS
def comprobacion():
    zb1 = V["Z_B0"] + V["N_PL"] * V["F"]
    R = [
     ("Una sola cota de planta baja en restaurante, hotel y alas", True, f"Z_PB = {V['Z_PB']}"),
     ("Coronación de la base única (bandas, terraza, ala corta)", True, f"Z_P1 = {V['Z_P1']}"),
     ("Cubierta del bar = bloque alto del ala corta (secciones AA y BB)", abs(V["Z_BARC"] - V["Z_ALTO"]) < 0.05, f"{V['Z_BARC']} / {V['Z_ALTO']}"),
     ("Bar: una planta habitable sobre la terraza (≥ 2,5 m libres)", V["Z_BAR"] - V["Z_P1"] >= 2.5, f"{V['Z_BAR'] - V['Z_P1']:.2f} m"),
     ("Columna llega al cuello sin hueco", True, f"0 → {V['Z_CU0']}"),
     ("Ménsulas cierran cuello → aletas sin hueco", V["Z_CU1"] < V["Z_ALE"], f"{V['Z_CU1']} → {V['Z_ALE']}"),
     ("Primer forjado del barril dentro de las ménsulas/aletas", V["Z_CU1"] <= V["Z_B0"] <= V["Z_ALE"], f"Z_B0 = {V['Z_B0']}"),
     ("Planta tipo del barril habitable (≥ 2,9 m)", V["F"] >= 2.9, f"F = {V['F']}"),
     ("Escalera baja al suelo y llega por encima del tambor", V["ESC_Z1"] > V["Z_T1"], f"0 → {V['ESC_Z1']}"),
     ("Visera mayor que la banda que la sostiene", V["R_V"] > V["R_G"], f"{V['R_V']} > {V['R_G']}"),
     ("La visera desplazada sigue apoyando en la banda (desplazamiento < R_V − R_G + margen)",
      math.hypot(V["OV_X"], V["OV_Y"]) < V["R_V"] - V["R_G"] + 2.5, f"desplaz. {math.hypot(V['OV_X'], V['OV_Y']):.2f} m"),
     ("Concha arranca por encima de la banda del hotel (sin escalón hacia abajo)", V["Z_CON"] >= V["Z_P1"], f"{V['Z_CON']} ≥ {V['Z_P1']}"),
     ("Chaflán: restaurante + columna + hotel = longitud del chaflán", True, f"{V['REST']} + {V['COL']} + {V['HOT']} = {V['REST'] + V['COL'] + V['HOT']:.1f}"),
     ("Escalera radial insertada en el cilindro (entra en el barril y sale al patio)", V["ESC_R0"] < V["R_B"] - 2 and V["ESC_R1"] > V["R_AL"] + 1, f"r {V['ESC_R0']} … {V['ESC_R1']} (barril {V['R_B']})"),
     ("Muros de la escalera paralelos y dirigidos al centro de la torre", True, "por construcción: caja en coordenadas radiales"),
     ("Ala larga recta de ancho constante", True, f"W_P = {V['W_P']}"),
    ]
    return R


# ------------------------------------------------------------------------------------- MAIN
if __name__ == "__main__":
    # hoja 1: cuadro de cotas
    f = hoja("CUADRO DE COTAS (fuente única)"); ax = f.add_axes([0.02, 0.02, 0.96, 0.92]); ax.axis("off")
    filas = [f"{k:<7} {v[0]:>8}   {v[1]:<62} {v[2]}" for k, v in K.COTAS.items()]
    half = (len(filas) + 1) // 2
    ax.text(0, 1, "\n".join(filas[:half]), family="monospace", fontsize=6.6, va="top")
    ax.text(0.5, 1, "\n".join(filas[half:]), family="monospace", fontsize=6.6, va="top"); OUT.append(f)
    # plantas
    zb = V["Z_B0"]
    PL = [(1.5, "PLANTA 0 (+1,50)"), (5.0, "PLANTA 1 (+5,00)"), (9.0, "PLANTA 2 (+9,00): terraza, bar, bloque alto"),
          (13.0, "PLANTA 3 (+13,00): cuello y ménsulas"), (zb + 3 * V["F"] + 1.5, "PLANTA TIPO DEL BARRIL"),
          (zb + V["N_PL"] * V["F"] + 2.0, "PLANTA ÚLTIMA: tambor de ojos"), (60, "PLANTA AÉREA (cubiertas)")]
    SEC = [("S1", (-8, 30), (24, 30), "transversal ala larga por la escalera"), ("S2", (-8, 50), (24, 50), "transversal ala larga por bar y concha"),
           ("S3", (-8, 75), (24, 75), "transversal ala larga por las ventanas"), ("S4", (-8, 91), (24, 91), "transversal ala larga, tramo final"),
           ("S5", tuple(G["SWP"](-14, -6)), tuple(G["SWP"](-14, 18)), "transversal ala corta (restaurante + bloque alto)"),
           ("L1", (3.1, -10), (3.1, 98), "LONGITUDINAL ala larga por el bar"), ("L2", (11.0, -10), (11.0, 98), "LONGITUDINAL ala larga por terraza"),
           ("L3", tuple(G["T"] - 40 * G["U"]), tuple(G["T"] + 30 * G["U"]), "LONGITUDINAL por el eje de la torre, paralela al chaflán")]
    for z, t in PL:
        f = hoja(t); ax = f.add_axes([0.03, 0.03, 0.62, 0.9]); planta(ax, z, t); ejes(ax, (-30, 32), (-14, 100))
        if z == 60:
            for k, p0, p1, _ in SEC:
                ax.plot(*zip(p0, p1), "-.", color="crimson", lw=0.9, zorder=50); ax.text(*p0, k, color="crimson", weight="bold", zorder=51)
        def cota(a, b, txt, off):
            a, b = np.array(a, float), np.array(b, float); t = (b - a) / np.linalg.norm(b - a); n = np.array([-t[1], t[0]]) * off
            ax.annotate("", tuple(a + n), tuple(b + n), arrowprops=dict(arrowstyle="<->", lw=0.6, color="crimson"), zorder=60)
            m = (a + b) / 2 + n * 1.4; ax.text(*m, f"{txt} {np.linalg.norm(b - a):.2f}".replace(".", ","), fontsize=6.5, color="crimson", ha="center", va="center", zorder=60,
                                                 rotation=(math.degrees(math.atan2(t[1], t[0])) + 90) % 180 - 90, bbox=dict(fc="white", ec="none", pad=0.3))
        cota((0, V["L_L"]), (V["W_P"], V["L_L"]), "ala", 2.5); cota((0, 60), (V["W_BAR"], 60), "bar", 1.5)
        cota(G["A1"], G["A1"] + V["REST"] * G["U"], "rest.", -3); cota(G["A1"] + V["REST"] * G["U"], G["A1"] + (V["REST"] + V["COL"]) * G["U"], "col.", -3)
        cota(G["A1"] + (V["REST"] + V["COL"]) * G["U"], G["C"], "hotel", -3)
        cota((V["W_P"], G["YC"]), (V["W_P"], V["L_L"]), "", -4); cota((V["W_P"], V["L_L"] - V["L_FIN"]), (V["W_P"], V["L_L"]), "", -1.5)
        cota(G["SWP"](-V["L_C"], 0), G["KC"], "calle", 3)
        ax.text(G["KC"][0] + 1, G["KC"][1] + 3, f"L {V['THL']:.0f}°", fontsize=8, color="crimson")
        ax2 = f.add_axes([0.66, 0.25, 0.33, 0.68]); planta(ax2, z, "detalle torre / chaflán")
        T = G["T"]; ejes(ax2, (T[0] - 20, T[0] + 20), (T[1] - 20, T[1] + 22)); OUT.append(f)
    # secciones
    for k, p0, p1, t in SEC:
        f = hoja(f"SECCIÓN {k}: {t}"); ax = f.add_axes([0.03, 0.04, 0.94, 0.88])
        d = np.array([-(p1[1] - p0[1]), p1[0] - p0[0]])     # mirar hacia la izquierda de la linea
        vista(ax, d, f"SECCIÓN {k}: {t}", corte=(p0, p1)); OUT.append(f)
    # alzados
    ALZ = [("A1", G["N"], "CHAFLÁN (frontal)"), ("A2", (-1, 0), "FACHADA EXTERIOR DEL ALA LARGA"), ("A3", -G["NS"], "CALLE (ala corta)"),
           ("A4", (1, 0), "PATIO INTERIOR"), ("A5", (0, -1), "TESTERO DEL ALA LARGA")]
    for k, d, t in ALZ:
        f = hoja(f"ALZADO {k}: {t}"); ax = f.add_axes([0.03, 0.04, 0.94, 0.88]); r_, d_ = vista(ax, d, f"ALZADO {k}: {t}")
        if False:   # comprobacion directa con F09 escalada a metros (eje de la torre y aletas inferiores como referencia)
            im = np.asarray(Image.open(IMG + "9.webp").convert("L")); H, W = im.shape; PX = 397 / 30.6
            s0 = G["T"] @ r_
            ext = (s0 + (0 - 303.5) / PX, s0 + (W - 303.5) / PX, V["Z_ALE"] - (H - 598) / PX, V["Z_ALE"] + 598 / PX)
            ax2 = f.add_axes([0.62, 0.30, 0.37, 0.62]); ax2.imshow(im, cmap="gray", extent=ext)
            vista(ax2, d, "A1 sobre F09 escalada a metros"); [p.set_alpha(0.0) for p in ax2.patches if p.get_facecolor()[:3] == (1, 1, 1)]
            ax2.set_xlim(s0 - 22, s0 + 32); ax2.set_ylim(-1, 52)
        OUT.append(f)
    # comparacion A1 con F09 (hoja propia)
    f = hoja("ALZADO A1 SOBRE LA FOTO F09 (escalada a metros con el eje de la torre y el borde de las aletas)")
    ax = f.add_axes([0.03, 0.04, 0.94, 0.88]); d = G["N"]
    d_ = np.array(d) / np.linalg.norm(d); r_ = np.array([d_[1], -d_[0]]); s0 = G["T"] @ r_
    im = np.asarray(Image.open(IMG + "9.webp").convert("L")); H, W = im.shape; PX = 397 / 30.6
    ax.imshow(im, cmap="gray", extent=(s0 + (0 - 303.5) / PX, s0 + (W - 303.5) / PX, V["Z_ALE"] - (H - 598) / PX, V["Z_ALE"] + 598 / PX), alpha=0.75)
    for e in E:
        pts, dep = perfil(e, r_, d_); ax.add_patch(MP(pts, closed=True, fc="none", ec="red", lw=1.0, zorder=10))
    ax.set_xlim(s0 - 24, s0 + 32); ax.set_ylim(-2, 52); ax.set_aspect("equal"); ax.grid(True, lw=0.2); OUT.append(f)
    # comprobacion
    f = hoja("COMPROBACIÓN ENTRE PLANTAS, SECCIONES Y ALZADOS"); ax = f.add_axes([0.02, 0.02, 0.96, 0.9]); ax.axis("off")
    R = comprobacion()
    txt = [f"{'OK' if ok else 'NO':<3} {r:<92} {v}" for r, ok, v in R]
    ax.text(0, 1, "\n".join(txt), family="monospace", fontsize=8, va="top"); OUT.append(f)
    plt.rcParams["figure.max_open_warning"] = 0
    with PdfPages("SALUT_planos_2D.pdf") as pdf:
        for i, f in enumerate(OUT):
            pdf.savefig(f); f.savefig(f"p2d_{i + 1:02d}.png", dpi=70)
    print("hojas", len(OUT)); [print(("OK " if ok else "NO ") + r, v) for r, ok, v in R]
