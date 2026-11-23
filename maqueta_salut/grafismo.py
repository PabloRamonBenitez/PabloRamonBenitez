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
    # continuación en curva (meseta a +7,2) alrededor de la esquina
    poly, borde = E.curva_poligono()
    WR = E.W_EXT - E.W_P
    arco = np.array(borde[1:-1])
    A, B, C = arco[0], arco[len(arco) // 2], arco[-1]           # centro del arco (circuncentro)
    d_ = 2 * (A[0] * (B[1] - C[1]) + B[0] * (C[1] - A[1]) + C[0] * (A[1] - B[1]))
    ux = ((A @ A) * (B[1] - C[1]) + (B @ B) * (C[1] - A[1]) + (C @ C) * (A[1] - B[1])) / d_
    uy = ((A @ A) * (C[0] - B[0]) + (B @ B) * (A[0] - C[0]) + (C @ C) * (B[0] - A[0])) / d_
    cen = np.array([ux, uy]); Ro = np.linalg.norm(A - cen)
    eje = [tuple(cen + (p - cen) * (Ro - WR / 2) / Ro) for p in arco[::3]]
    eje = [(xr, y0)] + eje
    xs, ys = zip(*eje)
    ax.plot(xs, ys, color=K, lw=0.6, ls=(0, (5, 3)) if arriba else "-", zorder=81)
    ax.add_patch(FancyArrowPatch(eje[-2], eje[-1], arrowstyle="-|>", mutation_scale=7, color=K, lw=0.6, zorder=81))
    mm = eje[len(eje) // 2]
    ax.text(mm[0] + 1.2, mm[1], "meseta en curva +7,20\n(entrada del hotel debajo)".replace(".", ","), fontsize=4.6, zorder=81)
    # 2) techo del restaurante en rampa: +7,2 → +11,5
    yb0 = E.T[1] + V["ESC_R1"] + 0.3; xb = (E.W_BAR + V["V_BAR"]) / 2
    p2 = (E.Z_BAR_C - V["Z_P1"]) / V["R2_L"] * 100
    eje_rampa(ax, [(xb, yb0 + 0.3), (xb, yb0 + V["R2_L"])], V["Z_P1"], E.Z_BAR_C,
              f"TECHO DEL RESTAURANTE EN RAMPA · sube · P = {p2:.0f} %", discont=zc is not None and zc < E.Z_BAR_C)


def escalera(ax, zc):
    """escalera de ida y vuelta dentro de la cuña: dos tramos radiales separados por el muro central"""
    V = E._v
    if zc is None or zc >= V["ESC_Z1"]:
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
    if zc < V["Z_P1"] - V["E_PLAT"]:
        poly, _ = E.curva_poligono()
        items.append(("meseta en curva (por encima)", Polygon(poly, closed=True, **sty), np.array(poly[2]) + np.array([0.6, -1.0])))
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
