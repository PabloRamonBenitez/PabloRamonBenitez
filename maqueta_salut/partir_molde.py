"""PARTIR EL MOLDE EN DOS PIEZAS (idea del usuario 27/11): el STL de molde se corta por un plano perpendicular al ala larga, en el pie de la
concha (Y_CUNA), donde acaba lo complicado:
  PIEZA A – torre, columna, chaflán, ala corta, bar y concha  (la parte con vuelos y huecos: molde de varias partes)
  PIEZA B – tramo final del ala larga, sin bar (un prisma bajo y sencillo: molde de una pieza abierto por arriba)
Ventajas para presupuestar: dos bloques de silicona mucho más pequeños que uno de 142 × 299 × 150 mm; el tramo B no necesita carcasa partida.
Salida: Hotel_Salut_MOLDE_A_torre.stl, Hotel_Salut_MOLDE_B_ala.stl (y sus versiones _baja) + PARTIR_MOLDE.md; cada una estanca y sin aristas no manifold."""
import os
os.environ["SALUT_MOLDE"] = "1"
import numpy as np, trimesh
import edificio as E, stl_limpio as SL

m = E.edificio(); k = 150.0 / E.Z_R1
yc = float(E.Y_CUNA) + 0.35                          # 0,35 m más allá del muro final de la concha (cortar justo en su plano deja una lámina de espesor 0)
arriba, abajo = m.split_by_plane((0, 1, 0), yc)            # arriba: y > yc (pieza B) · abajo: y < yc (pieza A)
partes = {"A_torre": abajo, "B_ala": arriba}
filas = []
for nombre, p in partes.items():
    me = p.to_mesh(); V = np.asarray(me.vert_properties)[:, :3] * k; F = np.asarray(me.tri_verts)
    V2, _ = SL.separar_contactos(V, F)
    f = f"Hotel_Salut_MOLDE_{nombre}.stl"; trimesh.Trimesh(V2, F, process=False).export(f)
    c = SL.comprobar(f)
    q = p.set_tolerance(0.004); mq = q.to_mesh()
    Vq, _ = SL.separar_contactos(np.asarray(mq.vert_properties)[:, :3] * k, np.asarray(mq.tri_verts))
    fb = f.replace(".stl", "_baja.stl"); trimesh.Trimesh(Vq, np.asarray(mq.tri_verts), process=False).export(fb)
    cb = SL.comprobar(fb)
    assert cb["no_manifold"] == 0 and cb["abiertas"] == 0 and cb["estanco"], (nombre, cb)
    filas.append((nombre, c, cb, os.path.getsize(fb) / 1e6))
    print(nombre, "completa:", {x: c[x] for x in ("caras", "no_manifold", "abiertas", "estanco", "cuerpos")}, "· caja mm", [round(x) for x in c["caja_mm"]],
          "· vol %.0f cm³" % c["volumen_cm3"], "| baja:", cb["caras"], "caras, %.2f MB" % (os.path.getsize(fb) / 1e6), flush=True)

tot = sum(c["volumen_cm3"] for _, c, _, _ in filas)
caja_unica = np.array([142.0, 299.0, 150.0])
vol_bloque = lambda cj, marg=10.0: float(np.prod(np.array(cj) + 2 * marg)) / 1000.0        # cm³ del bloque de silicona con 10 mm de margen por lado (solo orden de magnitud)
v1 = vol_bloque(caja_unica); v2 = sum(vol_bloque(c["caja_mm"]) for _, c, _, _ in filas)
L = ["# Molde en dos piezas", "",
     f"Corte por el plano y = {yc:.1f} m (pie de la concha, ya a 1:{round(1000 / k)}: y = {yc * k:.0f} mm del origen). Volumen de las dos piezas: {tot:.0f} cm³ (el modelo entero tiene 862 cm³; la diferencia es solo la cara de corte).", "",
     "| pieza | caja (mm) | volumen (cm³) | estanca | aristas no manifold | archivo de baja resolución |", "|---|---|---|---|---|---|"]
for n, c, cb, mb in filas:
    L.append(f"| {n} | {c['caja_mm'][0]:.0f} × {c['caja_mm'][1]:.0f} × {c['caja_mm'][2]:.0f} | {c['volumen_cm3']:.0f} | {'sí' if c['estanco'] else 'NO'} | {c['no_manifold']} | `Hotel_Salut_MOLDE_{n}_baja.stl` ({mb:.1f} MB) |")
L += ["", f"Orden de magnitud del bloque de silicona (caja + 10 mm por lado, sin tener en cuenta la carcasa): un molde único ≈ {v1 / 1000:.1f} L; dos moldes ≈ {v2 / 1000:.1f} L ({100 * (1 - v2 / v1):.0f} % menos). Es una estimación de la caja, no un presupuesto.", "",
      "La pieza B es un prisma bajo y sin vuelos: se puede moldear de una sola pieza abierta por arriba. La pieza A es la complicada (torre con vuelos) y necesita molde de varias partes con carcasa rígida.",
      "Las dos piezas se unen después de colar con una junta plana pegada. Si hace falta, se les añade una llave de alineación."]
open("PARTIR_MOLDE.md", "w").write("\n".join(L) + "\n")
print("\n".join(L[-6:-3]))
