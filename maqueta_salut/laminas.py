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
import ventanas as VT

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
        L.corte(ax, M.slice(zc), huecos=VT.cortados(zc))
        estructura_torre(ax, zc)
    ax.set_title(titulo, fontsize=10, loc="left")


def estructura_torre(ax, zc):
    """núcleo estructural (columna-núcleo de comunicaciones, muro 0,30) y particiones radiales entre habitaciones
    (0,20) en la dirección de cada aleta; solo en las plantas de habitaciones."""
    from matplotlib.patches import Circle, Polygon
    T = np.array(E.T)
    if zc < E.Z_CU0:
        return
    ax.add_patch(Circle(T, E.R_COL, fc="none", ec="k", lw=1.3, zorder=7))
    ax.add_patch(Circle(T, E.R_COL - VT.MURO, fc="white", ec="k", lw=1.0, zorder=7.5))
    from matplotlib.patches import Wedge
    ax.add_patch(Wedge(T, E.R_COL, 0, 360, width=VT.MURO, fc="#9a9a9a", ec="none", zorder=7.2))
    if not (E.Z_B0 < zc < E.Z_B1):
        return
    rf = E.R_B - 1.8; rc = E.R_COL + 2.2                         # pasillo anular de 2,2 m alrededor del núcleo
    ax.add_patch(Wedge(T, rc + VT.PART, 0, 360, width=VT.PART, fc="#bdbdbd", ec="k", lw=0.6, zorder=7.2))
    for k in range(E._v["N_AL"]):
        a = 2 * math.pi * k / E._v["N_AL"]; c, s_ = math.cos(a), math.sin(a); n_ = np.array([-s_, c]) * VT.PART / 2
        p0, p1 = T + rc * np.array([c, s_]), T + (rf - VT.MURO) * np.array([c, s_])
        ax.add_patch(Polygon([p0 - n_, p1 - n_, p1 + n_, p0 + n_], closed=True, fc="#bdbdbd", ec="k", lw=0.6, zorder=7.2))
    ax.text(*T, "núcleo", fontsize=6, ha="center", va="center", zorder=8)


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
    U = np.array(E.U); A1 = np.array(E.A1)
    k = E._k
    L.cota(ax, A1, A1 + (k - E.R_COL) * U, 5, "rest."); L.cota(ax, A1 + (k - E.R_COL) * U, A1 + (k + E.R_COL) * U, 5, "col.")
    L.cota(ax, A1 + (k + E.R_COL) * U, np.array(E.C), 5, "hotel")
    pv = np.array(E.P(0, 9.0)); ax.text(*pv, "vestíbulo /\ncirculaciones", fontsize=7, ha="center", va="center", style="italic", zorder=70,
                                        bbox=dict(fc="white", ec="0.5", lw=0.4, pad=1))
    xe = E._v["ESC_X"]; L.cota(ax, (xe - E.ESC_W / 2, E.ESC_Y1 + 1), (xe + E.ESC_W / 2, E.ESC_Y1 + 1), 1.2, "escalera")
    L.cota(ax, (0, E.ESC_Y0), (0, E.ESC_Y1), -1.2, "")
    ax.text(E.KC[0] + 1, 2, f"L {math.degrees(E.TH_L):.0f}°", fontsize=8, color="k")
    V_ = E._v; yA = E.L_L - V_["VEN_FIN"]
    L.cota(ax, (E.W_P, E.L_L), (E.W_P, yA), 7.0, "macizo", fs=5.5)
    L.cota(ax, (E.W_P, yA), (E.W_P, yA - V_["VEN_W"]), 7.0, "h", fs=5.5)
    L.cota(ax, (E.W_P, yA), (E.W_P, yA - V_["S_VEN"]), 8.5, "intereje", fs=5.5)
    ax.text(E.W_P + 10.5, yA - 6 * V_["S_VEN"], f"{int(V_['N_VEN'])} huecos a {V_['S_VEN']:.2f}\n(PB: los {int(V_['N_VEN_B'])} junto al testero)".replace(".", ","),
            fontsize=6, rotation=90, va="center")
    # cota de cubierta de cada volumen
    for (x, y), z in (((3, 70), E.Z_BAR_C), ((10, 70), E.Z_P1 + 1.0), ((tuple(E.SWP(-12, 9))), E.Z_ALTO), ((tuple(E.SWP(-21.5, 6))), E._v["Z_LAD1"]),
                      ((xe, (E.ESC_Y0 + E.ESC_Y1) / 2), E.Z_T1 + 1.0), ((14.2, 30), E._v["Z_CON"])):
        ax.text(x, y, f"+{z:.2f}".replace(".", ","), fontsize=6.5, color="navy", ha="center", bbox=dict(fc="white", ec="navy", lw=0.4, pad=0.6), zorder=70)
    # trazas de las secciones
    for k, p0, p1, _ in SECC:
        ax.plot(*zip(p0, p1), "-.", color="crimson", lw=0.7, zorder=65)
        ax.text(*p0, k, color="crimson", fontsize=8, weight="bold", zorder=66); ax.text(*p1, k, color="crimson", fontsize=8, weight="bold", zorder=66)


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
        fig.text(0.66, 0.25, f"Datos de planta: ala larga 12,74 / bar 6,21 (Bing) / bar 1984 hasta el hueco 11: tramo final {E.L_FIN:.2f} (F01, F47; Bing actual 7,81) / concha hasta {E.L_L - E._v['Y_CA']:.2f} del fondo (F73; Bing 35,13).\n"
                 f"Largo total 94,82 (Google). Esquina original a 90° con chaflán de {E.L_CH:.1f} m a {math.degrees(E.A_CH):.0f}°.\n"
                 f"Torre sobre el chaflán al {E._v['T_POS']*100:.0f} % desde la calle (algo a la derecha); la columna asoma 1,5 m.\n"
                 f"Detrás de la torre: vestíbulo y circulaciones. Escalera en el patio: {E.ESC_W:.1f} × {E._v['ESC_WY']:.1f} m (F36, F62, F73, F08, F11).", fontsize=7, va="top")
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
    cs = m.slice(0.0)
    L.corte(ax, cs, huecos=huecos_seccion(p0, p1))
    forjados_seccion(ax, cs)
    nucleo_seccion(ax, p0, p1)
    ax.axhline(0, color="k", lw=1.6)
    for z, t in ((E.Z_PB, "techo PB"), (E.Z_P1, "terraza / planta 1"), (E.Z_BAR, "bar"), (E.Z_ALTO, "bloque alto"),
                 (E.Z_B0, "1ª planta hab."), (E.Z_B1, "cubierta hab."), (E.Z_T1, "tambor"), (E.Z_V1, "visera"), (E.Z_R1, "remate")):
        L.nivel(ax, Lg + 1, z, t)
    cruces(ax, p0, p1, titulo.split(':')[0].replace('SECCIÓN ', '').strip())
    ejes(ax, (-2, Lg + 12), (-2, 53))
    ax.set_title(titulo, fontsize=9, loc="left")


def forjados_seccion(ax, cs):
    """forjados de 0,30 dentro de cada recinto cortado: techo de PB en la base y cada planta del barril"""
    from matplotlib.patches import Polygon
    from shapely.geometry import Polygon as SP, box
    niveles = [E.Z_PB] + [E.Z_B0 + i * E.F for i in range(1, E._v["N_PL"])]
    for P in cs.to_polygons():
        sp = SP(np.array(P)).buffer(0)
        if sp.is_empty: continue
        inn = sp.buffer(-VT.MURO)
        if inn.is_empty: continue
        x0, z0, x1, z1 = inn.bounds
        for zl in niveles:
            if not (z0 + 0.5 < zl < z1 - 0.5): continue
            g = inn.intersection(box(x0 - 1, zl - VT.MURO, x1 + 1, zl))
            for gm in getattr(g, "geoms", [g]):
                if gm.geom_type == "Polygon" and not gm.is_empty and gm.area > 0.3:
                    ax.add_patch(Polygon(np.array(gm.exterior.coords), closed=True, fc="#9a9a9a", ec="k", lw=0.9, zorder=6))


def nucleo_seccion(ax, p0, p1):
    """muros del núcleo estructural de la torre (R_COL, 0,30) donde la sección lo corta: suelo → cubierta de habitaciones"""
    from matplotlib.patches import Rectangle
    p0, p1 = np.array(p0, float), np.array(p1, float); d = p1 - p0; Lg = np.linalg.norm(d); tl = d / Lg
    T = np.array(E.T); q = T - p0; sc = q @ tl; dist = abs(q[0] * tl[1] - q[1] * tl[0])
    for R in (E.R_COL, E.R_COL - VT.MURO):
        pass
    if dist >= E.R_COL - 0.05: return
    h = math.sqrt(E.R_COL ** 2 - dist ** 2)
    for sg in (-1, 1):
        x = sc + sg * h
        ax.add_patch(Rectangle((x - (VT.MURO if sg > 0 else 0), 0), VT.MURO, E.Z_B1, fc="#9a9a9a", ec="k", lw=0.9, zorder=6.5))
    ax.text(sc, E.Z_B0 + 1.5 * E.F, "núcleo", fontsize=6, ha="center", rotation=90, zorder=7)


def huecos_seccion(p0, p1):
    """huecos del catálogo que corta el plano vertical p0→p1, en coordenadas de la sección (s, z)"""
    p0, p1 = np.array(p0, float), np.array(p1, float); d = p1 - p0; Lg = np.linalg.norm(d); tl = d / Lg
    out = []
    for h in VT.catalogo():
        p, t, n = np.array(h["p"]), np.array(h["t"]), np.array(h["n"])
        den = tl[0] * t[1] - tl[1] * t[0]
        if abs(den) < 1e-6: continue
        s = ((p[0] - p0[0]) * t[1] - (p[1] - p0[1]) * t[0]) / den
        u = ((p[0] - p0[0]) * tl[1] - (p[1] - p0[1]) * tl[0]) / den
        if 0 <= s <= Lg and abs(u) <= h["w"] / 2:
            sg = 1.0 if np.dot(n, tl) > 0 else -1.0
            out.append(dict(p=(s, (h["z0"] + h["z1"]) / 2), t=(0.0, 1.0), n=(sg, 0.0), w=h["z1"] - h["z0"], e=h["e"],
                            tipo="ventana" if h["tipo"] != "puerta" else "puerta_sec"))
    return out


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


def _secc():
    T = np.array(E.T); U = np.array(E.U); N = np.array(E.N); pl = E.plantas_base()
    xe = E._v["ESC_X"]; yc = (E.ESC_Y0 + E.ESC_Y1) / 2
    return [
     ("L1", (xe, -10), (xe, 100), "LONGITUDINAL por el eje de la escalera: escalera, barril, cuello, bar y ala larga entera"),
     ("L2", ((E.W_P + E.W_EXT) / 2, pl["Q"][1] - 6), ((E.W_P + E.W_EXT) / 2, 100), "LONGITUDINAL por la concha: su perfil curvo y la terraza detrás"),
     ("L3", tuple(T - 32 * U), tuple(T + 26 * U), "LONGITUDINAL por el eje de la torre paralela al chaflán: restaurante, columna, hotel y esquina a 90°"),
     ("S1", tuple(T - 18 * N), tuple(T + 32 * N), "por el eje de la torre perpendicular al chaflán: columna, cuello, ménsulas, barril, visera desplazada y escalera"),
     ("S2", (-8, yc), (24, yc), "transversal del ala larga por la escalera (encuentro escalera – barril – ala)"),
     ("S3", (-8, (pl["Q"][1] + E.Y_CUNA) / 2), (24, (pl["Q"][1] + E.Y_CUNA) / 2), "transversal del ala larga por el bar, la terraza y la concha"),
     ("S4", (-8, E.L_L - E._v["VEN_FIN"] - E._v["S_VEN"] - E._v["VEN_W"] / 2), (24, E.L_L - E._v["VEN_FIN"] - E._v["S_VEN"] - E._v["VEN_W"] / 2), "transversal del ala larga por el eje del hueco 2 (tramo final sin bar): huecos alto y bajo cortados"),
     ("S5", tuple(E.SWP(-14, -6)), tuple(E.SWP(-14, 18)), "transversal del ala corta: banda del restaurante, bloque alto y patio"),
    ]


SECC = _secc()


def cruces(ax, p0, p1, k0, ytop=50):
    """marca en la seccion k0 donde la cortan las demas secciones (relacion entre secciones)"""
    p0, p1 = np.array(p0, float), np.array(p1, float); d = p1 - p0; L_ = np.linalg.norm(d); t = d / L_
    for k, q0, q1, _ in SECC:
        if k == k0: continue
        q0, q1 = np.array(q0, float), np.array(q1, float); e = q1 - q0
        den = t[0] * e[1] - t[1] * e[0]
        if abs(den) < 1e-6: continue
        s = ((q0[0] - p0[0]) * e[1] - (q0[1] - p0[1]) * e[0]) / den
        u = ((q0[0] - p0[0]) * t[1] - (q0[1] - p0[1]) * t[0]) / den
        if 0 <= s <= L_ and 0 <= u <= 1:
            ax.plot([s, s], [-1, ytop], color="crimson", lw=0.7, ls="-.", zorder=60)
            ax.text(s, ytop + 0.5, k, color="crimson", fontsize=8, weight="bold", ha="center", zorder=60)



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
    for grupo in [[s] for s in SECC]:
        fig = hoja("SECCIONES " + " / ".join(k for k, *_ in grupo))
        n = len(grupo)
        for i, (k, p0, p1, t) in enumerate(grupo):
            ax = fig.add_axes([0.04, 0.05 + (n - 1 - i) * 0.9 / n, 0.92, 0.85 / n])
            seccion(ax, p0, p1, f"SECCIÓN {k}: {t}")
        OUT.append(fig)


def alzados():
    V = E._v
    lst = [((E.N[0], E.N[1]), "ALZADO 1 – CHAFLÁN (frontal)",
            [("9.webp", "F09"), ("14.webp", "F14"), ("70.webp", "F70"), ("71.webp", "F71")],
            [f"PB {V['Z_PB']} / base {V['Z_P1']}: F09 7,3 · F14 7,2 · F70 6,5 (rango 7,1±0,3)",
             f"rampa: peto arriba +{V['Z_CON'] + 1:.1f}: F09 8,3±0,8 · F71 9,6±1,2"]),
           ((-1, 0), "ALZADO 2 – FACHADA EXTERIOR DEL ALA LARGA (con la rampa)",
            [("73.webp", "F73 (desde el testero)"), ("71.webp", "F71"), ("76.webp", "F76 maqueta (orient.)"), ("47.webp", "F47")],
            [f"huecos: {V['N_VEN']} arriba y {V['N_VEN_B']} abajo (bajo los {V['N_VEN_B']} junto al testero), intereje {V['S_VEN']}, hueco {V['VEN_W']} (F73, F01, F47 + tu recuento)",
             f"alturas: fila alta {V['VA_0']}–{V['VA_1']}, baja {V['VB_0']}–{V['VB_1']} (verticales exactas en F73); marco que sale {V['MAR_P']}, vidrio {V['MAR_R']} adentro",
             f"rampa 1 al nivel de la terraza: meseta a +{V['Z_CON']} y pendiente hasta el suelo; arco debajo (F71, F73, F47, F76)",
             f"rampa 2 a la azotea del bar: +{V['Z_P1']} → +{V['Z_BARC']} en {V['R2_L']} m junto a la torre, arco de paso en su llegada, barandilla roja (F71, F73, F76)",
             f"bar 1984: acaba sobre el hueco 11 ({V['L_FIN']} m del testero) (F01, F47); peto +{V['Z_P1'] + V['H_PET']:.1f}; testero +{V['Z_FIN']}"]),
           ((0, 1), "ALZADO 3 – CALLE (ala corta)", [("1.webp", "F01"), ("19.webp", "F19"), ("72.webp", "F72")], []),
           ((1, 0), "ALZADO 4 – PATIO INTERIOR DE LA L", [("75.png", "F75 (escalera desde el patio)")], []),
           ((0, -1), "ALZADO 5 – TESTERO DEL ALA LARGA (hacia la torre)",
            [("73.webp", "F73"), ("13.webp", "F13"), ("12.png", "F12")],
            [f"testero +{V['Z_FIN']} con barandilla, puerta de servicio con marquesina y ventana encima (F73)",
             f"F73 es ACTUAL: lo que asoma tras el testero a ≈ +11 es el bar ampliado después; en 1984 (F01, F47) el bar acaba a {V['L_FIN']} m del testero",
             f"caja de escalera: lado corto {V['ESC_W']} m visto desde aquí (F73), sale {V['ESC_L']} m del barril, entrante hacia el patio (F75, F13)"])]
    for d, t, fotos, notas in lst:
        fig = hoja(t)
        ax = fig.add_axes([0.04, 0.16, 0.58, 0.78])
        alzado(ax, d, t)
        for i, (f, nm) in enumerate(fotos):
            c, r = i % 2, i // 2
            foto(fig.add_axes([0.63 + c * 0.185, 0.50 - r * 0.46, 0.18, 0.42]), f, f"comprobación: {nm}")
        for j, n in enumerate(notas):
            fig.text(0.05, 0.12 - j * 0.022, "• " + n.replace(".", ","), fontsize=7.5)
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
    a_ = math.degrees(math.atan2(E.N[1], E.N[0])) - 90.0
    m = M.rotate((0, 0, -a_)).rotate((-90, 0, 0))
    tx = E.T[0] * math.cos(math.radians(-a_)) - E.T[1] * math.sin(math.radians(-a_))
    L.dibujar_vista(ax2, m, res=0.02)
    ejes(ax2, (tx - 6, tx + 6), (E.Z_B0 - 3, E.Z_B0 + 3 * E.F + 0.5))
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
        dir_esc = math.degrees(math.atan2(E.ESC_Y1 - E.T[1], E._v["ESC_X"] - E.T[0]))
        lejos = np.abs((ang - dir_esc + 180) % 360 - 180) > 45
        dist = np.hypot(*(a - c).T)
        sel = lejos & (dist < 17.5)
        if not sel.any(): sel = dist < 17.5
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
            f"{'tramo final (1984)':<25} {37.74:>7.2f}   {E.L_FIN:>9.2f}   F01/F47 (Bing actual 7,81)",
            f"{'concha hasta el fondo':<25} {35.13:>7.2f}   {E.L_L - E.Y_CUNA:>9.2f}   Bing",
            f"{'chaflán (P1)':<25} {28.9:>7.2f}   {math.dist(E.A1, E.C):>9.2f}   F09 (12,8+6,5+9,6)",
            f"{'largo total':<25} {94.82:>7.2f}   {E.L_L:>9.2f}   Google",
            "", "Pendiente (no medible en fotos inclinadas): ángulo del chaflán (31°, de tu esquema) y fondo del ala corta (12 m)."]
    ax.text(0, 1, "\n".join(txt), family="monospace", fontsize=9, va="top")
    OUT.append(fig)


def cuadro_cotas():
    import cotas as K
    fig = hoja("CUADRO DE COTAS (fuente única) con márgenes")
    ax = fig.add_axes([0.01, 0.02, 0.98, 0.93]); ax.axis("off")
    filas = []
    for k, (v, d, src) in K.COTAS.items():
        r = K.RANGOS.get(k, None); rr = "—" if r in (None, 0) else f"± {r}"
        filas.append(f"{k:<7} {v:>8} {rr:>7}   {d[:60]:<60} {src[:70]}")
    h = (len(filas) + 1) // 2
    ax.text(0, 1, "\n".join(filas[:h]), family="monospace", fontsize=5.6, va="top")
    ax.text(0.5, 1, "\n".join(filas[h:]), family="monospace", fontsize=5.6, va="top")
    OUT.insert(0, fig)


if __name__ == "__main__":
    plantas(); secciones(); alzados(); detalles(); coherencia(); cuadro_cotas()
    plt.rcParams['figure.max_open_warning'] = 0
    with PdfPages("SALUT_planos_definitivos.pdf") as pdf:
        for i, f in enumerate(OUT):
            pdf.savefig(f)
            f.savefig(f"lam_{i + 1:02d}.png", dpi=80)
    print("laminas:", len(OUT))
