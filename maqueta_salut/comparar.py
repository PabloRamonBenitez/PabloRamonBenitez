import sys, trimesh, render_v2 as r, salut_v2 as s, numpy as np
from manifold3d import Manifold
from PIL import Image
S='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/'
m=s.construir() ^ Manifold.cube((106,300,400)).translate((-53,-150,-1))
me=m.to_mesh(); t=trimesh.Trimesh(np.asarray(me.vert_properties)[:,:3],np.asarray(me.tri_verts),process=False)
im=r.render(t,0,4,W=900,H=900,margen=0.03).convert('RGB')
ph=Image.open(S+'images/9.webp').convert('RGB').crop((90,120,530,700))
ph=ph.resize((int(ph.width*900/ph.height),900))
out=Image.new('RGB',(900+ph.width,900),'white'); out.paste(ph,(0,0)); out.paste(im,(ph.width,0))
out.save(S+'scratchpad/cmp.png')
