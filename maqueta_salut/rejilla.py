"""Rejilla de píxeles sobre una foto (para leer coordenadas exactas). uso: rejilla.py foto x0 y0 x1 y1 escala paso salida"""
import sys
from PIL import Image, ImageDraw
I='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'
f, x0, y0, x1, y1, s, st, out = sys.argv[1], *map(int, sys.argv[2:7]), int(sys.argv[7]), sys.argv[8]
im = Image.open(I + f).convert("RGB").crop((x0, y0, x1, y1)); im = im.resize((im.width * s, im.height * s), Image.LANCZOS)
d = ImageDraw.Draw(im)
for x in range((x0 // st + 1) * st, x1, st):
    X = (x - x0) * s; d.line([(X, 0), (X, im.height)], fill=(255, 0, 0) if x % (st * 5) == 0 else (255, 160, 160), width=1)
    d.text((X + 2, 2), str(x), fill=(255, 0, 0))
for y in range((y0 // st + 1) * st, y1, st):
    Y = (y - y0) * s; d.line([(0, Y), (im.width, Y)], fill=(0, 0, 255) if y % (st * 5) == 0 else (160, 160, 255), width=1)
    d.text((2, Y + 2), str(y), fill=(0, 0, 255))
im.save(out)
