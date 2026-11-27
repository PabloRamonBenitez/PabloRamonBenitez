"""STL LIMPIO para servicios de impresión y de moldes (puerta de entregables): sin aristas con más de 2 caras ni aristas abiertas.
Manifold deja VÉRTICES DUPLICADOS en cada contacto de arista o de punto entre sólidos que solo se tocan; un STL (solo geometría) los
funde y quedan aristas con 4 caras ('no manifold'). Aquí cada copia se retrae unas micras hacia dentro de su propio sólido (0,006 mm
a escala de maqueta, bajo la resolución de cualquier impresora) y las que acaben en el mismo punto se separan en direcciones distintas."""
import numpy as np
import trimesh


def separar_contactos(V, F, delta=0.006):
    V = np.asarray(V, float).copy(); F = np.asarray(F)
    R = np.round(V, 6); _, inv, cnt = np.unique(R, axis=0, return_inverse=True, return_counts=True)
    fn = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]]); fa = np.linalg.norm(fn, axis=1); fn = fn / np.maximum(fa[:, None], 1e-30)
    vn = np.zeros_like(V)
    for j in range(3): np.add.at(vn, F[:, j], fn * fa[:, None])
    vn = vn / np.maximum(np.linalg.norm(vn, axis=1)[:, None], 1e-30)
    V2 = V.copy(); mov = 0
    for pos in np.where(cnt > 1)[0]:
        for i in np.where(inv == pos)[0][1:]:
            V2[i] = V[i] - vn[i] * delta; mov += 1
    for it in range(4):                                   # copias que acaban en el mismo punto: cada una por su lado
        R = np.round(V2, 5); _, inv, cnt = np.unique(R, axis=0, return_inverse=True, return_counts=True)
        malos = np.where(cnt > 1)[0]
        if len(malos) == 0: break
        rng = np.random.default_rng(it)
        for pos in malos:
            for q, i in enumerate(np.where(inv == pos)[0][1:], 1):
                d = rng.normal(size=3); V2[i] += d / np.linalg.norm(d) * delta * (1 + q); mov += 1
    return V2, mov


def comprobar(path):
    """lo que verá el servicio de impresión: recarga el STL fundiendo vértices. → dict"""
    t = trimesh.load(path, process=True)
    u, inv = trimesh.grouping.unique_rows(t.edges_sorted); c = np.bincount(inv)
    return dict(caras=len(t.faces), no_manifold=int((c > 2).sum()), abiertas=int((c == 1).sum()), estanco=bool(t.is_watertight),
                coherente=bool(t.is_winding_consistent), cuerpos=int(t.body_count), volumen_cm3=float(t.volume / 1000), caja_mm=(t.bounds[1] - t.bounds[0]).tolist())
