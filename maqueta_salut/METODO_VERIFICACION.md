# Método de verificación (pasada 10)

## Por qué fallaba
- No ponía el plano y la foto en el mismo sistema de referencia. "Comparar" era mirar dos imágenes una al
  lado de otra y escoger 2-3 detalles. Con eso se escapan curvas, recuentos y proporciones evidentes.
- La herramienta para hacerlo (calibrar la cámara de cada foto con la torre y proyectar el modelo) ya existía;
  la abandoné cuando dio problemas (la torre es simétrica → la cámara puede girar) y la sustituí por estimar
  cotas sueltas con rangos. Un rango de una cota no es una comprobación.
- Usaba las fotos como mina de datos ("ya tengo lo que necesito"): saco un valor, cambio la cota, redibujo y doy
  por comprobado con la misma foto de la que saqué el valor. Es circular.
- Cambiaba cotas a partir de una sola observación, saltándome tu regla: anotar todas las diferencias primero,
  corregir en bloque después.
- Mi cobertura era igual a tus comentarios: comprobaba lo que me señalabas, no el edificio.

## Cómo es ahora
1. **Catálogo de puntos** (`puntos_ref.py` → PUNTOS_REFERENCIA.csv): 610 puntos y ~150 líneas por zonas
   (torre, escalera, ala larga, testero, ventanas una a una, bar, rampa, base), calculados solo del cuadro.
2. **Calibración por foto** (`verif_foto.calibrar`): torre (siluetas + forjados) y el mínimo de anclajes para fijar
   el giro. Lo que se verifica no entra en la calibración. Una cámara que no baje de un error razonable
   invalida la foto para la matriz (no se usa).
3. **Prueba conjunta**: si ninguna cámara encaja a la vez todas las anclas, el cuadro es incoherente con esa foto
   (ej. F01: la banda del hotel queda a 42 px con cualquier cámara).
4. **Apoyo por líneas** (`verif_foto.soporte`): cada línea del cuadro se proyecta y se muestrea; una muestra cuenta
   solo si en la foto hay una arista a < 0,35 m con la MISMA orientación. Resultado por línea y por zona.
5. **Matriz líneas × fotos** (SOPORTE_<foto>.csv): las líneas en magenta son diferencias anotadas.
6. **Corrección en bloque** solo cuando la matriz cubre todas las fotos; cada cambio de cota cita las líneas y
   fotos que lo justifican; después se repite la pasada completa y se comparan los porcentajes.

## Límites conocidos (y qué hago con ellos)
- Árboles, verjas y coches dan aristas falsas → falsos "apoyos". Hay que enmascarar esas zonas en cada foto.
- F73: calibración todavía mala (25 px) → sus resultados NO valen hasta remedir la torre con rejilla.
- Elementos que no están en el cuadro no se pueden verificar: la rampa a la azotea del bar falta → se añade al
  catálogo como elemento pendiente de definir, no se inventa.

## Primera fila fiable: F01 (1984, error de calibración 12,9 px)
| zona | apoyo |
|---|---|
| torre forjados | 86 % |
| torre tambor | 93 % |
| ventanas fila alta | 67 % |
| ventanas fila baja | **10 %** (tu recuento: 7 abajo, cuadradas; el plano tiene 10 + puerta, rectangulares) |
| rampa peto | **6 %** (la concha real está mucho más alta que mi rampa) |
| rampa arco | **25 %** |
| pie de fachada ala larga | 35 % |
| remate (borde superior) | 14 % |
Observaciones tuyas incorporadas a la matriz como dato: 11 ventanas arriba, 7 abajo, todas cuadradas; el
vuelo del bar termina antes del final; hay una segunda rampa a la azotea del bar.
NO se ha cambiado ninguna cota en esta pasada.
