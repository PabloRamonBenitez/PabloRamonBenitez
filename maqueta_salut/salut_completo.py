"""SALUT COMPLETO (detalle completo): exporta el modelo de máximo detalle como Salut_completo.stl (15 cm de alto, 1:339)
y su versión ligera Salut_completo_ENVIO.stl. Pasa la misma comprobación que los STL de molde (stl_limpio)."""
import os
import numpy as np, trimesh
import edificio as E, stl_limpio as SL

m = E.edificio(); k = 150.0 / E.Z_R1
me = m.to_mesh(); V = np.asarray(me.vert_properties)[:, :3] * k; F = np.asarray(me.tri_verts)
V2, mov = SL.separar_contactos(V, F)
trimesh.Trimesh(V2, F, process=False).export("Salut_completo.stl")
print("completo:", SL.comprobar("Salut_completo.stl"), flush=True)
q = m.set_tolerance(0.004); mq = q.to_mesh()
Vq, _ = SL.separar_contactos(np.asarray(mq.vert_properties)[:, :3] * k, np.asarray(mq.tri_verts))
trimesh.Trimesh(Vq, np.asarray(mq.tri_verts), process=False).export("Salut_completo_ENVIO.stl")
c = SL.comprobar("Salut_completo_ENVIO.stl")
print("envío:", c, "%.2f MB" % (os.path.getsize("Salut_completo_ENVIO.stl") / 1e6), flush=True)
