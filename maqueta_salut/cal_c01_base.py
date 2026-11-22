"""C01: la torre es simetrica y no fija el azimut; se calibra con torre + aristas de la base y se superpone."""
import json, math, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from PIL import Image
import edificio as E, calib_e as C
I='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'
W,H=828,762; T=np.array([*E.T,0.0]); yf=-(E.R_COL-E.RET); pl=E.plantas_base()
TOR=[("barril_sup",170,550,262),("barril_inf",187,532,476),("columna_pie",322,388,652),("forj",[281.7,320,358.3,396.7,435,473]),("tambor",190,525,232)]
def P3(X,Y,z): p=E.P(X,Y); return np.array([p[0],p[1],z])
LIN=[(P3(-14,yf,E.Z_P1),P3(-4,yf,E.Z_P1),(170,567),(320,562)),
     (np.array([E.W_P,pl["Q"][1]+3,E.Z_P1+1]),np.array([E.W_P,E.L_L,E.Z_P1+1]),(552,425),(727,352))]
def dl(K,A,B,q):
    s=np.linspace(-0.3,1.3,161); Pm=A[None]*(1-s[:,None])+B[None]*s[:,None]; pr=C.proj(K,Pm)
    return float(np.min(np.hypot(pr[:,0]-q[0],pr[:,1]-q[1])))
def res(x):
    # x[8:10]: desplazamiento de la BASE respecto a la torre (m, en planta)
    K=C.cam(x[:8],W,H); r=list(C.residuos(x[:8],TOR,W,H)); d=np.array([x[8],x[9],0])
    for A,B,q0,q1 in LIN: r+=[2*dl(K,A+d,B+d,q0),2*dl(K,A+d,B+d,q1)]
    r+=[x[8]*1.0,x[9]*1.0]
    return np.array(r)
best=None
for az in range(-180,180,20):
  for el in (20,35):
    try: rr=least_squares(res,[az,el,250,T[0],T[1],22,20,0,0,0],bounds=([-200,5,60,T[0]-50,T[1]-50,-5,8,-8,-8,-8],[200,80,1500,T[0]+50,T[1]+50,60,60,8,8,8]),loss="soft_l1",f_scale=6)
    except Exception: continue
    e=float(np.sqrt(np.mean(rr.fun**2)))
    if best is None or e<best[0]: best=(e,rr.x,rr.fun)
print("rms",round(best[0],1),np.round(best[1],1)); print(np.round(best[2],1))
K=C.cam(best[1][:8],W,H)
print('desplazamiento base (m):',np.round(best[1][8:],2))
M=E.edificio(); tor=E.torre(); bas=E.base().translate((best[1][8],best[1][9],0))
e,_=C.aristas(tor+bas,K)
a=np.asarray(Image.open(I+"1.webp").convert("RGB")).astype(float)*0.8+40; a[e]=(255,0,0)
plt.figure(figsize=(11,10)); plt.imshow(a.astype(np.uint8)); plt.axis("off"); plt.title(f"C01 con cámara ajustada a torre + base (error {best[0]:.1f} px)",fontsize=10,loc="left")
plt.savefig("SUPERPOSICION_C01_base.png",dpi=75,bbox_inches="tight")
json.dump(dict(cam=list(map(float,best[1])),rms=best[0]),open("cam_C01_base.json","w"))
