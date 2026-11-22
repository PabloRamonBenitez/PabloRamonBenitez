"""Calibra una foto (modelo CONGELADO) con torre + aristas de la base; guarda residuos y superposicion. NO modifica el modelo."""
import sys, json, math, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from PIL import Image
import edificio as E, calib_e as C
I='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'
yf=-(E.R_COL-E.RET); pl=E.plantas_base()
def P3(X,Y,z): p=E.P(X,Y); return np.array([p[0],p[1],z])
GEO={ # aristas 3D de la base con nombre
 "peto_ala": (np.array([E.W_P,pl["Q"][1]+3,E.Z_P1+1]),np.array([E.W_P,E.L_L,E.Z_P1+1])),
 "banda_rest": (P3(-14,yf,E.Z_P1),P3(-4,yf,E.Z_P1)),
 "banda_hotel": (P3(4,yf,E.Z_P1),P3(E.R_COL+E.HOT,yf,E.Z_P1)),
}
PTS={"fin_ala":np.array([E.W_P,E.L_L,E.Z_P1+1]), "esquina_hotel":np.array([*pl["P1"][2],E.Z_P1])}
def dl(K,A,B,q):
    s=np.linspace(-0.3,1.3,161); Pm=A[None]*(1-s[:,None])+B[None]*s[:,None]; pr=C.proj(K,Pm)
    return float(np.min(np.hypot(pr[:,0]-q[0],pr[:,1]-q[1])))
def run(nombre, foto, tor, lin, pts, hcam=None, az=(-180,180), el=(-60,85), fov=(5,100)):
    W,H=Image.open(I+foto).size; T=np.array(E.T)
    def res(x):
        K=C.cam(x,W,H); r=list(C.residuos(x,tor,W,H))
        if hcam: r.append((K[0][2]-hcam)*5)
        for k,q0,q1 in lin: A,B=GEO[k]; r+=[dl(K,A,B,q0),dl(K,A,B,q1)]
        for k,q in pts: u=C.proj(K,PTS[k])[0]; r+=[u[0]-q[0],u[1]-q[1]]
        return np.array(r)
    best=None
    for a in np.arange(az[0],az[1],20):
      for e in (el[0]+5,(el[0]+el[1])/2):
        for f in (fov[0]+5,(fov[0]+fov[1])/2):
          try: rr=least_squares(res,[a,e,200,T[0],T[1],20,f,0],bounds=([az[0],el[0],15,T[0]-60,T[1]-60,-10,fov[0],-15],[az[1],el[1],3000,T[0]+60,T[1]+60,70,fov[1],15]),loss="soft_l1",f_scale=8)
          except Exception: continue
          ee=float(np.sqrt(np.mean(rr.fun**2)))
          if best is None or ee<best[0]: best=(ee,rr.x,rr.fun)
    x=best[1]; K=C.cam(x,W,H)
    lab=[]
    for o in tor: lab+= [o[0]]*(6 if o[0]=="forj" else 3)
    if hcam: lab.append("altura cámara")
    for k,_,_ in lin: lab+=[k]*2
    for k,_ in pts: lab+=[k]*2
    out={}
    for l,v in zip(lab,best[2]): out.setdefault(l,[]).append(round(float(v),1))
    e,_=C.aristas(E.edificio(),K)
    a=np.asarray(Image.open(I+foto).convert("RGB")).astype(float)*0.8+40; a[e]=(255,0,0)
    plt.figure(figsize=(12,11)); plt.imshow(a.astype(np.uint8)); plt.axis("off")
    plt.title(f"{nombre} ({foto}) – modelo congelado, cámara ajustada (error {best[0]:.1f} px)",fontsize=10,loc="left")
    plt.savefig(f"PASADA_{nombre}.png",dpi=70,bbox_inches="tight"); plt.close()
    R=json.load(open("PASADA.json")) if __import__("os").path.exists("PASADA.json") else {}
    R[nombre]=dict(foto=foto,rms=round(best[0],1),cam=list(map(float,x)),residuos=out); json.dump(R,open("PASADA.json","w"),indent=1)
    print(nombre,"rms",round(best[0],1)); [print("  ",k,v) for k,v in out.items()]
