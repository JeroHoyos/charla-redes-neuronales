"""Nubes por clase y fronteras de decisión: las gráficas del cuaderno 02."""

import matplotlib.pyplot as plt
import torch

from . import estilo

X_ETIQUETA = "característica 1"
Y_ETIQUETA = "característica 2"


def _nube_por_clase(ax, datos, clases, nombres):
    """Los puntos reales, cada clase de un color."""
    for i, nombre in enumerate(nombres):
        dentro = clases == i
        ax.scatter(datos[dentro, 0], datos[dentro, 1], s=26, color=estilo.color(i),
                   edgecolor=estilo.FONDO, linewidth=0.5, zorder=3, label=nombre)


def _cuadricula(datos, puntos, margen=0.4):
    """Una rejilla que cubre el plano de los datos. Devuelve (malla_x, malla_y, entrada)."""
    ejes = []
    for columna in (0, 1):
        valores = datos[:, columna]
        ejes.append(torch.linspace(float(valores.min()) - margen,
                                   float(valores.max()) + margen, puntos))
    malla_x, malla_y = torch.meshgrid(*ejes, indexing="xy")
    entrada = torch.stack([malla_x.reshape(-1), malla_y.reshape(-1)], dim=1)
    return malla_x, malla_y, entrada


def dibujar_clases(x, etiquetas, nombres, titulo="Los datos",
                   x_etiqueta=X_ETIQUETA, y_etiqueta=Y_ETIQUETA):
    """Una nube de puntos coloreada por clase. `x` es (n, 2) y `etiquetas` es (n,)."""
    ax = estilo.lienzo(titulo, x_etiqueta, y_etiqueta, tam=(7, 6))
    _nube_por_clase(ax, x.detach(), etiquetas.detach().reshape(-1), nombres)
    ax.legend()
    plt.show()


@torch.no_grad()
def dibujar_frontera(predecir, x, etiquetas, nombres, titulo="La frontera de decisión",
                     x_etiqueta=X_ETIQUETA, y_etiqueta=Y_ETIQUETA, puntos=300):
    """El fondo pintado con la clase que elige el modelo, y encima los datos reales."""
    datos = x.detach()
    malla_x, malla_y, entrada = _cuadricula(datos, puntos)
    elegida = predecir(entrada).argmax(dim=1).reshape(malla_x.shape)

    ax = estilo.lienzo(titulo, x_etiqueta, y_etiqueta, tam=(7, 6))
    ax.contourf(malla_x, malla_y, elegida, levels=[i - 0.5 for i in range(len(nombres) + 1)],
                colors=[estilo.color(i) for i in range(len(nombres))], alpha=0.22, zorder=1)
    _nube_por_clase(ax, datos, etiquetas.detach().reshape(-1), nombres)
    ax.legend()
    plt.show()


def dibujar_entropia(titulo="Lo que cuesta equivocarse con confianza"):
    """La curva -log(p): la pérdida según la probabilidad que le dio a la clase correcta."""
    p = torch.linspace(0.01, 1.0, 300)
    ax = estilo.lienzo(titulo, "probabilidad que le dio a la clase correcta", "pérdida  -log(p)")
    ax.plot(p, -torch.log(p), color=estilo.PRIMARIO, linewidth=2.5)
    plt.show()
