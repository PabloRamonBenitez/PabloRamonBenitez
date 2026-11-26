"""DIBUJOS_EXPLICATIVOS.pdf: todas las láminas explicativas numeradas, en orden, una por página (con su título del LEEME)."""
import glob, os, re
from PIL import Image, ImageDraw, ImageFont
D = "DIBUJOS_EXPLICATIVOS"
tit = {}
for l in open(os.path.join(D, "LEEME.md"), encoding="utf-8"):
    m = re.match(r"\|\s*(\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|", l)
    if m: tit[int(m.group(1))] = (m.group(2).strip(), re.sub(r"\*\*", "", m.group(3).strip()))
pags = []
for f in sorted(glob.glob(os.path.join(D, "*.png")), key=lambda p: int(re.match(r"(\d+)", os.path.basename(p)).group(1))):
    n = int(re.match(r"(\d+)", os.path.basename(f)).group(1))
    im = Image.open(f).convert("RGB"); im.thumbnail((2400, 2400))
    t = f"{n:02d} · " + (tit[n][0] + " – " + tit[n][1] if n in tit else os.path.basename(f))
    pg = Image.new("RGB", (im.width, im.height + 60), "white"); pg.paste(im, (0, 60))
    dr = ImageDraw.Draw(pg)
    try: fnt = ImageFont.truetype("DejaVuSans.ttf", 22)
    except Exception: fnt = ImageFont.load_default()
    dr.text((14, 16), t[:180], fill="black", font=fnt)
    pags.append(pg)
pags[0].save(os.path.join(D, "DIBUJOS_EXPLICATIVOS.pdf"), save_all=True, append_images=pags[1:], resolution=110)
print(len(pags), "páginas")
