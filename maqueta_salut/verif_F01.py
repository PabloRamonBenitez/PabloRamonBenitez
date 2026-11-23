import json, numpy as np, verif_foto as VF, calib_e as C
tor=[("barril_sup",170,550,262),("barril_inf",187,532,476),("columna_pie",322,388,652),("forj",[281.7,320,358.3,396.7,435,473]),
     ("tambor",190,525,232),("remate",293,417,45)]
lin=[("banda_hotel",(431,538),(548,532)),("banda_rest",(156,566),(325,550))]
import edificio as E
V=E._v
pts=[((V["W_P"],V["L_L"],E.Z_P1+V["H_PET"]),(728,352)),((V["W_P"],V["L_L"],0.0),(727,458))]
best,(W,H)=VF.calibrar("1.webp",tor,lin,az=(-60,120),el=(5,75),fov=(8,60),pts=pts)
print("rms",round(best[0],1),np.round(best[1],2)); print(np.round(best[2],1))
json.dump(dict(foto="1.webp",rms=best[0],cam=list(map(float,best[1]))),open("cam_F01_verif.json","w"))
f=VF.verificar("F01","1.webp",best[1])
from collections import Counter
c=Counter((t[1],t[2]) for t in f)
for z in sorted(set(t[1] for t in f)):
    print(f"{z:22s}", {k:c[(z,k)] for k in ("OK","NO","oculto","fuera") if c[(z,k)]})
