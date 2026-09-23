"""El triqui visto de frente: la gráfica del cuaderno 04."""

import matplotlib.pyplot as plt

from . import estilo


def _lienzo_tablero(titulo):
    """Un cuadrado de 3x3 con las rayas del triqui y sin ejes."""
    ax = estilo.lienzo(titulo, tam=(5.4, 5.4))
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    ax.set_aspect("equal")
    ax.axis("off")
    for i in (1, 2):
        ax.plot([i, i], [0, 3], color=estilo.SECUNDARIO, linewidth=1.5, alpha=0.6, zorder=2)
        ax.plot([0, 3], [i, i], color=estilo.SECUNDARIO, linewidth=1.5, alpha=0.6, zorder=2)
    return ax


def _centro(casilla):
    """El centro de una casilla, numeradas de 0 a 8 desde arriba a la izquierda."""
    fila, columna = divmod(casilla, 3)
    return columna + 0.5, 2.5 - fila


def _pintar_marca(ax, casilla, valor):
    """La X o la O de una casilla ya jugada."""
    marca, color = ("X", estilo.PRIMARIO) if valor == 1 else ("O", estilo.AMBAR)
    x, y = _centro(casilla)
    ax.text(x, y, marca, ha="center", va="center", color=color, fontsize=34, zorder=3)


def _pintar_preferencia(ax, casilla, peso):
    """Tiñe una casilla libre según cuánto la prefiere la red, y escribe el porcentaje."""
    x, y = _centro(casilla)
    ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, color=estilo.PRIMARIO,
                               alpha=0.7 * peso, zorder=1))
    ax.text(x, y - 0.32, f"{peso:.0%}", ha="center", va="center",
            color=estilo.SECUNDARIO, fontsize=9, zorder=3)


def dibujar_tablero(tablero, probabilidades=None, titulo="El tablero"):
    """El triqui visto de frente.

    `tablero` son 9 casillas (1, -1 o 0) y `probabilidades` la preferencia de
    la red por cada una.
    """
    ax = _lienzo_tablero(titulo)
    for casilla in range(9):
        if tablero[casilla] != 0:
            _pintar_marca(ax, casilla, tablero[casilla])
        elif probabilidades is not None:
            _pintar_preferencia(ax, casilla, float(probabilidades[casilla]))
    plt.show()
