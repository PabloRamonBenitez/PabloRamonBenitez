"""Eslabon 1 (F02): camara + torre respecto a A-B-C-D con B y C (cubierta del bloque alto) y siluetas de la torre.
Incluye factor de deformacion vertical (escaneo). Obtiene F y el extremo de la banda junto a la columna en +7,3."""
import math, numpy as np, levantamiento as L, lev3
from scipy.optimize import least_squares
V=L.V; ZB1=V["Z_B0"]+V["N_PL"]*V["F"]
W,H=1794,1170; L.W,L.H=W,H
TOR=[(V["R_AL"],ZB1+0.65,(780,1365,410)),(V["R_AL"],V["Z_ALE"],(795,1350,760)),(V["R_T"],(ZB1+V["Z_T1"])/2,(805,1332,385)),(V["R_R"],(V["Z_V1"]+V["Z_R1"])/2,(975,1198,180))]
FORJ=[427.5,482.5,537.5,592.5,647.5,702.5]
A,B,C=lev3.geom(0.0,1,1)
PTS={"B":(B,(701,850)),"C":(C,(884,839))}
def cam(x):
    k=L.cam(x[:8]); return k
def proj(k,P,asp):
    q=L.proj(k,P); q[:,1]=H/2+(q[:,1]-H/2)*asp; return q
def res(x):
    k=cam(x); T=np.array(x[8:10]); asp=x[10]; r=[]
    for Rr,z,(xl,xr,y) in TOR:
        P=np.array([T[0],T[1],z]); v=P-k[0]; h=np.array([v[0],v[1],0]); h/=np.linalg.norm(h); l=np.array([-h[1],h[0],0])
        q=proj(k,np.array([P+Rr*l,P-Rr*l]),asp); q=q[np.argsort(q[:,0])]; r+=[q[0,0]-xl,q[1,0]-xr,(q[0,1]+q[1,1])/2-y]
    v=k[0][:2]-T; v/=np.linalg.norm(v)
    for j,yf in enumerate(FORJ):
        z=V["Z_B0"]+(6-j)*V["F"]; r.append(proj(k,np.array([[*(T+v*(V["R_AL"]-0.9)),z]]),asp)[0,1]-yf)
    for n,(p,px) in PTS.items():
        q=proj(k,np.array([[p[0],p[1],11.5]]),asp)[0]; r+=[2*(q[0]-px[0]),2*(q[1]-px[1])]
    r.append((k[0][2]-1.6)*5)
    return np.array(r)
best=None
for az in range(-180,180,15):
    for ty in (-60,-90):
        x0=[az,0,250,C[0]/2,ty,20,20,0,C[0]/2,ty,1.0]
        try: rr=least_squares(res,x0,bounds=([-200,-10,40,-150,-160,-10,5,-10,-150,-160,0.85],[200,40,2000,150,160,60,70,10,150,160,1.15]),loss="soft_l1",f_scale=6)
        except Exception: continue
        e=float(np.sqrt(np.mean(rr.fun**2)))
        if best is None or e<best[0]: best=(e,rr.x,rr.fun)
e,x,f=best; k=cam(x); T=x[8:10]; asp=x[10]
print("F02: error %.1f px · deformación vertical %.3f · altura cámara %.1f"%(e,asp,k[0][2]))
print("  residuos torre", np.round(f[:18],0)); print("  residuos B,C", np.round(f[18:22]/2,1))
def ray(px,z):
    c,r,u,d,ff=k; yy=H/2+(px[1]-H/2)/asp; dv=d+r*(px[0]-W/2)/ff-u*(yy-H/2)/ff; t=(z-c[2])/dv[2]; return (c+t*dv)[:2]
F=ray((755,909),7.3); Fb=ray((976,907),7.3)
u=(C-L.D)/np.linalg.norm(C-L.D); n=np.array([-u[1],u[0]]); loc=lambda P: ((P-L.D)@u,(P-L.D)@n)
print("  marco D→C: torre (%.2f, %.2f) · F (%.2f, %.2f) · fin banda junto a columna (%.2f, %.2f)"%(*loc(T),*loc(F),*loc(Fb)))
np.save("eslabon1.npy",dict(x=x,T=T,F=F,Fb=Fb),allow_pickle=True)
