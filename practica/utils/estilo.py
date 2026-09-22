"""Los colores y el lienzo que comparten todas las gráficas.

Importar este archivo deja el tema oscuro puesto para todo matplotlib, así que
las funciones de más abajo solo tienen que ocuparse de los datos.
"""

import matplotlib.pyplot as plt

FONDO = "#010409"
PRIMARIO = "#29c4d9"
SECUNDARIO = "#8dbccd"
CLARO = "#eaf6fc"
AMBAR = "#caa655"
MORADO = "#ac94f1"
VERDE = "#48d0a5"
ROJO = "#e06c75"

CICLO = [PRIMARIO, AMBAR, MORADO, VERDE, ROJO]

plt.rcParams.update({
    "font.family": "monospace",
    "font.monospace": ["JetBrains Mono", "DejaVu Sans Mono"],
    "figure.facecolor": FONDO,
    "axes.facecolor": FONDO,
    "axes.edgecolor": SECUNDARIO,
    "axes.labelcolor": SECUNDARIO,
    "axes.labelsize": 10,
    "axes.titlecolor": CLARO,
    "axes.titlesize": 13,
    "axes.titlepad": 14,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": SECUNDARIO,
    "grid.alpha": 0.15,
    "grid.linewidth": 0.8,
    "xtick.color": SECUNDARIO,
    "ytick.color": SECUNDARIO,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.facecolor": FONDO,
    "legend.edgecolor": SECUNDARIO,
    "legend.labelcolor": CLARO,
    "legend.framealpha": 0.9,
    "legend.fontsize": 9,
})


def color(i):
    """El color número `i` de la paleta, dando la vuelta si se acaban."""
    return CICLO[i % len(CICLO)]


def lienzo(titulo="", x_etiqueta="", y_etiqueta="", tam=(9, 5)):
    """Un eje vacío, ya con el título y los nombres puestos."""
    _, ax = plt.subplots(figsize=tam)
    ax.set_title(titulo)
    ax.set_xlabel(x_etiqueta)
    ax.set_ylabel(y_etiqueta)
    return ax
