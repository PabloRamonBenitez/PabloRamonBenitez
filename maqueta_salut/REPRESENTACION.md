# Norma de representación de los planos

Fuentes: Francis D. K. Ching, *Manual de dibujo arquitectónico* (5.ª ed., pp. 51–93: plantas, secciones, alzados, situación y axonometrías);
G. D. Escobar López, *Normas de graficación para la representación arquitectónica* (UNE 1-032 / ISO 128); modelo de planta del usuario.

## Jerarquía de valores de línea (lo más importante)
| valor | qué | dónde se aplica |
|---|---|---|
| 1 – el más grueso, continuo | contorno de lo **cortado** (muros, pilares, forjados, terreno). Nunca se cruza con otra línea ni acaba contra una más fina | `lineas.corte` (lw 1,1) |
| 2 – intermedio | bordes de lo **visto** cerca del plano de corte | `dibujar_vista` / `vista_vectorial` |
| 3 – fino, cada vez más | lo visto más lejos (perspectiva aérea: más lejos, más fino y más claro) | `vista_vectorial` en plantas (lw según cota) |
| 4 – el más fino | líneas superficiales (juntas, despiece, textura), cotas (0,2 mm), mobiliario | cotas, tramas |
| trazo largo y punto | ejes, línea de corte de las secciones (con **flecha de sentido de vista** en cada extremo) | planta de situación de secciones |
| guiones largos | lo que está **por encima** del corte (vuelos, aleros, lucernarios) | `lineas.encima` |
| guiones cortos / puntos | lo **oculto por debajo** | – |

## Plantas
- Corte a ~1,0–1,2 m; corta muros, pilares y huecos. Antepechos de ventana **no** cortados: línea fina.
- Lo cortado se distingue del vacío: trama o tono gris medio (no grandes zonas negras).
- Puertas: hoja perpendicular al hueco + barrido a 90° en línea muy fina.
- Escaleras: huellas hasta el plano de corte, **línea diagonal de corte**, flecha de subida; pasamanos distintos de los muros.
- Planta de cubiertas: forma, volúmenes, lucernarios, terrazas; en la planta de situación.
- Norte en todas las plantas; misma orientación en toda la presentación.

## Secciones
- Corte continuo, paralelo a los muros principales, por huecos, cambios de nivel, escaleras y lucernarios; **no por pilares**.
- Cortado con trazo grueso y **rayado a 45°** (hormigón armado); visto detrás con valores más finos según la distancia.
- Se corta también el **terreno**: línea gruesa continua y trama de tierra bajo la rasante (+ edificios contiguos si existen).
- Cotas de nivel referidas a ±0,00. **Figura humana** para la escala.
- Escalera: tramo cortado como losa con peldaños; rellanos cortados; tramo visto en línea fina; paso libre ≥ 2,10.

## Alzados
- Línea de terreno cortada por delante (la más gruesa), prolongada fuera del edificio.
- Planos más próximos con línea más gruesa; los lejanos más finos (superposición, perspectiva aérea, indefinición).
- Materiales con su trama (hormigón, ladrillo, vidrio) en línea superficial fina; figuras humanas.
- Nombre por orientación o por lo que mira («alzado a la calle», «alzado a la plaza»).
- Vistas alineadas: las cotas se transfieren de planta a alzado y de alzado a alzado.

## Planta de situación
- Construida **sobre la planta de cubiertas del modelo** (geometría comprobada), nunca dibujada desde una sola foto.
- Edificio como figura sobre el fondo (o al revés si hay sombras); lindes en trazo largo y dos puntos; viales, accesos, árboles.
- Escala gráfica y norte.

## Datos
- Lo que no tiene foto no se dibuja (interiores, diseño de barandillas). El exterior siempre según fotos contrastadas.

## Sistema de cotas relacionadas (cotas_rel.py)
- **Ejes con nombre**, los mismos en todas las vistas: T y T' (torre, paralelo y perpendicular al chaflán), A y C (chaflán),
  1 (esquina), 2 (pie de la concha), 3 (fin del bar), 4 (testero), a y b (fachadas del ala larga) y M (medianera).
  En planta llevan burbuja; en secciones y alzados se proyectan como trazo y punto, con la misma burbuja bajo la rasante.
- **Cadena horizontal** bajo la rasante en cada sección y alzado: cotas parciales entre ejes y puntos de corte
  (columna, cuello, barril, tambor) más la total. Son las mismas distancias que en planta.
- **Cadena vertical de niveles** (parciales + total) en el margen, con todos los niveles del cuadro referidos a ±0,00.
  Coinciden con las cotas de nivel rotuladas.
- **Cotas radiales** de la torre en planta (columna, cuello, barril, tambor), que se leen en la sección como los puntos de corte.
- Las vistas van alineadas: en cada hoja A3 la sección y el alzado comparten eje horizontal, y los ejes 1, 2, 3, 4 y T caen en la misma vertical.
