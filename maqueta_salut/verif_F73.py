import json, numpy as np, verif_foto as VF, edificio as E
from collections import Counter
s=1/0.4956; V=E._v
tor=[("barril_sup",120*s,362*s,205*s),("barril_inf",125*s,360*s,368*s),("tambor",135*s,355*s,185*s),
     ("visera",128*s,345*s,155*s),("remate",228*s,305*s,115*s),("forj",[215*s,240*s,265*s,290*s,315*s,340*s])]
lin=[]
pts=[((V["W_P"],V["L_L"],E.Z_P1+V["H_PET"]),(1060,505)),((0.0,V["L_L"],V["Z_FIN"]),(1720,600))]
best,(W,H)=VF.calibrar("73.webp",tor,lin,hcam=1.7,az=(-180,180),el=(-10,40),fov=(10,90),pts=pts)
print("rms",round(best[0],1),np.round(best[1],2)); print(np.round(best[2],1).tolist())
json.dump(dict(foto="73.webp",rms=best[0],cam=list(map(float,best[1]))),open("cam_F73_verif.json","w"))
f=VF.verificar("F73","73.webp",best[1])
c=Counter((t[1],t[2]) for t in f)
for z in sorted(set(t[1] for t in f)):
    print(f"{z:22s}", {k:c[(z,k)] for k in ("OK","NO","oculto","fuera") if c[(z,k)]})
