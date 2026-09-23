"""Cómo le fue a un clasificador: las métricas y la matriz de confusión."""

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from . import estilo

# El orden en que se leen: primero la global, después las del positivo.
ORDEN = [("accuracy", "accuracy"), ("precision", "precision"),
         ("recall", "recall"), ("f1", "f1 score")]

# Rampa de un solo tono, del fondo al primario: oscuro = pocos casos, claro = muchos.
RAMPA = LinearSegmentedColormap.from_list("semillero", [estilo.FONDO, estilo.PRIMARIO])


def _barras(ax, resultados):
    """Las métricas de 0 a 1, con el valor escrito al lado de cada barra."""
    ax.set_title("Las métricas")
    valores = [float(resultados[clave]) for clave, _ in ORDEN]
    posiciones = list(range(len(ORDEN)))

    ax.barh(posiciones, valores, height=0.42, color=estilo.PRIMARIO, zorder=3)
    for y, valor in zip(posiciones, valores):
        ax.text(valor + 0.025, y, f"{valor:.3f}", color=estilo.CLARO,
                va="center", fontsize=10, zorder=4)

    ax.set_yticks(posiciones, [nombre for _, nombre in ORDEN])
    ax.invert_yaxis()
    ax.set_xlim(0, 1.18)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_xlabel("0 = pésimo,  1 = perfecto")
    ax.grid(axis="x")
    ax.grid(axis="y", visible=False)


def _matriz(ax, matriz, nombres):
    """La matriz de confusión: filas lo que pasó, columnas lo que dijo el modelo."""
    ax.set_title("Matriz de confusión")
    conteos = [[int(v) for v in fila] for fila in matriz]
    mayor = max(max(fila) for fila in conteos) or 1

    ax.imshow(conteos, cmap=RAMPA, vmin=0, vmax=mayor)

    significados = [["verdadero negativo", "falso positivo"],
                    ["falso negativo", "verdadero positivo"]]
    for f, fila in enumerate(conteos):
        for c, conteo in enumerate(fila):
            # Sobre una casilla clara el texto oscuro se lee mejor.
            tinta = estilo.FONDO if conteo > 0.6 * mayor else estilo.CLARO
            ax.text(c, f - 0.1, conteo, color=tinta, ha="center", va="center",
                    fontsize=18)
            ax.text(c, f + 0.22, significados[f][c], color=tinta, ha="center",
                    va="center", fontsize=8, alpha=0.75)

    ax.set_xticks([0, 1], [f"dijo: {nombre}" for nombre in nombres])
    ax.set_yticks([0, 1], nombres)
    ax.set_xlabel("lo que dijo el modelo")
    ax.set_ylabel("lo que pasó")
    ax.grid(visible=False)
    for lado in ax.spines.values():
        lado.set_visible(False)

    # Una ranura del color del fondo entre casilla y casilla.
    ax.set_xticks([0.5], minor=True)
    ax.set_yticks([0.5], minor=True)
    ax.grid(which="minor", color=estilo.FONDO, linewidth=2, alpha=1)
    ax.tick_params(which="minor", length=0)


def dibujar_resultados(resultados, titulo="Cómo le fue al modelo",
                       nombres=("murió", "sobrevivió")):
    """Lo que devuelve `evaluar_metricas`, de un vistazo: barras y matriz."""
    figura, (izquierda, derecha) = plt.subplots(
        1, 2, figsize=(12, 4.6), gridspec_kw={"width_ratios": [1.2, 1]})
    figura.suptitle(titulo, color=estilo.CLARO, fontsize=14)

    _barras(izquierda, resultados)
    _matriz(derecha, resultados["matriz"], nombres)

    figura.tight_layout()
    plt.show()


def dibujar_comparacion(modelos, titulo="Modelo contra modelo"):
    """Las mismas métricas de varios modelos, lado a lado.

    `modelos` es {nombre: resultados}, tal como los devuelve `evaluar_metricas`.
    """
    nombres = list(modelos)
    alto = 0.8 / len(nombres)
    figura, ax = plt.subplots(figsize=(9, 1.1 * len(ORDEN) + 1.4))
    figura.suptitle(titulo, color=estilo.CLARO, fontsize=14)

    for i, nombre in enumerate(nombres):
        resultados = modelos[nombre]
        valores = [float(resultados[clave]) for clave, _ in ORDEN]
        # De arriba hacia abajo dentro de cada grupo de barras.
        posiciones = [f + (i - (len(nombres) - 1) / 2) * alto for f in range(len(ORDEN))]
        ax.barh(posiciones, valores, height=alto * 0.86, color=estilo.color(i),
                zorder=3, label=nombre)
        for y, valor in zip(posiciones, valores):
            ax.text(valor + 0.02, y, f"{valor:.3f}", color=estilo.CLARO,
                    va="center", fontsize=9, zorder=4)

    ax.set_yticks(range(len(ORDEN)), [nombre for _, nombre in ORDEN])
    ax.invert_yaxis()
    ax.set_xlim(0, 1.18)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_xlabel("0 = pésimo,  1 = perfecto")
    ax.grid(axis="x")
    ax.grid(axis="y", visible=False)
    # Arriba y por fuera, para no taparle el valor a ninguna barra.
    ax.legend(loc="lower right", bbox_to_anchor=(1, 1.01),
              ncol=min(len(nombres), 2), framealpha=0)

    figura.tight_layout()
    plt.show()
