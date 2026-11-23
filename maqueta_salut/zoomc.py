import sys
from PIL import Image, ImageOps, ImageDraw
I='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'
f,x0,y0,x1,y1,s,out=sys.argv[1],*map(int,sys.argv[2:7]),sys.argv[7]
im=Image.open(I+f).convert('L').crop((x0,y0,x1,y1)); im=ImageOps.autocontrast(im,cutoff=2).resize(((x1-x0)*s,(y1-y0)*s),Image.BICUBIC).convert('RGB')
d=ImageDraw.Draw(im)
for x in range(x0-x0%5+5,x1,5):
    X=(x-x0)*s; d.line([(X,0),(X,8 if x%10 else 20)],fill=(255,0,0),width=2)
    if x%10==0: d.text((X+2,22),str(x),fill=(255,0,0))
for y in range(y0-y0%5+5,y1,5):
    Y=(y-y0)*s; d.line([(0,Y),(8 if y%10 else 20,Y)],fill=(0,0,255),width=2)
    if y%10==0: d.text((22,Y-5),str(y),fill=(0,0,255))
im.save(out)
