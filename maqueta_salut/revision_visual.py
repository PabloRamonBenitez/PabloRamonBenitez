"""Cierre de las celdas «?» de la matriz v2 (26/11): revisión foto por foto.
Criterio: OK = proporción medida en la foto coincide con el modelo; ≈ = la zona se ve y coincide en forma, número y posición
(sin medida fiable en esa foto); – = la foto no sirve para esa zona (maqueta = solo organización; mapas = orientativos)."""
import json
R = {}
def put(col, zonas, est, nota):
    for z in zonas.split():
        R.setdefault(z, {})[col] = (est, nota)

# C16 F22 maqueta: el usuario la limita a organización → no verifica medidas
put("C16", "Z01 Z02 Z03 Z04 Z05 Z06 Z07 Z08 Z09 Z10 Z16 Z17 Z18 Z19 Z20 Z22 Z23 Z24 Z25 Z26 Z27 Z28 Z29 Z30 Z31", "–", "maqueta: solo organización (no es lo construido)")
put("C16", "Z21", "≈", "maqueta: giro de la rampa y techo inclinado coinciden en organización")
# C03 F14/F02 (1984, frontal desde la plaza; paso de forjados 41,2 px = 3,10 m)
put("C03", "Z02", "OK", "F14: canto de la visera 25 px = 1,88 m (modelo 1,89)")
put("C03", "Z06", "OK", "F14: 7 forjados equidistantes, paso 41,2 px (3,10 m); 19 módulos")
put("C03", "Z08", "OK", "F14: base del cuello +9,0/9,4 (duda 1); ménsulas bajo el barril")
put("C03", "Z01 Z03 Z04 Z05 Z07 Z10 Z11 Z12 Z13 Z14 Z15 Z16 Z17 Z18 Z20", "≈", "F14/F02: forma, número y posición coinciden; sin medida fiable (vista desde abajo)")
# C02 F23 (aérea 1984, como F01 más lejos)
put("C02", "Z01 Z02 Z03 Z04 Z05 Z06 Z07 Z10 Z16 Z18 Z19 Z21 Z24 Z25 Z26 Z27", "≈", "F23: igual que F01 desde más lejos; organización y proporciones coinciden")
# C09 F19 (calle, actual)
put("C09", "Z01 Z02 Z03 Z04 Z05 Z06 Z07 Z10 Z11 Z16 Z17 Z19", "≈", "F19: silueta desde la calle; letrero sobre el remate y rótulo ГОТЕЛЬ en la visera (actual)")
# C05 F18 (actual, desde la plaza)
put("C05", "Z02 Z04 Z06 Z07 Z08 Z09 Z10 Z12 Z14 Z15 Z21 Z22", "≈", "F18: cuello, ménsulas, bandas, concha con relieve; coincide en forma")
# C17 F35 (Google cenital: orientativo)
put("C17", "Z02 Z06 Z15 Z16 Z18 Z19 Z21 Z25 Z26 Z27 Z29 Z31", "≈", "F35: cenital orientativa; organización en planta coincide")
# C10 F08 (dron desde detrás)
put("C10", "Z01 Z02 Z03 Z04 Z05 Z06 Z07 Z29 Z30", "≈", "F08: tambor con ojos, banda, escalera con lamas y muro inclinado")
put("C10", "Z18 Z20", "≈", "F08: ala corta desde detrás, parcialmente tapada")
# C04 F09 (frontal teleobjetivo)
put("C04", "Z04 Z05", "OK", "F09: tambor +38,73 (corr. profundidad), barandilla de la cubierta del barril")
put("C04", "Z08 Z10 Z12 Z14 Z15 Z16 Z21 Z22", "≈", "F09: base del chaflán, columna y concha en forma")
# C08 F15 (1984, base con autobuses)
put("C08", "Z07 Z08 Z09 Z10 Z11 Z12 Z13 Z14 Z16 Z17", "≈", "F15: base, fuente, columna, bandas y PB hundida en forma")
# C01 F01 (restos)
put("C01", "Z03 Z05 Z07 Z13 Z14 Z15", "≈", "F01: visibles y coincidentes en forma (fuera del barrido por puntos)")
# C12 F10 (remate de cerca)
put("C12", "Z01 Z02 Z03 Z04 Z05", "≈", "F10: letras sobre el remate, visera con barandilla, banda acristalada, ojos con tubos")
# C14 F12 / C15 F13 / C13 F11 (escalera)
put("C14", "Z06 Z25 Z26 Z29 Z30", "≈", "F12: encuentro escalera–barril–cubierta")
put("C15", "Z06 Z28 Z29 Z30", "≈", "F13: escalera con lamas y borde del barril")
put("C13", "Z06 Z29 Z30", "≈", "F11: rellanos tras las lamas")
# C18 F38 (Bing con medidas)
put("C18", "Z21 Z23 Z26 Z27", "≈", "F38: medidas de planta del ala larga ya incorporadas (12,74 · 6,21 · 7,81 · 35,13)")
# C11 F04/F06 (barril de cerca)
put("C11", "Z04 Z05 Z06", "≈", "F04/F06: módulo del barril, ojos y barandilla")
json.dump(R, open("REVISION_VISUAL.json", "w"), ensure_ascii=False, indent=0)
print(sum(len(v) for v in R.values()))
