import math, json, numpy as np, edificio as E, calib_e as C
from scipy.optimize import least_squares
I='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'
W,H=1666,1270; s=1/0.8
TOR=[("barril_inf",275*s,880*s,600*s),("barril_sup",320*s,805*s,272*s),("cuello",395*s,875*s,690*s)]
yf=-(E.R_COL-E.RET); pl=E.plantas_base()
P=lambda X,Y,z:np.array([*E.P(X,Y),z])
PTS=[(P(-E.REST-E.COL/2,yf,7.3),(340*s,785*s)),(P(E.R_COL,yf,7.3),(600*s,735*s)),(np.array([*pl['P1'][2],7.3]),(760*s,735*s))]
az0=math.degrees(math.atan2(-E.N[0],E.N[1]))
def res(x,off=True):
    K=C.cam(x[:8],W,H); r=list(C.residuos(x[:8],TOR,W,H)); d=np.array([x[8],x[9],0]) if off else 0
    r.append((K[0][2]-1.6)*5)
    for p,q in PTS:
        u=C.proj(K,p+d)[0]; r+=[u[0]-q[0],u[1]-q[1]]
    r+=[x[8]*0.5,x[9]*0.5]
    return np.array(r)
best=None
T=np.array(E.T)
for daz in range(-70,71,10):
  for fv in (45,65):
    x0=[az0+daz,-20,60,T[0],T[1],15,fv,0,0,0]
    try: rr=least_squares(res,x0,bounds=([az0-90,-70,15,T[0]-40,T[1]-40,-5,25,-20,-10,-10],[az0+90,70,400,T[0]+40,T[1]+40,50,110,20,10,10]),loss="soft_l1",f_scale=8)
    except Exception: continue
    e=float(np.sqrt(np.mean(rr.fun**2)))
    if best is None or e<best[0]: best=(e,rr.x,rr.fun)
print("az frontal",round(az0,1)); print("rms",round(best[0],1),np.round(best[1],2)); print(np.round(best[2],1))
json.dump(dict(cam=list(map(float,best[1][:8])),off=list(map(float,best[1][8:]))),open('cam_C05.json','w'))
