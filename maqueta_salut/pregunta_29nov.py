import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(16, 10)); ax.set_xlim(0,16); ax.set_ylim(0,10); ax.axis('off')
ax.text(0.3,9.6,"Hotel Salut · preguntas para Pablo · 28/11/2026",fontsize=18,weight='bold')
def caja(x,y,w,h,col,tit,lin):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.05",fc=col,ec='#444'))
    ax.text(x+0.2,y+h-0.35,tit,fontsize=12.5,weight='bold',va='top')
    for i,l in enumerate(lin): ax.text(x+0.25,y+h-0.95-i*0.42,l,fontsize=10.5,va='top')
caja(0.3,5.0,7.6,4.2,'#e8eef8',"P1 · ¿Apruebas la división? (DESMONTABLE_DIVISION.png)",[
 "a) Corte a z = 13,71 m (fondo de las vigas)",
 "b) Cilindro Ø 9,0 m × 3,0 m  (maqueta ≈ 26,6 × 8,9 mm)",
 "c) Llave 1,2 × 0,9 + surco de entrada + canal 1,5 × 1,05",
 "",
 "⚠ Holgura: el plano dice 0,15 m real ≈ 0,44 mm por lado;",
 "   el traspaso dice 0,1 mm por lado en resina (≈ 0,034 m).",
 "   ¿Cuál? Sin esto no genero los modelos 3 y 4.",
 "Responde: «sí», «sí con 0,1 mm» o qué cambiar."])
caja(8.1,5.0,7.6,4.2,'#e8eef8',"P2 · Textos de Etsy: ¿apruebas cada uno?",[
 "Texto 1 → MoldeSilicona (Alfredo y Karina), ES",
 "Texto 2 → HOUSEOFMOLDS (Tania), EN",
 "Texto 2 adaptado → PLAybelope (Razieh), EN",
 "Texto 3 → 3DDeluxeStore (Scott), EN  (lleva enlace pieza A)",
 "Texto 4 → StudioRollins, EN  (promete imágenes)",
 "Textos completos: ESTADO_MOLDES_Y_PROVEEDORES.md §4",
 "Desde aquí no puedo enviar en Etsy: lo haces tú",
 "o la sesión del Mac con Chrome."])
caja(0.3,0.5,7.6,4.2,'#fde8b0',"Lo que he visto en Gmail (dato, no supuesto)",[
 "✗ moldesilicona.com (Alfredo Bueno) RECHAZÓ el 27/11:",
 "  «no puedo ofrecerle el servicio». No figuraba → cerrado.",
 "  (¿Es la misma persona que MoldeSilicona en Etsy? Sin confirmar.)",
 "✓ MinghuiLink: el texto 5 (tambor y base) YA SE ENVIÓ",
 "  el 28/11 a las 11:50. Sin respuesta todavía.",
 "· Flossy, Modelarte, Milab3D: sin respuesta.",
 "· Etsy: en Gmail solo hay 1 aviso por hilo (no veo Etsy)."])
caja(8.1,0.5,7.6,4.2,'#d8f0d8',"P3 · ¿Has contestado tú algún hilo?",[
 "En Etsy, WhatsApp o por teléfono, ¿has contestado",
 "a alguno de los cinco hilos de Etsy, a Aaron (MinghuiLink)",
 "o a algún otro proveedor?",
 "Desde aquí solo veo el correo de Gmail.",
 "",
 "Si alguno ya está contestado, lo quito de pendientes."])
plt.savefig('PREGUNTAS_29NOV.png',dpi=110,bbox_inches='tight')
