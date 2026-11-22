import numpy as np, salut_v2 as s, fit_fijo as F, superponer as sp, sys
I='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'
S='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/scratchpad/'
obs={"barril_sup":[170,550,262],"barril_inf":[187,532,476],"tambor_ojos":[190,525,232],"tambor_sup":[293,417,45],"columna_pie":[322,388,652]}
def P(X,Y,z): p=s.solar(X,Y); return [p[0],p[1],z]
lin=[(P(4,-s.RET,8.9),P(11,-s.RET,8.9),(431,538),(548,532)),
     (P(-13,-s.RET,8.9),P(-5,-s.RET,8.9),(156,566),(325,550)),
     ([s.W_P,25,9.9],[s.W_P,45,9.9],(555,405),(728,352))]
usar=sys.argv[1] if len(sys.argv)>1 else "012"
lin=[lin[int(i)] for i in usar]
x0s=[[az,el,250,s.CEN[0],s.CEN[1],24,f,0] for az in range(-20,91,15) for el in (15,25) for f in (20,30)]
b=F.ajustar(I+'1.webp',obs,lin,x0s,([-30,10,120,-60,-60,0,12,-6],[90,40,800,60,60,50,45,6]))
print(usar, round(b[0],1),np.round(b[1],2)); print(np.round(b[2][15:],1))
x=b[1]; sp.superponer(I+'1.webp',*x[:3],tuple(x[3:6]),x[6],x[7],S+f'f01_{usar}.png')
