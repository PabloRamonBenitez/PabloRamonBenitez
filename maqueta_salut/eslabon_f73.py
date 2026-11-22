"""F73 (ala larga desde su extremo): camara + posicion de la torre respecto al extremo del ala (D y E, a 17 m,
cara final perpendicular al ala; coronacion del peto ~+8,3). Comprueba si la solucion es fisica."""
import math, numpy as np, levantamiento as L
from scipy.optimize import least_squares
V=L.V; ZB1=V["Z_B0"]+V["N_PL"]*V["F"]; W,H=1816,1264; L.W,L.H=W,H
s=1/0.4956
TOR=[(V["R_AL"],ZB1+0.65,(120*s,362*s,205*s)),(V["R_AL"],V["Z_ALE"],(125*s,360*s,368*s)),(V["R_T"],(ZB1+V["Z_T1"])/2,(135*s,355*s,185*s)),
     (V["R_V"],(V["Z_G1"]+V["Z_V1"])/2,(128*s,345*s,155*s)),(V["R_R"],(V["Z_V1"]+V["Z_R1"])/2,(228*s,305*s,115*s))]
FORJ=[215*s,240*s,265*s,290*s,315*s,340*s]
PTS=[(np.array([0.0,0.0,8.3]),(525*s,255*s)),(np.array([-17.0,0.0,8.3]),(860*s,290*s))]   # D, E (ala hacia -y)
def res(x):
    k=L.cam(x[:8]); T=np.array(x[8:10]); r=[]
    for Rr,z,(xl,xr,y) in TOR:
        q=L.sil(k,T,Rr,z); r+=[q[0,0]-xl,q[1,0]-xr,(q[0,1]+q[1,1])/2-y]
    v=k[0][:2]-T; v/=np.linalg.norm(v)
    for j,yf in enumerate(FORJ):
        z=V["Z_B0"]+(6-j)*V["F"]; r.append(L.proj(k,np.array([*(T+v*(V["R_AL"]-0.9)),z]))[0,1]-yf)
    for P,px in PTS:
        q=L.proj(k,P)[0]; r+=[2*(q[0]-px[0]),2*(q[1]-px[1])]
    r.append((k[0][2]-1.7)*5)
    return np.array(r)
sols=[]
for az in range(-180,180,15):
    for ty in (-70,-95):
        for tx in (-15,5):
            x0=[az,2,120,0,-40,10,40,0,tx,ty]
            try: rr=least_squares(res,x0,bounds=([-200,-10,10,-80,-160,-10,10,-10,-60,-160],[200,45,600,80,40,60,100,10,60,0]),loss="soft_l1",f_scale=6)
            except Exception: continue
            sols.append((float(np.sqrt(np.mean(rr.fun**2))),rr.x))
sols.sort(key=lambda t:t[0])
for e,x in sols[:6]:
    print(f"error {e:5.1f} px · torre T=({x[8]:6.1f},{x[9]:6.1f}) · distancia D-torre {math.hypot(x[8],x[9]):5.1f} m · cámara az {x[0]:6.1f} h {L.cam(x[:8])[0][2]:4.1f}")
