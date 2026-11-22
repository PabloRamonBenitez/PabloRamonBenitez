"""Calibra la camara de una foto con la planta ACTUAL fija (cilindros + aristas de la base) y devuelve los
residuos por elemento: lo que no cuadra es discrepancia del modelo."""
import math, json, sys, numpy as np
from scipy.optimize import least_squares
from PIL import Image
import salut_v2 as s, calibrar as C, superponer as sp

def ajustar(foto, obs, lineas, x0s, bounds):
    W,H=Image.open(foto).size
    def res(x):
        r=list(C.residuos(x,obs,W,H))
        cam=sp.camara(*x[:3],tuple(x[3:6]),x[6],x[7],W,H)
        for pa,pb,q0,q1 in lineas:
            q0,q1=np.array(q0,float),np.array(q1,float); t=(q1-q0)/np.linalg.norm(q1-q0); nn=np.array([-t[1],t[0]])
            for a in np.linspace(0,1,5):
                P=np.array(pa)*(1-a)+np.array(pb)*a
                X,Y,Z=C.proyectar(cam,P); uu=np.array([W/2+cam[4]*X/Z,H/2-cam[4]*Y/Z]); r.append(float((uu-q0)@nn))
        return np.array(r)
    best=None
    for x0 in x0s:
        try: rr=least_squares(res,x0,bounds=bounds)
        except Exception: continue
        e=np.sqrt(np.mean(rr.fun**2))
        if best is None or e<best[0]: best=(e,rr.x,rr.fun)
    return best
