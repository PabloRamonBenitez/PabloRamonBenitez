"""Planimetria completa del Hotel Salut generada desde el modelo (metros reales, coordenadas de solar):
plantas, secciones y alzados. Todo se dibuja a la misma escala grafica para poder comparar con las fotos."""
import math
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
from matplotlib.backends.backend_pdf import PdfPages
from manifold3d import Manifold
import trimesh
import salut_v2 as s

M = s.construir(escalar=False)
ANG = math.degrees(math.atan2(s._U[1], s._U[0]))
Ms = M.rotate((0, 0, ANG)).translate((s.CEN[0], s.CEN[1], 0))       # torre -> solar
_mesh = Ms.to_mesh()
T = trimesh.Trimesh(np.asarray(_mesh.vert_properties)[:, :3], np.asarray(_mesh.tri_verts), process=False)
N = np.array([s._N[0], s._N[1], 0.0])
NIVELES = [(0, "±0"), (s.Z_PB, "PB techo"), (s.Z_P1, "terraza"), (12.0, "bar / bloque alto"),
           (s.Z_HAB0, "1ª hab."), (s.Z_HAB1, "cubierta hab."), (s.Z_OJOS1, "tambor"), (s.Z_VIS1, "visera"),
           (s.Z_TOP1, "remate")]


# ----------------------------------------------------------------------------------------------- utilidades
def poligonos(m, z):
    return [np.array(p) for p in m.slice(z).to_polygons()]


def planta(ax, z, titulo, fc, encima=(), xlim=(-28, 34), ylim=(-12, 100)):
    for P in poligonos(Ms, z):
        ax.add_patch(Polygon(P, closed=True, fc=fc, ec="k", lw=0.9))
    for zz, ls in encima:
        for P in poligonos(Ms, zz):
            ax.add_patch(Polygon(P, closed=True, fc="none", ec="0.4", lw=0.5, ls=ls))
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal"); ax.grid(True, lw=0.2)
    ax.set_title(titulo, fontsize=9, loc="left")


def seccion(ax, p0, p1, titulo):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = p1 - p0; L = float(np.linalg.norm(d)); t = d / L
    a = math.degrees(math.atan2(t[1], t[0]))
    m = Ms.translate((-p0[0], -p0[1], 0)).rotate((0, 0, -a)).rotate((-90, 0, 0))
    detras = m ^ Manifold.cube((600, 600, 400)).translate((-300, -300, 0.01))
    for P in detras.project().to_polygons():
        ax.add_patch(Polygon(P, closed=True, fc="0.9", ec="0.6", lw=0.3, zorder=0))
    for P in m.slice(0.0).to_polygons():
        ax.add_patch(Polygon(P, closed=True, fc="0.25", ec="k", lw=0.6, zorder=2))
    ax.axhline(0, color="k", lw=1)
    for z, nom in NIVELES:
        if z <= 13 or "hab" in nom:
            ax.axhline(z, color="tab:blue", lw=0.25, ls=":")
            ax.text(L + 0.5, z, f"+{z:.1f} {nom}".replace(".", ","), fontsize=5.5, color="tab:blue", va="center")
    ax.set_xlim(-2, L + 9); ax.set_ylim(-1, 52); ax.set_aspect("equal"); ax.grid(True, lw=0.2)
    ax.set_title(titulo, fontsize=8.5, loc="left")


def alzado(ax, d, titulo, res=0.1):
    """vista ortogonal horizontal mirando en la direccion d (x,y); eje horizontal = d x z"""
    d = np.array([d[0], d[1], 0.0]); d /= np.linalg.norm(d)
    r = np.array([d[1], -d[0], 0.0])
    V = T.vertices
    X, Z, D = V @ r, V[:, 2], V @ d
    x0, x1 = X.min() - 1, X.max() + 1
    W, H = int((x1 - x0) / res) + 1, int((Z.max() + 1) / res) + 1
    zb = np.full((H, W), np.inf); img = np.ones((H, W))
    nrm = T.face_normals
    luz = -d + np.array([0.35, 0.25, 0.55]); luz /= np.linalg.norm(luz)
    sh = 0.35 + 0.65 * np.clip(nrm @ luz, 0, 1)
    vis = nrm @ d < 0
    px, py = (X - x0) / res, (Z.max() + 1 - Z) / res
    for f, c in zip(T.faces[vis], sh[vis]):
        x, y, z = px[f], py[f], D[f]
        xa, xb = max(int(x.min()), 0), min(int(x.max()) + 1, W - 1)
        ya, yb = max(int(y.min()), 0), min(int(y.max()) + 1, H - 1)
        if xb < xa or yb < ya: continue
        XX, YY = np.meshgrid(np.arange(xa, xb + 1) + 0.5, np.arange(ya, yb + 1) + 0.5)
        den = (y[1] - y[2]) * (x[0] - x[2]) + (x[2] - x[1]) * (y[0] - y[2])
        if abs(den) < 1e-12: continue
        l0 = ((y[1] - y[2]) * (XX - x[2]) + (x[2] - x[1]) * (YY - y[2])) / den
        l1 = ((y[2] - y[0]) * (XX - x[2]) + (x[0] - x[2]) * (YY - y[2])) / den
        l2 = 1 - l0 - l1
        m = (l0 >= -1e-6) & (l1 >= -1e-6) & (l2 >= -1e-6)
        ZZ = l0 * z[0] + l1 * z[1] + l2 * z[2]
        sub = zb[ya:yb + 1, xa:xb + 1]; m &= ZZ < sub
        sub[m] = ZZ[m]; img[ya:yb + 1, xa:xb + 1][m] = c
    Dz = zb.copy(); fondo = ~np.isfinite(Dz); Dz[fondo] = np.nanmax(Dz[~fondo]) + 20
    gx = np.abs(np.diff(Dz, axis=1, prepend=Dz[:, :1])); gy = np.abs(np.diff(Dz, axis=0, prepend=Dz[:1]))
    img[np.maximum(gx, gy) > 0.2] *= 0.35
    img[fondo] = 1.0
    ax.imshow(img, cmap="gray", vmin=0, vmax=1, extent=(x0, x1, 0 - 0.0, Z.max() + 1), origin="upper",
              interpolation="nearest")
    for z, nom in NIVELES:
        ax.axhline(z, color="tab:blue", lw=0.25, ls=":")
        ax.text(x1 + 0.5, z, f"+{z:.1f} {nom}".replace(".", ","), fontsize=5.5, color="tab:blue", va="center")
    ax.set_xlim(x0, x1 + 12); ax.set_ylim(0, Z.max() + 2); ax.set_aspect("equal"); ax.grid(True, lw=0.15)
    ax.set_title(titulo, fontsize=8.5, loc="left")


def linea(ax, p, q, nom):
    ax.plot(*zip(p, q), "-.", color="crimson", lw=0.8)
    ax.text(*p, nom, color="crimson", fontsize=8, weight="bold", ha="center", va="center")
    ax.text(*q, nom, color="crimson", fontsize=8, weight="bold", ha="center", va="center")


SECC = {
    "B1": ((-6, 17.5), (22, 17.5), "ala larga junto a la torre (por la rampa)"),
    "B2": ((-6, 36.0), (22, 36.0), "ala larga por las ventanas"),
    "B3": ((-6, 62.0), (22, 62.0), "ala larga por el bar (centro)"),
    "B4": ((-6, 91.0), (22, 91.0), "ala larga, tramo final sin bar"),
    "BL": ((3.0, -6), (3.0, 100), "longitudinal del ala larga (por el bar)"),
    "A1": ((-21.5, -6), (-21.5, 16), "ala corta: bloque de ladrillo"),
    "A2": ((-12.0, -6), (-12.0, 16), "ala corta: restaurante + bloque alto"),
    "A3": ((-4.0, -6), (-4.0, 16), "ala corta junto a la torre"),
    "AL": ((-28, 8.5), (8, 8.5), "longitudinal del ala corta"),
    "T": (tuple(np.add(s.CEN, -16 * np.array(s._N))), tuple(np.add(s.CEN, 26 * np.array(s._N))),
          "por el eje de la torre, perpendicular al chaflan"),
}


def main():
    out = "Hotel_Salut_planimetria_completa.pdf"
    with PdfPages(out) as pdf:
        # ---------------- hoja 1: plantas de la base ----------------
        fig, axs = plt.subplots(1, 3, figsize=(23, 13))
        planta(axs[0], 1.5, "PLANTA BAJA (+1,5)", "#f2c4bd", encima=((6.0, "--"), (20.0, ":")))
        planta(axs[1], 6.0, "PLANTA PRIMERA (+6,0)", "#c9e6c9", encima=((1.5, "--"), (20.0, ":")))
        base = Ms ^ Manifold.cube((400, 400, 15.0)).translate((-200, -200, 0))
        for z in np.arange(0.25, 15.0, 0.25):
            for P in poligonos(base, z):
                axs[2].add_patch(Polygon(P, closed=True, fc=str(0.95 - 0.045 * z), ec="none"))
        for P in base.project().to_polygons():
            axs[2].add_patch(Polygon(np.array(P), closed=True, fc="none", ec="k", lw=0.8))
        for P in poligonos(Ms, 20.0):
            axs[2].add_patch(Polygon(P, closed=True, fc="none", ec="0.4", lw=0.5, ls=":"))
        axs[2].set_xlim(-28, 34); axs[2].set_ylim(-12, 100); axs[2].set_aspect("equal"); axs[2].grid(True, lw=0.2)
        axs[2].set_title("CUBIERTAS DE LA BASE (tono = altura)", fontsize=9, loc="left")
        for k, (p, q, _) in SECC.items():
            linea(axs[2], p, q, k)
        fig.suptitle("Hotel Salut - plantas de la base (m). Discontinuo: plantas encima/debajo; punteado: barril", fontsize=11)
        pdf.savefig(fig); fig.savefig("plan_01_plantas_base.png", dpi=80); plt.close(fig)
        # ---------------- hoja 2: plantas de la torre ----------------
        fig, axs = plt.subplots(1, 3, figsize=(23, 9))
        lim = dict(xlim=(s.CEN[0] - 18, s.CEN[0] + 18), ylim=(s.CEN[1] - 18, s.CEN[1] + 18))
        planta(axs[0], s.Z_HAB0 + 3 * 3 + 1.0, "PLANTA TIPO DE HABITACIONES (+26)", "#dddddd", encima=((s.Z_HAB0 - 0.3, "--"),), **lim)
        planta(axs[1], s.Z_OJOS0 + 2.0, "TAMBOR DE LOS OJOS Y TERRAZA DE SERVICIO (+36)", "#dddddd", encima=((s.Z_HAB1 + 0.2, "--"), (s.Z_VIS1 - 0.5, ":")), **lim)
        planta(axs[2], s.Z_VID0 + 1.0, "BANDA ACRISTALADA, VISERA (punteado) Y LETRERO", "#dddddd", encima=((s.Z_VIS1 - 0.5, ":"), (s.Z_TOP0 + 1.5, "--")), **lim)
        pdf.savefig(fig); fig.savefig("plan_02_plantas_torre.png", dpi=80); plt.close(fig)
        # ---------------- hojas 3-4: secciones ----------------
        for grupo, nombre in ((("B1", "B2", "B3", "B4"), "plan_03_secciones_ala_larga.png"),
                              (("A1", "A2", "A3", "T"), "plan_04_secciones_ala_corta_torre.png")):
            fig, axs = plt.subplots(2, 2, figsize=(20, 14))
            for ax, k in zip(axs.ravel(), grupo):
                p, q, tit = SECC[k]
                seccion(ax, p, q, f"SECCION {k}: {tit}")
            pdf.savefig(fig); fig.savefig(nombre, dpi=80); plt.close(fig)
        fig, axs = plt.subplots(2, 1, figsize=(22, 13))
        for ax, k in zip(axs, ("BL", "AL")):
            p, q, tit = SECC[k]
            seccion(ax, p, q, f"SECCION {k}: {tit}")
        pdf.savefig(fig); fig.savefig("plan_05_secciones_longitudinales.png", dpi=80); plt.close(fig)
        # ---------------- hojas 6-7: alzados ----------------
        fig, axs = plt.subplots(2, 1, figsize=(22, 15))
        alzado(axs[0], (s._N[0], s._N[1]), "ALZADO DEL CHAFLAN (frontal, mirando hacia dentro)")
        alzado(axs[1], (0, 1), "ALZADO A LA CALLE DEL ALA CORTA (desde y<0)")
        pdf.savefig(fig); fig.savefig("plan_06_alzados_chaflan_calle.png", dpi=80); plt.close(fig)
        fig, axs = plt.subplots(2, 1, figsize=(22, 15))
        alzado(axs[0], (-1, 0), "ALZADO EXTERIOR DEL ALA LARGA (desde x>0, con la rampa)")
        alzado(axs[1], (1, 0), "ALZADO INTERIOR (patio de la L, desde x<0)")
        pdf.savefig(fig); fig.savefig("plan_07_alzados_ala_larga_patio.png", dpi=80); plt.close(fig)
    print("ok", out)


if __name__ == "__main__":
    main()
