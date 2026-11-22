"""Lista de COLUMNAS (fotos) de la matriz: una por fuente original; recortes y duplicados agrupados.
Genera: hoja de contactos con las columnas, plano con el punto de vista aproximado de cada una y el Excel
zonas x columnas (celdas visibles = '?', no visibles = '–')."""
import math, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MP, Circle
from PIL import Image, ImageDraw
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import edificio as E, zonas_def as Z
IMG='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'
R=lambda a,b: [f"Z{i:02d}" for i in range(a,b+1)]
# (id, foto principal, otras versiones/recortes, descripcion, epoca, vista (angulo respecto a la normal del chaflan, distancia, altura), zonas visibles, uso)
COLS=[
 ("C01","1.webp","F41, F55; recortes F07?, F25, F26, F32, F44, F47","Aérea de época, delante del chaflán y algo a la derecha","1984-90",(10,120,40),
  R(1,7)+["Z09","Z10","Z11","Z12","Z13","Z14","Z15","Z16","Z18","Z19","Z20","Z21","Z22","Z23","Z24","Z25","Z26"],"Base, encuentro torre-L, ala larga, concha"),
 ("C02","23.webp","F29, F31; recortes F24, F27, F33","Aérea de época lejana con el Dnipro","1984-90",(5,250,80),
  R(1,7)+["Z10","Z16","Z18","Z19","Z21","Z24","Z25","Z26","Z27"],"Conjunto, ala larga completa"),
 ("C03","2.webp","F14 (recorte)","Época, desde la plaza, a nivel de calle, hacia el lado del restaurante","1984-90",(-30,110,2),
  R(1,14)+["Z15","Z16","Z17","Z18","Z20"],"Arranque de la torre, bandas, ala corta"),
 ("C04","9.webp","F52","Frontal con teleobjetivo, actual","2010s",(0,150,2),
  R(1,15)+["Z16","Z21","Z22"],"Alzado del chaflán, parte alta"),
 ("C05","18.webp","F51","Color actual desde la plaza, hacia el lado del hotel","2020s",(35,60,2),
  ["Z02","Z04"]+R(6,15)+["Z21","Z22"],"Ménsulas, cuello, bandas, relieve"),
 ("C06","50.webp","","Contrapicado frontal de cerca, color actual","2010s",(0,30,1.5),
  ["Z02","Z04"]+R(6,14),"Fondo del barril, cuello, bandas"),
 ("C07","3.webp","F16, F17 (recortes)","Contrapicado desde abajo, BN","2010s",(20,25,1.5),
  ["Z02","Z04","Z06","Z07","Z08","Z09"],"Barril visto desde abajo, ménsulas"),
 ("C08","15.png","","Época, base desde la plaza con autobuses","1984-90",(-15,70,2),
  R(7,14)+["Z16","Z17"],"Bandas, PB hundida, columna"),
 ("C09","19.webp","","Calle Ivana Mazepy, lejos, color","2020s",(-147,250,2),
  R(1,7)+["Z10","Z11","Z16","Z17","Z19"],"Silueta desde la calle, ala corta"),
 ("C10","8.webp","","Aérea desde detrás (lado de la ciudad)","2010s",(-140,150,40),
  R(1,7)+["Z18","Z20","Z29","Z30"],"Escalera trasera, ala corta desde detrás"),
 ("C11","4.webp","F06","Barril de cerca (dron)","2010s",(30,40,30),
  ["Z04","Z05","Z06"],"Módulo del barril, ojos"),
 ("C12","10.png","","Remate de cerca, BN","2010s",(-10,40,40),
  R(1,5),"Remate, letrero, visera, banda"),
 ("C13","11.webp","","Escalera trasera de cerca","2010s",(175,20,20),
  ["Z06","Z29","Z30"],"Lamas y caja de la escalera"),
 ("C14","12.png","","Encuentro escalera-barril","2010s",(160,15,15),
  ["Z06","Z25","Z26","Z29","Z30"],"Encuentro escalera, barril y ala"),
 ("C15","13.webp","","Escalera desde un lateral","2010s",(200,40,20),
  ["Z06","Z28","Z29","Z30"],"Escalera y fachada al patio"),
 ("C16","22.webp","F20, F21","Maqueta original del proyecto","proyecto",(0,0,0),
  R(1,10)+R(16,31),"SOLO organización (no medidas)"),
 ("C17","35.webp","F48","Bing casi cenital","2020s",(0,0,0),
  ["Z02","Z06","Z15","Z16","Z18","Z19","Z21","Z25","Z26","Z27","Z29","Z31"],"Planta: posiciones"),
 ("C18","38.png","F36, F37, F39","Bing con medidas (12,74 · 6,21 · 7,81 · 35,13)","2020s",(0,0,0),
  ["Z21","Z23","Z25","Z26","Z27"],"Planta: medidas del ala larga"),
]
NO_USAR="F05, F28, F34, F40, F42, F43, F45, F46, F49, F53, F54, F56 (renders y planos míos); F30 (tu esquema)"

def contactos():
    W=330; n=len(COLS); cols=6; rows=math.ceil(n/cols)
    sh=Image.new("RGB",(W*cols,(W+40)*rows),"white"); d=ImageDraw.Draw(sh)
    for i,c in enumerate(COLS):
        im=Image.open(IMG+c[1]).convert("RGB"); im.thumbnail((W-8,W-50))
        x,y=(i%cols)*W,(i//cols)*(W+40)
        sh.paste(im,(x+4,y+34)); d.text((x+6,y+3),f"{c[0]}  (F{int(c[1].split('.')[0]):02d})  {c[4]}",fill=(180,0,0))
        import unicodedata
        t=unicodedata.normalize("NFKD",c[3][:52]).encode("ascii","ignore").decode()
        d.text((x+6,y+17),t,fill=(0,0,0))
    sh.save("COLUMNAS_fotos.png")

def plano():
    fig,ax=plt.subplots(figsize=(13,13))
    pl=E.plantas_base(); ax.add_patch(MP(pl["P1"],closed=True,fc="0.9",ec="k"))
    ax.add_patch(Circle(E.T,E.R_AL,fc="none",ec="0.4",ls="--"))
    T=np.array(E.T); nout=-np.array(E.N); u=np.array(E.U)
    for c in COLS:
        a,dist,h=c[5]
        if dist==0: continue
        r=math.radians(a); v=nout*math.cos(r)+u*math.sin(r)
        dd=min(dist,75)*0.55+18; p=T+v*dd
        ax.annotate("",xy=T+v*(E.R_AL+1),xytext=p,arrowprops=dict(arrowstyle="-|>",color="crimson",lw=1.2))
        ax.text(*(p+v*2.5),f"{c[0]}\n{'alta' if h>10 else 'calle'}",fontsize=8,ha="center",va="center",color="crimson",
                bbox=dict(fc="white",ec="crimson",lw=0.5,pad=1))
    ax.set_aspect("equal"); ax.set_xlim(-75,75); ax.set_ylim(-70,100); ax.grid(True,lw=0.2)
    ax.set_title("Punto de vista aproximado de cada columna (flecha hacia la torre). C16-C18 son planta/maqueta.",fontsize=10,loc="left")
    fig.savefig("COLUMNAS_puntos_de_vista.png",dpi=80)

def excel():
    wb=Workbook(); th=Side(style="thin",color="999999"); B=Border(th,th,th,th)
    ws=wb.active; ws.title="Columnas (fotos)"
    hdr=["Col.","Foto principal","Otras versiones / recortes","Descripción y punto de vista","Época","Para qué sirve","Nº zonas visibles"]
    ws.append(hdr)
    for c in COLS:
        ws.append([c[0],f"F{int(c[1].split('.')[0]):02d}",c[2],c[3],c[4],c[7],len(c[6])])
    ws.append([]); ws.append(["","No se usan:",NO_USAR])
    for col,w in zip("ABCDEFG",(6,10,34,58,10,40,10)): ws.column_dimensions[col].width=w
    for row in ws.iter_rows(min_row=1,max_row=len(COLS)+1):
        for cell in row: cell.border=B; cell.alignment=Alignment(wrap_text=True,vertical="center"); cell.font=Font(size=9,bold=cell.row==1)
    m=wb.create_sheet("Matriz zonas x fotos")
    m.append(["Zona","Descripción","Grupo"]+[f"{c[0]}\nF{int(c[1].split('.')[0]):02d}" for c in COLS]+["Visibles"])
    fill={"?":"FFEB9C","–":"EDEDED"}
    for r,(k,n,g,*_) in enumerate(Z.ZONAS,start=2):
        vals=["?" if k in c[6] else "–" for c in COLS]
        m.append([k,n,g]+vals+[vals.count("?")])
        for j in range(len(COLS)):
            cell=m.cell(r,4+j); cell.fill=PatternFill("solid",fgColor=fill[cell.value]); cell.alignment=Alignment(horizontal="center")
    r=len(Z.ZONAS)+3
    m.cell(r,2).value="JUNTAS (se comprueban desde las dos zonas)"; m.cell(r,2).font=Font(bold=True)
    for i,(a,b,t) in enumerate(Z.JUNTAS,start=1):
        m.cell(r+i,1).value=f"J{i:02d}"; m.cell(r+i,2).value=f"{a} / {b}: {t}"
        for j,c in enumerate(COLS):
            v="?" if (a in c[6] and b in c[6]) else "–"
            cell=m.cell(r+i,4+j); cell.value=v; cell.fill=PatternFill("solid",fgColor=fill[v]); cell.alignment=Alignment(horizontal="center")
    m.column_dimensions["A"].width=6; m.column_dimensions["B"].width=58; m.column_dimensions["C"].width=10
    for j in range(len(COLS)+1): m.column_dimensions[get_column_letter(4+j)].width=7.5
    m.row_dimensions[1].height=30; m.freeze_panes="D2"
    wb.save("MATRIZ_ZONAS_FOTOS.xlsx")
    tz=sum(len(c[6]) for c in COLS); tj=sum(1 for a,b,_ in Z.JUNTAS for c in COLS if a in c[6] and b in c[6])
    sinfoto=[k for k,*_ in Z.ZONAS if not any(k in c[6] for c in COLS if c[0] not in ("C16",))]
    print("celdas zona:",tz,"celdas junta:",tj,"zonas sin foto real:",sinfoto)

if __name__=="__main__":
    contactos(); plano(); excel()
