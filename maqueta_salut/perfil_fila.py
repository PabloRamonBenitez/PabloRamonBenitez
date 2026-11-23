"""Ventanas de una fila medidas como mínimos de intensidad a lo largo de la recta de la fila (objetivo)."""
import sys, numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates, gaussian_filter1d
from scipy.signal import find_peaks
I='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'
def perfil(foto, x0, x1, y0, m, ancho=2):
    g = np.asarray(Image.open(I+foto).convert("L")).astype(float)
    xs = np.linspace(x0, x1, int((x1-x0)*4)); n = np.array([-m, 1])/np.hypot(m, 1)
    pr = np.mean([map_coordinates(g, [y0+m*(xs-x0)+k*n[1], xs+k*n[0]], order=1) for k in np.linspace(-ancho, ancho, 5)], axis=0)
    return xs, pr
def mejor_recta(foto, x0, x1, yr, mr):
    best=None
    for y0 in np.arange(*yr, 0.5):
        for m in np.arange(*mr, 0.01):
            xs, pr = perfil(foto, x0, x1, y0, m); v = np.std(gaussian_filter1d(pr, 2))
            if best is None or v > best[0]: best = (v, y0, m)
    return best
def minimos(foto, x0, x1, y0, m, dist=3):
    xs, pr = perfil(foto, x0, x1, y0, m); p = gaussian_filter1d(pr, 1.5)
    k, _ = find_peaks(-p, distance=dist*4, prominence=4)
    return xs[k], p
