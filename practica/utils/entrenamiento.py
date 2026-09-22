"""La pérdida y las demás métricas, época a época."""

import matplotlib.pyplot as plt

from . import estilo


def dibujar_perdida(historial, titulo="La pérdida época a época", escala_log=False):
    """La curva de entrenamiento."""
    ax = estilo.lienzo(titulo, "época", "pérdida (MSE)")
    ax.plot(range(1, len(historial) + 1), historial, color=estilo.PRIMARIO, linewidth=2)
    if escala_log:
        ax.set_yscale("log")
    plt.show()


def dibujar_metricas(series, titulo="Entrenamiento", y_etiqueta="pérdida", escala_log=False):
    """Varias curvas época a época. `series` es {etiqueta: lista de valores}."""
    ax = estilo.lienzo(titulo, "época", y_etiqueta)
    for i, (etiqueta, valores) in enumerate(series.items()):
        ax.plot(range(1, len(valores) + 1), valores, color=estilo.color(i),
                linewidth=2, label=etiqueta)
    if escala_log:
        ax.set_yscale("log")
    ax.legend()
    plt.show()
