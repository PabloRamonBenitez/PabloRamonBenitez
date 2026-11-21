# Maqueta del Hotel Salut (Kyiv, 1984) – escala 1:300

Edificio **construido** (no el proyecto original de 18 plantas). Cotas reales estimadas (no hay planos publicados).

- `Hotel_Salut_maqueta_1-300.pdf` – planos, plantillas 1:1 e instrucciones para vaciar en yeso.
- `Hotel_Salut_1-300.stl` – modelo 3D en mm (196 × 74 × 103 mm), malla estanca.
- `geometria.py` – todas las cotas en un sitio; cambia `ESCALA` o las medidas y regenera:
  `python3 generar_pdf.py && python3 generar_stl.py` (requiere reportlab, numpy, manifold3d, trimesh).
