"""Planimetria acotada del modelo (en metros reales): planta de cubiertas, secciones AA y BB, alzado del chaflan.
Las cotas llevan etiquetas para poder corregirlas por referencia."""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.backends.backend_pdf import PdfPages
from manifold3d import Manifold
import salut_v2 as s

# modelo en metros reales (sin escalar)
M = s.construir(escalar=False)

# transformacion solar -> torre (misma que en salut_v2.base_y_estilobato)
W_L, L_L, L_CH, D_REST, RET = 15.7, 94.8, 27.2, 14.6, 1.5
A_CH = math.radians(31)
A1 = np.array([W_L - L_CH * math.cos(A_CH), 0.0]); A2 = np.array([W_L, L_CH * math.sin(A_CH)])
ang = math.atan2(*(A2 - A1)[::-1]); u = np.array([math.cos(ang), math.sin(ang)]); n = np.array([-u[1], u[0]])
cen = A1 + D_REST * u + RET * n


def solar_a_torre(p):
    q = np.asarray(p, float) - cen
    return np.array([q @ u, q @ n])


# trabajar en coordenadas de solar: deshacer el giro de la torre
Ms = M.rotate((0, 0, math.degrees(ang))).translate((cen[0], cen[1], 0))

GRIS = lambda z: str(0.93 - 0.55 * min(z, 50) / 50)


def planta(ax):
    for z in np.arange(0.25, 15.3, 0.25):
        for poly in Ms.slice(z).to_polygons():
            ax.add_patch(Polygon(poly, closed=True, fc=GRIS(z * 3), ec="none"))
    for poly in Ms.slice(1.0).to_polygons():
        ax.add_patch(Polygon(poly, closed=True, fc="none", ec="k", lw=0.5, ls=":"))
    for z, ls in ((20.0, "--"), (36.0, "-.")):
        for poly in Ms.slice(z).to_polygons():
            ax.add_patch(Polygon(poly, closed=True, fc="none", ec="0.3", lw=0.6, ls=ls))
    base = Ms ^ Manifold.cube((400, 400, 15.2)).translate((-200, -200, 0))
    for poly in base.project().to_polygons():
        ax.add_patch(Polygon(poly, closed=True, fc="none", ec="k", lw=0.9))
    ax.set_aspect("equal"); ax.autoscale_view()


def cota(ax, p0, p1, txt, off=2.0, color="crimson"):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = p1 - p0; L = np.linalg.norm(d); t = d / L; nn = np.array([-t[1], t[0]]) * off
    a, b = p0 + nn, p1 + nn
    ax.plot(*zip(a, b), color=color, lw=0.8)
    for pp, qq in ((p0, a), (p1, b)):
        ax.plot(*zip(pp, qq + nn * 0.15), color=color, lw=0.4)
        ax.plot(*zip(qq - t * 0.4 - nn * 0.1, qq + t * 0.4 + nn * 0.1), color=color, lw=0.8)
    m = (a + b) / 2 + nn / max(np.linalg.norm(nn), 1e-9) * 1.0
    rot = math.degrees(math.atan2(t[1], t[0]))
    if rot > 90: rot -= 180
    if rot < -90: rot += 180
    ax.text(*m, f"{txt} = {L:.1f}".replace(".", ","), color=color, fontsize=7, ha="center", va="center", rotation=rot,
            bbox=dict(fc="white", ec="none", pad=0.5))


def altura(ax, p, z, tag):
    ax.text(p[0], p[1], f"{tag}\n+{z:.1f}".replace(".", ","), fontsize=6.5, ha="center", va="center", color="navy",
            bbox=dict(fc="white", ec="navy", lw=0.4, pad=0.8, alpha=0.85))


def techo(x, y):
    """altura de cubierta en un punto (x,y) solar, buscando el nivel mas alto que lo contiene"""
    from matplotlib.path import Path
    zt = 0.0
    for z in np.arange(0.25, 15.2, 0.25):
        if any(Path(p).contains_point((x, y)) for p in Ms.slice(z).to_polygons()):
            zt = z
    return zt


def seccion(ax, p0, p1, titulo):
    """seccion vertical por la linea p0-p1 (coords solar), vista con p0 a la izquierda"""
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = p1 - p0; L = np.linalg.norm(d); t = d / L
    a = math.degrees(math.atan2(t[1], t[0]))
    # llevar la linea al eje X y cortar por el plano y=0 -> girar 90 en X para que ese plano sea horizontal
    m = Ms.translate((-p0[0], -p0[1], 0)).rotate((0, 0, -a)).rotate((-90, 0, 0))
    cs = m.slice(0.0)
    for poly in cs.to_polygons():
        P = np.array(poly)
        ax.add_patch(Polygon(P, closed=True, fc="0.35", ec="k", lw=0.6))
    # vista mas alla del corte (proyeccion de lo que queda detras), en gris claro
    detras = m ^ Manifold.cube((400, 400, 300)).translate((-200, -200, 0.01))
    for poly in detras.project().to_polygons():
        ax.add_patch(Polygon(poly, closed=True, fc="0.88", ec="0.6", lw=0.3, zorder=0))
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xlim(-2, L + 2); ax.set_aspect("equal"); ax.autoscale_view()
    ax.set_title(titulo, fontsize=9, loc="left")


def main():
    with PdfPages("Hotel_Salut_planimetria.pdf") as pdf:
        # ---------------- PLANTA ----------------
        fig, ax = plt.subplots(figsize=(16.5, 11.7))
        planta(ax)
        cota(ax, (W_L, A2[1]), (W_L, L_L), "B1 largo ala", off=-6)
        cota(ax, (0, L_L), (W_L, L_L), "B2 ancho ala", off=-2.5)
        cota(ax, A1, A2, "C1 chaflan", off=4)
        cota(ax, (-24, 0), (A1[0], 0), "A1 frente calle ala corta", off=4)
        cota(ax, (-24, 0), (-24, 12), "A2 fondo ala corta", off=3)
        cota(ax, (0, 24), (0, L_L - 4), "B3 bar (largo)", off=6)
        Y_A, Y_T = A2[1] - 8, A2[1] + 38
        Y_V = Y_A + 0.45 * (Y_T - Y_A)
        cota(ax, (0, 50), (8.5, 50), "B4 ancho bar", off=2); cota(ax, (8.5, 55), (10.0, 55), "B7 voladizo", off=2)
        cota(ax, (W_L, Y_A + 2), (W_L, Y_A + 34), "B5 concha", off=-12)
        cota(ax, (W_L, Y_A + 2), (W_L + 4.5, Y_A + 2), "B6 ancho concha", off=-3)
        # alturas
        for tag, p in [("H1 restaurante", (-12, 2.5)), ("H2 bloque alto", (-12, 9)), ("H3 ladrillo", (-21.5, 6)),
                       ("H4 bar", (4, 60)), ("H5 terraza", (13, 60)), ("H8 banda hotel", tuple(cen + 9 * u - 0.2 * n))]:
            altura(ax, p, techo(*p), tag)
        c = cen
        ax.plot(*c, "k+", ms=10); ax.text(c[0] + 1, c[1] - 2, "eje torre", fontsize=7)
        ax.set_title("PLANTA DE CUBIERTAS DE LA BASE (m). Tono = altura. Torre: discontinua = barril, punto-raya = tambor/visera. Rojo: cotas; azul: alturas", fontsize=10, loc="left")
        ax.plot([A1[0] - 3, (A1 + 0.5 * (A2 - A1))[0]], [0, 0], alpha=0)
        ax.annotate("", xy=(30, 95), xytext=(30, 85), arrowprops=dict(arrowstyle="->"))
        ax.text(31, 90, "hacia el Dnipro", fontsize=7)
        # lineas de seccion
        SA = ((-12, -6), (-12, 18)); SB = ((-6, 30), (W_L + 10, 30))
        for (p, q), nm in ((SA, "A"), (SB, "B")):
            ax.plot(*zip(p, q), "k-.", lw=0.8)
            ax.text(*p, nm, fontsize=11, weight="bold"); ax.text(*q, nm, fontsize=11, weight="bold")
        ax.grid(True, lw=0.2); ax.set_xlabel("m"); ax.set_ylabel("m")
        pdf.savefig(fig); fig.savefig("Hotel_Salut_planta_acotada.png", dpi=110); plt.close(fig)
        # ---------------- SECCIONES ----------------
        fig, axs = plt.subplots(2, 1, figsize=(16.5, 11.7))
        seccion(axs[0], *SA, "SECCION A-A (ala de la calle; izquierda = calle)")
        seccion(axs[1], *SB, "SECCION B-B (ala larga por el bar y la terraza; izquierda = patio interior, derecha = concha)")
        for ax in axs:
            ax.grid(True, lw=0.2)
            ax.set_yticks(range(0, 52, 2)); ax.set_ylim(-1, 52)
        pdf.savefig(fig); fig.savefig("Hotel_Salut_secciones.png", dpi=110); plt.close(fig)
        # ---------------- ALZADO DEL CHAFLAN ----------------
        fig, ax = plt.subplots(figsize=(11.7, 16.5))
        m = M.rotate((-90, 0, 0))  # vista desde -Y (frente del chaflan) en coords de torre
        for poly in M.rotate((90, 0, 0)).project().to_polygons():
            P = np.array(poly); P[:, 1] = -P[:, 1]
            ax.add_patch(Polygon(P, closed=True, fc="0.85", ec="k", lw=0.4))
        ax.set_aspect("equal"); ax.autoscale_view(); ax.grid(True, lw=0.2)
        ax.set_yticks(range(0, 52, 2))
        ax.set_title("ALZADO DEL CHAFLAN (silueta, m). Eje x=0 = eje de la torre", fontsize=10, loc="left")
        pdf.savefig(fig); fig.savefig("Hotel_Salut_alzado_chaflan.png", dpi=90); plt.close(fig)


if __name__ == "__main__":
    main()
