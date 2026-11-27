# Hotel Salut (Kyiv, 1984) – documentación del levantamiento (26/11/2026)

Todo sale de una fuente única: el cuadro de cotas (`cotas.py`). De ahí se generan el 3D, las plantas, las secciones, los alzados y el STL.
Normas de representación: Ching, *Manual de dibujo arquitectónico*, y *Normas de graficación* (ver `REPRESENTACION.md`).

## Planos
Los juegos A3 y A4 y el plano de lugar van **en ucraniano** (`traduccion.py`). Las hojas de trabajo, las tablas y los informes siguen en español.

| Archivo | Contenido |
|---|---|
| `SALUT_planos_A3_presentacion.pdf` | **Juego de presentación A3**: portada e índice, **plano de lugar 1984**, plantas 1:400, secciones y alzados alineados (1:500), detalle del módulo. Todas las láminas llevan sus fotos de contraste. |
| `SALUT_planos_A4.pdf` | Juego para imprimir en A4: sección, planta y alzado alineados en cada hoja; plantas por niveles. |
| `PLANO_LUGAR_1984.pdf` | Plano de lugar a 1:750, con el entorno según las fotos de 1984: calle Ivana Mazepy, plaza de asfalto abierta a la calle, césped, vial de servicio que rodea el testero (F01, F47), parque y colindante. Lleva el recorrido del camión desde la calle. `ACCESO_VEHICULO.png` muestra las pruebas. |
| `SALUT_planos_definitivos.pdf` | Láminas de trabajo: plantas, secciones, alzados, detalles, comprobaciones y cuadro de cotas. |
| `SALUT_planos_2D.pdf` | Cuadro de cotas completo (valor, fuente y margen) y reglas de coherencia de los planos. |

## Modelo
| Archivo | Contenido |
|---|---|
| `Hotel_Salut_15cm_MOLDE.stl` | **Versión para el molde de silicona y la colada de hormigón**, a la misma escala. Grosores ≥ 0,6 m (1,8 mm), rendijas ≥ 0,35 m (1 mm), sin barandillas abiertas, lamas macizas, letras en relieve sobre el remate. Una sola pieza con base plana. Ver `MOLDE.md` y `MOLDE_COMPARACION.png`. |
| `Hotel_Salut_15cm_MOLDE_baja.stl` | El mismo STL de molde con la malla simplificada a 0,012 mm de maqueta (23 064 triángulos, 1,2 MB). Es el que se comparte con los proveedores (enlace de Drive). Estanco y sin aristas no manifold. |
| `PROVEEDORES_MOLDES.md` | Estado de las consultas a proveedores de molde de silicona (correo y Etsy), con lo que han contestado y los textos para Etsy. |
| `Hotel_Salut_15cm_v3.stl` | STL para el molde de silicona: 15 cm de alto, escala ≈ 1:339. Las gárgolas no van en el STL (medirían 0,3 mm). |
| `VISTA3D_1…4.png` | Vistas del 3D junto a la foto equivalente. |

## Comprobación
| Archivo | Contenido |
|---|---|
| `MATRIZ_ZONAS_FOTOS_v2.xlsx` / `MATRIZ_v2.png` | Tabla de 35 zonas × 28 fotos: **80 OK · 144 ≈ · 0 NO · 0 ?**. Incluye las hojas Evidencias, Conflictos, Columnas y Juntas. |
| `COHERENCIA_VISTAS.md` | 94 comprobaciones entre el 3D, el catálogo de huecos y los planos (triangulación A–B, A–C y A–D exactas): 94/94 OK. |
| `CALIDAD_GRAFICA.md` | Puerta 3b: rótulos que se pisan, caen sobre líneas o se salen del dibujo o de la hoja, en todas las láminas. |
| `ORDENES.md` | **Lista viva de órdenes y mandatos** del usuario, con fecha y control. Se repasa entera antes de cada entrega. |
| `METODO_COMPROBACION.md` / `AUDITORIA_PLANOS.md` / `AUDITORIA_NUDOS.png` | Las 5 puertas de comprobación. Auditoría automática de todas las plantas y secciones: **0 defectos** (astillas, rendijas, nudos, reglas del usuario y entregables antiguos). Hoja de los encuentros más complejos ampliados. |
| `RONDA_ABSOLUTA.md` | Informe de la ronda del 26/11: tus indicaciones una por una, las hipótesis H1–H4, las preguntas P3–P5 y la duda 7, con sus pruebas. |
| `DIBUJOS_EXPLICATIVOS/DIBUJOS_EXPLICATIVOS.pdf` | Láminas explicativas **del estado actual**, regeneradas desde el modelo: zonas, MGF, collages de Alamy, F09 y la base, escalera, matriz y plano de lugar. |
| `DIBUJOS_EXPLICATIVOS/HISTORICO/HISTORICO_DECISIONES.pdf` | Dudas, hipótesis y análisis tal como se plantearon. **Geometría superada**: no son planos. |
| `HISTORICO/` | Juegos de planos, PDF y STL de días anteriores (no usar). |

## Pendiente
- **Patio de la L**: no sale en ninguna foto. No se sabe si el vial de servicio sale por él o da allí la vuelta (en el plano de lugar va a trazos con «?»).
- 4 zonas sin ningún OK, porque no hay foto que las mida: PB del ala corta, línea posterior, fachada del patio y patio.
- En las secciones, lo visto tras el corte sigue siendo una imagen, no líneas.
- Por encima del tambor, Alamy no coincide con las demás fotos (≈ 10 %): se usan sus alturas, no sus anchos.
