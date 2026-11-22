import numpy as np, trimesh, edificio as E
m = E.edificio()
me = m.to_mesh(); V = np.asarray(me.vert_properties)[:, :3]; F = np.asarray(me.tri_verts)
f = 150.0 / (V[:, 2].max() - V[:, 2].min())
t = trimesh.Trimesh(V * f, F, process=False)
t.export("Hotel_Salut_15cm.stl")
print("escala 1:%d" % round(1000 / f), "caja mm", np.round(t.bounds[1] - t.bounds[0], 1), "estanco", t.is_watertight)
