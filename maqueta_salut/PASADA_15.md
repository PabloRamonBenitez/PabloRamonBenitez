# Pasada 15 – planimetría con muros, huecos y estructura enlazados

- **Catálogo único de huecos** (`ventanas.py`, 157 huecos): ala larga 11 + 7, testero (puerta + ventana), banda del
  hotel, bandas del chaflán (restaurante, hotel), banda del ala corta, torre 19 × 6 plantas, 19 ojos del tambor.
  El 3D abre sus huecos desde esta lista; plantas y secciones dibujan desde la misma lista → coinciden por construcción.
  Comprobado: los 132 huecos de ala + torre están abiertos en el 3D en el punto que dice el catálogo.
- **Plantas**: muros de carga y fachada a 0,30 con trama, huecos abiertos con su símbolo (caras del muro + doble
  línea de carpintería/vidrio), puertas con hoja y arco, lo que queda por encima con dos líneas discontinuas,
  cotas de huecos del ala (macizo, hueco, intereje, nº).
- **Estructura de la torre**: núcleo (muro 0,30 en R_COL) en todas las plantas desde el cuello; en plantas de
  habitaciones, pasillo anular de 2,2 m y 19 particiones radiales de 0,20 en la dirección de cada aleta (los huecos
  quedan entre aletas, uno por habitación).
- **Secciones**: muros 0,30, forjados de 0,30 (techo de PB y cada planta del barril), núcleo de la torre donde la
  sección lo corta y huecos cortados en su sitio; S4 pasa ahora por el eje del hueco 2 (corta el alto y el bajo).
- **Alzados**: salen del mismo 3D → mismos huecos.

Supuesto (no visto en fotos): distribución interior de la torre (núcleo + pasillo + habitaciones radiales) deducida
de la geometría: una habitación por módulo entre aletas.
Pendiente de la pasada 14: cara curva de la concha, coronación del ala corta (F72), banda del hotel (F01), remate.
