"""Superposicion del modelo COMPLETO sobre las fotos calibradas (camaras de la fase 1b)."""
import json, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import edificio as E, calib_e as C
I='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'
r=json.load(open('FASE1b_resultados.json')); M=E.edificio()
fig,axs=plt.subplots(1,3,figsize=(24,9))
for ax,(k,f) in zip(axs,(("C04","9.webp"),("C01","1.webp"),("C03","2.webp"))):
    W,H=Image.open(I+f).size; K=C.cam(r[k]["camara"],W,H)
    e,occ=C.aristas(M,K)
    a=np.asarray(Image.open(I+f).convert("RGB")).astype(float)*0.8+40; a[e]=(255,0,0)
    ax.imshow(a.astype(np.uint8)); ax.axis("off"); ax.set_title(f"{k} ({f}) – modelo completo en rojo (cámara calibrada con la torre)",fontsize=9,loc="left")
fig.tight_layout(); fig.savefig("SUPERPOSICION_final.png",dpi=70)
