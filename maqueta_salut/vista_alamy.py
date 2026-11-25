"""Dirección de la vista de Alamy, fijada con referencias NO periódicas (la cuña de la escalera en el borde izquierdo de la silueta)
y afinada con las 19 aletas (dispersión 0,8°). ALFA = ángulo en planta de la dirección torre → cámara."""
import math
import numpy as np
import edificio as E

ALFA = E._v["VISTA_ALAMY"]
_e = lambda d: np.array([math.cos(math.radians(d)), math.sin(math.radians(d))])
DERECHA = _e(ALFA + 90)          # derecha de la foto en planta
HACIA_CAMARA = _e(ALFA)
MIRA = tuple(-HACIA_CAMARA)      # dirección en la que mira la cámara (para laminas.alzado)
T = np.array(E.T)
lat = lambda p: float((np.asarray(p) - T) @ DERECHA)          # m a la derecha del eje de la torre
delante = lambda p: float((np.asarray(p) - T) @ HACIA_CAMARA) > 0


def x_eje_alzado():
    """coordenada x del eje de la torre en laminas.alzado(ax, MIRA)"""
    a = math.radians(-(math.degrees(math.atan2(MIRA[1], MIRA[0])) - 90))
    return math.cos(a) * E.T[0] - math.sin(a) * E.T[1]
