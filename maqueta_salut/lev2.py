import math, numpy as np, levantamiento as L
from scipy.optimize import least_squares
out=[]
for sA in (-1,1):
  for sC in (-1,1):
    for sB in (1,-1):
        A=L.tri(L.D,L.E,106.69,102.96,sA); C=L.tri(L.D,A,95.17,16.66,sC)
        ca=A-C; th=sB*math.atan2(7.3,math.sqrt(ca@ca-7.3**2))
        R=np.array([[math.cos(th),-math.sin(th)],[math.sin(th),math.cos(th)]]); B=C+(R@ca/np.linalg.norm(ca))*math.sqrt(ca@ca-7.3**2)
        L.PT={"A":A,"B":B,"C":C,"D":L.D}   # E oculto: fuera
        yb=float(np.sign(A[1]))
        best=None
        for az in range(-180,180,20):
            for ty in (40*yb,70*yb):
                x0=[az,30,200,A[0]/2,ty,20,25,0,A[0]/2,ty]
                try: rr=least_squares(L.res,x0,args=(11.5,L.V["Z_P1"]),bounds=([-200,5,50,-120,-160,-10,8,-10,-120,-160],[200,85,1500,120,160,60,70,10,120,160]),loss="soft_l1",f_scale=6)
                except Exception: continue
                e=float(np.sqrt(np.mean(rr.fun**2)))
                if best is None or e<best[0]: best=(e,rr.x,rr.fun)
        e,x,f=best; nT=18
        out.append((e,sA,sC,sB,x,f))
        print(f"sA {sA:+d} sC {sC:+d} sB {sB:+d}: error {e:5.1f}  torre {np.round(f[:nT],0).max():.0f}  puntos", np.round(f[nT:],0), " T", np.round(x[8:10],1))
