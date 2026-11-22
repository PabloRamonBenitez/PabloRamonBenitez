import sys, superponer as sp
from PIL import Image, ImageDraw
foto, sal = sys.argv[1], sys.argv[2]
vs = [list(map(float, v.split(','))) for v in sys.argv[3:]]
ims = []
for v in vs:
    az, el, dist, tx, ty, tz, fov = v[:7]; roll = v[7] if len(v) > 7 else 0
    im = sp.superponer(foto, az, el, dist, (tx, ty, tz), fov, roll)
    ImageDraw.Draw(im).text((8, 8), ",".join(f"{x:g}" for x in v), fill=(255, 255, 0))
    im.thumbnail((700, 700)); ims.append(im)
W, H = ims[0].size
out = Image.new("RGB", (W * 2, H * ((len(ims) + 1) // 2)), "white")
for i, im in enumerate(ims):
    out.paste(im, ((i % 2) * W, (i // 2) * H))
out.save(sal)
