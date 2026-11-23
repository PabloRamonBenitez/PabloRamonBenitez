# Pasada 9 – Alzado 2 punto por punto (y por qué fallaba el método)

## El error de método
1. Comprobaba **cotas sueltas** (2-3 alturas por foto) y daba la zona por buena si esas cifras caían en rango.
   No recorría el contorno completo ni contaba los elementos repetidos.
2. Si una foto "no contradecía" una hipótesis, la marcaba como confirmada (la rampa elíptica: F73 solo decía
   "cae al final"; nunca miré si era una rampa transitable ni si había un arco debajo).
3. Las fotos de comprobación las elegía para cada lámina una vez y no volvía a cruzarlas cuando aparecían fotos nuevas
   (F71, F73, F76 llegaron después y la lámina seguía con F47/F24, que son la misma foto).
4. Las piezas que no tenían una cota numérica en el cuadro (nº de ventanas, puerta, entrante de la escalera,
   largo del bar en 1984) no entraban en la verificación: lo que no tiene cota no se comprobaba.

Corrección del método: por cada alzado, **lista de puntos/elementos visibles × todas las fotos** donde salen; cada
elemento repetido se cuenta; cada pieza del alzado tiene su cota en el cuadro; y una sonda (`coherencia_vistas.py`)
comprueba en la geometría que plantas/secciones/alzados dan lo mismo que el cuadro (incluido el recuento de huecos).

## Matriz del Alzado 2 (elemento × foto)
| elemento | F73 (actual, testero) | F71 (actual, frontal) | F47 / F24 (1984, es la misma) | F01 (1984) | F76 maqueta | plano |
|---|---|---|---|---|---|---|
| nº ventanas fila alta | **11** | se ven sobre la rampa | **11** | **11** | ojos de buey (proyecto) | 11 ✔ |
| nº huecos fila baja | 3 visibles + resto tras árboles | – | 7 visibles (resto tapado por la concha) | ~11 | – | 10 + puerta ✔ |
| solo en tramo final (tras la rampa) | sí, acaban en el arco | sí | sí | sí | – | ✔ |
| macizo hasta el testero | ~2 interejes (perspectiva cercana) | – | 1,3 | 1,5 | – | 4,5 m ✔ |
| marco profundo fila alta | sí | – | sombra | – | – | ✔ (0,3 m) |
| puerta al pie de fachada | tapada por verja | – | **sí** (rectángulo claro) | **sí** | – | hueco 7 ✔ |
| rampa: meseta arriba + pendiente | ve el final | arriba casi horizontal, luego baja | – | – | banda recta inclinada | ✔ |
| arco bajo la rampa | **curva a la izquierda** | **curva + vacío en sombra** | concha clara, vacío oscuro debajo | concha | **arco** bajo el tramo alto | ✔ (forma estimada) |
| bar (1984) | (actual: ampliado hasta el testero) | – | acaba sobre la 1ª ventana | acaba sobre la 1ª ventana | barra sobre pilares | acaba en Y=59,7 ✔ |
| vuelo cubierta bar | – | – | sí | sí (sombra) | sí | 1,2 m frente y extremo ✔ (sin "tacón") |
| peto terraza +8,5 | sí | sí | sí | sí | – | ✔ |
| testero +7,2 + barandilla, puerta con marquesina | **sí** | – | – | – | – | ✔ |
| caja escalera alargada con entrante | lado corto ~7 m | – | – | – | – | 7 × (8 fuera del barril), entrante 2 m ✔ |

## Lo que sigue siendo estimado (no medido)
- forma exacta del arco (arranque +3,2 y llegada al suelo al 72 % de la rampa): rango ± 0,1 en U_ARC;
- fin del bar en 1984: ± 5 m;
- dimensiones de la escalera: ancho 7 ± 1, salida 7,5 ± 1,5.

Coherencia geometría ↔ cuadro: 17/17 OK. planos2d: 16/16 OK. 3D/STL NO regenerado.
