# Cadena de puntos: de lo seguro a lo nuevo, foto a foto

Regla: en cada eslabón la foto debe ver **a la vez** puntos ya seguros (para fijar la cámara) y puntos nuevos (para obtenerlos). Un punto nuevo pasa a «seguro» cuando dos fotos independientes lo dan con ≤ 2 m de diferencia.

## Puntos seguros hoy
| Punto | Qué es | Por qué es seguro |
|---|---|---|
| Torre (eje, alturas, radios) | barril, cuello, columna, tambor, visera, remate | encaja en F09, F01, F23 con 3-7 px |
| D | esquina final de la terraza (+7,3) | satélite + visible en F01/F23 |
| A, B, C | cubierta del bloque alto del ala corta (+11,5) | satélite (A-B 7,3 ⟂ vecino, A-C 16,66, D-C 95,17, A-D 106,69) |
| Cotas de la base | PB +3,2, planta primera +7,3 | F15 (autobús), F09, F14 |

## Eslabones
| # | Foto | Seguros que ve | Nuevos que da | Se comprueba con |
|---|---|---|---|---|
| 1 | F02 (1794 px, plaza, lado restaurante) | torre, C, bloque alto | F (esquina de la banda baja), arranque del chaflán en la calle | F14 (otra copia, distinta deformación) + F09 |
| 2 | F18 (1666 px, plaza, lado hotel) | torre, arranque del chaflán (del eslabón 1) | G (fin de la banda del hotel / arranque de la concha), columna en el chaflán | F09 |
| 3 | F08 (2000 px, desde detrás) | torre, C | escalera (posición y ancho), rincón interior de la L | F11-F13 |
| 4 | F47/F24 (terraza) | D, G | bar (inicio y fin), ventanas del ala | F23 |

Problema conocido: la torre es casi simétrica y no fija hacia dónde mira la cámara; por eso cada eslabón necesita al menos dos puntos seguros fuera de la torre (en F02: C y el bloque alto; en F18: el arranque del chaflán del eslabón 1).

## Eslabón 1 (F02) – resultado: FALLIDO
- Ajuste aparente bueno (7,8 px; deformación vertical 0,96), pero la torre sale a 145 m de D: solución degenerada.
- Causa: en F02 solo se ven dos puntos seguros fuera de la torre (B y C, en la misma arista). Con la torre simétrica, dos puntos en línea no fijan la orientación ni la distancia: hay infinitas cámaras que los explican.
- Para que el eslabón funcione hacen falta ≥ 3 puntos seguros no alineados en la misma foto. Ninguna de las fotos grandes ve a la vez A-B-C y D.

## Eslabón F73 (ala larga desde su extremo) – resultado: FALLIDO
- Con la torre + las dos esquinas del extremo (D, E a 17 m, peto ~+8,3) la cámara no converge: la torre se va al límite (171 m de D), error 17,7 px.
- Causa probable: no conozco con seguridad la cota del bloque final (en F73 y en la maqueta F76 parece más alto que la terraza) ni qué esquina es cuál; con eso mal, el cálculo no tiene solución física.
- Lectura cualitativa que sí vale: la escalera se ve pegada al barril del lado del ala; el ala tiene dos filas de ventanas pequeñas; al final hay un bloque con barandilla en cubierta; el peto del ala va recto hasta ese bloque.
