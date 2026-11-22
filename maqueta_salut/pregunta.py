import math, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse, FancyArrowPatch
from PIL import Image
I='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'
fig=plt.figure(figsize=(18,11))
# --- foto F09 con el muro marcado ---
ax=fig.add_axes([0.01,0.05,0.42,0.88])
im=np.asarray(Image.open(I+'9.webp').convert('RGB')); ax.imshow(im); ax.axis('off')
ax.add_patch(Polygon([(455,688),(640,690),(640,800),(455,800)],closed=True,fc=(1,0,0,0.25),ec='red',lw=3))
ax.text(470,660,"¿ESTE MURO?",color='red',fontsize=15,weight='bold')
ax.add_patch(Polygon([(330,700),(455,700),(455,745),(330,745)],closed=True,fc='none',ec='blue',lw=2.5))
ax.text(335,690,"hotel",color='blue',fontsize=11,weight='bold')
ax.add_patch(Polygon([(80,700),(246,700),(246,745),(80,745)],closed=True,fc='none',ec='green',lw=2.5))
ax.text(85,690,"restaurante",color='green',fontsize=11,weight='bold')
ax.annotate("cámara de esta foto:\nmirando de frente al chaflán",(437,880),fontsize=10,ha='center')
ax.set_title("Foto F09 (frontal)",fontsize=13,loc='left')
# --- planos de las dos opciones ---
def planta(ax, titulo, muro, nota):
    A=math.radians(31); u=np.array([math.cos(A),math.sin(A)]); n=np.array([-u[1],u[0]])
    A1=np.array([15.7-27.2*math.cos(A),0]); A2=np.array([15.7,27.2*math.sin(A)])
    L=[(-24,0),tuple(A1),tuple(A2),(12.7,A2[1]),(12.7,60),(0,60),(0,12),(-24,12)]
    ax.add_patch(Polygon(L,closed=True,fc='0.88',ec='k',lw=1.2))
    cen=A1+14.6*u+1.5*n
    ax.add_patch(Circle(cen,14.4,fc='none',ec='0.5',ls='--',lw=1)); ax.add_patch(Circle(cen,3,fc='0.3'))
    # restaurante / hotel sobre el chaflan
    p=lambda X,Y: cen+X*u+Y*n
    ax.plot(*zip(p(-14.6,-1.5),p(-3,-1.5)),color='green',lw=5); ax.plot(*zip(p(3,-1.5),p(12.6,-1.5)),color='blue',lw=5)
    ax.plot(*zip(*muro),color='red',lw=7,solid_capstyle='butt')
    # camara
    c=cen-60*n; ax.add_patch(FancyArrowPatch(tuple(c),tuple(cen-20*n),arrowstyle='-|>',mutation_scale=25,color='k'))
    ax.text(*(c+np.array([1,-3])),"cámara F09",fontsize=10)
    ax.text(-22,6,"ala corta\n(calle)",fontsize=9); ax.text(3,45,"ala larga\n(hacia el Dnipro)",fontsize=9,rotation=90)
    ax.set_xlim(-30,60); ax.set_ylim(-45,62); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(titulo,fontsize=13,loc='left',color='red'); ax.text(-29,-44,nota,fontsize=10,va='bottom')
A=math.radians(31); u=np.array([math.cos(A),math.sin(A)]); n=np.array([-u[1],u[0]])
A2=np.array([15.7,27.2*math.sin(A)])
ax1=fig.add_axes([0.45,0.05,0.27,0.88])
planta(ax1,"OPCIÓN A: es la fachada del ala larga,\nvista en escorzo",[(15.7,A2[1]),(15.7,A2[1]+28)],
       "El muro va a lo largo del ala larga (rojo).\nDesde la cámara se ve de lado, más corto.")
ax2=fig.add_axes([0.73,0.05,0.27,0.88])
A1=np.array([15.7-27.2*math.cos(A),0]); cen=A1+14.6*u+1.5*n
q0=cen+12.6*u-1.5*n
planta(ax2,"OPCIÓN B: es otro muro que mira a la plaza\n(sigue la línea del chaflán)",[tuple(q0),tuple(q0+14*u)],
       "El muro continúa la línea del chaflán (rojo)\nmás allá del hotel, mirando a la cámara.")
fig.suptitle("PREGUNTA: el muro con estrellas en relieve (y la tienda Ridne debajo), ¿es A o B? ¿O ninguna? Puedes dibujarlo encima.",fontsize=15,weight='bold')
fig.savefig("pregunta_muro_relieve.png",dpi=90)
