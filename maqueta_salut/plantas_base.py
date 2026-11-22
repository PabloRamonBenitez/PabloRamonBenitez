"""Plantas de la base junto a la torre, dibujadas desde los mismos poligonos que generan el modelo 3D.
Planta baja (corte +1,5) y planta primera (corte +6,0), con proyecciones; y seccion por el hotel."""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
from matplotlib.backends.backend_pdf import PdfPages
import salut_v2 as s
import planos as P

pl = s.plantas()
CEN = s.CEN
XLIM, YLIM = (-27, 24), (-10, 32)


def poli(ax, pts, **kw):
    ax.add_patch(Polygon(pts, closed=True, **kw))


def proyecciones(ax):
    for r, ls, nom in ((s.R_B, "--", "barril"), (s.R_CUELLO, ":", "cuello")):
        ax.add_patch(Circle(CEN, r, fc="none", ec="0.45", lw=0.7, ls=ls))
    for poly in P.Ms.slice(25.0).to_polygons():                        # caja de escalera (y aletas) a +25
        P_ = np.array(poly)
        if np.max(np.hypot(P_[:, 0] - CEN[0], P_[:, 1] - CEN[1])) > s.R_B + 0.6 or len(P_) < 6:
            ax.add_patch(Polygon(P_, closed=True, fc="none", ec="0.45", lw=0.5, ls="--"))
    ax.add_patch(Circle(CEN, s.R_COL, fc="0.35", ec="k", lw=1.0))      # columna (cortada)
    ax.plot(*CEN, "w+", ms=8)


def acabado(ax, titulo):
    ax.set_xlim(*XLIM); ax.set_ylim(*YLIM); ax.set_aspect("equal"); ax.grid(True, lw=0.25)
    ax.set_title(titulo, fontsize=10, loc="left")
    ax.text(-2, -8.5, "CALLE / PLAZA", fontsize=8, style="italic")


def main():
    PB, P1, C, Q = pl["PB"], pl["P1"], pl["C"], pl["Q"]
    with PdfPages("Hotel_Salut_plantas_base.pdf") as pdf:
        fig, axs = plt.subplots(1, 2, figsize=(19, 9.2))
        # ------------------- PLANTA BAJA -------------------
        ax = axs[0]
        poli(ax, PB, fc="#f2c4bd", ec="k", lw=1.3)
        poli(ax, P1, fc="none", ec="green", lw=0.9, ls="--")                       # planta primera encima
        ramp = [pl["G_c"], pl["G_r"], (s.W_L, pl["G_r"][1] + 0.2), (s.W_P, s.L_L - 35)]
        poli(ax, [pl["G_c"], pl["G_r"], (s.W_P, s.L_L - 35)], fc="#d9d9d9", ec="k", lw=0.8)  # rampa
        for xp in (-s.L_C + 0.6, -s.L_C + 4.4):
            for yp in (0.6, s.W_C - 0.6):
                ax.add_patch(plt.Rectangle((xp - 0.4, yp - 0.4), 0.8, 0.8, fc="k"))
        poli(ax, [(-s.L_C + 5, 5.5), (-2.5, 5.5), (-2.5, s.W_C), (-s.L_C + 5, s.W_C)], fc="none", ec="k", lw=0.5, ls=":")
        proyecciones(ax)
        P.cota(ax, PB[1], PB[2], "PB fachada chaflan", off=2.2)
        P.cota(ax, (PB[0][0], RETR := s.RETR), PB[1], "PB fachada calle", off=2.2)
        P.cota(ax, (P1[1][0], 0), (P1[1][0], s.RETR), "vuelo P1", off=-2.5)
        ax.text(*np.add(pl["G_c"], (0.4, 6)), "rampa", fontsize=7, rotation=90)
        ax.text(-s.L_C + 0.3, 5.5, "ladrillo\nsobre pilares", fontsize=6.5)
        ax.text(-14, 9, "bloque alto (+12)", fontsize=6.5)
        acabado(ax, "PLANTA BAJA (+1,5). Rosa: cortado. Verde discontinuo: planta primera encima. Gris: torre encima")
        # ------------------- PLANTA PRIMERA -------------------
        ax = axs[1]
        poli(ax, P1, fc="#c9e6c9", ec="k", lw=1.3)
        poli(ax, PB, fc="none", ec="red", lw=0.9, ls="--")                          # planta baja debajo
        poli(ax, [pl["G_c"], pl["G_r"], (s.W_P, s.L_L - 35)], fc="#d9d9d9", ec="k", lw=0.8)
        proyecciones(ax)
        P.cota(ax, P1[1], s.solar(-s.R_COL, -s.RET), "P1 restaurante", off=2.2)
        P.cota(ax, s.solar(s.R_COL, -s.RET), C, "P1 hotel", off=2.2)
        P.cota(ax, C, Q, "cara 90", off=-1.8)
        P.cota(ax, (s.W_P, Q[1] + 1.5), (s.W_L, Q[1] + 1.5), "rampa", off=1.5)
        P.cota(ax, s.solar(-s.R_COL, -s.RET - 3.2), s.solar(s.R_COL, -s.RET - 3.2), "columna", off=0)
        acabado(ax, "PLANTA PRIMERA (+6,0). Verde: cortado. Rojo discontinuo: planta baja debajo")
        pdf.savefig(fig); fig.savefig("Hotel_Salut_plantas_base.png", dpi=100); plt.close(fig)
        # ------------------- SECCION POR EL HOTEL -------------------
        fig, axs = plt.subplots(1, 2, figsize=(19, 9.2), gridspec_kw=dict(width_ratios=[1, 1.4]))
        p0, p1 = s.solar(7.5, -12), s.solar(7.5, 26)
        ax = axs[0]
        poli(ax, P1, fc="#c9e6c9", ec="k", lw=1); proyecciones(ax)
        ax.plot(*zip(p0, p1), "k-.", lw=1.2)
        for pp in (p0, p1):
            ax.text(*pp, "S", fontsize=13, weight="bold")
        acabado(ax, "Situacion de la seccion S-S (por la banda del hotel, perpendicular al chaflan)")
        P.seccion(axs[1], p0, p1, "SECCION S-S (izquierda = plaza)")
        axs[1].set_ylim(-1, 52); axs[1].set_yticks(range(0, 52, 2)); axs[1].grid(True, lw=0.25)
        pdf.savefig(fig); fig.savefig("Hotel_Salut_seccion_hotel.png", dpi=100); plt.close(fig)


if __name__ == "__main__":
    main()
