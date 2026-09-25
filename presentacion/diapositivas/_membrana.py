import numpy as np
from manim import (
    Dot,
    Line,
    Rectangle,
    RoundedRectangle,
    VGroup,
    VMobject,
)

from componentes import texto
from estilo import FONDO, SECUNDARIO

X_IZQ = -6.2
X_DER = 6.2
Y_MEMBRANA = 0.0
ALTO_CABEZA = 0.30
RADIO_CABEZA = 0.115


def bicapa(y=Y_MEMBRANA, x_izq=X_IZQ, x_der=X_DER, n=None):
    if n is None:
        n = max(2, int((x_der - x_izq) / (2 * RADIO_CABEZA)) + 1)
    xs = np.linspace(x_izq, x_der, n)

    nucleo = Rectangle(
        width=x_der - x_izq + 2 * RADIO_CABEZA, height=2 * ALTO_CABEZA,
        stroke_width=0,
    ).set_fill(SECUNDARIO, opacity=0.07).move_to([(x_izq + x_der) / 2, y, 0])

    capa = VGroup(nucleo)
    for x in xs:
        for signo in (1, -1):
            cuello = y + signo * (ALTO_CABEZA - 0.04)
            for sesgo in (-0.045, 0.045):
                capa.add(Line(
                    [x, cuello, 0], [x + sesgo, y + signo * 0.05, 0],
                    color=SECUNDARIO, stroke_width=1.5, stroke_opacity=0.45,
                ))
            capa.add(Dot(
                [x, y + signo * ALTO_CABEZA, 0],
                radius=RADIO_CABEZA, color=SECUNDARIO, fill_opacity=0.6,
            ))
    return capa


def ion(carga, posicion, color, radio=0.17, tam=18):
    disco = Dot(posicion, radius=radio, color=color, fill_opacity=0.28)
    borde = Dot(posicion, radius=radio, color=color, fill_opacity=0)
    borde.set_stroke(color=color, width=2.5)
    etiqueta = texto(carga, tam, color=color).move_to(posicion)
    return VGroup(disco, borde, etiqueta)


ANCHO_MITAD = 0.3
ALTO_CANAL = 2 * ALTO_CABEZA + 0.44


def canal(x, color, y=Y_MEMBRANA, abertura=0.0):
    mitades = VGroup()
    for signo in (-1, 1):
        mitad = RoundedRectangle(
            width=ANCHO_MITAD, height=ALTO_CANAL, corner_radius=0.13,
            stroke_color=color, stroke_width=3,
            fill_color=FONDO, fill_opacity=1.0,
        )
        mitad.move_to([x + signo * (ANCHO_MITAD / 2 + abertura), y, 0])
        mitades.add(mitad)
    return mitades


def voltimetro(valor, color, posicion):
    return texto(valor, 26, color=color).move_to(posicion)


def trazo_suave(puntos, color, grosor=4):
    curva = VMobject(color=color, stroke_width=grosor)
    curva.set_points_smoothly([np.array(p) for p in puntos])
    return curva


__all__ = [
    "bicapa", "ion", "canal", "voltimetro", "trazo_suave",
    "X_IZQ", "X_DER", "Y_MEMBRANA", "ALTO_CABEZA",
]
