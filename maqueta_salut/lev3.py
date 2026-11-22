import math, numpy as np, levantamiento as L
from scipy.optimize import least_squares
def geom(phi,sC,sB):
    A=106.69*np.array([math.sin(phi),-math.cos(phi)]); C=L.tri(L.D,A,95.17,16.66,sC)
    ca=A-C; th=sB*math.atan2(7.3,math.sqrt(ca@ca-7.3**2))
    R=np.array([[math.cos(th),-math.sin(th)],[math.sin(th),math.cos(th)]]); B=C+(R@ca/np.linalg.norm(ca))*math.sqrt(ca@ca-7.3**2)
    return A,B,C
def res(x,sC,sB):
    A,B,C=geom(x[10],sC,sB); L.PT={"A":A,"B":B,"C":C,"D":L.D}
    return L.res(x[:10],11.5,L.V["Z_P1"])
best=None
for sC in (-1,1):
  for sB in (-1,1):
    for phi in np.radians([-30,-15,0,15,30]):
      for az in range(-180,180,30):
        A,_,_=geom(phi,sC,sB)
        x0=[az,30,200,A[0]/2,A[1]/2,20,25,0,A[0]/2,A[1]*0.7,phi]
        try: rr=least_squares(res,x0,args=(sC,sB),bounds=([-200,5,50,-150,-160,-10,8,-10,-150,-160,-1.2],[200,85,1500,150,160,60,70,10,150,160,1.2]),loss="soft_l1",f_scale=6)
        except Exception: continue
        e=float(np.sqrt(np.mean(rr.fun**2)))
        if best is None or e<best[0]: best=(e,rr.x,rr.fun,sC,sB)
e,x,f,sC,sB=best; A,B,C=geom(x[10],sC,sB); k=L.cam(x[:10]); T=x[8:10]
print("error %.1f px (sC %d sB %d) · torre max %.0f px · puntos %s"%(e,sC,sB,np.abs(f[:18]).max(),np.round(f[18:],1)))
print("A",A.round(2),"B",B.round(2),"C",C.round(2),"T",np.round(T,2))
F=L.ray_plane(k,L.PIX_F,7.3); G=L.ray_plane(k,L.PIX_G,7.3); X=L.ray_plane(k,L.PIX_X,7.3)
print("F",F[:2].round(2),"G",G[:2].round(2),"X",X[:2].round(2))
dw=(G[:2]-L.D); dw/=np.linalg.norm(dw)   # fachada exterior del ala: D->G
bc=(C-B)/np.linalg.norm(C-B)
print("dirección ala (D->G) vs fachada B-C: ángulo %.1f°"%math.degrees(math.acos(abs(dw@bc))))
n=np.array([-dw[1],dw[0]])
for nm,P in (("torre",T),("C",C),("F",F[:2]),("A",A)):
    q=P-L.D; print(f"  {nm}: a lo largo del ala {q@dw:7.2f} m · perpendicular {q@n:7.2f} m")
np.save("levantamiento3.npy",dict(x=x,sC=sC,sB=sB),allow_pickle=True)
