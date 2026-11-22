# Revisión autónoma: modelo frente a fotos (mientras estabas fuera)

## Método aplicado
- Cada foto se calibra matemáticamente: la cámara se ajusta por mínimos cuadrados a las siluetas de los cilindros (barril, tambor, remate, columna) y a las aristas del chaflán.
- Después se superpone el modelo completo (aristas en rojo, volumen en azul) y se anota qué coincide y qué no.
- Pasadas hechas: 3 sobre F01 (aérea de época, con variaciones del ángulo del chaflán) y 1 sobre F09 (frontal con teleobjetivo).

## Lo que COINCIDE (comprobado varias veces)
| Rasgo | Fotos | Resultado |
|---|---|---|
| Torre: barril, tambor de ojos, tambor superior | F01, F09 | Error de calibración de unos 5–7 px |
| Visera desplazada hacia la izquierda, unos 2,4 m (F09) | F09 | Coincide con el modelo |
| Columna de unos 6 m de ancho | F09 | 84 px ≈ 6,1 m |
| Restaurante en el chaflán, unos 12 m | F09 | El modelo tiene 11,6 m |
| Ala corta (restaurante, bloque alto con lucernarios, ladrillo sobre pilares) | F01 | Posición y alturas aproximadamente correctas |
| Chaflán: banda de planta primera a +8,9 | F01, F09 | Coincide |

## Lo que NO coincide (discrepancias detectadas)
1. **Dirección del ala larga respecto al chaflán (la más grave).**
   - En F01 el bloque de la terraza sale hacia la derecha con poca pendiente, hasta x≈728 px. En el modelo, el ala larga sale casi recta hacia atrás, escondida detrás de la torre.
   - He probado ángulos del chaflán de 31°, 34–49°, 40° y 50° (`revision_F01_chaflan_40_50.png`). Con 40–50° la dirección mejora, pero la pendiente no llega a coincidir con ningún ángulo.
   - Conclusión: la relación torre–L de la planta (ángulo del chaflán y posición de la torre sobre él) no está bien. Ninguna combinación de los parámetros actuales encaja F01 y F09 a la vez, así que no la he cambiado a ciegas.
2. **Frente del hotel en planta primera.**
   - F09 da unos 9,1 m (de la columna a la esquina); el modelo tiene 11,9 m.
   - Con la planta actual, 9,1 m no llega al borde de la rampa, y la esquina a 90° quedaría hacia dentro, contra tu dibujo. Es otra señal de que la discrepancia 1 es real. Lo dejo pendiente.
3. **Muro del relieve de estrellas (F09).**
   - A la derecha de la banda del hotel, F09 muestra un muro casi frontal de unos 13 m a la misma altura que la banda, con la planta baja hundida debajo. En el modelo no hay nada equivalente.
   - Por su tamaño aparente, podría ser la cara exterior de la rampa o concha vista en escorzo, que en F01 es mucho más grande que en el modelo: unos 8 m de alto junto a la torre y muy ancha.
4. **Ventanas del ala larga:** estaban junto a la torre. **CORREGIDO:** ahora hay 2 filas de 12 al final del ala, en los últimos 30 m (F01, F24, F33).
5. **«Parte diagonal» en la unión con el cilindro:** no me llegó la imagen que mencionabas. Por las plantas, sospecho que es la diagonal del chaflán dentro del ala larga en planta baja, o el arranque en cuña de la rampa. Pendiente de confirmar.

## Fallos del PROCESO que he detectado
- Calibrar una foto solo con cilindros es ambiguo, porque la torre es simétrica alrededor de su eje. Sin aristas de la base, el ajuste da cámaras imposibles (desde detrás, o con un objetivo de 80°). Solución aplicada: limitar la cámara a delante del chaflán y añadir aristas de la base.
- Las aristas que leo a mano en fotos pequeñas tienen errores de 5–10 px. Si asigno mal un elemento, el ajuste sale imposible en vez de dar un error claro.
- Las vistas de Google y Bing con medidas (F35–F39) son 3D inclinadas: sirven para longitudes a nivel de cubierta, no para la posición de la torre.

## Lo que necesito de ti al volver (respuestas cortas)
1. En F01, el bloque de la terraza con sombrillas que sale a la derecha hasta el borde de los árboles, ¿es el ala larga completa (94 m) o solo un tramo?
2. En F09, el muro con el relieve de estrellas a la derecha de «ГОТЕЛЬ», ¿es la cara exterior de la rampa o concha, o es otra pieza?
3. ¿Qué parte es la «diagonal» de la unión con el cilindro? Un círculo sobre cualquier imagen basta.

Con esas tres respuestas puedo fijar la planta torre–L y volver a pasar todas las fotos.
