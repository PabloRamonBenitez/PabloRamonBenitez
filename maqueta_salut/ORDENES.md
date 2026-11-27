# Órdenes y mandatos del usuario: lista viva (se repasa ENTERA antes de cada entrega)

Cada orden lleva su fecha y cómo se comprueba. Si una entrega contradice una línea, no sale.
**A** = automática (`auditoria_planos.py` / `coherencia_vistas.py`), **F** = foto (collage o lámina), **M** = revisión manual en la hoja de nudos.

## Método (cómo trabajar)
| # | Orden | Fecha | Control |
|---|---|---|---|
| M1 | Lo nuevo **complementa** lo medido; nunca se pisa un dato comprobado (p. ej. la triangulación A–B–C–D) con una lectura suelta | 25/11 | A (triangulación) |
| M2 | Nada inventado sin datos; el 3D solo lo que se sabe. Los supuestos, marcados como tales en planos e informes | 26/11 | M |
| M3 | Cada duda: aislarla, reunir **todas** las fotos, intentar resolverla; si no, **preguntar con gráfico**, nunca solo con texto | 26/11 | M |
| M4 | Una imagen tiene que coincidir con **todas**: cada cambio se compara con todas las fotos que lo muestran, no solo con una | 26/11, 27/11 | F |
| M5 | Las cámaras ajustadas no valen; se trabaja con proporciones y geometría descriptiva (abatimientos, giros, homografías de planos conocidos) | 26/11 | M |
| M6 | Repasar la conversación y esta lista antes de entregar; leer las marcas del usuario en su contexto | 26/11, 27/11 | esta lista |
| M7 | Una cota, una fuente: ninguna medida definida en dos sitios (p. ej. suelos del barril → `niveles_suelo()`) | 27/11 | A (escalera = forjado) |
| M8 | Alamy manda en la torre en **alturas y posiciones**; en anchos por encima del tambor mandan las otras 5 fotos | 25–26/11 | F (collage Alamy y F09) |
| M9 | Plano de lugar y entorno: **según la foto histórica (1984)**, no según la actual (vallas, Google) | 26/11, 27/11 | F (F01, F47, F23) |

## Representación
| # | Orden | Fecha | Control |
|---|---|---|---|
| R1 | Normas de Ching y de graficación: solo líneas, sin colores; cortado grueso con trama, visto fino, por encima discontinuo | 26/11 | M |
| R2 | Rampas: contorno y triángulo muy fino, base en el arranque y vértice arriba, sin punto; nunca curvas de nivel | 26/11 | M |
| R3 | Sistema de cotas relacionadas (planta ↔ sección ↔ alzado) y proyecciones de vigas | 26/11 | M |
| R4 | Escalera en planta y sección de ida y vuelta: rellano de vuelta en el cono, rellanos de planta = forjados, paso libre, acaba en la última planta | 26/11, 27/11 | A + M |
| R5 | Carpintería dibujada como en arquitectura (marco, hoja, vidrio, vierteaguas) | 26/11 | M |
| R6 | Textos de los juegos A3/A4 y del plano de lugar en **ucraniano** | 26/11 | A (0 palabras en español) |
| R8 | Sin símbolos repetidos: un solo camión, como referencia de tamaño | 27/11 | M |
| R9 | En planta, lo que queda **debajo** de un elemento más alto se oculta: la cubierta del restaurante y la rampa bajo el barril, incluidos sus rótulos. Los rótulos caben en la parte que se ve | 27/11 | M (`laminas.oculta`) |
| R7 | Sin interiores inventados, salvo lo autorizado: núcleo 0,45, pasillo 1,20, muros radiales en el eje de las aletas (solo en planos) | 26/11 | M |

## Edificio: decisiones cerradas (no se pueden perder)
| # | Orden | Fecha | Control |
|---|---|---|---|
| E1 | Planta redonda; 19 módulos; balcones de 1,20 con el suelo a la cota de la habitación | 21/11, 26/11 | A |
| E2 | Sin ángulo de 90° en la parte de atrás; línea posterior paralela al chaflán | 22/11, 25/11, 26/11 | A |
| E3 | X sale de la triangulación (A–B 7,3 · A–C 16,66 · A–D 106,69 · D–C ≤ 1,5 %) | 22/11, 25/11, 26/11 | A |
| E4 | Ala larga recta, sin zapato ni tacón; el muro de ventanas retranqueado 0,80 llega hasta el testero | 22/11, 23/11, 26/11, 27/11 | A |
| E5 | Base de la torre en ángulo recto: fondo plano, vigas rectas, aletas con escalón, 1.ª planta de pavés enrasada, cuello sin losa volada | 26/11 | A + F (collage base) |
| E6 | Escalera: cuña con 16 lamas, cristalera y puerta a la izquierda, muro de coronación sobre el tambor que vierte hacia dentro | 25/11, 26/11 | A + F |
| E7 | Letrero САЛЮТ ×2 en arco y **en volumen**, arriba, alrededor del remate | 22/11, 26/11, 27/11 | A + F |
| E8 | Visera R 12,9 y remate R 5,1 (5 fotos); banda desplazada; remate en el eje | 26/11 | A + F |
| E9 | Concha P2 / G3; giro de 180° en U; techo del restaurante inclinado (no rampa de paso); cristalera bajo el arco: 3 paños | 26/11 | A |
| E10 | Fachada del chaflán plana (sin el «sofito» de los toldos); 5 y pico + 4 y pico ventanas; cristaleras en la PB bajo las dos bandas | 26/11, 27/11 | A |
| E11 | Garaje en la PB del ala corta junto a la medianera, bajo la logia (F72) | 27/11 | A |
| E12 | **Sin fuente** | 27/11 | A |
| E13 | 6 lucernarios pequeños bajo el cuello (≈ 75°), en el camino de la rampa | 26/11 | A |
| E14 | 10 lucernarios del bloque alto: **pirámides** de base cuadrada (1,30 × 1,20, `PIR_*` en el cuadro), junto a la medianera. Colocación: **duda 8 pendiente** (`DUDA8_LUCERNARIOS.png`, H1/H2/H3); el modelo lleva H1 como provisional | 26/11, 27/11 | F (duda 8) |
| E15 | Gárgolas: una por módulo y planta (solo en planos) | 26/11 | A |

## Entorno (plano de lugar, foto histórica)
| # | Orden | Fecha | Control |
|---|---|---|---|
| L1 | Desde arriba, con el verde exterior según la foto histórica; sin vallas posteriores | 26/11 | F (F47, F01) |
| L2 | Caminos según las marcas verdes del usuario: vial paralelo al ala desde la plaza que **rodea el testero por detrás**, paso transversal a la fachada, senda junto al césped | 26/11 | F (F47) |
| L3 | Recorrido de un vehículo de servicio que pueda maniobrar (dibujado con su barrido) | 26/11 | M |
| L5 | Todo recorrido **empieza y acaba en la vía pública**: que se vea desde dónde llega el vehículo. Entra por la calle Ivana Mazepy y cruza la plaza, que está abierta a la calle (F14, F01). El tramo del patio, sin foto, va a trazos con «?» | 27/11 | M (`ACCESO_VEHICULO.png`) |
| L4 | Nada de la foto actual (Google) que contradiga la histórica | 27/11 | F |

## Molde
| # | Orden | Fecha | Control |
|---|---|---|---|
| D1 | Versión paralela del volumen para molde de silicona y colada de hormigón, con el detalle que tenga sentido a 15 cm | 27/11 | A (`molde_stl.py`) |
