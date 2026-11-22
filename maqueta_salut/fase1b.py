"""FASE 1 (2ª pasada): calibracion con TODAS las observaciones; los residuos por elemento dicen si el modelo
es coherente con la foto. Umbral: <= 1,5% del diametro del barril en pixeles (~0,45 m)."""
import json, numpy as np, edificio as E, calib_e as C
I='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'
F={
 "C04":dict(f="9.webp",az=(-80,170),el=(-3,25),fov=(3,40),hcam=(2.0,5.0),
   obs=[("barril_sup",105,502,366),("barril_inf",108,500,598),("columna",246,330,720),("forj",[373,413,453,493,533,575]),
        ("tambor",133,485,335),("visera",110,442,245),("remate",240,385,190)]),
 "C03":dict(f="2.webp",az=(-80,170),el=(-8,40),fov=(5,70),hcam=(1.6,5.0),
   obs=[("barril_sup",780,1365,410),("barril_inf",795,1350,760),("forj",[427.5,482.5,537.5,592.5,647.5,702.5]),
        ("tambor",805,1332,385),("visera",785,1252,305),("remate",975,1198,180)]),
 "C01":dict(f="1.webp",az=(-80,170),el=(5,75),fov=(10,60),hcam=None,
   obs=[("barril_sup",170,550,262),("barril_inf",187,532,476),("columna_pie",322,388,652),("forj",[281.7,320,358.3,396.7,435,473]),
        ("tambor",190,525,232),("remate",293,417,45)]),
}
out={}
for k,d in F.items():
    best,(W,H)=C.calibrar(I+d["f"],d["obs"],d["az"],d["el"],d["fov"],d["hcam"])
    r=list(best[2][1:] if d["hcam"] else best[2]); x=best[1]; K=C.cam(x,W,H)
    dpx=abs(C.silueta(K,C.CIL["barril_sup"][0],E.R_AL,20)[1,0]-C.silueta(K,C.CIL["barril_sup"][0],E.R_AL,20)[0,0])
    umbral=0.015*dpx; fila={}; i=0
    for o in d["obs"]:
        n=6 if o[0]=="forj" else 3
        vals=np.array(r[i:i+n]); i+=n
        fila[o[0]]=dict(res=[round(float(v),1) for v in vals], max=round(float(np.abs(vals).max()),1),
                        estado="OK" if np.abs(vals).max()<=umbral else "NO")
    out[k]=dict(rms=round(best[0],1),umbral_px=round(umbral,1),altura_camara=round(float(K[0][2]),1),camara=[round(float(v),2) for v in x],elementos=fila)
    print(k,"rms",round(best[0],1),"umbral",round(umbral,1),"h cam",round(float(K[0][2]),1),"cam",np.round(x,1))
    for e,v in fila.items(): print("   ",e,v["estado"],v["max"],v["res"])
json.dump(out,open("FASE1b_resultados.json","w"),indent=1,ensure_ascii=False)
