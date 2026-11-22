"""FASE 2 – implantacion: camara de F01 + angulo del chaflan (que fija como sale la L respecto a la torre).
Observaciones de la torre (fase 1) + aristas de la base leidas en F01. Para cada angulo se recalcula toda la
geometria de edificio.py (subproceso) y se ajusta la camara; se compara el error."""
import os, sys, json, subprocess, numpy as np
CODE = r'''
import json, math, numpy as np, sys
from scipy.optimize import least_squares
import edificio as E, calib_e as C
W,H=828,762
T=np.array([*E.T,0.0]); yf=-(E.R_COL-E.RET); pl=E.plantas_base()
DEL=math.radians(float(sys.argv[2]))   # giro del ala larga alrededor de la esquina del chaflan (0 = perpendicular a la calle)
Cx,Cy=E.C
def gira(p):
    dx,dy=p[0]-Cx,p[1]-Cy
    return np.array([Cx+dx*math.cos(DEL)-dy*math.sin(DEL), Cy+dx*math.sin(DEL)+dy*math.cos(DEL), p[2]])
TOR=[("barril_sup",170,550,262),("barril_inf",187,532,476),("columna_pie",322,388,652),
     ("forj",[281.7,320,358.3,396.7,435,473]),("tambor",190,525,232)]
def P3(X,Y,z): p=E.P(X,Y); return np.array([p[0],p[1],z])
LIN=[ # (punto A 3D, punto B 3D, q0, q1, peso)
 (P3(-14,yf,E.Z_P1),P3(-4,yf,E.Z_P1),(170,567),(320,562),1.0),          # coronacion banda restaurante
 (gira(np.array([E.W_P,pl["Q"][1],E.Z_P1+1.0])),gira(np.array([E.W_P,E.L_L,E.Z_P1+1.0])),(552,425),(727,352),1.0),  # peto exterior del ala larga
]
PTS=[(gira(np.array([E.W_P,E.L_L,E.Z_P1+1.0])),(727,352),1.0)]                  # esquina final del ala (testero)
def dist_linea(K,A,B,q):
    s=np.linspace(-0.2,1.2,281); Pm=A[None,:]*(1-s[:,None])+B[None,:]*s[:,None]
    pr=C.proj(K,Pm); return float(np.min(np.hypot(pr[:,0]-q[0],pr[:,1]-q[1])))
def res(x):
    K=C.cam(x,W,H); r=list(C.residuos(x,TOR,W,H))
    for A,B,q0,q1,w in LIN: r+= [w*dist_linea(K,A,B,q0), w*dist_linea(K,A,B,q1)]
    for Pp,q,w in PTS:
        pr=C.proj(K,Pp)[0]; r+= [w*(pr[0]-q[0]), w*(pr[1]-q[1])]
    return np.array(r)
best=None
for az in range(-80,171,15):
  for el in (15,30,45):
    for fv in (20,35):
      try: rr=least_squares(res,[az,el,150,T[0],T[1],20,fv,0],bounds=([-90,5,40,T[0]-50,T[1]-50,-5,8,-8],[180,80,1500,T[0]+50,T[1]+50,60,70,8]))
      except Exception: continue
      e=float(np.sqrt(np.mean(rr.fun**2)))
      if best is None or e<best[0]: best=(e,rr.x,rr.fun)
nT=3*4+6
print(json.dumps(dict(ach=float(sys.argv[1]),dl=float(sys.argv[2]),rms=best[0],cam=list(map(float,best[1])),torre=list(map(float,best[2][:nT])),base=list(map(float,best[2][nT:])))))
'''
if __name__ == "__main__":
    out = []
    import itertools
    for th, a in itertools.product([92, 102, 112], [40, 57, 72]):
        dl = 0
        r = subprocess.run([sys.executable, "-c", CODE, str(a), str(dl)], env=dict(os.environ, ACH=str(a), THL=str(th)), capture_output=True, text=True)
        try:
            d = json.loads(r.stdout.strip().splitlines()[-1]); out.append(d)
            print(f"L {th:3d}°  chaflán {a:5.1f}°  error total {d['rms']:6.1f} px  | torre max {max(map(abs,d['torre'])):5.1f}  | base {np.round(d['base'],1)}")
        except Exception:
            print(a, "fallo", r.stderr[-300:])
    json.dump(out, open("FASE2_barrido.json", "w"), indent=1)
