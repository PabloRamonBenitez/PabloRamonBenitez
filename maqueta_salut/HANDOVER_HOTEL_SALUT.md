# TRASPASO del proyecto Hotel Salut (28/11/2026)

Este documento es para el proyecto nuevo «Hotel Salut Proyecto Continuo». Lo que aquí está escrito es lo que hay ahora mismo. Lo que no esté aquí no se ha hecho.

## 1. Prompt de arranque (pégalo como primer mensaje del proyecto nuevo)

> Eres el responsable del proyecto Hotel Salut (Kyiv, 1984): maqueta a escala 1:339 hecha a partir de fotos antiguas. Tu primera tarea es leer este documento entero y después los archivos de la sección 2, en este orden: ESTADO_MOLDES_Y_PROVEEDORES.md, ORDENES.md, DESMONTABLE_DIVISION.png y MATERIALES_Y_AJUSTES.md.
>
> Reglas del usuario (Pablo): las órdenes de ORDENES.md mandan y se repasan antes de cada entrega. Nada inventado sin datos: lo supuesto va marcado. Cada cambio se compara con todas las fotos. Las preguntas al usuario van con un gráfico. Pablo no quiere que se le pidan cosas que ya tiene resueltas: antes de preguntar, mira este documento.
>
> Al empezar: confirma con Pablo los dos pendientes de la sección 6 y pregúntale si ya se ha contestado algún hilo de Etsy. No envíes nada a proveedores sin su visto bueno del texto concreto.

## 2. Dónde está cada cosa

| Qué | Dónde | Cómo se llega |
|---|---|---|
| Código, planos, cuadro de cotas, órdenes | GitHub: PabloRamonBenitez/PabloRamonBenitez, rama `ccr-3578fcb9-cjje54`, carpeta `maqueta_salut` | Conector de GitHub (repo privado) |
| Documento de estado de moldes y proveedores | Drive: ESTADO_MOLDES_Y_PROVEEDORES.md (carpeta «Stl salyt») | https://drive.google.com/file/d/1HcjV2uHXErb_KYIpb0LfW3e4zVlhfsbO/view?usp=drivesdk |
| Gráfico de estado | Drive: ESTADO_MOLDES_GRAFICO.png | https://drive.google.com/file/d/1OFaeiSWdMzuRybp4OXJkQPyuLrnhIrL0/view?usp=drivesdk |
| STL pieza A, torre (142 × 190 × 150 mm, 762 cm³) | Drive: Hotel_Salut_MOLDE_A_torre_baja.stl | https://drive.google.com/file/d/1topn7aZmwcl3bnqjx9znnLregA_Co2gm/view?usp=drivesdk |
| STL pieza B, ala (38 × 109 × 34 mm, 100 cm³) | Drive: Hotel_Salut_MOLDE_B_ala_baja.stl | https://drive.google.com/file/d/1W04Q6l6ScJM0CdcjoB-EfuZ8-caqUL3P/view?usp=drivesdk |
| STL modelo entero, menos detalle | Drive: Hotel_Salut_15cm_MOLDE_baja.stl | Carpeta «Stl salyt» |
| Copia de la pieza A en el Mac | Descargas: Hotel_Salut_MOLDE_A_torre_baja.stl | Sesión local en el Mac |
| Borrador de textos de Etsy | Gmail: «Textos para copiar y pegar en Etsy» | Conector de Gmail |
| Carpeta del proyecto en el Mac | No existe: el proyecto vive en GitHub y en Drive | — |

## 3. Comunicaciones: quién ha recibido qué

**Correo (Gmail)**
| Proveedor | Enviado | Respuesta | Estado |
|---|---|---|---|
| MinghuiLink (China, Aaron Lin) | 25/11: petición. 27/11: seguimiento con STL. 28/11: propuesta de dos moldes. 28/11: propuesta de dos piezas (tambor y base). | 25/11: dos puntos estructurales (molde de varias partes, detalles de 1 mm frágiles). Sin precio. | **Esperando precio y plazo** |
| BK Silicone (Sam Zhong) | 25/11 y 27/11 | 27/11: rechaza, demasiado complejo | Cerrado |
| Flossy Candle (Polonia) | 25/11 y 27/11 | Sin respuesta | Esperar; si no contesta, dar por perdido |
| moldesilicona.com | 25/11 y 27/11 | Sin respuesta | Esperar |
| Modelarte (España) | 25/11 y 27/11 | Sin respuesta | Esperar |
| Milab3D (España) | 25/11 y 27/11 | Sin respuesta | Esperar |

**Etsy (Pablo tiene sesión iniciada; los mensajes los envía él o la sesión local con su aprobación)**
| Tienda | Qué pidió | Qué toca |
|---|---|---|
| MoldeSilicona (Alfredo y Karina) | Revisaron el STL, «comentamos» | Texto 1 (pendiente de envío) |
| HOUSEOFMOLDS (Tania) | Pidió el archivo | Texto 2 (pendiente) |
| 3DDeluxeStore (Scott Presbrey) | Pidió imagen o modelo | Texto 3 (pendiente) |
| PLAybelope (Razieh Hamidi) | Pidió el STL en Drive | Texto 2 en inglés (pendiente) |
| StudioRollins | Pide una imagen de la pieza. No consta en nuestra lista | Texto 4 (pendiente). **Promete imágenes**: hay que mandarlas (renders del modelo) |

**Web (sin contacto todavía)**
- Hubs / Protolabs: pieza A subida o pendiente de subir desde la sesión local. Sin precio.
- JLC3DP, Craftcloud, 3DEXPERIENCE Make, Xometry Europe: sin presupuesto.
- Innovatia3D, Additium3D, Dynamical 3D, Aitiip, Pantur: sin correo verificado (hay que sacarlo de su web).
- FormX (silicona, España): sin precio.

## 4. Conexiones que necesita el proyecto nuevo
1. **Gmail:** para escribir a proveedores por correo.
2. **Drive:** para leer y guardar los archivos y el documento de estado.
3. **GitHub:** para leer el código y los planos del repositorio.
4. **Sesión local en el Mac con Claude in Chrome:** solo para lo que exige el navegador (subir archivos a Hubs, escribir en Etsy). Hay que abrirla desde la app de escritorio, en «Esta computadora», con la carpeta Workspace y con Chrome conectado. Sin esa sesión, Etsy y Hubs no se pueden hacer.

## 5. Lo que ya está decidido
- Maqueta en cuatro modelos: original y menos detalle, cada uno en versión de una pieza y en versión desmontable (tambor y base).
- Encaje: cilindro Ø 9,0 m × 3,0 m, holgura 0,1 mm por lado en resina, llave con surco de entrada y canal.
- Orden de trabajo: primero imprimir los másters en resina, después el molde de silicona.
- Si se hace el molde en silicona, lo hace Pablo o lo encarga un proveedor (se decidirá con los presupuestos).

## 6. Pendientes, en orden
1. **Confirmar la división** de la maqueta (corte a z = 13,71 m, llave, surco y canal). Ver DESMONTABLE_DIVISION.png. Sin esto no se generan los modelos desmontables.
2. **Presupuesto de impresión de la pieza A** en Hubs: lo hace la sesión local. Después la pieza B.
3. **Contestar en Etsy** a los cinco hilos (sección 3). Los textos están en el documento de estado.
4. **Mandar las imágenes** prometidas a StudioRollins.
5. **Generar los modelos desmontables** (tambor y base) cuando se confirme la división. Sus STL se comparten en Drive con versión de baja resolución.
6. **Buscar correos verificados** de los proveedores españoles y de Shapeways, Sculpteo y Materialise (en sus webs).
7. **Elegir proveedor** cuando haya precios para comparar. Esperar a los hilos antes de presupuestar más.

## 7. Cosas que conviene no olvidar
- El molde de silicona se lee con el modelo impreso; un máster de resina necesita curado total antes de verter (ver MATERIALES_Y_AJUSTES.md).
- La holgura de 0,1 mm por lado se va a probar con una pieza de prueba antes de fijarla.
- El cuello del edificio tiene Ø 18 m y el cilindro del encaje Ø 9 m: deja 4,5 m de pared a cada lado.
- Las medidas de los dos moldes son las de la caja, no un cálculo de volumen de silicona.
