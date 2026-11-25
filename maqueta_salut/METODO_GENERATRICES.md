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

## Dirección de la vista de Alamy: corregida de 230° a 179,7° (`vista_alamy.py`, PLANTA_ORIENTACION_ALAMY.png)
- **Error:** las aletas se repiten cada 18,95°, así que solo fijan el giro módulo un paso. El giro de 7,6° escondía una dirección de vista equivocada.
- **Referencia no periódica:** la cuña de la escalera aparece en el borde izquierdo de la silueta (s −15,8…−16,2; corona +40,6/+41,7),
  así que su eje está a ~90° del eje de la vista. Con las aletas (α mod 18,95° = 9,21°, dispersión 0,8°) quedan tres candidatas:
  160,8° (la escalera taparía los balcones de la izquierda ✗), **179,7° ✓** y 198,7° (la escalera quedaría oculta ✗).
- **Consecuencias:**
  - giro de los muros 14,21°: M3 = 71,05° y M5 = 108,95° son los bordes del hueco de escalera, de 2 módulos (37,9°);
  - lado ciego 110°–166°, junto a la escalera; 14 ojos;
  - desplazamientos (componente lateral de Alamy + componente U de F09): banda (−0,5; −3,70), visera (−2,4; −4,09), remate (0,6; −0,38), lucernario (0; −13,06).
- **Comprobación:** aletas, residuo medio 0,03 m; escalera lateral −16,20 (foto −15,8…−16,2); lucernario lateral 8,34 (foto 8,34); MGF y 66 + 18 comprobaciones OK.

## Barandillas abiertas (25/11)
La barandilla de la visera y la del barril estaban modeladas como muros macizos de 1 m y 0,85 m. En el alzado se dibujaban como parte de la losa:
la visera parecía medir 2,9 m en lugar de 1,89 m, y el modelo no se parecía a la foto aunque la medida fuera correcta.
Ahora son barandillas abiertas (pasamanos, travesaño y postes cada 2 m), como se ven en las fotos (transparentes).
Regla del método: **en el alzado del modelo se mira el silueteado de cada pieza, no solo su cota**; un elemento transparente en la foto no puede ser macizo en el modelo.

## Collage y perspectiva oculta (25/11) – `collage_alamy.py` → COLLAGE_ALAMY.png
**Paso fijo del método:** la foto, al 50 %, se superpone al alzado del modelo con la misma escala, el mismo eje y la misma cota. Se resuelve todo lo que no coincide.
- **Altura de la cámara.** Los forjados del barril se curvan con los extremos hacia arriba, porque están por debajo del ojo. La visera se curva con los extremos hacia abajo, porque está por encima.
  La cámara está a ≈ +38 m y lejos (vista de teleobjetivo). Consecuencias:
  - el remate y la visera se ven desde abajo, así que su coronación aparente es el borde frontal: la lectura en la generatriz es correcta;
  - el efecto de la perspectiva sobre las cotas es de ≤ 0,1 m.
- **Diferencias resueltas con el collage:**
  1. Caja de escalera: por encima del tambor termina en r = 10,2 (entre ella y la banda se ve cielo). Su cubierta está inclinada, de +41,6 fuera a +40,8 dentro. Antes llegaba a la banda y era plana a +41,29.
  2. Letrero САЛЮТ: 5 letras en un plano frente a la cámara, de s −7,2 a +4,0 y de +46,3 a +48,5. La de la izquierda vuela sobre la celosía.
  3. Zócalo (poyete) del remate: R 5,7, de +43,18 a +43,58.
  4. Barandillas abiertas (ver arriba).
- **Comprobado sin cambios:** remate, visera, banda, tambor, forjados, aletas, lucernario; los ojos quedan a ≤ 0,4 m.

## Caja de escalera con las fotos nuevas (25/11) – `escalera_fotos.py` → ESCALERA_FOTOS.png
- **Foto lateral.** Su escala sale de la propia caja: las juntas de las lamas van cada 138 px = 3,10 m, a la altura de los forjados.
  Medidas: remate de hormigón de 2,97 m sin lamas, con la cubierta **horizontal**; frente de lamas de 6,0 m, más una escalera de gato de 0,7 m.
- **Dron.** La parte alta es una caja apoyada en la terraza del tambor. El peto del tambor se corta en la escalera y las lamas siguen por fuera del barril.
- **Corrección (usuario):** la coronación SÍ es inclinada: +41,6 fuera → +40,8 dentro. Puede ser un muro o un lucernario en pendiente para el agua.
  Alamy la ve de perfil y el dron lo confirma. La foto lateral mira la caja de frente y no puede ver la pendiente: fue un error mío darla por plana.
  **Regla:** una foto solo mide lo que tiene de perfil.
- Lamas finas: espesor 0,08 cada 0,35 m (antes 0,24 cada 0,8), hasta +38,20.
- **Lucernarios bajo el cuello:** no forman un anillo completo, porque la caja de escalera ocupa ese sector (usuario).

## Escalera de frente (25/11, fotos del usuario) – `escalera_frente.py` → ESCALERA_FRENTE.png
Esto es ahora la verdad sobre la escalera:
- **16 lamas** en el frente del cuerpo.
- **Bordes del corte del barril cerrados con lamas**, de +13,90 a la coronación del tambor (+38,73), en los dos lados.
  Detrás puede haber muro o vidrio; el lado derecho es seguro y el izquierdo se supone igual.
- **~2 m (una puerta)** entre el corte del barril y el cuerpo de la escalera: la cuña pasa de 25° a **20,2°**.
  Su frente queda en 5,6 m, que coincide con los 5,8–6,0 m de la foto lateral (antes daba 6,9).
- Las lamas del cuerpo terminan bajo el remate (+38,20). El remate es inclinado; su punto más alto es la esquina exterior (+41,6).
