import sys, trimesh, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
t = trimesh.load("Hotel_Salut_1-300.stl")
fig = plt.figure(figsize=(12, 6), dpi=110)
for i, (el, az) in enumerate([(18, -60), (12, 200)]):
    ax = fig.add_subplot(1, 2, i + 1, projection="3d")
    tri = t.vertices[t.faces]
    light = np.array([0.4, -0.6, 0.7]); light /= np.linalg.norm(light)
    sh = 0.35 + 0.65 * np.clip(t.face_normals @ light, 0, 1)
    pc = Poly3DCollection(tri, facecolors=np.c_[sh, sh, sh*0.97], edgecolor="none")
    ax.add_collection3d(pc)
    b = t.bounds; c = b.mean(0); r = (b[1]-b[0]).max()/2
    ax.set_xlim(c[0]-r, c[0]+r); ax.set_ylim(c[1]-r, c[1]+r); ax.set_zlim(0, 2*r)
    ax.view_init(el, az); ax.set_box_aspect((1,1,1)); ax.axis("off")
plt.suptitle("Hotel Salut 1:300 (edificio construido, cotas estimadas) - 196 x 74 x 103 mm")
plt.tight_layout(); plt.savefig("Hotel_Salut_vista_3D.png")
