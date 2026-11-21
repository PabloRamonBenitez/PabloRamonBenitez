"""Genera el modelo 3D (STL, en mm, escala 1:300) del Hotel Salut construido.
Usa la misma geometria estimada que el PDF (geometria.py)."""
import math
import numpy as np
import trimesh
from manifold3d import Manifold, CrossSection
from geometria import *

SEG = 160          # segmentos de las elipses
ALETA = 1.0        # grosor de los muros radiales en maqueta (mm)


def prisma_eliptico(a, b, z0, z1):
    cs = CrossSection.circle(1.0, SEG).scale((a, b))
    return Manifold.extrude(cs, z1 - z0).translate((0, 0, z0))


def caja(x0, x1, y0, y1, z0, z1):
    return Manifold.cube((x1 - x0, y1 - y0, z1 - z0)).translate((x0, y0, z0))


def construir():
    partes = []
    # B base cilindrica + A estilobato
    partes.append(prisma_eliptico(mm(BASE_R), mm(BASE_R), mm(BASE_Z0), mm(BASE_Z1)))
    partes.append(caja(mm(ESTI_X0) - 2, mm(ESTI_X1), -mm(ESTI_ANCHO) / 2, mm(ESTI_ANCHO) / 2, 0, mm(ESTI_H)))
    # C planta tecnica
    partes.append(prisma_eliptico(mm(TEC_A), mm(TEC_B), mm(TEC_Z0), mm(TEC_Z1)))
    # D plantas de habitaciones
    for p in PLANTAS:
        z0, z1 = mm(p["z0"]), mm(p["z1"])
        zl = z0 + mm(LOSA)
        a, b, fa, fb = mm(p["a"]), mm(p["b"]), mm(p["fa"]), mm(p["fb"])
        partes.append(prisma_eliptico(a, b, z0, zl))            # losa-balcon
        partes.append(prisma_eliptico(fa, fb, zl - 0.01, z1))    # fachada
        for k in range(N_MUROS):
            th = 2 * math.pi * k / N_MUROS
            ex, ey = a * math.cos(th), b * math.sin(th)
            L = math.hypot(ex, ey)
            ang = math.degrees(math.atan2(ey, ex))
            r0 = min(fa, fb) - 1.0
            aleta = (Manifold.cube((L - r0 - 0.05, ALETA, z1 - zl + 0.01))
                     .translate((r0, -ALETA / 2, zl - 0.01)).rotate((0, 0, ang)))
            partes.append(aleta)
    # cubierta + sala
    pu = PLANTAS[-1]
    partes.append(prisma_eliptico(mm(pu["a"]), mm(pu["b"]), mm(TECHO_Z) - 0.01, mm(TECHO_Z + CUBIERTA)))
    partes.append(prisma_eliptico(mm(SUP_A), mm(SUP_B), mm(SUP_Z0) - 0.01, mm(SUP_Z1)))
    modelo = partes[0]
    for p in partes[1:]:
        modelo = modelo + p
    return modelo


def a_trimesh(m):
    mesh = m.to_mesh()
    return trimesh.Trimesh(vertices=np.asarray(mesh.vert_properties)[:, :3],
                           faces=np.asarray(mesh.tri_verts), process=True)


if __name__ == "__main__":
    t = a_trimesh(construir())
    t.export("Hotel_Salut_1-300.stl")
    ext = t.bounds[1] - t.bounds[0]
    print("estanco:", t.is_watertight, " caja (mm):", np.round(ext, 1), " volumen cm3:", round(t.volume / 1000, 1))
