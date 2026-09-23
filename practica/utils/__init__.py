"""Gráficas de apoyo para los cuadernos, con la paleta del semillero.

    estilo.py         los colores y el lienzo que comparten todas
    regresion.py      puntos y curvas (cuadernos 00 y 01)
    entrenamiento.py  la pérdida y las demás métricas, época a época
    clasificacion.py  nubes por clase y fronteras de decisión (cuaderno 02)
    metricas.py       cómo le fue al clasificador, ya entrenado (cuadernos 02 y 03)
    imagenes.py       las fotos y su veredicto (cuaderno 03)
    tablero.py        el triqui (cuaderno 04)

Desde los cuadernos basta con `import utils` y llamar, por ejemplo,
`utils.dibujar_datos(...)`.
"""

from .clasificacion import dibujar_clases, dibujar_entropia, dibujar_frontera
from .entrenamiento import dibujar_metricas, dibujar_perdida
from .imagenes import dibujar_muestra, dibujar_predicciones, dibujar_veredicto
from .metricas import dibujar_comparacion, dibujar_resultados
from .regresion import dibujar_ajuste, dibujar_datos
from .tablero import dibujar_tablero

__all__ = [
    "dibujar_ajuste",
    "dibujar_clases",
    "dibujar_comparacion",
    "dibujar_datos",
    "dibujar_entropia",
    "dibujar_frontera",
    "dibujar_metricas",
    "dibujar_muestra",
    "dibujar_perdida",
    "dibujar_predicciones",
    "dibujar_resultados",
    "dibujar_tablero",
    "dibujar_veredicto",
]
