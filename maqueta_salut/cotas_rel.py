"""SISTEMA DE COTAS RELACIONADAS (planta ↔ sección ↔ alzado).

Una sola lista de EJES con nombre (en planta) y una sola lista de NIVELES (en altura). Cada vista los proyecta:
  - planta: ejes con burbuja y cadenas de cotas entre ejes;
  - sección / alzado: los mismos ejes como líneas de trazo y punto con la misma burbuja, cadena de cotas horizontal
    bajo la rasante (parciales entre ejes + total) y cadena vertical de niveles (parciales + total) en el margen.
Así una cota leída en planta se encuentra igual en la sección y en el alzado (Ching: vistas alineadas, transferencia
de medidas; normas: líneas de cota 0,2 mm, cotas de nivel referidas a ±0,00)."""
import math
import numpy as np
import edificio as E
import lineas as L

V = E._v
T = np.array(E.T); U = np.array(E.U); N = np.array(E.N)


def ejes():
    """[(nombre, punto, dirección del eje en planta)] – ejes verticales de referencia del edificio"""
    pl = E.plantas_base()
    out = [("T", T, U), ("T'", T, N),                                  # ejes de la torre (paralelo y perpendicular al chaflán)
           ("A", np.array(E.A1), N), ("C", np.array(E.C), N),          # arranque y fin del chaflán
           ("1", np.array((0.0, pl["Q"][1])), np.array((1.0, 0.0))),   # encuentro ala larga – esquina
           ("2", np.array((0.0, E.Y_CUNA)), np.array((1.0, 0.0))),     # pie de la concha
           ("3", np.array((0.0, V["L_L"] - V["L_FIN"])), np.array((1.0, 0.0))),   # fin del bar
           ("4", np.array((0.0, V["L_L"])), np.array((1.0, 0.0))),     # testero
           ("a", np.array((0.0, 0.0)), np.array((0.0, 1.0))),          # fachada al patio del ala larga
           ("b", np.array((V["W_P"], 0.0)), np.array((0.0, 1.0))),     # fachada exterior del ala larga
           ("M", np.array(E.SWP(-V["L_C"], 0)), np.array(E.SWP(-V["L_C"], 1)) - np.array(E.SWP(-V["L_C"], 0)))]   # medianera
    return out


def niveles():
    return sorted({0.0: "±0,00", E.Z_PB: "techo PB", E.Z_P1: "terraza / planta 1", E.Z_ALTO: "bar / bloque alto",
                   V["Z_CU0"]: "base del cuello", E.Z_B0: "1.ª planta hab.", E.Z_B1: "cubierta del barril", E.Z_T1: "tambor",
                   E.Z_G1: "banda / intradós visera", E.Z_V1: "visera", E.Z_R1: "remate"}.items())


def _u(p, p0, d):
    return float((np.asarray(p, float) - p0) @ d)


def proyectar(p0, d, n, extra=()):
    """posición (u) de cada eje que corta la línea de vista (p0, d): un eje es una recta en planta; se toma su cruce"""
    out = []
    for nom, q, e in ejes():
        e = np.asarray(e, float); e = e / np.linalg.norm(e)
        den = d[0] * e[1] - d[1] * e[0]
        if abs(den) < 0.2: continue                              # eje casi paralelo a la vista: no se ve como línea
        w = q - p0; s = (w[0] * e[1] - w[1] * e[0]) / den
        out.append((nom, s))
    return out + list(extra)


def dibujar(ax, p0, d, umin, umax, zmax=52.0, extra=(), xl=None):
    """ejes + cadena horizontal bajo rasante + cadena vertical de niveles, en una sección/alzado con eje horizontal u"""
    p0 = np.asarray(p0, float); d = np.asarray(d, float); d = d / np.linalg.norm(d); n = np.array([-d[1], d[0]])
    ejes_ = [(nm, u) for nm, u in proyectar(p0, d, n, ()) if umin - 0.5 <= u <= umax + 0.5]
    ext_ = [(nm, u) for nm, u in extra if umin - 0.5 <= u <= umax + 0.5]
    E_ = sorted(ejes_ + ext_, key=lambda t: t[1])
    # ejes con nombre: trazo y punto + burbuja; si dos burbujas se pisan (< 2 m), la segunda baja una fila (Ching: legibilidad)
    from matplotlib.patches import Circle
    filas = []
    for nm, u in sorted(ejes_, key=lambda t: t[1]):
        f = 0
        while any(abs(u - u2) < 1.9 and f == f2 for u2, f2 in filas): f += 1
        filas.append((u, f)); yb = -4.2 - 1.9 * f
        ax.plot([u, u], [yb + 0.85, zmax], color="k", lw=0.25, ls=(0, (10, 2, 1, 2)), zorder=2)
        ax.add_patch(Circle((u, yb), 0.85, fc="white", ec="k", lw=0.5, zorder=70))
        ax.text(u, yb, nm, fontsize=5.5, ha="center", va="center", zorder=71)
    # puntos de corte de la torre (columna, cuello, barril, tambor): solo un tic en la cadena, sin burbuja
    for nm, u in ext_:
        ax.plot([u, u], [-1.9, -1.3], color="k", lw=0.3, zorder=3)
    us = []
    for _, u in E_:                                             # cadena sin tramos de menos de 0,3 m (puntos casi iguales)
        if not us or u - us[-1] > 0.3: us.append(u)
    if len(us) >= 2:
        for a, b in zip(us[:-1], us[1:]):
            if b - a > 0.3: L.cota(ax, (a, -1.6), (b, -1.6), 0.0, "", fs=4.6)
        L.cota(ax, (us[0], -2.6), (us[-1], -2.6), 0.0, "", fs=4.8)
    # cadena vertical de niveles en el margen derecho
    x = umin - 5.0                                              # a la izquierda (los niveles se rotulan a la derecha)
    zs = [z for z, _ in niveles()]
    for (z0, _), (z1, _) in zip(niveles()[:-1], niveles()[1:]):
        L.cota(ax, (x, z0), (x, z1), 0.0, "", fs=4.2)
    L.cota(ax, (x - 1.6, zs[0]), (x - 1.6, zs[-1]), 0.0, "", fs=4.6)
    for z, t in niveles():
        ax.plot([x - 2.2, x + 0.6], [z, z], color="k", lw=0.25, zorder=3)


def planta(ax):
    """ejes con burbuja en planta (los mismos de las secciones y alzados)"""
    from matplotlib.patches import Circle
    for nm, q, e in ejes():
        e = np.asarray(e, float); e = e / np.linalg.norm(e)
        a, b = q - e * 12, q + e * (110 if nm in ("a", "b") else 12)
        ax.plot(*zip(a, b), color="k", lw=0.25, ls=(0, (10, 2, 1, 2)), zorder=2)
        ax.add_patch(Circle(tuple(a - e * 0.9), 0.85, fc="white", ec="k", lw=0.5, zorder=70))
        ax.text(*(a - e * 0.9), nm, fontsize=5.5, ha="center", va="center", zorder=71)
    # cotas radiales de la torre (las mismas que en sección): columna, cuello, barril, tambor
    for r, t in ((E.R_COL, "columna"), (E.R_CU, "cuello"), (E.R_B, "barril"), (E.R_T, "tambor")):
        L.cota(ax, tuple(T), tuple(T - N * r), 0.0, "", fs=4.4)
