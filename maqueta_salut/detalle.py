import sys, trimesh, numpy as np, render_v2 as r
from manifold3d import Manifold
from PIL import Image
import salut_v2 as s
m = s.construir()
def recorte(x0,x1,y0,y1,z0,z1):
    q = m ^ Manifold.cube((x1-x0,y1-y0,z1-z0)).translate((x0,y0,z0))
    me=q.to_mesh(); return trimesh.Trimesh(np.asarray(me.vert_properties)[:,:3],np.asarray(me.tri_verts),process=False)
S='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/scratchpad/'
a = r.render(recorte(-40,40,0,60,70,130), 200, 20, W=700, H=700)   # trasera: escalera, puerta, terraza
b = r.render(recorte(-50,10,-60,0,30,70), 20, 8, W=700, H=700)      # primera planta del barril
out = Image.new('L',(1400,700),255); out.paste(a,(0,0)); out.paste(b,(700,0)); out.save(S+'det.png')
