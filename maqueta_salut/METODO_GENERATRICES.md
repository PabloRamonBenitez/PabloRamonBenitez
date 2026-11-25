# Método de las Generatrices Frontales (MGF)

**Para qué sirve:** medir cuerpos cilíndricos no coaxiales (tambor, banda, visera y remate) a partir de una foto casi en alzado.

## Principio
En un cilindro fotografiado casi en alzado, solo hay una vertical que se ve en verdadera magnitud: la **generatriz frontal**, la más cercana a la cámara. En la foto cae en el **centro de su silueta**. Fuera de ella, los bordes son elipses y las alturas que se leen quedan falseadas.
Como los cilindros están desplazados entre sí, **cada uno tiene su propio origen**, y cada altura se lee sobre la generatriz de su cilindro.

## Pasos
1. **Escala vertical** con un patrón repetido de la foto (paso de forjados del barril: 175 px = 3,10 m → 56,5 px/m).
   Escala horizontal por separado (foto de pantalla deformada): 64,4 px/m.
2. **Referencia de cota** en un plano conocido (losa superior del barril +32,50) y **comprobación independiente** en otro plano
   (coronación del tambor: foto +38,19, F09 +38,20).
3. **Siluetas:** bordes izquierdo y derecho de cada cilindro → centro (= su generatriz frontal) y diámetro.
4. **Alturas:** base y coronación de cada cilindro leídas solo sobre su propia generatriz.
5. **Marcar las cotas teóricas** del modelo en el alzado del modelo, con los mismos orígenes, y llevarlas a la foto (`generatrices_alamy.py`).
6. **Tomar la foto como origen:** donde la diferencia supera la tolerancia, el cuadro de cotas adopta el valor de la foto
   y guarda en su fuente el valor anterior y de dónde venía.
7. **Comprobar:** se regenera el modelo y el script vuelve a medir la diferencia foto − modelo.
   Tolerancias: 0,10 m en cota y 0,15 m en eje y radio. Además se pasan las comprobaciones de coherencia y las reglas de planos.

## Aplicación del 25/11 (Alamy)
| | antes | foto (MGF) | después | diferencia final |
|---|---|---|---|---|
| coronación de la banda (= intradós de la visera) | +40,50 (F09) | +40,75 | +40,75 | 0,00 |
| coronación de la visera (canto) | +42,30 (1,80) | +42,65 (1,90) | +42,65 | 0,00 |
| coronación del remate | +49,70 (7,40) | +50,29 (7,63) | +50,30 | −0,01 |
| eje de la banda (−N) | 2,60 | 2,75 | 2,75 | 0,00 |
| eje de la visera (−N) | 4,30 | 4,46 | 4,45 | +0,01 |
| eje del remate (+N) | 0,50 | 0,22 | 0,20 | −0,02 |
| radio de la banda / del remate | 9,50 / 4,85 | 9,45 / 4,77 | 9,45 / 4,77 | 0,00 |
| eje del lucernario (−N) | 8,20 | 8,34 | 8,30 | – |
| tambor, visera R, lucernario h | – | coinciden | sin cambio | ≤ 0,04 |

La cuña de la escalera sigue llegando a la visera (+40,75).
Resultado: MGF OK, 66/66 comprobaciones de coherencia, 18/18 reglas de planos.

## Límites
- La base de la banda queda oculta tras el peto del tambor, así que no se puede medir.
- La foto es una captura de pantalla: las escalas vertical y horizontal se sacan por separado.
- La escala tiene un error de ±1 % (paso de forjados ±2 px), unos ±0,2 m en lo alto del remate.

## Aplicación 2 (25/11): tambor, aletas, ojos y balcones (`mgf_tambor.py` → MGF_TAMBOR.png)
Un elemento a radio R y ángulo φ del eje de la vista cae en x = R·sen φ. Así se leen los ángulos en la foto.
| elemento | foto | modelo antes | acción | resultado |
|---|---|---|---|---|
| aletas (postes de los balcones) | 6 medidas, paso 18,9° → **19** | 19, módulo sin giro | **FASE_AL = 7,6°** (desfase medido 7,2–8,1°) | residuo medio 0,04 m, máx 0,24 m en el borde |
| ojos: cota del centro | +35,31 | +35,35 | – | OK |
| ojos: diámetro | 1,67 | 1,60 | – | dentro de ±0,1 |
| ojos: posición | en el centro de módulo (13,5°, 35°, 54,6°); hacia el borde salen más por los tubos (~1 m de vuelo) | centro de módulo | – | OK salvo el primero (−1,1 m) |
| paso de forjados | 3,12 | 3,10 | – | OK |
| borde de balcones (silueta con aletas) | R ≈ 15,1 | R_AL 15,3 | – | OK |
| **sector sin ojos** | a la izquierda del eje (≈ 140°–215° absolutos) no hay ojos | el modelo pone 3–4 | **PENDIENTE**: hace falta otra foto de ese lado | – |
