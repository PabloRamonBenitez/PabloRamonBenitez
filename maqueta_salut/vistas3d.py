"""3D del cuadro actual: STL a 15 cm y vistas desde los puntos de vista de las fotos (lado a lado con ellas)."""
import math, numpy as np, trimesh, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import edificio as E, lineas as L
I = '/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'
m = E.edificio()
# STL a 15 cm de altura total
me = m.to_mesh(); Vv = np.asarray(me.vert_properties)[:, :3]; F = np.asarray(me.tri_verts)
k = 150.0 / E.Z_R1
trimesh.Trimesh(Vv * k, F).export("Hotel_Salut_15cm_v3.stl")
print("STL: Hotel_Salut_15cm_v3.stl  escala 1:%d" % round(1000 / k))
def orientar(m, az, el):
    """vista desde la dirección (az grados desde +x, el elevación): devuelve el modelo girado para mirar hacia -z"""
    a, e = math.radians(az), math.radians(el)
    v = np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])
    r = np.cross([0, 0, 1], v); r /= np.linalg.norm(r); u = np.cross(v, r)
    R = np.vstack([r, u, v])
    return m.transform(np.hstack([R, np.zeros((3, 1))]).tolist())
VISTAS = [("desde el patio (como F08 / F07)", 125, 22, ["8.webp", "7.webp"]),
          ("desde el testero del ala larga, lado exterior (como F73)", 80, 4, ["73.webp"]),
          ("frontal elevada desde la plaza (como F01)", -40, 25, ["1.webp"]),
          ("cenital (como F36 / F62)", 0, 89.9, ["36.webp"])]
for i, (t, az, el, fotos) in enumerate(VISTAS):
    fig = plt.figure(figsize=(16, 7))
    ax = fig.add_axes([0.01, 0.03, 0.48, 0.9]); L.dibujar_vista(ax, orientar(m, az, el), res=0.06); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(f"3D del cuadro actual – {t}", fontsize=10, loc="left")
    for j, f in enumerate(fotos):
        a2 = fig.add_axes([0.5 + j * 0.25, 0.03, 0.245 if len(fotos) > 1 else 0.49, 0.9]); a2.imshow(Image.open(I + f)); a2.axis("off"); a2.set_title("F" + f.split(".")[0], fontsize=9, loc="left")
    fig.savefig(f"VISTA3D_{i + 1}.png", dpi=80); plt.close(fig)
    print("vista", i + 1, t)
