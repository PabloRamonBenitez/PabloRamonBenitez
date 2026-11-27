"""ACCESO_VEHICULO.png – desde dónde llega el vehículo de servicio (pregunta del usuario 27/11):
recorte del plano de lugar (regenerado) junto a las dos fotos de 1984 que lo prueban (F14: plaza abierta a la calle; F01: autobús
en la boca del vial). Se regenera desde PLANO_LUGAR_1984.pdf para que nunca quede antiguo (puerta 5)."""
import pypdfium2 as pdfium
from PIL import Image, ImageDraw, ImageFont
import laminas as LM

f = lambda s: ImageFont.truetype("DejaVuSans.ttf", s)
pg = pdfium.PdfDocument("PLANO_LUGAR_1984.pdf")[0]
im = pg.render(scale=2).to_pil(); w, h = im.size
plan = im.crop((0, int(h * 0.08), int(w * 0.47), int(h * 0.92))).convert("RGB")
plan = plan.crop((60, 280, 1500, 1760)) if plan.width > 1500 else plan
plan.thumbnail((1300, 1340))
f14 = Image.open(LM.IMG + "14.webp").convert("RGB"); f14.thumbnail((640, 640))
f01 = Image.open(LM.IMG + "1.webp").convert("RGB").crop((420, 300, 828, 762)); f01.thumbnail((640, 700))
W = plan.width + 680; H = max(plan.height, f14.height + f01.height + 160) + 90
c = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(c)
d.text((20, 15), "¿Desde dónde llega el vehículo? Desde la calle Ivana Mazepy, cruzando la plaza (abierta a la calle, sin bordillo)",
       fill="black", font=f(24))
c.paste(plan, (10, 70))
x = plan.width + 30; y = 70
d.text((x, y), "F14 (1984): la plaza es asfalto continuo con la calle;", fill="black", font=f(19))
d.text((x, y + 24), "un coche circula por ella y los autobuses aparcan", fill="black", font=f(19))
c.paste(f14, (x, y + 55)); y2 = y + 55 + f14.height + 20
d.text((x, y2), "F01 (1984): el autobús está en la boca del vial,", fill="black", font=f(19))
d.text((x, y2 + 24), "donde la plaza se une al vial de servicio", fill="black", font=f(19))
c.paste(f01, (x, y2 + 55))
sx = f01.width / 408; bx, by = (770 - 420) * sx, (640 - 300) * sx
d.ellipse((x + bx - 40, y2 + 55 + by - 30, x + bx + 40, y2 + 55 + by + 30), outline="black", width=4)
c.save("ACCESO_VEHICULO.png"); print("ok", c.size)
