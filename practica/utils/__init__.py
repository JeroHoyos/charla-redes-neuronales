"""Gráficas de apoyo para los cuadernos, con la paleta del semillero.

    estilo.py         los colores y el lienzo que comparten todas
    regresion.py      puntos y curvas (cuadernos 00 y 01)
    entrenamiento.py  la pérdida y las demás métricas, época a época
    clasificacion.py  nubes por clase y fronteras de decisión (cuaderno 02)
    tablero.py        el triqui (cuaderno 03)

Desde los cuadernos basta con `import utils` y llamar, por ejemplo,
`utils.dibujar_datos(...)`.
"""

from .clasificacion import dibujar_clases, dibujar_entropia, dibujar_frontera
from .entrenamiento import dibujar_metricas, dibujar_perdida
from .regresion import dibujar_ajuste, dibujar_datos
from .tablero import dibujar_tablero

__all__ = [
    "dibujar_ajuste",
    "dibujar_clases",
    "dibujar_datos",
    "dibujar_entropia",
    "dibujar_frontera",
    "dibujar_metricas",
    "dibujar_perdida",
    "dibujar_tablero",
]
