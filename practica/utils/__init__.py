"""Lo que acompaña a los cuadernos.

    configuracion.py  las constantes, las semillas y el estilo de las gráficas
    graficas.py       todas las gráficas (cuadernos 00 a 03)
    tictactoe.py      las reglas del juego y el tablero para jugarle a la red (cuaderno 04)

Desde los cuadernos basta con `import utils` y llamar, por ejemplo,
`utils.plot_data(...)`.
"""

from .configuracion import CLASS_NAMES, DEVICE, EPOCHS, WEIGHTS, set_seeds
from .graficas import (plot_comparison, plot_data, plot_fit, plot_loss, plot_metrics,
                       plot_predictions, plot_results, plot_sample)
from .tictactoe import EMPTY, free_cells, play_against, step, symmetries

__all__ = [
    "CLASS_NAMES",
    "DEVICE",
    "EMPTY",
    "EPOCHS",
    "WEIGHTS",
    "free_cells",
    "play_against",
    "plot_comparison",
    "plot_data",
    "plot_fit",
    "plot_loss",
    "plot_metrics",
    "plot_predictions",
    "plot_results",
    "plot_sample",
    "set_seeds",
    "step",
    "symmetries",
]
