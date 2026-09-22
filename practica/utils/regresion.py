"""Puntos y curvas: las gráficas de los cuadernos 00 y 01."""

import matplotlib.pyplot as plt
import torch

from . import estilo

X_ETIQUETA = "minutos sin responder"
Y_ETIQUETA = "mensajes enviados"


def _puntos(ax, x, y, color=estilo.PRIMARIO):
    """La nube con los datos reales."""
    ax.scatter(x.detach().reshape(-1), y.detach().reshape(-1), s=45, color=color,
               edgecolor=estilo.FONDO, linewidth=0.8, zorder=3, label="datos reales")


@torch.no_grad()
def _curva(predecir, x, puntos=300):
    """Lo que predice el modelo a lo largo del rango de `x`. Devuelve (eje_x, eje_y).

    `predecir` puede ser un modelo de torch o cualquier función que reciba un
    tensor de (n, 1) y devuelva otro igual.
    """
    plano = x.detach().reshape(-1)
    malla = torch.linspace(float(plano.min()), float(plano.max()), puntos).reshape(-1, 1)
    return malla.reshape(-1), predecir(malla).reshape(-1)


def dibujar_datos(x, y, titulo="Los datos", x_etiqueta=X_ETIQUETA, y_etiqueta=Y_ETIQUETA):
    """Nada más los puntos."""
    ax = estilo.lienzo(titulo, x_etiqueta, y_etiqueta)
    _puntos(ax, x, y)
    ax.legend()
    plt.show()


def dibujar_ajuste(x, y, predecir, etiqueta="lo que aprendió el modelo",
                   titulo="Los datos y el modelo", x_etiqueta=X_ETIQUETA,
                   y_etiqueta=Y_ETIQUETA):
    """Los puntos y encima la curva del modelo. `predecir` recibe (n, 1) y devuelve (n, 1)."""
    ax = estilo.lienzo(titulo, x_etiqueta, y_etiqueta)
    _puntos(ax, x, y, estilo.SECUNDARIO)
    eje_x, eje_y = _curva(predecir, x)
    ax.plot(eje_x, eje_y, color=estilo.PRIMARIO, linewidth=2.5, zorder=2, label=etiqueta)
    ax.legend()
    plt.show()
