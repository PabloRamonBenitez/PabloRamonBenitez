"""PLANOS A4 MONTADOS COMO EN ARQUITECTURA: en cada hoja, sección longitudinal (arriba), planta (centro) y
alzado (abajo) a la MISMA escala y alineados en el mismo eje horizontal, con líneas de referencia que cruzan
los tres dibujos. Plantas completas en hojas aparte. Todo sale de la misma geometría (edificio.py / cotas.py)."""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
from matplotlib.backends.backend_pdf import PdfPages
import edificio as E
import laminas as LM
import lineas as L
import imprimir_a4 as IA

A4L = (297, 210)
ZL = (-1.0, 51.5)                       # rango vertical de alzados y secciones


def plan_girada(ax, zc, e):
    """planta dibujada con el eje horizontal = e (coordenada P·e) y vertical = n = e girado +90° (P·n)"""
    e = np.array(e, float); n = np.array([-e[1], e[0]])
    antes = set(ax.get_children())
    LM.planta(ax, zc, "")
    tr = Affine2D(np.array([[e[0], e[1], 0], [n[0], n[1], 0], [0, 0, 1]])) + ax.transData
    for a in set(ax.get_children()) - antes:
        try:
            a.set_transform(tr)
            a.set_clip_on(True)
        except Exception:
            pass
    return e, n


def referencias(axes, us, etiquetas):
    for ax in axes:
        for u in us:
            ax.axvline(u, color="0.55", lw=0.35, ls=(0, (6, 3)), zorder=0.5)
    for u, t in zip(us, etiquetas):
        axes[0].text(u, ZL[1] - 0.5, t, fontsize=4.5, color="0.35", ha="center", va="top", rotation=90)


def hoja_triple(titulo, e, u_rng, v_rng, secc, zc, d, t_alz, den, refs):
    """secc = (k, p0, p1, texto) con p1 - p0 en la dirección e; d = dirección de vista del alzado (e = (d_y, -d_x))"""
    fig = IA.pagina(A4L, titulo)
    w, h = fig._mm
    k = 1000 / den
    hz = (ZL[1] - ZL[0]) * k; hp = (v_rng[1] - v_rng[0]) * k; wd = (u_rng[1] - u_rng[0]) * k
    x0 = 14; gap = 3.5
    y_alz = 12; y_pl = y_alz + hz + gap; y_se = y_pl + hp + gap
    # sección
    k_, p0, p1, tx = secc
    p0, p1 = np.array(p0, float), np.array(p1, float)
    off = float(p0 @ np.array(e))
    ax_s = fig.add_axes([x0 / w, y_se / h, wd / w, hz / h])
    LM.seccion(ax_s, p0, p1, "")
    [t_.remove() for t_ in list(ax_s.texts) if t_.get_text().startswith('+')]; [l_.remove() for l_ in list(ax_s.lines) if (len(l_.get_xdata()) == 4 or (len(l_.get_xdata()) == 2 and abs(max(l_.get_xdata()) - min(l_.get_xdata()) - 1.2) < 0.05))]
    ax_s.set_xlim(u_rng[0] - off, u_rng[1] - off); ax_s.set_ylim(*ZL); ax_s.set_aspect("equal"); ax_s.axis("off")
    ax_s.text(u_rng[0] - off + 0.5, ZL[1] - 1, f"SECCIÓN {k_}", fontsize=6.5, weight="bold", va="top")
    # planta
    ax_p = fig.add_axes([x0 / w, y_pl / h, wd / w, hp / h])
    plan_girada(ax_p, zc, e)
    ee = np.array(e); nn = np.array([-e[1], e[0]])
    q0, q1 = p0 @ ee, p1 @ ee; v = p0 @ nn
    ax_p.plot([q0, q1], [v, v], "-.", color="crimson", lw=0.7, zorder=60)
    ax_p.text(q0, v + 0.8, k_, color="crimson", fontsize=6, weight="bold", zorder=61)
    ax_p.annotate("", xy=(u_rng[1] - 3, v_rng[0] + 0.5), xytext=(u_rng[1] - 3, v_rng[0] + 5),
                  arrowprops=dict(arrowstyle="-|>", lw=0.7))                          # dirección de vista del alzado
    ax_p.set_xlim(*u_rng); ax_p.set_ylim(*v_rng); ax_p.set_aspect("equal"); ax_p.axis("off")
    ax_p.add_patch(plt.Rectangle((u_rng[0], v_rng[0]), u_rng[1] - u_rng[0], v_rng[1] - v_rng[0], fill=False, lw=0.3, ec="0.6"))
    ax_p.text(u_rng[0] + 0.5, v_rng[1] - 1, f"PLANTA a +{zc:.2f}".replace(".", ","), fontsize=6.5, weight="bold", va="top")
    # alzado
    ax_a = fig.add_axes([x0 / w, y_alz / h, wd / w, hz / h])
    LM.alzado(ax_a, d, "")
    [t_.remove() for t_ in list(ax_a.texts) if t_.get_text().startswith('+')]; [l_.remove() for l_ in list(ax_a.lines) if (len(l_.get_xdata()) == 4 or (len(l_.get_xdata()) == 2 and abs(max(l_.get_xdata()) - min(l_.get_xdata()) - 1.2) < 0.05))]
    ax_a.set_xlim(*u_rng); ax_a.set_ylim(*ZL); ax_a.set_aspect("equal"); ax_a.axis("off")
    ax_a.text(u_rng[0] + 0.5, ZL[1] - 1, t_alz, fontsize=6.5, weight="bold", va="top")
    # referencias comunes (en coordenada mundo u para planta/alzado; desplazada en la sección)
    us = [r[0] for r in refs]
    for ax in (ax_p, ax_a):
        for u in us:
            ax.axvline(u, color="0.55", lw=0.35, ls=(0, (6, 3)), zorder=0.5)
    for u in us:
        ax_s.axvline(u - off, color="0.55", lw=0.35, ls=(0, (6, 3)), zorder=0.5)
    for u, t in refs:
        ax_s.text(u - off, ZL[1] - 0.3, t, fontsize=4.3, color="0.3", ha="center", va="top", rotation=90)
    # columna derecha: leyenda + niveles + cajetín
    xr = x0 + wd + 8
    fig.text(xr / w, (h - 18) / h, titulo, fontsize=8, weight="bold", va="top", wrap=True)
    fig.text(xr / w, (h - 26) / h,
             "Los tres dibujos están a la misma escala y alineados:\nla misma vertical de puntos cruza sección, planta y alzado.\n"
             f"Sección {k_}: {tx[:60]}\nPlanta: corte a +{zc:.2f}; flecha = vista del alzado.\n"
             "Trazo grueso con trama: cortado · fino: visto ·\ndiscontinuo: por encima.".replace(".", ",", 0), fontsize=5.3, va="top")
    niv = [(0, "±0,00"), (E.Z_PB, "techo PB"), (E.Z_P1, "terraza / planta 1"), (E.Z_BAR_C, "cub. bar / bloque alto"),
           (E.Z_B0, "1ª planta hab."), (E.Z_B1, "cubierta hab."), (E.Z_T1, "tambor"), (E.Z_V1, "visera"), (E.Z_R1, "remate")]
    fig.text(xr / w, (h - 62) / h, "Niveles:\n" + "\n".join(f"+{z:5.2f}  {t}".replace(".", ",") for z, t in niv), fontsize=5.2,
             va="top", family="monospace")
    IA.barra(fig, xr, 40, den, 20)
    IA.cajetin(fig, f"1:{den}")
    IA.PAGS.append(fig)


def hoja_transversal(den=600):
    """alzado 5 (testero) y secciones S3 y S4 lado a lado, misma escala y mismo eje horizontal (−x)"""
    titulo = "Testero y secciones transversales del ala larga (S3, S4)"
    fig = IA.pagina(A4L, titulo)
    w, h = fig._mm; k = 1000 / den
    u_rng = (-24.0, 14.0)                                   # u = −x
    wd = (u_rng[1] - u_rng[0]) * k; hz = (ZL[1] - ZL[0]) * k
    S = {kk: (kk, p0, p1, t) for kk, p0, p1, t in LM.SECC}
    paneles = [("ALZADO 5 – testero", None), ("SECCIÓN S3 (bar, terraza, concha)", S["S3"]), ("SECCIÓN S4 (huecos alto y bajo)", S["S4"])]
    for i, (t, sc) in enumerate(paneles):
        x0 = 14 + i * (wd + 6)
        ax = fig.add_axes([x0 / w, 60 / h, wd / w, hz / h])
        if sc is None:
            LM.alzado(ax, (0, -1), ""); off = 0.0
        else:
            _, p0, p1, _ = sc
            LM.seccion(ax, p1, p0, "")                      # de +x a −x: horizontal = −x
            off = -p1[0]
        [t_.remove() for t_ in list(ax.texts) if t_.get_text().startswith('+')]; [l_.remove() for l_ in list(ax.lines) if (len(l_.get_xdata()) == 4 or (len(l_.get_xdata()) == 2 and abs(max(l_.get_xdata()) - min(l_.get_xdata()) - 1.2) < 0.05))]
        ax.set_xlim(u_rng[0] - off, u_rng[1] - off); ax.set_ylim(*ZL); ax.set_aspect("equal"); ax.axis("off")
        for xw, tt in ((0.0, "fachada patio"), (E.W_P, "fachada ext."), (E.W_EXT, "concha")):
            ax.axvline(-xw - off, color="0.55", lw=0.35, ls=(0, (6, 3)), zorder=0.5)
            ax.text(-xw - off, ZL[1] - 0.3, tt, fontsize=4.3, color="0.3", ha="center", va="top", rotation=90)
        ax.text(u_rng[0] - off + 0.5, ZL[1] - 1, t, fontsize=6.5, weight="bold", va="top")
    fig.text(14 / w, 50 / h, "Los tres dibujos tienen el mismo eje horizontal (−x): las verticales discontinuas son las mismas fachadas en los tres.",
             fontsize=5.5)
    IA.barra(fig, 14, 40, den, 20)
    IA.cajetin(fig, f"1:{den}")
    IA.PAGS.append(fig)


if __name__ == "__main__":
    plt.rcParams["figure.max_open_warning"] = 0
    p = IA.portada(); IA.PAGS.append(p)
    S = {k: (k, p0, p1, t) for k, p0, p1, t in LM.SECC}
    T = np.array(E.T); U = np.array(E.U); N = np.array(E.N)
    pl = E.plantas_base(); V = E._v
    # 1) ala larga, fachada exterior: e = +y
    hoja_triple("ALA LARGA – sección L1, planta 1 y alzado 2 (fachada exterior)", (0, 1), (-14, 99), (-22, 12),
                S["L1"], 5.6, (-1, 0), "ALZADO 2 – fachada exterior", 800,
                [(T[1], "eje torre"), (pl["Q"][1], "esquina chaflán"), (E.ESC_Y1, "escalera"), (V["Y_CA"], "fin concha"),
                 (V["L_L"] - V["L_FIN"], "fin bar"), (V["L_L"], "testero")])
    # 2) ala larga, patio: e = −y (alzado desde el patio, d = +x)
    hoja_triple("ALA LARGA – sección L5 por el bar, planta 2 y alzado 4 (patio)", (0, -1), (-99, 14), (-14, 22),
                ("L5", (3.1, 100.0), (3.1, -14.0), "longitudinal por el bar, la escalera y la torre"), 9.2, (1, 0), "ALZADO 4 – patio interior", 800,
                [(-T[1], "eje torre"), (-E.ESC_Y1, "escalera"), (-(V["L_L"] - V["L_FIN"]), "fin bar"), (-V["L_L"], "testero")])
    # 3) chaflán: e = U, alzado frontal d = N
    hoja_triple("CHAFLÁN – sección L3, planta 0 y alzado 1 (frontal)", tuple(U), (T @ U - 38, T @ U + 34),
                (T @ N - 19, T @ N + 19), S["L3"], 1.8, tuple(N), "ALZADO 1 – chaflán", 800,
                [(T @ U, "eje torre"), (np.array(E.A1) @ U, "inicio chaflán"), (np.array(E.C) @ U, "fin chaflán")])
    # 4) ala corta / calle: e = +x, sección propia a lo largo de la calle por el bloque alto
    p0 = np.array(E.SWP(-E.L_C - 3, 8.0)); p1 = np.array(E.SWP(E.W_P + 18, 8.0))
    d_ = (p1 - p0) / np.linalg.norm(p1 - p0)
    hoja_triple("ALA CORTA – sección L4 a lo largo de la calle, planta 2 y alzado 3", tuple(d_), (-30, 36),
                (float(np.array([-d_[1], d_[0]]) @ T) - 22, float(np.array([-d_[1], d_[0]]) @ T) + 16),
                ("L4", tuple(p0), tuple(p1), "a lo largo del ala corta por el bloque alto y la torre"), 9.2, (-d_[1], d_[0]),
                "ALZADO 3 – calle", 800, [(T @ d_, "eje torre"), (np.array(E.SWP(-E.L_C, 0)) @ d_, "extremo ala corta")])
    hoja_transversal()
    for zc, t in [(1.8, "Planta 0 (baja) – corte a +1,80"), (5.6, "Planta 1 – corte a +5,60"),
                  (9.2, "Planta 2 – corte a +9,20 (terraza, bar, rampas)"), (13.0, "Planta 3 – corte a +13,00 (cuello)"),
                  (E.Z_B0 + 3 * E.F + 2.0, f"Planta tipo de habitaciones – corte a +{E.Z_B0 + 3 * E.F + 2.0:.2f}"),
                  (E.Z_B1 + 2.5, f"Planta última – tambor – corte a +{E.Z_B1 + 2.5:.2f}"), (None, "Planta de cubiertas")]:
        IA.hoja_planta(zc, t.replace(".", ","))
    IA.hoja_detalles()
    p.text(15 / 297, 163 / 210, "Índice", fontsize=9, weight="bold")
    for i, t in enumerate(IA.INDICE):
        p.text(15 / 297, (156 - i * 6.6) / 210, f"{i + 1:02d}   {t}", fontsize=6.5)
    with PdfPages("SALUT_planos_A4.pdf") as pdf:
        for i, f in enumerate(IA.PAGS):
            pdf.savefig(f)
    print("páginas:", len(IA.PAGS))
