"""Render z-buffer sencillo (ortografico) del STL para comparar con fotos."""
import sys, math, numpy as np, trimesh
from PIL import Image

def render(t, az, el, W=700, H=700, margen=0.06):
    v = t.vertices - t.bounds.mean(0)
    a, e = math.radians(az), math.radians(el)
    # camara: mira hacia el origen desde direccion (az, el); az=0 -> desde -Y (fachada principal)
    c = np.array([math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)])  # posicion camara
    d = -c
    right = np.cross(d, [0, 0, 1]); right /= np.linalg.norm(right)
    up = np.cross(right, d)
    cam = d
    p = np.c_[v @ right, v @ up, v @ d]
    s = (1 - 2 * margen) * min(W, H) / max(np.ptp(p[:, 0]), np.ptp(p[:, 1]))
    px = (p[:, 0] - p[:, 0].mean()) * s + W / 2
    py = H / 2 - (p[:, 1] - p[:, 1].mean()) * s
    pz = p[:, 2]
    zb = np.full((H, W), np.inf); img = np.ones((H, W)) * 1.0
    luz = c + np.array([-0.5, 0, 0.6]); luz /= np.linalg.norm(luz)
    sh = 0.35 + 0.65 * np.clip(t.face_normals @ luz, 0, 1)
    vis = t.face_normals @ c > 0  # caras hacia la camara
    for f, c in zip(t.faces[vis], sh[vis]):
        x, y, z = px[f], py[f], pz[f]
        x0, x1 = max(int(x.min()), 0), min(int(x.max()) + 1, W - 1)
        y0, y1 = max(int(y.min()), 0), min(int(y.max()) + 1, H - 1)
        if x1 < x0 or y1 < y0: continue
        X, Y = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        d = (y[1] - y[2]) * (x[0] - x[2]) + (x[2] - x[1]) * (y[0] - y[2])
        if abs(d) < 1e-9: continue
        l0 = ((y[1] - y[2]) * (X - x[2]) + (x[2] - x[1]) * (Y - y[2])) / d
        l1 = ((y[2] - y[0]) * (X - x[2]) + (x[0] - x[2]) * (Y - y[2])) / d
        l2 = 1 - l0 - l1
        m = (l0 >= -1e-6) & (l1 >= -1e-6) & (l2 >= -1e-6)
        Z = l0 * z[0] + l1 * z[1] + l2 * z[2]
        sub = zb[y0:y1 + 1, x0:x1 + 1]
        m &= Z < sub
        sub[m] = Z[m]
        img[y0:y1 + 1, x0:x1 + 1][m] = c
    # oscurecer huecos (oclusion aproximada por profundidad local) y dibujar aristas
    D = zb.copy(); fondo = ~np.isfinite(D); D[fondo] = np.nanmax(D[~fondo]) + 5
    def blur(a, r):
        k = np.ones(2 * r + 1) / (2 * r + 1)
        a = np.apply_along_axis(lambda v: np.convolve(np.pad(v, r, mode='edge'), k, 'valid'), 0, a)
        return np.apply_along_axis(lambda v: np.convolve(np.pad(v, r, mode='edge'), k, 'valid'), 1, a)
    escala_mm = s  # pixeles por mm de modelo
    ao = np.clip((D - blur(D, max(2, int(0.8 * s)))) / (0.8), 0, 1)
    img = img * (1 - 0.55 * ao)
    gx = np.abs(np.diff(D, axis=1, prepend=D[:, :1])); gy = np.abs(np.diff(D, axis=0, prepend=D[:1]))
    img[(np.maximum(gx, gy) > 0.35)] *= 0.45
    img[fondo] = 1.0
    return Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))

if __name__ == "__main__":
    t = trimesh.load(sys.argv[1])
    vistas = [(0, 3), (35, 25), (180, 20), (215, 35)]
    ims = [render(t, az, el) for az, el in vistas]
    out = Image.new("L", (1400, 1400), 255)
    for i, im in enumerate(ims):
        out.paste(im, ((i % 2) * 700, (i // 2) * 700))
    out.save(sys.argv[2])
