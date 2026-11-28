"""SALUT COMPLETO (detalle completo): exporta el modelo de máximo detalle como Salut_completo.stl (15 cm de alto, 1:339)
y su versión ligera Salut_completo_ENVIO.stl. Pasa la misma comprobación que los STL de molde (stl_limpio).
Un solo cuerpo: las piezas que no están unidas al edificio se quitan antes de exportar y se listan."""
import os
import numpy as np, trimesh
import edificio as E, stl_limpio as SL

K = 150.0 / E.Z_R1                                    # mm de STL por metro real


def cuerpo_unico(V, F, nombre):
    """Devuelve solo el cuerpo principal; cada pieza suelta se quita y se imprime con su posición en metros reales."""
    V2, _ = SL.separar_contactos(V, F)
    t = trimesh.Trimesh(V2, F, process=True)
    partes = sorted(t.split(only_watertight=False), key=lambda p: -len(p.faces))
    for p in partes[1:]:
        b = p.bounds / K
        print("%s: quitada pieza suelta x %.2f..%.2f y %.2f..%.2f z %.2f..%.2f m (%d caras)"
              % (nombre, b[0][0], b[1][0], b[0][1], b[1][1], b[0][2], b[1][2], len(p.faces)), flush=True)
    return partes[0].vertices, partes[0].faces


m = E.edificio()
me = m.to_mesh(); Vc, Fc = cuerpo_unico(np.asarray(me.vert_properties)[:, :3] * K, np.asarray(me.tri_verts), "completo")
trimesh.Trimesh(Vc, Fc, process=False).export("Salut_completo.stl")
print("completo:", SL.comprobar("Salut_completo.stl"), flush=True)
q = m.set_tolerance(0.004); mq = q.to_mesh()
Vq, Fq = cuerpo_unico(np.asarray(mq.vert_properties)[:, :3] * K, np.asarray(mq.tri_verts), "envío")
trimesh.Trimesh(Vq, Fq, process=False).export("Salut_completo_ENVIO.stl")
c = SL.comprobar("Salut_completo_ENVIO.stl")
print("envío:", c, "%.2f MB" % (os.path.getsize("Salut_completo_ENVIO.stl") / 1e6), flush=True)
