"""Juego de planos del Hotel Salut (desde edificio.py, medidas de fotos):
7 plantas (0,1,2,3,4, ultima, aerea), 8 secciones (3 longitudinales), 5 alzados con su foto de comprobacion."""
import traduccion  # textos de los planos en ucraniano (usuario 26/11)
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


_OCL = {}


def ocluyente_torre():
    """huella en planta de todo lo que está por encima del fondo del barril (Z_BI): en las cubiertas y en las plantas del barril
    TAPA lo que queda debajo (cubierta inclinada del restaurante, rampa, rótulos) [usuario 27/11: la rampa se veía por encima]"""
    if "g" not in _OCL:
        from shapely.geometry import Polygon as _SP
        from shapely.ops import unary_union as _uu
        top = M.trim_by_plane((0, 0, 1), E._v["Z_BI"] - 0.05)
        _OCL["g"] = _uu([_SP(p).buffer(0) for p in top.project().to_polygons() if len(p) > 2]).buffer(0.02)
    return _OCL["g"]


def oculta(zc):
    """ocluyente si el barril tapa lo de debajo (vista aérea o corte por encima de su fondo); None si queda por encima del corte"""
    return ocluyente_torre() if (zc is None or zc >= E._v["Z_BI"]) else None


def _visibles(geom, ocl):
    from shapely.geometry import Polygon as _SP, LineString as _LS
    g = geom if ocl is None else geom.difference(ocl)
    return [x for x in getattr(g, "geoms", [g]) if not x.is_empty and x.geom_type in ("Polygon", "LineString")]
BIG = 400.0
OUT = []


def hoja(titulo, w=16.5, h=11.7):
    fig = plt.figure(figsize=(w, h))
    fig.text(0.01, 0.985, "HOTEL SALUT (Kyiv, 1984) – " + titulo, fontsize=13, weight="bold", va="top")
    fig.text(0.01, 0.962, "Cotas en m. Medidas de fotos (F01, F08, F09, F14, F36, F47, F58, F70–F73…, ver CUADRO DE COTAS) y de Bing/Google. Trazo grueso con trama: cortado. "
             "Fino: visto. Discontinuo: por encima.", fontsize=8, va="top")
    return fig


def ejes(ax, xl, yl):
    ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect("equal")
    ax.tick_params(labelsize=6); ax.grid(True, lw=0.15, color="0.85")


# ======================================================================================= PLANTAS
def planta(ax, zc, titulo, aerea=False):
    if aerea:
        L.vista_vectorial(ax, M)
    else:
        abajo = M ^ Manifold.cube((BIG, BIG, zc)).translate((-BIG / 2, -BIG / 2, -1))
        arriba = M ^ Manifold.cube((BIG, BIG, 100)).translate((-BIG / 2, -BIG / 2, zc))
        L.vista_vectorial(ax, abajo, ztop=zc)
        L.encima(ax, arriba)
        for zn in (E._v["Z_VOL0"] + 0.3, E.Z_P1 + 0.5, E.Z_ALTO - 0.5):        # contornos interiores de lo que hay encima
            if zn > zc + 0.3:
                for P in M.slice(zn).to_polygons():
                    P = np.array(P)
                    if len(P) > 2 and abs(np.dot(P[:, 0], np.roll(P[:, 1], -1)) - np.dot(P[:, 1], np.roll(P[:, 0], -1))) / 2 > 2.0:
                        ax.plot(*np.vstack([P, P[:1]]).T, color="0.3", lw=0.6, ls=(0, (5, 3)), zorder=4)
        L.corte(ax, M.slice(zc), huecos=VT.cortados(zc))
        estructura_torre(ax, zc)
        proyecciones_planta(ax, zc)
        # sin interiores inventados: solo lo que sale de fotos (usuario, 26/11)
    if (not aerea) and E.Z_P1 < zc < E._v["Z_BI"]:      # lucernarios piramidales bajo el cuello (solo se ven en las plantas bajo el barril) [F78]
        from matplotlib.patches import Polygon as _Pg
        LS = E.lucernarios_cuello()
        for L_ in LS:
            u = np.array([math.cos(L_["a"]), math.sin(L_["a"])]); v = np.array([-u[1], u[0]]); c = np.array(L_["c"]); h = L_["l"] / 2
            q = [c + u * h + v * h, c - u * h + v * h, c - u * h - v * h, c + u * h - v * h]
            ax.add_patch(_Pg(q, closed=True, fc="white", ec="k", lw=0.5, zorder=6.4))
            for qq in q: ax.plot(*zip(c, qq), color="k", lw=0.3, zorder=6.45)
        if LS:
            c = np.array(LS[len(LS) // 2]["c"]); d = c - np.array(E.T); d /= np.linalg.norm(d)
            ax.annotate("lucernarios piramidales\n(vidrio, +7,20 → +8,70)", c, c + d * 6, fontsize=4.5, ha="center", zorder=9,
                        arrowprops=dict(arrowstyle="-", lw=0.3, color="0.3"))
    mascara_rampas(ax, None if aerea else zc)
    recorridos(ax, None if aerea else zc)
    for tx in ax.texts: tx.set_clip_on(True)           # ningún rótulo fuera de su planta
    ax.set_title(titulo, fontsize=10, loc="left")



def mascara_rampas(ax, zc=None, zb=3.5):
    """Ching: una rampa o una cubierta inclinada se dibuja en planta con su CONTORNO y la flecha de subida (grafismo.rampas),
    nunca con las curvas de nivel de la malla (parecían peldaños). Tapa esas líneas en la parte VISTA (por debajo del corte)
    y redibuja contorno y peto. zc = cota del corte (None = cubiertas / vista aérea)."""
    from matplotlib.patches import Rectangle
    V_ = E._v; pl = E.plantas_base()
    y0 = pl["Q"][1] + V_["D_HOTF"]; YB = E.Y_CUNA; LR = YB - y0
    if zc is None or zc >= V_["Z_CON"]: ya = y0
    elif zc <= 0: ya = None
    else: ya = y0 + LR * (1 - zc / V_["Z_CON"]) ** (1 / V_["RAMPA_P"])
    from shapely.geometry import Polygon as _SP, LineString as _LS
    ocl = oculta(zc)

    def _rect(x0, y0_, w, h):
        for g in _visibles(_SP([(x0, y0_), (x0 + w, y0_), (x0 + w, y0_ + h), (x0, y0_ + h)]), ocl):
            if g.geom_type == "Polygon": ax.add_patch(plt.Polygon(np.c_[g.exterior.xy], closed=True, fc="white", ec="none", zorder=zb))

    def _lin(xs, ys, **k):
        for g in _visibles(_LS(list(zip(xs, ys))), ocl):
            if g.geom_type == "LineString" and g.length > 0.05: ax.plot(*g.xy, **k)
    if ya is not None:                                            # 1) rampa de acceso (concha)
        x0, x1 = E.W_P, E.W_EXT
        _rect(x0 + 0.02, ya, x1 - x0 - 0.04, YB - ya)
        _lin([x0, x1, x1, x0, x0], [ya, ya, YB, YB, ya], color="k", lw=0.45, zorder=zb + 0.1)
        _lin([x1 - 0.25, x1 - 0.25], [ya, YB], color="k", lw=0.35, zorder=zb + 0.1)                 # peto
        if zc is not None and ya > y0 + 0.2:                       # línea de corte de la rampa (Ching: quiebro en diagonal)
            _lin([x0, x1], [ya - 0.6, ya + 0.6], color="k", lw=0.5, zorder=zb + 0.2)
    yb0 = pl["Q"][1] + V_["R2_Y0"]; yr1 = yb0 + V_["R2_L"]; WB = E.W_BAR + V_["V_BAR"]
    if zc is None or zc >= E.Z_BAR_C: yt = yr1
    elif zc <= E.Z_P1: yt = None
    else: yt = yb0 + (zc - E.Z_P1) / (E.Z_BAR_C - E.Z_P1) * (yr1 - yb0)
    if yt is not None:                                            # 2) techo inclinado del restaurante (la parte bajo el barril, oculta)
        _rect(0.02, yb0, WB - 0.04, yt - yb0)
        _lin([0, WB, WB, 0, 0], [yb0, yb0, yt, yt, yb0], color="k", lw=0.45, zorder=zb + 0.1)


def proyecciones_planta(ax, zc):
    """proyección (trazo largo) de lo que está por encima del corte: las 19 ménsulas/vigas radiales bajo el barril
    (de R_CU a R_AL, ancho 0,40), el borde del barril y de las aletas, la losa volada del cuello, y en las plantas
    de la torre la banda, la visera y el remate desplazados"""
    from matplotlib.patches import Circle, Polygon as Pg
    if zc is None: return
    T = np.array(E.T); LS = (0, (6, 3)); V = E._v
    def circ(c, r, t=None):
        ax.add_patch(Circle(tuple(c), r, fill=False, ec="0.25", lw=0.4, ls=LS, zorder=4.2))
    if zc < E.Z_CU1:
        for k in range(V["N_AL"]):
            a = 2 * math.pi * k / V["N_AL"] + E.FASE_AL; u = np.array([math.cos(a), math.sin(a)]); w = np.array([-u[1], u[0]]) * 0.2
            ax.add_patch(Pg([T + u * E.R_CU - w, T + u * E.R_AL - w, T + u * E.R_AL + w, T + u * E.R_CU + w], closed=True, fill=False,
                            ec="0.25", lw=0.4, ls=LS, zorder=4.2))
        circ(T, E.R_AL); circ(T, E.R_B)
        if zc < E.Z_CU0: circ(T, E.R_CU + 0.6); circ(T, E.R_CU)
        ax.text(*(T + np.array([0, -(E.R_AL + 1.0)])), "vigas radiales (ménsulas) y barril por encima", fontsize=4.2, ha="center", style="italic", zorder=9)
    if zc < E.Z_T1:
        circ(E.P(*E.OFF_B), E.R_G); circ(E.P(*E.OFF_V), E.R_V); circ(E.P(*E.OFF_R), E.R_R)

def recorridos(ax, zc=None):
    """grafismo de arquitectura: rampas, escalera, proyecciones y cotas de nivel (grafismo.py)"""
    import grafismo as G
    G.dibujar(ax, zc)
    V = E._v
    G.cota_nivel(ax, (9.6, (E.L_L - V["L_FIN"] + E.T[1] + V["ESC_R1"] + V["R2_L"]) / 2), V["Z_P1"])
    ax.text(9.6, (E.L_L - V["L_FIN"] + E.T[1] + V["ESC_R1"] + V["R2_L"]) / 2 - 8, "terraza-restaurante", fontsize=4.8, rotation=90,
            ha="center", va="center", style="italic", zorder=80)
    G.cota_nivel(ax, (E.W_EXT + 3.5, E.Y_CUNA + 4), 0.0)


def estructura_torre(ax, zc):
    """núcleo estructural (columna-núcleo de comunicaciones, muro 0,30) y particiones radiales entre habitaciones
    (0,20) en la dirección de cada aleta; solo en las plantas de habitaciones."""
    from matplotlib.patches import Circle, Polygon
    T = np.array(E.T)
    da_esc = E.ESC_HA + 0.02
    # muros de carga de la escalera dentro del edificio: dos muros paralelos hacia el centro + testero interior
    if E._v["ESC_Z0"] < zc < E._v["ESC_Z1"]:     # escalera: cuerpo en cuña (muros 0,30) forrado de lamas; arriba solo el muro
        def sec(r0, r1, d0, d1, n=12):
            return [E.esc_ang_pt(r1, d0 + (d1 - d0) * k / n) for k in range(n + 1)] + [E.esc_ang_pt(r0, d1 - (d1 - d0) * k / n) for k in range(n + 1)]
        HB, mw = E.ESC_HB, math.atan2(VT.MURO, E.ESC_RC)
        for d0, d1 in (((-HB, -HB + mw), (HB - mw, HB)) if zc < E.Z_T1 else ()):
            ax.add_patch(Polygon(sec(E.ESC_R0, E.ESC_RC, d0, d1), closed=True, fc="white", ec="k", hatch="////", lw=1.0, zorder=7.3))
        for r0 in ((E.ESC_R0, E.ESC_RC - VT.MURO) if zc < E.Z_T1 else ()):
            ax.add_patch(Polygon(sec(r0, r0 + VT.MURO, -HB, HB), closed=True, fc="white", ec="k", hatch="////", lw=1.0, zorder=7.3))
        if zc > E.Z_T1:                                   # por encima del tambor: solo el muro de coronación inclinada [dron, usuario]
            ax.add_patch(Polygon(sec(E._v["ESC_RS"], E.ESC_R1 + 0.3, -HB, -HB + 0.3 / E._v["ESC_RS"]), closed=True, fc="white", ec="k", hatch="////", lw=1.0, zorder=7.4))
        if E._v["ESC_Z0"] < zc < E._v["ESC_ZL"]:
            nl = int(E._v["LAMA_N"]) - 1
            for k in range(nl + 1):
                da = -HB + 2 * HB * k / nl
                ax.plot(*zip(E.esc_ang_pt(E.ESC_R1 - 0.5, da), E.esc_ang_pt(E.ESC_R1, da)), color="k", lw=1.6, zorder=7.3)
            for sg in (-1, 1):
                r = E.R_B - 1.6
                while r < E.ESC_R1 - 0.3:
                    da = sg * (HB + math.atan2(0.45, r)); p = np.array(E.esc_ang_pt(r, da)); d = np.array(E.esc_ang_pt(r + 0.01, da)) - p
                    d = d / np.linalg.norm(d); nn = np.array([-d[1], d[0]])
                    ax.plot(*zip(p - nn * 0.125, p + nn * 0.125), color="k", lw=1.0, zorder=7.3); r += E._v["LAMA_P"]
            if E.Z_B0 < zc < E.Z_T1:                       # borde derecho del corte del barril cerrado con lamas [fotos 25/11]
                r = E._v["ESC_RR"] + 0.2
                while r < E.R_B:
                    da = E.ESC_HA - math.atan2(0.2, r); p = np.array(E.esc_ang_pt(r, da))
                    ax.plot(*zip(p - 0.04 * (p - np.array(E.T)) / r, p + 0.04 * (p - np.array(E.T)) / r), color="k", lw=1.0, zorder=7.3); r += E._v["LAMA_P"]
            if zc < E.Z_T1:
                ax.text(*E.esc_ang_pt((E.ESC_R0 + E.ESC_RC) / 2, 0), "escalera", fontsize=6, ha="center", rotation=math.degrees(E.ESC_ANG) - 90, zorder=8)
        if zc > E.Z_T1:
            ax.text(*E.esc_ang_pt((E._v["ESC_RS"] + E.ESC_R1) / 2, -HB + 0.12), f"muro de coronación inclinada +{E._v['ESC_ZI']:.2f} → +{E._v['ESC_Z1']:.2f}".replace(".", ","),
                    fontsize=4.5, ha="center", rotation=math.degrees(E.ESC_ANG - HB) - 90, zorder=8)
    # PLANTAS DE HABITACIONES (usuario 26/11, supuesto razonado, solo en planos): núcleo central de muro NUC_E, pasillo anular de PAS_A,
    # tabique TAB_E y muros radiales PAR_E en el eje de cada aleta hasta la fachada de ventanas (RF); en el sector de la escalera,
    # el pasillo se abre al rellano
    V_ = E._v
    if not (E.Z_B0 + 0.3 < zc < E.Z_B1): return
    def anillo(r0, r1, d0=None, d1=None, n=96):
        if d0 is None:
            t = np.linspace(0, 2 * math.pi, n + 1)
            return [tuple(T + r1 * np.array([math.cos(a), math.sin(a)])) for a in t] + [tuple(T + r0 * np.array([math.cos(a), math.sin(a)])) for a in t[::-1]]
        t = np.linspace(d0, d1, max(int(abs(d1 - d0) / (2 * math.pi) * n), 2) + 1)
        return [tuple(T + r1 * np.array([math.cos(a), math.sin(a)])) for a in t] + [tuple(T + r0 * np.array([math.cos(a), math.sin(a)])) for a in t[::-1]]
    rn1 = E.R_COL; rn0 = rn1 - V_["NUC_E"]; rp = rn1 + V_["PAS_A"]; rt = rp + V_["TAB_E"]
    sty = dict(closed=True, fc="white", ec="k", hatch="////", lw=1.0, zorder=7.2)
    ax.add_patch(Polygon(anillo(rn0, rn1), **sty))                                   # núcleo (cortado)
    a_esc = E.ESC_ANG; he = E.ESC_HB + math.atan2(0.6, rt)
    ax.add_patch(Polygon(anillo(rp, rt, a_esc + he, a_esc - he + 2 * math.pi), **sty))   # tabique del pasillo, abierto a la escalera
    for k in range(int(V_["N_AL"])):                                                  # muros radiales en el eje de las aletas
        a = 2 * math.pi * k / V_["N_AL"] + E.FASE_AL
        if abs(math.remainder(a - a_esc, 2 * math.pi)) < E.ESC_HA + 0.03: continue
        u = np.array([math.cos(a), math.sin(a)]); n_ = np.array([-u[1], u[0]]) * V_["PAR_E"] / 2
        q = [T + u * rt + n_, T + u * E.RF + n_, T + u * E.RF - n_, T + u * rt - n_]
        ax.add_patch(Polygon([tuple(p) for p in q], **sty))
    ac = a_esc + math.pi                                                              # rótulos (lado opuesto a la escalera)
    ax.text(*(T + (rn1 + V_["PAS_A"] / 2) * np.array([math.cos(ac), math.sin(ac)])), f"pasillo {V_['PAS_A']:.2f}".replace(".", ","),
            fontsize=4.6, ha="center", va="center", rotation=math.degrees(ac) - 90, zorder=8)
    ax.text(*T, "núcleo", fontsize=6, ha="center", va="center", zorder=8)
    a2 = 2 * math.pi * 9.5 / V_["N_AL"] + E.FASE_AL
    ax.text(*(T + (rt + E.RF) / 2 * np.array([math.cos(a2), math.sin(a2)])), "habitación", fontsize=4.6, ha="center", va="center",
            rotation=math.degrees(a2) - 90, zorder=8)
    ax.text(*(T + (E.RF + E.R_B) / 2 * np.array([math.cos(a2), math.sin(a2)])), f"balcón {V_['BAL_P']:.2f}".replace(".", ","), fontsize=4.2,
            ha="center", va="center", rotation=math.degrees(a2) - 90, zorder=8)


def cadena(ax, pts, off, fs=4.8, color="k"):
    """cadena de cotas exterior (estándar): segmentos parciales consecutivos sobre una misma línea"""
    for p0, p1 in zip(pts[:-1], pts[1:]):
        if np.linalg.norm(np.array(p1) - np.array(p0)) > 0.15:
            L.cota(ax, p0, p1, off, "", fs=fs, color=color)


def cotas_planta(ax):
    import cotas_rel as CR
    CR.planta(ax)
    pl = E.plantas_base()
    # cadenas en dos niveles de la fachada exterior del ala larga: huecos (parcial) y total [estándar]
    hs = sorted([h for h in VT.catalogo() if h["grupo"] == "ala larga fila alta"], key=lambda h: h["p"][1])
    pts = [(E.W_P, pl["Q"][1])] + [p for h in hs for p in ((E.W_P, h["p"][1] - h["w"] / 2), (E.W_P, h["p"][1] + h["w"] / 2))] + [(E.W_P, E.L_L)]
    cadena(ax, pts, -1.6)
    # ala corta, fachada a la calle: medianera, logia (muros y pilar), vuelo y chaflán
    V_ = E._v; sw = lambda x: tuple(np.array(E.SWP(x, 0)))
    x0 = -V_["L_C"]
    xs = [x0, x0 + V_["LOG_X0"], x0 + V_["LOG_PX"] - 0.35, x0 + V_["LOG_PX"] + 0.35, x0 + V_["LOG_X1"], x0 + V_["VOL_L"], x0 + V_["L_C"]]
    cadena(ax, [sw(x) for x in sorted(xs)], -1.5)
    L.cota(ax, (0, E.L_L), (E.W_P, E.L_L), 2.5, "ala")
    L.cota(ax, (0, E.L_L - 20), (E.W_BAR, E.L_L - 20), 1.5, "bar")
    L.cota(ax, (E.W_P, pl["Q"][1]), (E.W_P, E.L_L), -5, "")
    L.cota(ax, (E.W_P, E.Y_CUNA), (E.W_P, E.L_L), -2.5, "pie concha")
    L.cota(ax, (E.W_P, E.L_L - E.L_FIN), (E.W_P, E.L_L), -1.0, "")
    L.cota(ax, E.A1, E.C, -3, "chaflán")
    L.cota(ax, (-E.L_C, 0), E.A1, -3, "calle")
    L.cota(ax, (-E.L_C, 0), (-E.L_C, E.W_C), 3, "")
    L.cota(ax, (E.W_P, E.C[1]), E.C, 2, "")
    U = np.array(E.U); A1 = np.array(E.A1)
    k = E._k
    import cotas as KK
    E90 = np.array(KK.planta()["E90"])
    L.cota(ax, A1, A1 + (k - E.R_COL) * U, 5, "X rest."); L.cota(ax, A1 + (k - E.R_COL) * U, A1 + (k + E.R_COL) * U, 5, "col.")
    L.cota(ax, A1 + (k + E.R_COL) * U, E90, 5, "Y hotel")
    pv = np.array(E.P(0, 9.0)); ax.text(*pv, "vestíbulo /\ncirculaciones", fontsize=7, ha="center", va="center", style="italic", zorder=70,
                                        bbox=dict(fc="white", ec="0.5", lw=0.4, pad=1))
    xe = E._v["ESC_X"]
    L.cota(ax, E.esc_ang_pt(E.ESC_R0, -E.ESC_HB), E.esc_ang_pt(E.ESC_R1, -E.ESC_HB), -1.5, "escalera")
    L.cota(ax, E.esc_ang_pt(E.ESC_R1, -E.ESC_HB), E.esc_ang_pt(E.ESC_R1, E.ESC_HB), -1.5, f"cuña {E._v['ESC_SECB']:.0f}°")
    ax.text(E.KC[0] + 1, 2, f"L {math.degrees(E.TH_L):.0f}°", fontsize=8, color="k")
    V_ = E._v; yA = E.L_L - V_["VEN_FIN"]
    L.cota(ax, (E.W_P, E.L_L), (E.W_P, yA), 7.0, "macizo", fs=5.5)
    L.cota(ax, (E.W_P, yA), (E.W_P, yA - V_["VEN_W"]), 7.0, "h", fs=5.5)
    L.cota(ax, (E.W_P, yA), (E.W_P, yA - V_["S_VEN"]), 8.5, "intereje", fs=5.5)
    ax.text(E.W_P + 10.5, yA - 6 * V_["S_VEN"], f"{int(V_['N_VEN'])} huecos a {V_['S_VEN']:.2f}\n(PB: los {int(V_['N_VEN_B'])} junto al testero)".replace(".", ","),
            fontsize=6, rotation=90, va="center")
    # cota de cubierta de cada volumen
    for (x, y), z in (((3, 70), E.Z_BAR_C), ((10, 70), E.Z_P1 + E._v["H_PET"]), ((tuple(E.SWP(-12, 9))), E.Z_ALTO), 
                      (E.esc_ang_pt(E.ESC_R0 - 1.2, 0), E._v["ESC_Z1"])):
        ax.text(x, y, f"+{z:.2f}".replace(".", ","), fontsize=6.5, color="k", ha="center", bbox=dict(fc="white", ec="k", lw=0.4, pad=0.6), zorder=70)
    # trazas de las secciones
    for k, p0, p1, _ in SECC:
        ax.plot(*zip(p0, p1), "-.", color="k", lw=0.7, zorder=65)
        t_ = (np.array(p1, float) - np.array(p0, float)); t_ /= np.linalg.norm(t_); n_ = np.array([-t_[1], t_[0]])   # sentido de la vista (Ching, p. 70)
        for q in (np.array(p0, float), np.array(p1, float)):
            ax.annotate("", tuple(q + n_ * 2.2), tuple(q), arrowprops=dict(arrowstyle="-|>", color="k", lw=0.8), zorder=66)
        ax.text(*p0, k, color="k", fontsize=8, weight="bold", zorder=66); ax.text(*p1, k, color="k", fontsize=8, weight="bold", zorder=66)
    for tx in ax.texts: tx.set_clip_on(True)

def plantas():
    lst = [(1.8, "PLANTA BAJA (suelo ±0,00) – corte a +1,80"), (5.6, "PLANTA 1 (suelo +3,20) – corte a +5,60, por las ventanas"),
           (9.2, "PLANTA 2 (suelo +7,20: terraza, bar, bloque alto) – corte a +9,20"), (13.0, "PLANTA 3 (cuello) – corte a +13,00"),
           (E.Z_B0 + 3 * E.F + 2.0, f"PLANTA 4 – planta tipo de habitaciones (corte a +{E.Z_B0 + 3 * E.F + 2.0:.2f})".replace(".", ",")),
           (E.Z_B1 + 2.5, f"PLANTA ÚLTIMA – tambor de ojos y terraza de servicio (corte a +{E.Z_B1 + 2.5:.2f})".replace(".", ",")), (None, "PLANTA AÉREA – cubiertas")]
    for zc, tit in lst:
        fig = hoja(tit)
        ax = fig.add_axes([0.04, 0.04, 0.6, 0.9])
        planta(ax, zc, "", aerea=zc is None)
        cotas_planta(ax)
        ejes(ax, (-30, 34), (-10, 100))
        ax.annotate("N", xy=(28 - 0.914 * 5, 88 + 0.407 * 5), xytext=(28, 88), arrowprops=dict(arrowstyle="-|>"), fontsize=8, ha="center")   # ala larga a ~66° del N (F36, Google norte arriba)
        # detalle ampliado de la torre y el chaflan
        ax2 = fig.add_axes([0.66, 0.30, 0.33, 0.62])
        planta(ax2, zc, "detalle torre / chaflán", aerea=zc is None)
        ejes(ax2, (E.T[0] - 20, E.T[0] + 20), (E.T[1] - 18, E.T[1] + 22))
        fig.text(0.66, 0.25, f"Datos de planta: ala larga 12,74 / bar 6,21 (Bing) / tramo final sin bar {E.L_FIN:.2f} (Bing, F73) / pie de la concha a {E.L_L - E.Y_CUNA:.2f} del fondo (F73; Bing 35,13).\n"
                 f"Largo total 94,82 (Google). Esquina original a 90° con chaflán de {E.L_CH:.1f} m a {math.degrees(E.A_CH):.0f}°.\n"
                 f"Torre sobre el chaflán al {E._v['T_POS']*100:.0f} % desde la calle (algo a la derecha); la columna asoma 1,5 m.\n"
                 f"Detrás de la torre: vestíbulo y circulaciones. Escalera: hueco de {E._v['ESC_SEC']:.0f}° en el cilindro; cuerpo en cuña de {E._v['ESC_SECB']:.1f}° con {int(E._v['LAMA_N'])} lamas hasta +{E._v['ESC_ZL']:.2f}; lado izq.: rellanos, cristalera y puerta del tambor; lado dcho.: borde con lamas; arriba, muro de coronación inclinada (fotos 25/11).", fontsize=7, va="top")
        OUT.append(fig)


# ======================================================================================= SECCIONES / ALZADOS
def orientar(m, p0=None, a_deg=0.0):
    """lleva la vista a 'mirar hacia -z': rota en z por -a (direccion de la linea -> +x), deja delante y<0,
    y gira -90 en x (z' = -y, y' = z)."""
    if p0 is not None:
        m = m.translate((-p0[0], -p0[1], 0))
    return m.rotate((0, 0, -a_deg)).rotate((-90, 0, 0))



def tramos_escalera(ax, p0, p1):
    """escalera de ida y vuelta en sección [usuario 26/11; Ching]:
    - un tramo por media planta: cada FORJADO del barril es rellano de planta y a media altura hay rellano intermedio;
    - rellanos de 1,60 (lo que hace falta para girar con el ancho del tramo);
    - muro central entre los dos tramos (ojo de la escalera);
    - la escalera llega a la ÚLTIMA planta (salida a la cubierta del barril) y no sigue: por encima, paso libre hasta el forjado superior;
    - si el corte pasa por el muro central, el muro va cortado; si pasa por un tramo, ese tramo va cortado y detrás
      se ve el muro central (el otro tramo queda oculto, en discontinua)."""
    from matplotlib.patches import Polygon as Pg, Rectangle
    V = E._v; p0 = np.array(p0, float); p1 = np.array(p1, float); d = (p1 - p0) / np.linalg.norm(p1 - p0); n = np.array([-d[1], d[0]])
    ax_ = np.array([math.cos(E.ESC_ANG), math.sin(E.ESC_ANG)]); T = np.array(E.T)
    pin, pout = T + (V["ESC_R0"] + 0.3) * ax_, T + (V["ESC_RC"] - 0.3) * ax_
    off = (T - p0) @ n                                          # distancia del corte al eje de la escalera
    if abs(off) > V["ESC_RC"] * math.sin(E.ESC_HB): return
    uin, uout = (pin - p0) @ d, (pout - p0) @ d; s = np.sign(uout - uin)
    nst, h, t, w, LR = 9, E.F / 18, 0.28, 0.15, 1.60
    run = (nst - 1) * t
    uB = uout - s * LR; uA = uB - s * run
    CUT = dict(fc="white", ec="k", lw=1.1, hatch="////", zorder=31)
    NS = E.niveles_suelo()                                      # FUENTE ÚNICA: los rellanos de planta son los forjados (mismas cotas)
    z_fin = NS[-1]                                              # última planta: salida a la cubierta del barril
    muro_cortado = abs(off) < 0.2
    zz0 = NS[0]
    if muro_cortado:                                            # muro central cortado entre los tramos
        ax.add_patch(Rectangle((min(uA, uB), zz0), abs(uB - uA), z_fin - zz0, **CUT))
    else:                                                       # muro central visto detrás del tramo cortado
        ax.add_patch(Rectangle((min(uA, uB), zz0), abs(uB - uA), z_fin - zz0, fc="none", ec="k", lw=0.45, zorder=29))
    cosa = t / math.hypot(t, h)
    for z, zsig in zip(NS[:-1], NS[1:]):                      # una vuelta por planta, de suelo a suelo (la 1.ª es más baja: 2,49)
        hp = zsig - z; h = hp / (2 * nst); cosa = t / math.hypot(t, h)
        zi = z + hp / 2
        for k, (ua_, ub_, za, zb) in enumerate(((uA, uB, z, zi), (uB, uA, zi, zsig))):
            sg = np.sign(ub_ - ua_)
            top = [(ua_, za)]
            for i_ in range(nst):
                top += [(ua_ + sg * t * i_, za + h * (i_ + 1)), (ua_ + sg * t * (i_ + 1) if i_ < nst - 1 else ub_, za + h * (i_ + 1))]
            sol = [(ub_, zb - w / cosa), (ua_, za - w / cosa)]
            cortado = (not muro_cortado) and ((k == 0) == (off * s > 0))
            if muro_cortado or cortado:
                if cortado: ax.add_patch(Pg(top + sol, closed=True, **CUT))
            else:                                               # tramo oculto tras el muro central
                ax.plot(*np.array(top).T, color="k", lw=0.3, ls=(0, (3, 2)), zorder=28)
        # rellanos cortados (abarcan todo el ancho): intermedio contra el muro exterior y de planta = forjado del barril
        ax.add_patch(Rectangle((min(uB, uout), zi - 0.20), abs(uout - uB), 0.20, **CUT))
        ax.add_patch(Rectangle((min(uin, uA), zsig - 0.20), abs(uA - uin), 0.20, **CUT))
    ax.add_patch(Rectangle((min(uin, uA), zz0 - 0.20), abs(uA - uin), 0.20, **CUT))
    # paso libre de cabeza sobre el último rellano hasta el forjado superior
    zt = V["ESC_ZL"] - 0.3
    L.cota(ax, ((uin + uA) / 2, z_fin), ((uin + uA) / 2, zt), 0.0, "paso libre", fs=4.5)

def seccion(ax, p0, p1, titulo):
    a = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
    Lg = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    m = orientar(M, p0, a)
    mas_alla = m ^ Manifold.cube((BIG, 100, BIG)).translate((-BIG / 2, -50, -BIG))      # z' < 0  (y > 0)
    L.dibujar_vista(ax, mas_alla)                                     # visto: aristas con valor según profundidad
    cs = m.slice(0.0)
    L.corte(ax, cs, huecos=huecos_seccion(p0, p1), hatch="////")     # cortado: trazo grueso + rayado a 45° (H.A.)
    L.terreno(ax, -16, Lg + 2)
    L.figura(ax, Lg * 0.08 + 1.0, 0.0)
    forjados_seccion(ax, cs, hueco_escalera(p0, p1))
    nucleo_seccion(ax, p0, p1)
    for z, t in ((E.Z_PB, "techo PB"), (E.Z_P1, "terraza / planta 1"), (E.Z_BAR, "bar"), (E.Z_ALTO, "bloque alto"),
                 (E.niveles_suelo()[0], "1ª planta hab."), (E.Z_B1, "cubierta hab."), (E.Z_T1, "tambor"), (E.Z_V1, "visera"), (E.Z_R1, "remate")):
        L.nivel(ax, Lg + 1, z, t)
    tramos_escalera(ax, p0, p1)
    import cotas_rel as CR
    _d = (np.array(p1, float) - np.array(p0, float)); _d /= np.linalg.norm(_d); _q = np.array(E.T) - np.array(p0, float)
    _sc = float(_q @ _d); _di = abs(float(_q[0] * _d[1] - _q[1] * _d[0])); _ex = []
    for _r, _n in ((E.R_COL, "col"), (E.R_CU, "cue"), (E.R_B, "bar"), (E.R_T, "tam")):
        if _di < _r - 0.05:
            _h = math.sqrt(_r ** 2 - _di ** 2); _ex += [(_n, _sc - _h), (_n, _sc + _h)]
    CR.dibujar(ax, p0, _d, -12, Lg, extra=_ex, xl=Lg)
    cruces(ax, p0, p1, titulo.split(':')[0].replace('SECCIÓN ', '').strip())
    ejes(ax, (-10, Lg + 12), (-6, 53))
    ax.set_title(titulo, fontsize=9, loc="left")



def hueco_escalera(p0, p1):
    """tramo [u0, u1] de la línea de sección que cae dentro de la cuña de la escalera (en planta), o None"""
    from shapely.geometry import Polygon as SP, LineString
    V = E._v; n = 24
    pts = [E.esc_ang_pt(V["ESC_RC"], -E.ESC_HB + 2 * E.ESC_HB * k / n) for k in range(n + 1)] + \
          [E.esc_ang_pt(V["ESC_R0"], E.ESC_HB - 2 * E.ESC_HB * k / n) for k in range(n + 1)]
    g = SP(pts).buffer(0).intersection(LineString([p0, p1]))
    if g.is_empty or g.length < 0.5: return None
    p0 = np.array(p0, float); d = (np.array(p1, float) - p0); d /= np.linalg.norm(d)
    us = [(np.array(c) - p0) @ d for c in g.coords] if g.geom_type == "LineString" else [(np.array(c) - p0) @ d for gg in g.geoms for c in gg.coords]
    return (min(us) + VT.MURO, max(us) - VT.MURO)

def forjados_seccion(ax, cs, hueco_u=None):
    """forjados de 0,30 dentro de cada recinto cortado: techo de PB en la base y cada planta del barril;
    se interrumpen en la caja de la escalera (hueco_u = tramo de la sección dentro de la cuña) [usuario 26/11]"""
    from matplotlib.patches import Polygon
    from shapely.geometry import Polygon as SP, box
    # forjados del barril con la cara superior en la del canto: el suelo del balcón y el de la habitación a la misma cota (usuario 26/11)
    niveles = [E.Z_PB] + E.niveles_suelo()[1:-1]               # FUENTE ÚNICA (la 1.ª es el fondo plano y la última la cubierta)
    for P in cs.to_polygons():
        sp = SP(np.array(P)).buffer(0)
        if sp.is_empty: continue
        inn = sp.buffer(-VT.MURO, join_style=2)
        if inn.is_empty: continue
        x0, z0, x1, z1 = inn.bounds
        for zl in niveles:
            if not (z0 + 0.5 < zl < z1 - 0.5): continue
            g = inn.intersection(box(x0 - 1, zl - VT.MURO, x1 + 1, zl))
            if hueco_u is not None and zl > E.Z_CU1:
                g = g.difference(box(hueco_u[0], zl - 1, hueco_u[1], zl + 1))
            for gm in getattr(g, "geoms", [g]):
                if gm.geom_type == "Polygon" and not gm.is_empty and gm.area > 0.3:
                    ax.add_patch(Polygon(np.array(gm.exterior.coords), closed=True, fc="white", ec="k", hatch="////", lw=0.9, zorder=6))


def nucleo_seccion(ax, p0, p1):
    """muros del núcleo estructural de la torre (R_COL, 0,30) donde la sección lo corta: suelo → cubierta de habitaciones"""
    from matplotlib.patches import Rectangle
    p0, p1 = np.array(p0, float), np.array(p1, float); d = p1 - p0; Lg = np.linalg.norm(d); tl = d / Lg
    T = np.array(E.T); q = T - p0; sc = q @ tl; dist = abs(q[0] * tl[1] - q[1] * tl[0])
    for R in (E.R_COL, E.R_COL - VT.MURO):
        pass
    # BASE DEL TAMBOR cortada: muros del cuello (0,40) con su fondo y fondo plano del barril (0,50), todo en ángulo recto [usuario 26/11]
    if dist < E.R_CU:
        hc = math.sqrt(E.R_CU ** 2 - dist ** 2)
        for sg in (-1, 1):
            x = sc + sg * hc
            ax.add_patch(Rectangle((x - (0.4 if sg > 0 else 0), E.Z_CU0), 0.4, E.Z_CU1 - E.Z_CU0, fc="white", ec="k", hatch="////", lw=0.9, zorder=6.5))
        ax.add_patch(Rectangle((sc - hc + 0.4, E.Z_CU0), 2 * hc - 0.8, 0.4, fc="white", ec="k", hatch="////", lw=0.9, zorder=6.5))   # fondo del cuello entre muros (esquina en L, sin vuelo)
    if dist < E.R_B:
        hb = math.sqrt(E.R_B ** 2 - dist ** 2)
        ax.add_patch(Rectangle((sc - hb, E._v["Z_BI"]), 2 * hb, E.niveles_suelo()[0] - E._v["Z_BI"], fc="white", ec="k", hatch="////", lw=0.9, zorder=6.5))   # fondo plano = forjado de la 1.ª planta
    # ALETA + VIGA proyectadas (muro visto tras el corte), según el croquis del usuario: la aleta sobresale de la 2.ª planta arriba y acaba
    # con escalón en ángulo recto; en la 1.ª planta queda enrasada con la banda y sigue por debajo como viga de canto hasta el cuello
    V_ = E._v; zf = V_["Z_BI"] - V_["VIG_H"]
    perfil = [(E.R_AL, E.Z_B1 + V_["FOR_C"]), (E.R_AL, V_["Z_ALE"]), (E.R_B, V_["Z_ALE"]), (E.R_B, zf), (E.R_CU, zf)]
    for sg in (-1, 1):
        ax.plot([sc + sg * r for r, z in perfil], [z for r, z in perfil], color="k", lw=0.55, zorder=6.4)
    if dist < E.R_T:                                            # forjado de cubierta del barril y suelo de la banda (+pasillo) [usuario 26/11]
        ht = math.sqrt(E.R_T ** 2 - dist ** 2)
        ax.add_patch(Rectangle((sc - ht, E.Z_B1 + E._v["FOR_C"] - 0.3), 2 * ht, 0.3, fc="white", ec="k", hatch="////", lw=0.9, zorder=6.5))
    if dist < E.R_G + 1:
        hg = math.sqrt(max(E.R_T ** 2 - dist ** 2, 0))
        ax.add_patch(Rectangle((sc - hg, E.Z_T1 - E._v["H_PT"] - 0.3), 2 * hg, 0.3, fc="white", ec="k", hatch="////", lw=0.9, zorder=6.5))
    pv = np.array(E.P(*E.OFF_V)) - p0; scv = pv @ tl; dv = abs(pv[0] * tl[1] - pv[1] * tl[0])
    if dv < E.R_V:                                              # visera: losas inferior y superior cortadas en todo su ancho [usuario 26/11]
        hv = math.sqrt(E.R_V ** 2 - dv ** 2)
        for z0_ in (E.Z_G1, E.Z_V1 - 0.35):
            ax.add_patch(Rectangle((scv - hv, z0_), 2 * hv, 0.35, fc="white", ec="k", hatch="////", lw=1.1, zorder=6.6))
    rp = E.R_COL + V_["PAS_A"]                                   # tabique del pasillo (supuesto, usuario 26/11) en las plantas de habitaciones
    if dist < rp:
        hp = math.sqrt(rp ** 2 - dist ** 2)
        for i in range(int(V_["N_PL"])):
            z = E.Z_B0 + i * E.F + (V_["FOR_C"] if i else 0.5)
            for sg in (-1, 1):
                x = sc + sg * hp
                ax.add_patch(Rectangle((x - (0 if sg > 0 else V_["TAB_E"]), z), V_["TAB_E"], E.Z_B0 + (i + 1) * E.F - z, fc="white", ec="k",
                                       hatch="////", lw=0.6, zorder=6.5))
        ax.text(sc - hp + V_["PAS_A"] / 2 - 0.1, E.Z_B0 + 2.5 * E.F, f"pasillo {V_['PAS_A']:.2f}".replace(".", ","), fontsize=4.5, rotation=90,
                ha="center", va="center", zorder=7)
    if dist >= E.R_COL - 0.05: return
    h = math.sqrt(E.R_COL ** 2 - dist ** 2); ne = V_["NUC_E"]                     # núcleo con muro de NUC_E
    for sg in (-1, 1):
        x = sc + sg * h
        ax.add_patch(Rectangle((x - (ne if sg > 0 else 0), 0), ne, E.Z_G1, fc="white", ec="k", hatch="////", lw=0.9, zorder=6.5))
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
                            tipo="garaje" if h["tipo"] == "garaje" else ("ventana" if h["tipo"] != "puerta" else "puerta_sec")))
    return out



def letras_alzado(ax, d):
    """rótulo САЛЮТ dibujado sobre sus 5 letras en cualquier alzado (las letras miran a la cámara de Alamy)"""
    d = np.array(d, float) / np.linalg.norm(d); r_ = np.array([d[1], -d[0]])
    a = math.degrees(math.atan2(d[1], d[0])) - 90.0; ca, sa = math.cos(math.radians(-a)), math.sin(math.radians(-a))
    for L_ in E.letrero():
        nrm = np.array([math.cos(math.radians(L_["rot"])), math.sin(math.radians(L_["rot"]))])
        vis = -(nrm @ d)
        if vis < 0.15: continue
        x = ca * L_["c"][0] - sa * L_["c"][1]
        ax.text(x, (L_["z0"] + L_["z1"]) / 2, L_["ch"], fontsize=9 * max(vis, 0.4), ha="center", va="center", weight="bold", zorder=40,
                family="DejaVu Sans", color="k", clip_on=True)
    for gx, gy, gz, ga in E.gargolas():                     # gárgolas: una por módulo y planta [F18, F08] (solo en planos)
        if -(np.array([math.cos(ga), math.sin(ga)]) @ d) < 0.2: continue
        ax.plot([ca * gx - sa * gy], [gz], "o", ms=1.1, color="k", zorder=41, clip_on=True)


def vidrios_alzado(ax, d, umap, figuras=True):
    """Ching: el vidrio en alzado se indica con trazos diagonales de reflejo (línea superficial fina); figura humana para
    la escala. d = dirección en la que mira el observador; umap(P) = coordenada horizontal del alzado de un punto de planta."""
    import ventanas as VT
    d = np.asarray(d, float) / np.linalg.norm(d)
    for h in VT.catalogo():
        if h["tipo"] not in ("ventana", "puerta") or h["grupo"].startswith("torre planta") or h["grupo"] == "escalera retranqueo": continue
        n = np.asarray(h["n"], float)
        if n @ d > -0.3: continue
        t = np.asarray(h["t"], float); p = np.asarray(h["p"], float)
        ua, ub = sorted((umap(p - t * h["w"] / 2), umap(p + t * h["w"] / 2)))
        du, dz = ub - ua, h["z1"] - h["z0"]
        if du < 0.4 or dz < 0.4: continue
        for f0, f1 in ((0.18, 0.62), (0.42, 0.82)):
            ax.plot([ua + f0 * du, ua + (f0 + 0.22) * du], [h["z0"] + (f1 - 0.3) * dz, h["z0"] + f1 * dz], color="k", lw=0.22, zorder=42, clip_on=True)
    V = E._v; pb = np.array(E.P(V["OB_X"], V["OB_Y"])); uc = umap(pb)            # banda acristalada del tambor
    for k in np.arange(-0.8, 0.81, 0.2):
        u0 = uc + k * E.R_G
        ax.plot([u0, u0 + 0.9], [E.Z_T1 + 0.4, E.Z_T1 + 1.5], color="k", lw=0.22, zorder=42, clip_on=True)
    if figuras:                                                                    # figuras humanas a pie de calle
        ut = umap(np.array(E.T))
        for du_ in (-14.0, -11.5, 13.0):
            L.figura(ax, ut + du_, 0.0)


def alzado(ax, d, titulo):
    if np.allclose(d, (0, 1)):                       # alzado a la calle: dibujado pieza a pieza (alzado_calle.py)
        import alzado_calle as AC
        uT, uM = AC.dibujar(ax)
        ejes(ax, (uM - 6, uT + 32), (-6, 52)); ax.set_title(titulo, fontsize=9, loc="left")
        return uM - 6, uT + 19
    a = math.degrees(math.atan2(d[1], d[0])) - 90.0          # d -> +y
    m = M.rotate((0, 0, -a)).rotate((-90, 0, 0))
    L.dibujar_vista(ax, m)
    letras_alzado(ax, d)
    _a = math.radians(-a); _c, _s = math.cos(_a), math.sin(_a)
    vidrios_alzado(ax, d, lambda P_: _c * P_[0] - _s * P_[1])
    V = np.asarray(m.to_mesh().vert_properties)[:, :2]
    x0, x1 = V[:, 0].min(), V[:, 0].max()
    import cotas_rel as CR
    _dd = np.array(d, float); _dd /= np.linalg.norm(_dd); _r = np.array([_dd[1], -_dd[0]])        # eje horizontal del alzado
    _ca, _sa = math.cos(math.radians(-a)), math.sin(math.radians(-a))
    _o = np.array([0.0, 0.0])                                    # u = ca*x - sa*y  ⇒  dirección (ca, -sa) en planta
    _dir = np.array([_ca, -_sa])
    _T = np.array(E.T); _uT = _ca * _T[0] - _sa * _T[1]
    _ex = [("bar", _uT - E.R_B), ("bar", _uT + E.R_B)]
    CR.dibujar(ax, _o, _dir, x0, x1, extra=_ex, xl=x1)
    ax.axhline(0, color="k", lw=1.6)
    for z, t in ((E.Z_PB, "techo PB"), (E.Z_P1, "planta 1 / terraza"), (E.Z_ALTO, "cub. bar / bloque alto"), (E.niveles_suelo()[0], "1ª hab."),
                 (E.Z_B1, "cub. hab."), (E.Z_T1, "tambor"), (E.Z_G1, "banda"), (E.Z_V1, "visera"), (E.Z_R1, "remate")):
        L.nivel(ax, x1 + 1, z, t)
    ejes(ax, (x0 - 10, x1 + 13), (-6, 52))
    ax.set_title(titulo, fontsize=9, loc="left")
    return x0, x1


def foto(ax, f, titulo):
    ax.imshow(Image.open(IMG + f).convert("RGB")); ax.axis("off"); ax.set_title(titulo, fontsize=8, loc="left")


def _secc():
    T = np.array(E.T); U = np.array(E.U); N = np.array(E.N); pl = E.plantas_base()
    xe = E.esc_ang_pt(10.0, 0.0)[0]; yc = (E.ESC_Y0 + E.ESC_Y1) / 2       # eje de la escalera (= eje radial de la torre)
    return [
     ("L1", (xe, -10), (xe, 100), "LONGITUDINAL por el eje de la escalera: escalera, barril, cuello, bar y ala larga entera"),
     ("L2", ((E.W_P + E.W_EXT) / 2, pl["Q"][1] - 6), ((E.W_P + E.W_EXT) / 2, 100), "LONGITUDINAL por la concha: su perfil curvo y la terraza detrás"),
     ("L3", tuple(T - 32 * U), tuple(T + 26 * U), "LONGITUDINAL por el eje de la torre paralela al chaflán: restaurante, columna, hotel y esquina a 90°"),
     ("L4", (E.W_BAR + E._v["V_BAR"] + 1.6, pl["Q"][1] - 4), (E.W_BAR + E._v["V_BAR"] + 1.6, 100), "LONGITUDINAL por la terraza mirando al bar: el bar, su vuelo y la cubierta inclinada en alzado"),
     ("S1", tuple(T - 18 * N), tuple(T + 32 * N), "por el eje de la torre perpendicular al chaflán: columna, cuello, ménsulas, barril, visera desplazada y escalera"),
     ("S2", E.esc_pt(E.ESC_R1 + 6, 0), E.esc_pt(-8, 0), "por el eje de la escalera, radial al cilindro: caja insertada en la torre y su salida al patio"),
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
            ax.plot([s, s], [-1, ytop], color="k", lw=0.7, ls="-.", zorder=60)
            ax.text(s, ytop + 0.5, k, color="k", fontsize=8, weight="bold", ha="center", zorder=60)



def secciones():
    # hoja de situacion
    fig = hoja("SITUACIÓN DE SECCIONES")
    ax = fig.add_axes([0.05, 0.04, 0.55, 0.9])
    planta(ax, None, "situación de las secciones", aerea=True)
    for k, p0, p1, _ in SECC:
        ax.plot(*zip(p0, p1), "-.", color="k", lw=1)
        ax.text(*p0, k, color="k", fontsize=10, weight="bold"); ax.text(*p1, k, color="k", fontsize=10, weight="bold")
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
            [("alamy_torre.png", "ALAMY medida por MGF – torre completa (código de la verdad)"), ("alamy_alto.png", "ALAMY – parte alta: generatrices de cada cilindro"), ("alamy_barril.png", "ALAMY – barril: canto, hueco, poyete, ranura"), ("71.webp", "F71")],
            [f"PB {V['Z_PB']} / base {V['Z_P1']}: F09 7,3 · F14 7,2 · F70 6,5 (rango 7,1±0,3)",
             f"rampa: peto arriba +{V['Z_CON'] + 1:.1f}: F09 8,3±0,8 · F71 9,6±1,2"]),
           ((-1, 0), "ALZADO 2 – FACHADA EXTERIOR DEL ALA LARGA (con la rampa)",
            [("73.webp", "F73 (desde el testero)"), ("71.webp", "F71"), ("76.webp", "F76 maqueta (orient.)"), ("47.webp", "F47")],
            [f"huecos: {V['N_VEN']} arriba y {V['N_VEN_B']} abajo (bajo los {V['N_VEN_B']} junto al testero), intereje {V['S_VEN']}, hueco {V['VEN_W']} (F73, F01, F47 + tu recuento)",
             f"alturas: fila alta {V['VA_0']}–{V['VA_1']}, baja {V['VB_0']}–{V['VB_1']} (verticales exactas en F73); marco que sale {V['MAR_P']}, vidrio {V['MAR_R']} adentro",
             f"rampa de acceso público: sube desde la plaza (pie a {E.Y_CUNA:.1f}) hasta la terraza-restaurante +{V['Z_CON']}, perfil curvo; arco de paso debajo junto al hotel (F76, F47, F71, F73)",
             f"el techo del restaurante empieza en rampa: junto a la torre nace a +{V['Z_P1']} (terraza) y sube {V['R2_L']} m hasta la azotea +{V['Z_BARC']} (F76, F71)",
             f"bar hasta {V['L_FIN']} m del testero (Bing, F73, F47); peto +{V['Z_P1'] + V['H_PET']:.1f}; testero +{V['Z_FIN']}"]),
           ((0, 1), "ALZADO 3 – CALLE (ala corta)", [("alamy_torre.png", "ALAMY medida por MGF – torre completa (código de la verdad)"), ("19.webp", "F19"), ("72.webp", "F72")], []),
           ((1, 0), "ALZADO 4 – PATIO INTERIOR DE LA L", [("75.png", "F75 (escalera desde el patio)")], []),
           ((0, -1), "ALZADO 5 – TESTERO DEL ALA LARGA (hacia la torre)",
            [("73.webp", "F73"), ("13.webp", "F13"), ("12.png", "F12")],
            [f"testero +{V['Z_FIN']} con barandilla, puerta de servicio con marquesina y ventana encima (F73)",
             f"lo que asoma tras el testero a ≈ +11,3 es el extremo del bar, a {V['L_FIN']} m",
             f"escalera: hueco de {V['ESC_SEC']:.0f}° en el cilindro, cuerpo en cuña de {V['ESC_SECB']:.1f}° con {int(V['LAMA_N'])} lamas; lado izq. rellanos + cristalera + puerta del tambor, lado dcho. borde con lamas; muro de coronación inclinada +{V['ESC_ZI']}→+{V['ESC_Z1']} (fotos 25/11)"])]
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
    a = 360 * 0.5 / E.N_AL + math.degrees(E.A_CH) - 90   # (sección de detalle: módulo genérico)
    ang = math.radians(a)
    p0 = (E.T[0], E.T[1]); p1 = (E.T[0] + 20 * math.cos(ang), E.T[1] + 20 * math.sin(ang))
    ax = fig.add_axes([0.04, 0.06, 0.40, 0.86])
    seccion(ax, p0, p1, "sección radial por un módulo (izquierda = núcleo)")
    ejes(ax, (6, 17), (E.Z_B0 - 3, E.Z_B0 + 3 * E.F + 0.5))
    rf = E.RF
    V = E._v; FC, FR, FP = V["FOR_C"], V["FOR_R"], V["FOR_P"]
    for i in range(1, 3):                                   # plantas de habitaciones: canto, ranura, poyete y ventana [MGF Alamy, F09]
        z = E.Z_B0 + i * E.F
        L.cota(ax, (E.R_B + 0.6, z), (E.R_B + 0.6, z + FC), 0.6, "canto 0,59", fs=5.5)
        L.cota(ax, (E.R_B + 0.6, z + FC + FR), (E.R_B + 0.6, z + FC + FR + FP), 0.6, "poyete 0,78", fs=5.5)
        L.cota(ax, (rf - 0.6, z + FC), (rf - 0.6, z + E.F), -0.6, "puerta balconera", fs=5.5)
    L.cota(ax, (E.R_B - 0.25, E.Z_B0 + E.F + FC), (E.R_B - 0.25, E.Z_B0 + E.F + FC + FR), -1.2, "ranura 0,27", fs=5.5)
    # 1.ª planta (pavés): banda continua sin ranura y fondo inclinado [F09, F18]
    L.cota(ax, (E.R_B + 0.6, V["Z_BI"]), (E.R_B + 0.6, V["Z_BI"] + V["BAN_1"]), 0.6, "banda 1,09 sin ranura", fs=5.5)
    L.cota(ax, (rf - 0.6, V["Z_BI"] + V["BAN_1"]), (rf - 0.6, E.Z_B0 + E.F), -0.6, "pavés 1,40", fs=5.5)
    L.cota(ax, (E.R_CU, E.Z_B0 - 0.8), (E.R_B, E.Z_B0 - 0.8), -0.4, "fondo plano +%.2f · vigas %.2f" % (V["Z_BI"], V["VIG_H"]), fs=5.5)
    L.cota(ax, (rf, E.Z_B0 + 3 * E.F + 0.3), (E.R_B, E.Z_B0 + 3 * E.F + 0.3), 0.4, "balcón", fs=6)
    L.cota(ax, (E.R_B, E.Z_B0 - 1.6), (E.R_AL, E.Z_B0 - 1.6), -0.4, "vuelo aleta", fs=6)
    # alzado de 3 modulos
    ax2 = fig.add_axes([0.47, 0.06, 0.25, 0.86])
    a_ = math.degrees(math.atan2(E.N[1], E.N[0])) - 90.0
    m = M.rotate((0, 0, -a_)).rotate((-90, 0, 0))
    tx = E.T[0] * math.cos(math.radians(-a_)) - E.T[1] * math.sin(math.radians(-a_))
    L.dibujar_vista(ax2, m, res=0.02)
    ejes(ax2, (tx - 6, tx + 6), (E.Z_B0 - 3, E.Z_B0 + 3 * E.F + 0.5))
    ax2.set_title("alzado frontal de 3 módulos (aletas cada 360/19 = 18,9°)", fontsize=8, loc="left")
    foto(fig.add_axes([0.74, 0.52, 0.25, 0.40]), "alamy_barril.png", "comprobación ALAMY (MGF): canto, hueco, poyete, ranura, aletas")
    foto(fig.add_axes([0.74, 0.08, 0.25, 0.40]), "alamy_alto.png", "comprobación ALAMY (MGF): tambor, ojos, banda, visera, remate")
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
        dir_esc = math.degrees(E.ESC_ANG)
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
           ("remate", 50.1, E.Z_R1)]
    txt += ["", "Cota                      foto (m)   planos (m)   dif.", "-" * 70]
    for n, fv, mv in alt:
        txt.append(f"{n:<25} {fv:>7.2f}   {mv:>9.2f}   {mv - fv:>+5.2f}   F09/F14")
    pl = E.plantas_base()
    txt += ["", "Planta                    fuente (m)  planos (m)", "-" * 70,
            f"{'ala larga ancho':<25} {12.74:>7.2f}   {E.W_P:>9.2f}   Bing",
            f"{'bar ancho':<25} {6.21:>7.2f}   {E.W_BAR:>9.2f}   Bing",
            f"{'tramo final':<25} {7.81:>7.2f}   {E.L_FIN:>9.2f}   Bing / F73",
            f"{'pie de la concha al fondo':<25} {35.13:>7.2f}   {E.L_L - E.Y_CUNA:>9.2f}   Bing (F73 hueco 11 visible)",
            f"{'chaflán (P1)':<25} {20.0:>7.2f}   {E.L_CH:>9.2f}   Google / usuario",
            f"{'largo total':<25} {94.82:>7.2f}   {E.L_L:>9.2f}   Google",
            "", f"Pendiente: ángulo de la L ({math.degrees(E.TH_L):.0f}° ± 2,3) y fondo del ala corta (12,74 m) sin foto frontal."]
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
    traduccion.ACTIVO = False                       # hojas de trabajo (notas y tablas): en español; los juegos A3/A4 y el plano de lugar, en ucraniano
    plantas(); secciones(); alzados(); detalles(); coherencia(); cuadro_cotas()
    plt.rcParams['figure.max_open_warning'] = 0
    with PdfPages("SALUT_planos_definitivos.pdf") as pdf:
        for i, f in enumerate(OUT):
            pdf.savefig(f)
            f.savefig(f"lam_{i + 1:02d}.png", dpi=80)
    print("laminas:", len(OUT))
