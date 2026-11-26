"""RONDA ABSOLUTA (26/11 tarde): medidas nuevas para la matriz v2. Prevalecen sobre las anteriores de la misma celda.
Método: cocientes dentro de una misma fila de la foto (sin cámaras), escala por el paso de forjados (F09 12,9 px/m),
ojos como referencia angular en Alamy (5 ojos, residuo ±5 px), vistas cruzadas (abatimiento F09 ⟂ Alamy)."""
import json
R = {}
def put(col, zonas, est, nota):
    for z in zonas.split():
        R.setdefault(z, {})[col] = (est, nota)

# Z01 remate y letrero
put("C04", "Z01", "OK", "F09: remate/tambor 0,375 → R 5,1; centrado (+0,07); САЛ con la С a +15° → 2.ª palabra (az 330°)")
put("C03", "Z01", "OK", "F02 0,376 · F14 0,377; centrado (0,0 / −0,22)")
put("C01", "Z01", "OK", "F01: remate/tambor 0,382; «ЮТ … liso … С»: hueco entre las dos palabras")
put("C02", "Z01", "OK", "F23: remate/tambor 0,387")
put("C24", "Z01", "≈", "alturas OK (MGF); ancho 4,6 = −10 % (Alamy comprimida por encima del tambor: 5 fotos contra 1); palabra 1 de −90° a +38°")
put("C09", "Z01", "≈", "F19: САЛЮТ sigue la curva del remate (С de canto, Т girando); ГОТЕЛЬ es reciente → fuera")
put("C10", "Z01", "≈", "F08: …АЛЮТ y otra С a la derecha → la palabra se repite")
# Z02 visera
put("C04", "Z02", "OK", "F09: visera/tambor 0,948 → R 12,9; vuela 0,9 m fuera del peto del barril (modelo 0,90); centro −2,37 según U")
put("C03", "Z02", "OK", "F14 0,953 (canto 1,88/1,89) · F02 0,944; centro F14 −2,87")
put("C01", "Z02", "OK", "F01: visera/tambor 0,953")
put("C02", "Z02", "OK", "F23: visera/tambor 0,958")
put("C24", "Z02", "≈", "canto 1,89 y cotas OK; R 11,4 calibrada con los ojos (−10 %, ver Z01)")
# Z03 banda
put("C04", "Z03", "OK", "F09: centro −1,55 según U (antes −0,5 supuesto) → OB (−1,7, −2,26) con el lateral de Alamy 2,75")
put("C03", "Z03", "OK", "F14: ancho 0,70 del tambor = Alamy (R 9,45); centro −1,94")
# Z04 tambor
put("C24", "Z04", "OK", "5 ojos visibles (OJ08–OJ12) ajustan con residuo ±5 px: vista 179,7° y fase de ojos confirmadas; R 13,54 por el borde")
put("C04", "Z04", "OK", "F09: 8 ojos cada ≈19°; ojo frontal 20 px = 1,55 m (modelo 1,60)")
# Z06 barril + gárgolas
put("C04", "Z06", "OK", "F09: peto del barril/tambor 368/349 = 1,054 (modelo 1,063)")
put("C05", "Z06", "OK", "F18: gárgolas, una por módulo y planta en el canto bajo la ranura (modelo 17 × 6, solo en planos)")
put("C10", "Z06", "≈", "F08: gárgola centrada entre aletas en el canto de la cubierta del barril")
# Z07 1.ª planta (pavés)
put("C04", "Z07", "OK", "F09 (12,9 px/m): banda 1,09 SIN ranura + pavés 1,40; borde inferior +14,51")
put("C05", "Z07", "OK", "F18: techo visible sobre el pavés (retranqueado, en el plano de las ventanas); banda continua")
# Z08 fondo inclinado y ménsulas
put("C04", "Z08", "OK", "F09: fondo en sombra bajo la banda (borde +14,51 → cuello +13,90)")
put("C05", "Z08", "OK", "F18: 19 vigas bajo el fondo inclinado, de la aleta al cuello")
# Z09 cuello
put("C04", "Z09", "OK", "F09: cuello 223 px = 17,3 m (modelo 18,0; ±1)")
# Z15 fuente
put("C01", "Z15", "OK", "F01: vaso en media luna, cuerda 145 px frente a la columna 83 px (6,5 m) → 11,4 m (R 5,7)")
put("C03", "Z15", "≈", "F14: chorros en abanico ante la cristalera de PB, bordillo bajo")
put("C08", "Z15", "≈", "F15: chorros en abanico")
# Z10 columna, Z14 entrada en hueco
put("C03", "Z10", "OK", "F14 (13,29 px/m): columna 80 px = 6,0 m (modelo 6,5 ± 0,6); asoma delante de la banda del restaurante")
put("C08", "Z14", "OK", "F15: techo de PB +3,20 con el autobús como escala; PB oscura retranqueada bajo la banda")
put("C03", "Z15", "≈", "F14: chorros en abanico a la izquierda de la columna (6,5 m), la derecha tapada por el autobús; bordillo bajo")
# Z34 dientes de sierra
put("C01", "Z34", "OK", "F01 (1984): recuento 5 en línea + 5 escalonados (usuario 26/11)")
# Z29 escalera: conflicto nuevo con F09
put("C04", "Z29", "OK", "F09: con el muro sobre el tambor (eje de la cuña, hasta r 13,85) no asoma a la derecha de la visera (antes sí: DUDA 7)")
put("C28", "Z29", "OK", "dron del usuario 26/11: muro sobre la terraza del tambor, acaba en su borde (fuera solo lamas), coronación que vierte hacia dentro")
put("C28", "Z01", "OK", "dron del usuario 26/11: САЛЮТ entero y de frente desde el patio = 2.ª palabra del arco")
put("C28", "Z02", "OK", "dron del usuario 26/11: claraboya hacia la plaza (az 320°), a ≈130° de la escalera")
put("C24", "Z29", "≈", "Alamy: coronación +40,6 → +41,7 OK; su extremo exterior ≈ 1,5 m más fuera que el muro (Alamy por encima del tambor)")
put("C31", "Z07", "OK", "postal 1984 (usuario 26/11): pavés en la 1.ª planta, banda continua debajo y ménsulas")
json.dump(R, open("RONDA_ABSOLUTA.json", "w"), ensure_ascii=False, indent=0)
print(sum(len(v) for v in R.values()), "celdas")
