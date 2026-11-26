# Repaso general (26/11): conversación completa, documentación y matriz v2

## 1. Cómo se ha trabajado (21/11 → 26/11)
| fase | qué pasó | lección |
|---|---|---|
| 21–22/11 | volumen a ojo; el usuario detecta planta no redonda, balcones, desplazamiento de la visera | medir proporciones, no copiar |
| 22/11 | matriz zonas × fotos (31 zonas, 18 columnas) creada y **nunca rellenada** (todo «?») | se abandonó al pasar a corregir |
| 22/11 noche | triangulación A–B–C–D–E del usuario sobre F01 | dato firme; no se puede pisar con una sola foto |
| 23/11 | ventanas 11+7 por proporciones en F73/F01/F47; escalera en cuña; rampa al techo del restaurante; giro H1 | — |
| 24–25/11 | planos A3/A4; proveedores del molde | — |
| 25/11 | X medida en foto frontal (12,7) **pisó la triangulación** → revertido | información nueva = complementaria |
| 25/11 | Alamy como código de la verdad: MGF (generatriz frontal por cilindro), referencia +32,50, vista 179,7° fijada con la escalera | referencias no periódicas |
| 25/11 | escalera: cuña 20,2°, 16 lamas, remate 3 m, muro inclinado, puerta del tambor, cristalera | una foto solo mide lo que ve de perfil |
| 25/11 tarde | interiores inventados en planos y lucernarios colocados por regla | **retirados** (26/11): solo lo que dicen las fotos |

## 2. Cambios de hoy
- Fuera de los planos: distribuciones, ascensores, pasillo anular y tabiques radiales interiores (no hay datos).
- Se mantienen solo elementos con foto: muros y huecos de fachada, logia, escalera, aletas, lucernarios visibles.
- Zonas renovadas (35) y juntas (37): las zonas desaparecidas (dientes de sierra, bloque de ladrillo) se sustituyen por las actuales; nuevas Z32–Z35.
- **MATRIZ_ZONAS_FOTOS_v2.xlsx**: 35 zonas × 28 fotos, con hojas Evidencias, Conflictos, Columnas y Juntas.

## 3. Estado de la matriz v2
| estado | celdas |
|---|---|
| OK (medido o superpuesto) | 32 |
| ≈ (coincide en forma) | 20 |
| NO (conflicto abierto) | 2 |
| ? (visible, sin contrastar tras los cambios) | 173 |

Zonas sin ninguna comprobación: Z10 columna, Z12/Z14 PB del chaflán, Z15 pie de columna, Z20 línea posterior, Z22/Z23 ala larga junto a la torre, Z28 fachada del patio, Z31 patio.

## 4. Conflictos abiertos
Ver la hoja «Conflictos abiertos»: base del cuello (F09 +9,0 / modelo +10,40), perfil de la concha (Booking), posición de los lucernarios del cuello (F78), losa de arranque de la escalera, línea posterior del ala corta, cara superior de la visera, U de 180° y curva abierta de la planta de cubiertas.

## 5. Siguiente paso propuesto
Barrido foto por foto (no zona por zona): para cada foto se hace su collage al 50 % sobre la vista del modelo desde la misma dirección y se marcan todas sus zonas a la vez. Orden: F01 → F73 → F47 → F18 → F09 → F08 → F71 → F78 → resto.

## Barrido foto por foto (26/11)
Herramienta: verif_foto.py. Calibra la cámara SOLO con la torre (siluetas y forjados) y proyecta 622 puntos de referencia del modelo actual.
Cada punto visible es OK si cae a ≤ 0,6 m de una arista de la foto. Zona = OK si ≥ 80 %, ≈ si ≥ 50 %, NO si menos.
- Actualizado: perfil de la concha (P2/G3) y cubierta inclinada del restaurante en puntos_ref.py; canto del barril (0,59) en calib_e.py.
- **F01** (rms de la cámara 12 px): 230 OK / 80 NO. Torre, bar y testero OK. Columna y borde de la concha ≈ (pie tapado; poco contraste).
  NO: pie de la fachada exterior del ala larga en y 67–82 (1,5–3,4 m) → **duda 7**.
- **F73** (rms 27 px, más débil): 275 OK / 15 NO. Concha 20/20 OK, ala larga, ventanas y testero OK. Remate 0/5 (atribuible a la cámara).
  Esquina alta del bar vista sobre el testero (2 puntos) → **duda 8**.
- Nuevo en F01: dientes de sierra sobre una cubierta a la izquierda de la torre (1984) → **duda 9** (se habían quitado).
Matriz: 60 OK · 27 ≈ · 1 NO · 157 ?.

## Cambios pedidos tras el barrido (26/11)
- **Método:** las cámaras ajustadas se descartan como prueba (usuario). A partir de ahora la comprobación se hace con geometría descriptiva:
  proporciones sobre planos conocidos, abatimientos y giros.
- **Ala larga:** la fachada de ventanas queda 0,80 m por dentro del borde (canto de la terraza y peto vuelan 0,80). Ventanas y marcos se mueven con ella.
- **Vuelo del bar:** 1,20 m (F47), sin cambio.
- **Ala corta:** 10 lucernarios en diente de sierra (5 en línea y 5 escalonados) en lugar de las 3 claraboyas (F01, 1984).
- **Sección L4:** longitudinal por la terraza mirando al bar, con nueva hoja A3 «el bar: sección L4 y alzado 2».
- **Entorno 1984** (ENTORNO_1984.png/pdf): fuente en media luna al pie de la columna (F01, F14), plaza con autobuses, calle Mazepy, edificio colindante y parque (esquemático).
