"""Organiza DIBUJOS_EXPLICATIVOS en dos juegos para que no vuelva a salir geometría superada:
  ACTUAL    – solo láminas que reflejan el modelo de hoy (regeneradas por sus scripts justo antes)
  HISTORICO – dudas, hipótesis y análisis de cada momento (documentan decisiones; su geometría es la de entonces)
Genera DIBUJOS_EXPLICATIVOS.pdf (actual) e HISTORICO_DECISIONES.pdf, cada uno con un rótulo por página."""
import glob, os, re, shutil
from PIL import Image, ImageDraw, ImageFont
D = "DIBUJOS_EXPLICATIVOS"; H = os.path.join(D, "HISTORICO")
os.makedirs(H, exist_ok=True)
ACTUAL = [  # (n.º, archivo fuente regenerado, título)
 (1, None, "ZONAS_01"), (2, None, "ZONAS_02"), (3, None, "ZONAS_03"), (4, None, "ZONAS_04"), (5, None, "ZONAS_05"), (6, None, "ZONAS_06"),
 (7, None, "ZONAS_07"), (8, None, "ZONAS_08"), (9, None, "ZONAS_09"), (10, None, "ZONAS_10"), (11, None, "ZONAS_11"),
 (20, "ALZADO_CALLE.png", "ALZADO_CALLE – alzado 3 a la calle (solo líneas)"),
 (24, "GENERATRICES_ESQUEMA.png", "GENERATRICES_ESQUEMA – método MGF"), (25, "GENERATRICES_ALAMY.png", "GENERATRICES_ALAMY – MGF sobre Alamy"),
 (26, "MGF_TAMBOR.png", "MGF_TAMBOR"), (27, "ALZADO_TORRE_ALAMY.png", "ALZADO_TORRE_ALAMY – alturas de Alamy"),
 (29, "PLANTA_ORIENTACION_ALAMY.png", "PLANTA_ORIENTACION_ALAMY"), (30, "COLLAGE_ALAMY.png", "COLLAGE_ALAMY – foto al 50 % sobre el modelo"),
 (31, "ESCALERA_FOTOS.png", "ESCALERA_FOTOS"), (32, "ESCALERA_FRENTE.png", "ESCALERA_FRENTE"),
 (52, "COLLAGE_F09.png", "COLLAGE_F09 – foto al 50 % sobre el modelo (2.ª vista)"),
 (54, "MATRIZ_v2.png", "MATRIZ_v2 – tabla zonas × fotos"), (56, "DUDA7_RESUELTA.png", "DUDA7_RESUELTA – muro de coronación de la escalera"),
 (57, "PLANO_LUGAR_1984.png", "PLANO_LUGAR_1984 – planta de situación"),
 (58, "COLLAGE_BASE.png", "COLLAGE_BASE – base de la torre en ángulo recto sobre F09 y F14"),
]
ZON = sorted(glob.glob("zon_*.png"))


def rotulo(im, t):
    im = im.convert("RGB"); im.thumbnail((2400, 2400))
    pg = Image.new("RGB", (im.width, im.height + 60), "white"); pg.paste(im, (0, 60))
    try: fnt = ImageFont.truetype("DejaVuSans.ttf", 22)
    except Exception: fnt = ImageFont.load_default()
    ImageDraw.Draw(pg).text((14, 16), t[:190], fill="black", font=fnt)
    return pg


# 1) todo lo que no esté en ACTUAL pasa a HISTORICO (se conserva, no se borra)
nums = {n for n, _, _ in ACTUAL}
for f in glob.glob(os.path.join(D, "*.png")):
    m = re.match(r"(\d+)_", os.path.basename(f))
    if m and int(m.group(1)) not in nums:
        shutil.move(f, os.path.join(H, os.path.basename(f)))
# 2) copia las versiones regeneradas
for n, src, t in ACTUAL:
    if n <= 11:
        if len(ZON) >= n: shutil.copy(ZON[n - 1], os.path.join(D, f"{n:02d}_ZONAS_{n:02d}.png"))
    elif src and os.path.exists(src):
        for old in glob.glob(os.path.join(D, f"{n:02d}_*.png")): os.remove(old)
        shutil.copy(src, os.path.join(D, f"{n:02d}_{os.path.splitext(src)[0]}.png"))
# 3) PDFs
pags = [rotulo(Image.open(f), os.path.basename(f)[:-4].replace("_", " "))
        for f in sorted(glob.glob(os.path.join(D, "*.png")), key=lambda p: int(re.match(r"(\d+)", os.path.basename(p)).group(1)))]
pags[0].save(os.path.join(D, "DIBUJOS_EXPLICATIVOS.pdf"), save_all=True, append_images=pags[1:], resolution=110)
hs = sorted(glob.glob(os.path.join(H, "*.png")), key=lambda p: int(re.match(r"(\d+)", os.path.basename(p)).group(1)))
hp = [rotulo(Image.open(f), "HISTÓRICO (geometría de entonces, superada) · " + os.path.basename(f)[:-4].replace("_", " ")) for f in hs]
if hp: hp[0].save(os.path.join(H, "HISTORICO_DECISIONES.pdf"), save_all=True, append_images=hp[1:], resolution=100)
open(os.path.join(H, "LEEME.md"), "w").write(
    "# Histórico de decisiones\n\nDudas, hipótesis y análisis tal como se plantearon en su momento. **Su geometría está superada**: "
    "no se usan como planos. El estado actual está en `../DIBUJOS_EXPLICATIVOS.pdf` y en los juegos A3/A4.\n")
print(len(pags), "actuales ·", len(hp), "históricas")
