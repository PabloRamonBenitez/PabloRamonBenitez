import json, sys, numpy as np, edificio as E, calib_e as C
from PIL import Image
r=json.load(open('FASE1_resultados.json'))
I='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'
def check(k, f, foto):
    W,H=Image.open(I+f).size; K=C.cam(r[k]["cam"],W,H)
    T=np.array([*E.T,0.0]); v=K[0]-T; v[2]=0; v/=np.linalg.norm(v)
    out=[]
    for j,yf in enumerate(foto):
        z=E.Z_B0+(6-j)*E.F
        y=C.proj(K,T+v*E.R_B+np.array([0,0,z]))[0,1]; out.append(y-yf)
    print(k, "dif px:", np.round(out,1), " px/m aprox:", round(abs(C.proj(K,T+v*E.R_B+np.array([0,0,20]))[0,1]-C.proj(K,T+v*E.R_B+np.array([0,0,21]))[0,1]),1))
check("C04","9.webp",[373,413,453,493,533,575])
check("C03","2.webp",[427.5,482.5,537.5,592.5,647.5,702.5])
check("C01","1.webp",[281.7,320,358.3,396.7,435,473])
