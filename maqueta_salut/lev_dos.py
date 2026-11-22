"""Restitucion independiente en dos fotos (F01 y F23) con la misma planta de satelite A-B-C-D.
Si ambas dan la misma posicion de la torre, F y G respecto a A-B-C-D, el resultado es fiable."""
import math, numpy as np, levantamiento as L, lev3
from scipy.optimize import least_squares
V=L.V; ZB1=V["Z_B0"]+V["N_PL"]*V["F"]
FOT={"F01":dict(WH=(828,762),tor=[(V["R_AL"],ZB1+0.65,(170,550,262)),(V["R_AL"],V["Z_ALE"],(187,532,476)),(V["R_T"],(ZB1+V["Z_T1"])/2,(190,525,232)),(V["R_COL"],0.5,(322,388,652))],
            px=dict(A=(0,515),B=(54,524),C=(206,500),D=(722,353)),F=(153,575),G=(551,520)),
     "F23":dict(WH=(732,650),tor=[(V["R_AL"],ZB1+0.65,(228,500,300)),(V["R_AL"],V["Z_ALE"],(236,490,465)),(V["R_T"],(ZB1+V["Z_T1"])/2,(240,480,275))],
            px=dict(A=(83,481),B=(119,478),C=(244,467),D=(619,373)),F=(136,523),G=(497,453))}
def run(nombre):
    f=FOT[nombre]; L.W,L.H=f["WH"]
    def res(x):
        A,B,C=lev3.geom(x[10],1,1); P={"A":A,"B":B,"C":C,"D":L.D}
        k=L.cam(x[:8]); T=np.array(x[8:10]); r=[]
        for Rr,z,(xl,xr,y) in f["tor"]:
            q=L.sil(k,T,Rr,z); r+=[q[0,0]-xl,q[1,0]-xr,(q[0,1]+q[1,1])/2-y]
        for n,p in P.items():
            z=11.5 if n in "ABC" else 7.3; q=L.proj(k,np.array([p[0],p[1],z]))[0]; r+=[q[0]-f["px"][n][0],q[1]-f["px"][n][1]]
        return np.array(r)
    best=None
    for az in range(-180,180,20):
        for phi in np.radians([-40,-20,0]):
            A,_,_=lev3.geom(phi,1,1); x0=[az,30,200,A[0]/2,A[1]/2,20,25,0,A[0]/2,A[1]*0.8,phi]
            try: rr=least_squares(res,x0,bounds=([-200,5,50,-150,-160,-10,8,-10,-150,-160,-1.2],[200,85,1500,150,160,60,70,10,150,160,1.2]),loss="soft_l1",f_scale=6)
            except Exception: continue
            e=float(np.sqrt(np.mean(rr.fun**2)))
            if best is None or e<best[0]: best=(e,rr.x,rr.fun)
    e,x,fun=best; A,B,C=lev3.geom(x[10],1,1); k=L.cam(x[:8]); T=x[8:10]
    G=L.ray_plane(k,f["G"],7.3)[:2]; F=L.ray_plane(k,f["F"],7.3)[:2]
    # marco intrinseco: origen D, eje u = D->C (independiente del giro)
    u=(C-L.D)/np.linalg.norm(C-L.D); n=np.array([-u[1],u[0]])
    loc=lambda P: ((P-L.D)@u,(P-L.D)@n)
    print(f"{nombre}: error {e:.1f} px · máx {np.abs(fun).max():.0f}")
    for nm,P in (("torre",T),("F",F),("G",G),("A",A)): print(f"   {nm:6s} (a lo largo de D→C, perpendicular) = ({loc(P)[0]:7.2f}, {loc(P)[1]:7.2f})")
    return dict(T=loc(T),F=loc(F),G=loc(G))
r1=run("F01"); r2=run("F23")
for k in ("T","F","G"):
    d=np.hypot(r1[k][0]-r2[k][0],r1[k][1]-r2[k][1]); print(f"diferencia entre fotos para {k}: {d:.1f} m")
