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

## Corrección de la referencia (25/11, tarde) y comprobación de la torre completa en F09 (`mgf_f09.py`)
- **Error:** en Alamy tomé la banda blanca de y = 1306 como +32,50. Es la **cara superior** del canto de 0,65 de la losa de cubierta del barril: +33,15 (la cara inferior está en y = 1337).
  Se nota porque la barandilla queda 0,9 m por encima de esa banda.
- **Contraste independiente en F09:** ajuste proyectivo con las caras inferiores de los 7 forjados del barril (rms 0,02 m).
  Las piezas que no están en el plano del frente de balcones se corrigen por profundidad (cámara a 1,6 m de altura, D ≈ 239 m).
  | pieza | Alamy (MGF) | F09 real | modelo nuevo |
  |---|---|---|---|
  | tambor | +38,84 | +38,73 | +38,85 |
  | visera, cara inferior | +41,40 | +41,37 | +41,40 |
  | visera, cara superior | +43,30 | +43,60 | +43,30 |
  | remate | +50,94 | +50,95 | +50,95 |
- **Partes bajas:** la base del cuello sale a **+9,03** en F09 (modelo +10,40). Es un conflicto con la lectura anterior: **no se cambia sin confirmación**.
- **Ojos:** 13 (lado ciego entre 140° y 215°, primer ojo girado −4,3°), Ø 1,70, tubo de 0,8, centro a +35,95. Residuos en Alamy ≤ 0,4 m.

## Alamy como código de la verdad (25/11, noche): torre completa (`alzado_torre_alamy.py` → ALZADO_TORRE_ALAMY.png)
- Referencia definitiva: **cara inferior de la losa de cubierta del barril (y = 1337) = +32,50**. Es independiente del grueso del canto.
  La escala sale de la propia foto: 5 forjados con paso de 175,25 px → 56,53 px/m.
- Barril, leído en la vertical de medida del usuario (x ≈ 1186):
  forjados +32,50 / 29,35 / 26,29 / 23,17 / 20,09 (modelo 32,5 / 29,4 / 26,3 / 23,2 / 20,1);
  canto 0,59 · hueco 1,45 · poyete 0,78 · ranura 0,27 (antes 0,65 / – / 0,90 / 0,10) · barandilla de cubierta 0,85.
- Parte alta: tambor +38,73 · visera +41,29 / +43,18 · remate +50,81 · centro de los ojos +35,84.
- F09 y las demás fotos antiguas de la torre ya no son referencia. En las láminas se sustituyen por la foto de Alamy medida
  (alamy_torre / alamy_alto / alamy_barril).
