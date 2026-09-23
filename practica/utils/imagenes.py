"""Las fotos del cuaderno 03: en cuadrícula y con el veredicto encima."""

import matplotlib.pyplot as plt
import torch

from . import estilo

# Con estas cuentas se normalizaron las fotos que entran a la red (las de ImageNet).
MEDIA = (0.485, 0.456, 0.406)
DESV = (0.229, 0.224, 0.225)

NOMBRES = ("no hot dog", "hot dog")


def _a_imagen(tensor, media=MEDIA, desv=DESV):
    """Deshace la normalización: de tensor (C, alto, ancho) a algo que se pueda mirar."""
    if not torch.is_tensor(tensor):
        return tensor                       # ya viene como foto (PIL o arreglo)
    media = torch.as_tensor(media).view(-1, 1, 1)
    desv = torch.as_tensor(desv).view(-1, 1, 1)
    return (tensor.detach().cpu() * desv + media).clamp(0, 1).permute(1, 2, 0).numpy()


def _marco(ax, color=None):
    """Sin ejes, y con un borde de color alrededor de la foto si se pide."""
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(visible=False)
    for lado in ax.spines.values():
        lado.set_visible(color is not None)
        lado.set_color(color or estilo.SECUNDARIO)
        lado.set_linewidth(2.5)


def _cuadricula(cantidad, columnas, titulo):
    """La figura y sus ejes, ya con el título puesto y los sobrantes escondidos."""
    columnas = min(columnas, cantidad)
    filas = (cantidad + columnas - 1) // columnas
    figura, _ = plt.subplots(filas, columnas, figsize=(2.0 * columnas, 2.3 * filas),
                             squeeze=False)
    figura.suptitle(titulo, color=estilo.CLARO, fontsize=14)

    for sobrante in figura.axes[cantidad:]:
        sobrante.set_visible(False)

    return figura, figura.axes[:cantidad]


def dibujar_muestra(imagenes, titulos=None, columnas=6, titulo="Unas fotos",
                    media=MEDIA, desv=DESV):
    """Una cuadrícula con las fotos tal como las ve la red."""
    figura, ejes = _cuadricula(len(imagenes), columnas, titulo)

    for i, ax in enumerate(ejes):
        ax.imshow(_a_imagen(imagenes[i], media, desv))
        if titulos is not None:
            ax.set_title(titulos[i], color=estilo.SECUNDARIO, fontsize=9, pad=6)
        _marco(ax)

    figura.tight_layout()
    plt.show()


def dibujar_predicciones(imagenes, reales, probabilidades, nombres=NOMBRES, umbral=0.5,
                         columnas=6, titulo="Lo que dijo el modelo",
                         media=MEDIA, desv=DESV):
    """Cada foto con su veredicto: borde verde si acertó, rojo si se equivocó.

    `probabilidades` es la probabilidad que le dio el modelo a la clase positiva,
    o sea a `nombres[1]`.
    """
    reales = torch.as_tensor(reales).flatten()
    probabilidades = torch.as_tensor(probabilidades).flatten()
    figura, ejes = _cuadricula(len(imagenes), columnas, titulo)

    for i, ax in enumerate(ejes):
        probabilidad = float(probabilidades[i])
        dijo = int(probabilidad >= umbral)
        acerto = dijo == int(reales[i])
        color = estilo.VERDE if acerto else estilo.ROJO

        ax.imshow(_a_imagen(imagenes[i], media, desv))
        ax.set_title(f"{nombres[dijo]}  {max(probabilidad, 1 - probabilidad):.0%}",
                     color=color, fontsize=9, pad=6)
        _marco(ax, color)

    figura.tight_layout()
    plt.show()


def dibujar_veredicto(imagen, probabilidad, nombres=NOMBRES, umbral=0.5,
                      media=MEDIA, desv=DESV):
    """Una sola foto, grande, con lo que respondió la app."""
    dijo = int(probabilidad >= umbral)
    color = estilo.PRIMARIO if dijo else estilo.AMBAR

    _, ax = plt.subplots(figsize=(4.8, 4.8))
    ax.imshow(_a_imagen(imagen, media, desv))
    ax.set_title(f"{nombres[dijo].upper()}\n"
                 f"{max(probabilidad, 1 - probabilidad):.1%} de confianza",
                 color=color, fontsize=14)
    _marco(ax, color)

    plt.tight_layout()
    plt.show()
