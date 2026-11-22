"""Juego de planos del Hotel Salut (desde edificio.py, medidas de fotos):
7 plantas (0,1,2,3,4, ultima, aerea), 8 secciones (3 longitudinales), 5 alzados con su foto de comprobacion."""
import math, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image
from manifold3d import Manifold
import edificio as E
import lineas as L

IMG = '/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'
M = E.edificio()
BIG = 400.0
OUT = []


def hoja(titulo, w=16.5, h=11.7):
    fig = plt.figure(figsize=(w, h))
    fig.text(0.01, 0.985, "HOTEL SALUT (Kyiv, 1984) – " + titulo, fontsize=13, weight="bold", va="top")
    fig.text(0.01, 0.962, "Cotas en m. Medidas tomadas de fotos (F01, F09, F14, F47) y de Bing/Google. Trazo grueso con trama: cortado. "
             "Fino: visto. Discontinuo: por encima.", fontsize=8, va="top")
    return fig


def ejes(ax, xl, yl):
    ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect("equal")
    ax.tick_params(labelsize=6); ax.grid(True, lw=0.15, color="0.85")


# ======================================================================================= PLANTAS
def planta(ax, zc, titulo, aerea=False):
    if aerea:
        L.dibujar_vista(ax, M)
    else:
        abajo = M ^ Manifold.cube((BIG, BIG, zc)).translate((-BIG / 2, -BIG / 2, -1))
        arriba = M ^ Manifold.cube((BIG, BIG, 100)).translate((-BIG / 2, -BIG / 2, zc))
        L.dibujar_vista(ax, abajo)
        L.encima(ax, arriba)
        L.corte(ax, M.slice(zc))
    ax.set_title(titulo, fontsize=10, loc="left")


def cotas_planta(ax):
    pl = E.plantas_base()
    L.cota(ax, (0, E.L_L), (E.W_P, E.L_L), 2.5, "ala")
    L.cota(ax, (0, E.L_L - 20), (E.W_BAR, E.L_L - 20), 1.5, "bar")
    L.cota(ax, (E.W_P, pl["Q"][1]), (E.W_P, E.L_L), -5, "")
    L.cota(ax, (E.W_P, E.Y_CUNA), (E.W_P, E.L_L), -2.5, "")
    L.cota(ax, (E.W_P, E.L_L - E.L_FIN), (E.W_P, E.L_L), -1.0, "")
    L.cota(ax, E.A1, E.C, -3, "chaflán")
    L.cota(ax, (-E.L_C, 0), E.A1, -3, "calle")
    L.cota(ax, (-E.L_C, 0), (-E.L_C, E.W_C), 3, "")
    L.cota(ax, (E.W_P, E.C[1]), E.C, 2, "")


def plantas():
    lst = [(1.8, "PLANTA 0 (baja) – corte a +1,80"), (5.6, "PLANTA 1 – corte a +5,60 (bandas de ventanas)"),
           (9.2, "PLANTA 2 – corte a +9,20 (terraza, bar, bloque alto)"), (13.0, "PLANTA 3 – corte a +13,00 (cuello)"),
           (E.Z_B0 + 3 * E.F + 2.0, "PLANTA 4 – planta tipo de habitaciones (corte a +25,9)"),
           (E.Z_B1 + 2.5, "PLANTA ÚLTIMA – tambor de ojos y terraza de servicio (corte a +35,1)"), (None, "PLANTA AÉREA – cubiertas")]
    for zc, tit in lst:
        fig = hoja(tit)
        ax = fig.add_axes([0.04, 0.04, 0.6, 0.9])
        planta(ax, zc, "", aerea=zc is None)
        cotas_planta(ax)
        ejes(ax, (-30, 34), (-10, 100))
        ax.annotate("N aprox.", xy=(30, 96), xytext=(30, 88), arrowprops=dict(arrowstyle="-|>"), fontsize=7, ha="center")
        # detalle ampliado de la torre y el chaflan
        ax2 = fig.add_axes([0.66, 0.30, 0.33, 0.62])
        planta(ax2, zc, "detalle torre / chaflán", aerea=zc is None)
        ejes(ax2, (E.T[0] - 20, E.T[0] + 20), (E.T[1] - 18, E.T[1] + 22))
        fig.text(0.66, 0.25, "Datos de planta: ala larga 12,74 / bar 6,21 / tramo final 7,81 / concha hasta 35,13 del fondo\n"
                 "(Bing). Largo total 94,82 y ancho máx. 15,7 (Google). Chaflán: restaurante 12,8 + columna 6,5 + hotel 9,6 (F09).\n"
                 "Ángulo del chaflán 31° (tu esquema). Torre: eje sobre el chaflán; la columna asoma 1,5 m.", fontsize=7, va="top")
        OUT.append(fig)


# ======================================================================================= SECCIONES / ALZADOS
def orientar(m, p0=None, a_deg=0.0):
    """lleva la vista a 'mirar hacia -z': rota en z por -a (direccion de la linea -> +x), deja delante y<0,
    y gira -90 en x (z' = -y, y' = z)."""
    if p0 is not None:
        m = m.translate((-p0[0], -p0[1], 0))
    return m.rotate((0, 0, -a_deg)).rotate((-90, 0, 0))


def seccion(ax, p0, p1, titulo):
    a = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
    Lg = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    m = orientar(M, p0, a)
    mas_alla = m ^ Manifold.cube((BIG, 100, BIG)).translate((-BIG / 2, -50, -BIG))      # z' < 0  (y > 0)
    L.dibujar_vista(ax, mas_alla)
    L.corte(ax, m.slice(0.0))
    ax.axhline(0, color="k", lw=1.6)
    for z, t in ((E.Z_PB, "techo PB"), (E.Z_P1, "terraza / planta 1"), (E.Z_BAR, "bar"), (E.Z_ALTO, "bloque alto"),
                 (E.Z_B0, "1ª planta hab."), (E.Z_B1, "cubierta hab."), (E.Z_T1, "tambor"), (E.Z_V1, "visera"), (E.Z_R1, "remate")):
        L.nivel(ax, Lg + 1, z, t)
    ejes(ax, (-2, Lg + 12), (-2, 52))
    ax.set_title(titulo, fontsize=9, loc="left")


def alzado(ax, d, titulo):
    a = math.degrees(math.atan2(d[1], d[0])) - 90.0          # d -> +y
    m = M.rotate((0, 0, -a)).rotate((-90, 0, 0))
    L.dibujar_vista(ax, m)
    V = np.asarray(m.to_mesh().vert_properties)[:, :2]
    x0, x1 = V[:, 0].min(), V[:, 0].max()
    ax.axhline(0, color="k", lw=1.6)
    for z, t in ((E.Z_PB, "techo PB"), (E.Z_P1, "planta 1 / terraza"), (E.Z_ALTO, "bloque alto"), (E.Z_B0, "1ª hab."),
                 (E.Z_B1, "cub. hab."), (E.Z_T1, "tambor"), (E.Z_G1, "banda"), (E.Z_V1, "visera"), (E.Z_R1, "remate")):
        L.nivel(ax, x1 + 1, z, t)
    ejes(ax, (x0 - 2, x1 + 13), (-2, 52))
    ax.set_title(titulo, fontsize=9, loc="left")
    return x0, x1


def foto(ax, f, titulo):
    ax.imshow(Image.open(IMG + f).convert("RGB")); ax.axis("off"); ax.set_title(titulo, fontsize=8, loc="left")


SECC = [
    ("S1", (22, 26.0), (-8, 26.0), "transversal del ala larga por la escalera y el arranque de la concha (mirando hacia la torre)"),
    ("S2", (22, 45.0), (-8, 45.0), "transversal del ala larga por el bar, la terraza y la concha"),
    ("S3", (22, 75.0), (-8, 75.0), "transversal del ala larga por el bar y las ventanas"),
    ("S4", (22, 91.0), (-8, 91.0), "transversal del ala larga, tramo final sin bar"),
    ("S5", (-14.0, 20), (-14.0, -6), "transversal del ala corta: restaurante + bloque alto (mirando hacia la torre)"),
    ("L1", (3.1, 100), (3.1, -8), "LONGITUDINAL del ala larga por el bar (mirando hacia fuera)"),
    ("L2", (11.0, -8), (11.0, 100), "LONGITUDINAL del ala larga por la terraza (mirando hacia dentro)"),
    ("L3", (-28, E.T[1]), (32, E.T[1]), "LONGITUDINAL del ala corta por el eje de la torre"),
]


def secciones():
    # hoja de situacion
    fig = hoja("SITUACIÓN DE SECCIONES")
    ax = fig.add_axes([0.05, 0.04, 0.55, 0.9])
    planta(ax, None, "situación de las secciones", aerea=True)
    for k, p0, p1, _ in SECC:
        ax.plot(*zip(p0, p1), "-.", color="crimson", lw=1)
        ax.text(*p0, k, color="crimson", fontsize=10, weight="bold"); ax.text(*p1, k, color="crimson", fontsize=10, weight="bold")
    ejes(ax, (-32, 36), (-12, 102))
    OUT.append(fig)
    for grupo in (SECC[0:2], SECC[2:4], SECC[4:5], SECC[5:6], SECC[6:7], SECC[7:8]):
        fig = hoja("SECCIONES " + " / ".join(k for k, *_ in grupo))
        n = len(grupo)
        for i, (k, p0, p1, t) in enumerate(grupo):
            ax = fig.add_axes([0.04, 0.05 + (n - 1 - i) * 0.9 / n, 0.92, 0.85 / n])
            seccion(ax, p0, p1, f"SECCIÓN {k}: {t}")
        OUT.append(fig)


def alzados():
    lst = [((E.N[0], E.N[1]), "ALZADO 1 – CHAFLÁN (frontal)", [("9.webp", "F09"), ("14.webp", "F14")]),
           ((-1, 0), "ALZADO 2 – FACHADA EXTERIOR DEL ALA LARGA (con la concha)", [("47.webp", "F47"), ("24.webp", "F24")]),
           ((0, 1), "ALZADO 3 – CALLE (ala corta)", [("1.webp", "F01"), ("19.webp", "F19")]),
           ((1, 0), "ALZADO 4 – PATIO INTERIOR DE LA L", []),
           ((0, -1), "ALZADO 5 – TESTERO DEL ALA LARGA (hacia la torre)", [("13.webp", "F13"), ("12.png", "F12")])]
    for d, t, fotos in lst:
        fig = hoja(t)
        ax = fig.add_axes([0.04, 0.05, 0.62 if fotos else 0.92, 0.88])
        alzado(ax, d, t)
        for i, (f, nm) in enumerate(fotos):
            foto(fig.add_axes([0.68, 0.52 - i * 0.46, 0.31, 0.42]), f, f"comprobación: {nm}")
        if not fotos:
            fig.text(0.05, 0.02, "Sin foto del patio interior: alzado deducido de plantas y secciones.", fontsize=8)
        OUT.append(fig)




def detalles():
    """Detalles a escala: modulo del barril (seccion radial + alzado de 3 modulos) comparado con F04/F06,
    y chaflan (seccion por el hotel) comparado con F18."""
    fig = hoja("DETALLE 1 – MÓDULO DEL BARRIL: poyetes, entrantes, huecos y aletas")
    # seccion radial por el centro de un modulo
    a = 360 * 0.5 / E.N_AL + math.degrees(E.A_CH) - 90
    ang = math.radians(a)
    p0 = (E.T[0], E.T[1]); p1 = (E.T[0] + 20 * math.cos(ang), E.T[1] + 20 * math.sin(ang))
    ax = fig.add_axes([0.04, 0.06, 0.40, 0.86])
    seccion(ax, p0, p1, "sección radial por un módulo (izquierda = núcleo)")
    ejes(ax, (6, 17), (E.Z_B0 - 3, E.Z_B0 + 3 * E.F + 0.5))
    rf = E.R_B - 1.8
    for i in range(3):
        z = E.Z_B0 + i * E.F
        L.cota(ax, (E.R_B + 0.6, z), (E.R_B + 0.6, z + 0.45), 0.6, "forjado", fs=5.5)
        L.cota(ax, (E.R_B + 0.6, z + 0.75), (E.R_B + 0.6, z + 1.45), 0.6, "poyete", fs=5.5)
        L.cota(ax, (rf - 0.6, z + 1.25 if i else z + 1.1), (rf - 0.6, (z + 2.55) if i else z + 2.3), -0.6, "ventana" if i else "pavés", fs=5.5)
    L.cota(ax, (rf, E.Z_B0 + 3 * E.F + 0.3), (E.R_B, E.Z_B0 + 3 * E.F + 0.3), 0.4, "balcón", fs=6)
    L.cota(ax, (E.R_B, E.Z_B0 - 1.2), (E.R_AL, E.Z_B0 - 1.2), -0.4, "vuelo aleta", fs=6)
    L.cota(ax, (E.R_B - 0.25, E.Z_B0 + 0.45), (E.R_B - 0.25, E.Z_B0 + 0.75), -1.2, "ranura", fs=5.5)
    # alzado de 3 modulos
    ax2 = fig.add_axes([0.47, 0.06, 0.25, 0.86])
    m = M.rotate((0, 0, -(math.degrees(E.A_CH) - 0))).rotate((-90, 0, 0))
    L.dibujar_vista(ax2, m, res=0.02)
    ejes(ax2, (-6, 6), (E.Z_B0 - 3, E.Z_B0 + 3 * E.F + 0.5))
    ax2.set_title("alzado frontal de 3 módulos (aletas cada 360/19 = 18,9°)", fontsize=8, loc="left")
    foto(fig.add_axes([0.74, 0.52, 0.25, 0.40]), "4.webp", "comprobación F04: poyete alto, ranura, aletas")
    foto(fig.add_axes([0.74, 0.08, 0.25, 0.40]), "6.webp", "comprobación F06")
    OUT.append(fig)
    fig = hoja("DETALLE 2 – CHAFLÁN: planta baja hundida, banda volada, columna, esquina a 90°")
    pa = E.P(7.0, -12); pb = E.P(7.0, 12)
    ax = fig.add_axes([0.04, 0.06, 0.45, 0.86])
    seccion(ax, pa, pb, "sección por la banda del hotel, perpendicular al chaflán (izquierda = plaza)")
    ejes(ax, (4, 22), (-1, 18))
    yfr = 12 - (E.R_COL - E.RET)
    L.cota(ax, (yfr, -0.6), (yfr + E.RETR, -0.6), -0.4, "retranqueo PB", fs=6)
    L.cota(ax, (yfr - 0.6, 0), (yfr - 0.6, E.Z_PB), -0.4, "PB", fs=6)
    L.cota(ax, (yfr - 0.6, E.Z_PB), (yfr - 0.6, E.Z_P1), -0.4, "P1", fs=6)
    foto(fig.add_axes([0.52, 0.50, 0.46, 0.42]), "18.webp", "comprobación F18: banda volada sobre PB acristalada en sombra")
    foto(fig.add_axes([0.52, 0.06, 0.46, 0.40]), "47.webp", "comprobación F47: esquina del hotel y arranque de la concha")
    OUT.append(fig)


def coherencia():
    """comprobacion cruzada automatica: cada cota leida en las fotos frente a la medida en el modelo en varias vistas"""
    import salut_v2  # noqa: F401  (solo para garantizar que no se usa: el juego sale de edificio.py)
    filas = []
    def ancho_en(z, d):
        cs = M.slice(z); P = [np.array(p) for p in cs.to_polygons()]
        if not P: return 0
        a = np.vstack(P); dd = np.array(d) / np.linalg.norm(d); r = np.array([-dd[1], dd[0]])
        pr = a @ r; return pr.max() - pr.min()
    dch = (E.N[0], E.N[1])
    for nom, z, foto_v, fuente in [("barril con aletas", 24.0, 30.6, "F09"), ("tambor de ojos", 35.0, 27.1, "F09"),
                                   ("banda acristalada", 39.3, 21.7, "F09"), ("visera", 42.0, 25.6, "F09"),
                                   ("remate", 46.0, 11.2, "F09"), ("cuello", 12.5, 15.0, "F09")]:
        cs = M.slice(z); P = [np.array(p) for p in cs.to_polygons()]
        # diametro de la pieza circular alrededor de su centro: maximo alcance radial *2 desde el eje
        a = np.vstack(P); c = np.array(E.T)
        if nom in ("visera",): c = np.array(E.P(*E.OFF_V))
        if nom in ("remate",): c = np.array(E.P(*E.OFF_R))
        # excluir la caja de escalera (sector trasero, en linea con el ala larga) y el estilobato
        ce = np.array(E.T)
        ang = np.degrees(np.arctan2(a[:, 1] - ce[1], a[:, 0] - ce[0]))
        dir_esc = math.degrees(math.atan2(E.ESC_Y1 - E.T[1], (E.W_BAR / 2 + 0.5) - E.T[0]))
        lejos = np.abs((ang - dir_esc + 180) % 360 - 180) > 45
        dist = np.hypot(*(a - c).T)
        sel = lejos & (dist < 17.5)
        dm = 2 * np.percentile(dist[sel], 99.5)
        filas.append((nom, foto_v, dm, fuente))
    fig = hoja("COMPROBACIÓN CRUZADA – medidas de las fotos frente a los planos")
    ax = fig.add_axes([0.05, 0.1, 0.9, 0.8]); ax.axis("off")
    txt = ["Pieza                     foto (m)   planos (m)   dif.   fuente", "-" * 70]
    for n, fv, mv, s in filas:
        txt.append(f"{n:<25} {fv:>7.2f}   {mv:>9.2f}   {mv - fv:>+5.2f}   {s}")
    alt = [("techo PB", 3.9, E.Z_PB), ("planta 1 / terraza", 7.3, E.Z_P1), ("borde inferior barril", 15.2, E.Z_B0),
           ("cubierta habitaciones", 32.6, E.Z_B1), ("tambor", 38.2, E.Z_T1), ("banda", 40.5, E.Z_G1), ("visera", 43.7, E.Z_V1),
           ("remate", 49.1, E.Z_R1)]
    txt += ["", "Cota                      foto (m)   planos (m)   dif.", "-" * 70]
    for n, fv, mv in alt:
        txt.append(f"{n:<25} {fv:>7.2f}   {mv:>9.2f}   {mv - fv:>+5.2f}   F09/F14")
    pl = E.plantas_base()
    txt += ["", "Planta                    fuente (m)  planos (m)", "-" * 70,
            f"{'ala larga ancho':<25} {12.74:>7.2f}   {E.W_P:>9.2f}   Bing",
            f"{'bar ancho':<25} {6.21:>7.2f}   {E.W_BAR:>9.2f}   Bing",
            f"{'tramo final':<25} {7.81:>7.2f}   {E.L_FIN:>9.2f}   Bing",
            f"{'concha hasta el fondo':<25} {35.13:>7.2f}   {E.L_L - E.Y_CUNA:>9.2f}   Bing",
            f"{'chaflán (P1)':<25} {28.9:>7.2f}   {math.dist(E.A1, E.C):>9.2f}   F09 (12,8+6,5+9,6)",
            f"{'largo total':<25} {94.82:>7.2f}   {E.L_L:>9.2f}   Google",
            "", "Pendiente (no medible en fotos inclinadas): ángulo del chaflán (31°, de tu esquema) y fondo del ala corta (12 m)."]
    ax.text(0, 1, "\n".join(txt), family="monospace", fontsize=9, va="top")
    OUT.append(fig)


if __name__ == "__main__":
    plantas(); secciones(); alzados(); detalles(); coherencia()
    plt.rcParams['figure.max_open_warning'] = 0
    with PdfPages("SALUT_planos_desde_fotos.pdf") as pdf:
        for i, f in enumerate(OUT):
            pdf.savefig(f)
            f.savefig(f"lam_{i + 1:02d}.png", dpi=80)
    print("laminas:", len(OUT))
