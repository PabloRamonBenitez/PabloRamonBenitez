"""Grafismo arquitectónico de planta: rampas (eje con triángulo de arranque, flecha de subida, pendiente y cotas de
nivel en los extremos), escalera (peldaños, flecha, línea de corte en zigzag, tramo por encima en discontinua),
proyecciones rotuladas de lo que vuela por encima y cotas de nivel. Todo con parches/líneas para que funcione
también en las plantas giradas de los planos A4."""
import math
import numpy as np
from matplotlib.patches import FancyArrowPatch, Polygon, Circle, Rectangle
import edificio as E

K = "k"


def _ang(p, q):
    return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))


def cota_nivel(ax, p, z, z_=82):
    """cota de nivel en planta: recuadro con +z"""
    ax.text(p[0], p[1], f"{'±' if abs(z) < 1e-6 else '+'}{abs(z):.2f}".replace(".", ","), fontsize=5, ha="center", va="center",
            bbox=dict(boxstyle="square,pad=0.15", fc="white", ec=K, lw=0.5), zorder=z_)


def eje_rampa(ax, pts, z0, z1, rotulo, discont=False, z_=81):
    """pts: polilínea del eje de abajo (z0) a arriba (z1)"""
    pts = [np.array(p, float) for p in pts]
    ls = (0, (5, 3)) if discont else "-"
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=K, lw=0.6, ls=ls, zorder=z_)
    # triángulo de arranque (abajo)
    d = pts[1] - pts[0]; d /= np.linalg.norm(d); n = np.array([-d[1], d[0]])
    a = pts[0]; tri = [a + n * 0.45, a - n * 0.45, a + d * 0.8]
    ax.add_patch(Polygon(tri, closed=True, fc=K, ec=K, lw=0.4, zorder=z_))
    # flecha de subida (arriba)
    ax.add_patch(FancyArrowPatch(tuple(pts[-2] + (pts[-1] - pts[-2]) * 0.6), tuple(pts[-1]), arrowstyle="-|>", mutation_scale=7,
                                 color=K, lw=0.6, zorder=z_))
    L = sum(np.linalg.norm(pts[i + 1] - pts[i]) for i in range(len(pts) - 1))
    m = pts[len(pts) // 2 - 1] + (pts[len(pts) // 2] - pts[len(pts) // 2 - 1]) * 0.5 if len(pts) > 2 else (pts[0] + pts[1]) / 2
    ang = _ang(pts[0], pts[1]) if len(pts) == 2 else _ang(pts[len(pts) // 2 - 1], pts[len(pts) // 2])
    if ang > 90: ang -= 180
    if ang < -90: ang += 180
    ax.text(m[0] + n[0] * 0.6, m[1] + n[1] * 0.6, rotulo, fontsize=5, rotation=ang, rotation_mode="anchor", ha="center",
            va="bottom", zorder=z_)
    cota_nivel(ax, pts[0] - d * 1.2, z0)
    dl = pts[-1] - pts[-2]; dl /= np.linalg.norm(dl)
    cota_nivel(ax, pts[-1] + dl * 1.2, z1)


def rampas(ax, zc):
    V = E._v
    pl = E.plantas_base(); y0 = pl["Q"][1] + V["D_HOTF"]
    xr = (E.W_P + E.W_EXT) / 2
    arriba = zc is not None and zc < V["Z_P1"] - 1.0           # la rampa queda por encima del corte en su tramo alto
    # 1) rampa de acceso público (concha): de la plaza (±0) a la terraza (+7,2); sigue en curva a +7,2
    pmax = V["Z_CON"] * (1 + V["RAMPA_C"]) / (E.Y_CUNA - y0) * 100
    pmin = V["Z_CON"] * (1 - V["RAMPA_C"]) / (E.Y_CUNA - y0) * 100
    eje_rampa(ax, [(xr, E.Y_CUNA - 0.3), (xr, y0)], 0.0, V["Z_CON"],
              f"RAMPA DE ACCESO · sube · P = {pmin:.0f}–{pmax:.0f} %", discont=arriba)
    # recorrido del coche: sube por la rampa, a la izquierda siguiendo la curva hacia fuera, y a la derecha por la
    # meseta (sobre la prolongación del chaflán) hasta el arranque del techo del restaurante, bajo la escalera
    import cotas as KK
    g = KK.planta(); C = np.array(g["C"]); E90 = np.array(g["E90"]); yS = g["YS"]
    yb0 = C[1] + 0.5; xb = (E.W_BAR + V["V_BAR"]) / 2
    ctrl = [np.array([xr, yS + 4.0]), np.array([xr + 0.3, yS - 1.5]), (E90 + C) / 2 + np.array([1.5, 1.8]),
            np.array([E.W_P - 1.0, C[1] + 1.2]), np.array([xb + 2.5, C[1] + 0.8]), np.array([xb, yb0 + 2.5])]
    def bez(P, n=60):
        out = []
        for i in range(len(P) - 2):
            p0, p1, p2 = (P[i] + P[i + 1]) / 2, P[i + 1], (P[i + 1] + P[i + 2]) / 2
            if i == 0: p0 = P[0]
            if i == len(P) - 3: p2 = P[-1]
            for t in np.linspace(0, 1, n // (len(P) - 2)):
                out.append((1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2)
        return np.array(out)
    cam = bez(ctrl)
    ax.plot(cam[:, 0], cam[:, 1], color="#1a5fb4", lw=0.8, ls=(0, (6, 2, 1, 2)), zorder=81)
    ax.add_patch(FancyArrowPatch(tuple(cam[-4]), tuple(cam[-1]), arrowstyle="-|>", mutation_scale=7, color="#1a5fb4", lw=0.8, zorder=81))
    ax.text(E90[0] + 0.6, E90[1] + 1.5, "90°", fontsize=5, zorder=81)
    ax.text((E90[0] + C[0]) / 2 + 1.2, (E90[1] + C[1]) / 2 + 3.0, "meseta +7,20\n(hotel debajo)".replace(".", ","), fontsize=4.4, style="italic", zorder=81)
    # 2) techo del restaurante en rampa: +7,2 → +11,5
    p2 = (E.Z_BAR_C - V["Z_P1"]) / V["R2_L"] * 100
    eje_rampa(ax, [(xb, yb0 + 0.3), (xb, yb0 + V["R2_L"])], V["Z_P1"], E.Z_BAR_C,
              f"TECHO DEL RESTAURANTE EN RAMPA (bajo la escalera) · sube · P = {p2:.0f} %", discont=zc is not None and zc < E.Z_BAR_C)


def escalera(ax, zc):
    """escalera de ida y vuelta dentro de la cuña: dos tramos radiales separados por el muro central"""
    V = E._v
    if zc is None or zc >= V["ESC_Z1"]:
        return
    if zc < V["ESC_Z0"]:                                          # la caja queda por encima: contorno en discontinua
        n = 12
        pts = [E.esc_ang_pt(V["ESC_RC"], -E.ESC_HB + 2 * E.ESC_HB * k / n) for k in range(n + 1)] + \
              [E.esc_ang_pt(V["ESC_R0"], E.ESC_HB - 2 * E.ESC_HB * k / n) for k in range(n + 1)]
        ax.add_patch(Polygon(pts, closed=True, fill=False, ec="0.25", lw=0.8, ls=(0, (6, 3)), zorder=79))
        c = E.esc_ang_pt((V["ESC_R0"] + V["ESC_RC"]) / 2, 0)
        ax.text(c[0], c[1], f"caja de escalera\npor encima (+{V['ESC_Z0']:.2f})".replace(".", ","), fontsize=4.3, ha="center", va="center",
                style="italic", color="0.25", zorder=79)
        return
    r0, r1 = V["ESC_R0"] + 0.3, V["ESC_RC"] - 0.3
    ra, rb = r0 + 1.3, r1 - 1.3                                   # rellanos en los extremos
    nps = 10; huella = (rb - ra) / nps
    rc = ra + (rb - ra) * 0.55                                    # corte del tramo (a la altura del plano)
    for sg in (-1, 1):
        for k in range(nps + 1):
            r = ra + k * huella
            hw = r * math.sin(E.ESC_HB) - 0.35
            p, q = E.esc_ang_pt(r, sg * 0.15 / r), E.esc_ang_pt(r, sg * hw / r)
            arr = sg < 0 and r > rc                                # tramo de subida por encima del corte: discontinuo
            ax.plot([p[0], q[0]], [p[1], q[1]], color=K, lw=0.45, ls=(0, (3, 2)) if arr else "-", zorder=79)
    a, b = E.esc_ang_pt(ra, 0), E.esc_ang_pt(rb, 0)
    ax.plot([a[0], b[0]], [a[1], b[1]], color=K, lw=0.9, zorder=79)                        # muro central (ojo)
    # flecha "sube" en el tramo de un lado y vuelta en el otro
    s = -1
    pa = E.esc_ang_pt(ra + 0.2, s * 1.0 / ra); pb = E.esc_ang_pt(rc, s * 1.0 / rc)
    ax.add_patch(FancyArrowPatch(pa, pb, arrowstyle="-|>", mutation_scale=6, color=K, lw=0.5, zorder=80))
    ax.add_patch(Circle(pa, 0.18, fc=K, ec=K, zorder=80))
    ax.text(*E.esc_ang_pt((ra + rc) / 2, s * 2.2 / ((ra + rc) / 2)), "sube", fontsize=4.5, ha="center", zorder=80)
    # línea de corte en zigzag
    hw = rc * math.sin(E.ESC_HB) - 0.3
    z1 = E.esc_ang_pt(rc - 0.4, -hw / rc); z2 = E.esc_ang_pt(rc - 0.1, -hw / 2 / rc); z3 = E.esc_ang_pt(rc + 0.1, -hw / 2 / rc)
    z4 = E.esc_ang_pt(rc + 0.4, -0.1 / rc)
    ax.plot([z1[0], z2[0], z3[0], z4[0]], [z1[1], z2[1], z3[1], z4[1]], color=K, lw=0.7, zorder=80)
    for rr in (ra, rb):                                            # rellanos
        p = E.esc_ang_pt(rr - 0.6 if rr == ra else rr + 0.6, 0)
        ax.text(*p, "rell.", fontsize=3.8, ha="center", va="center", zorder=80)


def proyecciones(ax, zc):
    """vuelos por encima del corte, en discontinua gruesa y rotulados"""
    if zc is None:
        return
    V = E._v; T = np.array(E.T)
    sty = dict(fill=False, ec="0.25", lw=0.8, ls=(0, (6, 3)), zorder=6)
    items = []
    if zc < E.Z_B0:
        items.append(("vuelo del barril", Circle(T, E.R_AL, **sty), T + np.array([0, -E.R_AL - 1.2])))
    if zc < E.Z_G1:
        pv = np.array(E.P(*E.OFF_V))
        items.append(("visera desplazada", Circle(pv, E.R_V, **sty), pv + np.array([E.R_V * 0.7, E.R_V * 0.75])))
    if zc < E.Z_PB:
        poly, _ = E.curva_poligono()
        items.append(("planta 1 / meseta (por encima)", Polygon(poly, closed=True, **sty), np.array(poly[3]) + np.array([0.6, -1.0])))
    if zc < E.Z_BAR:
        yb0 = T[1] + V["ESC_R1"] + 0.3
        items.append(("vuelo de la cubierta del bar", Rectangle((E.W_BAR, yb0 + V["R2_L"]), V["V_BAR"], E.L_L - V["L_FIN"] - yb0 - V["R2_L"], **sty),
                      np.array([E.W_BAR + V["V_BAR"] + 0.3, E.L_L - V["L_FIN"] - 6])))
    for t, patch, pos in items:
        ax.add_patch(patch)
        ax.text(pos[0], pos[1], t, fontsize=4.5, style="italic", color="0.25", zorder=81)


def dibujar(ax, zc):
    if zc is None or zc < E.Z_B0:
        rampas(ax, zc)
    escalera(ax, zc)
    proyecciones(ax, zc)
