import numpy as np
from manim import (
    DOWN,
    UP,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    ValueTracker,
    VGroup,
)

from componentes import titulo as hacer_titulo
from estilo import CLARO, MORADO, PRIMARIO, ROJO

from . import _error

X_IZQ, X_DER = _error.X_COLUMNAS
FONDO_X = 3.0
PENDIENTE_V = 0.75
LARGO_TANGENTE = 1.5
X_SALIDA = 0.9


def _cuenco(x):
    return 0.32 * (x - FONDO_X) ** 2 + 0.25


def _derivada_cuenco(x):
    return 0.64 * (x - FONDO_X)


def _ve(x):
    return PENDIENTE_V * abs(x - FONDO_X) + 0.25


def _derivada_ve(x):
    return PENDIENTE_V * np.sign(x - FONDO_X)


def _direccion(ejes, funcion, pendiente, x):
    punto = ejes.c2p(x, funcion(x))
    direccion = ejes.c2p(x + 1, funcion(x) + pendiente) - punto
    return punto, direccion / np.linalg.norm(direccion)


def _tangente(ejes, funcion, pendiente, x, color=MORADO):
    punto, direccion = _direccion(ejes, funcion, pendiente, x)
    return VGroup(
        Line(punto - direccion * LARGO_TANGENTE / 2,
             punto + direccion * LARGO_TANGENTE / 2,
             color=color, stroke_width=4),
        Dot(punto, radius=0.08, color=CLARO),
    )


def construir(scene):
    encabezado = hacer_titulo("Diferenciable")

    ejes_izq = _error.ejes_columna(X_IZQ)
    ejes_der = _error.ejes_columna(X_DER)
    cuenco = ejes_izq.plot(_cuenco, x_range=[0.4, 5.6, 0.05], color=PRIMARIO)
    ve = ejes_der.plot(_ve, x_range=[0.4, 5.6, 0.02], color=PRIMARIO,
                       use_smoothing=False)
    VGroup(cuenco, ve).set_stroke(width=3.5)

    x_izq, x_der = ValueTracker(X_SALIDA), ValueTracker(X_SALIDA)

    def tangente_izq():
        x = x_izq.get_value()
        return _tangente(ejes_izq, _cuenco, _derivada_cuenco(x), x)

    def tangente_der():
        x = x_der.get_value()
        return _tangente(ejes_der, _ve, _derivada_ve(x), x)

    t_izq, t_der = tangente_izq(), tangente_der()
    dudas = VGroup(*[
        _tangente(ejes_der, _ve, signo * PENDIENTE_V, FONDO_X, ROJO)
        for signo in (-1, 1)
    ])

    diferenciable = _error.etiqueta(True, "diferenciable", X_IZQ)
    no_diferenciable = _error.etiqueta(False, "no diferenciable", X_DER)

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(Create(ejes_izq), Create(ejes_der), run_time=0.7)
    scene.play(Create(cuenco), Create(ve), run_time=1.0)
    scene.play(FadeIn(t_izq, scale=0.6), FadeIn(t_der, scale=0.6),
               run_time=0.4)
    t_izq.add_updater(lambda m: m.become(tangente_izq()))
    t_der.add_updater(lambda m: m.become(tangente_der()))
    scene.play(
        x_izq.animate.set_value(FONDO_X),
        x_der.animate.set_value(FONDO_X - 1e-6),
        run_time=2.2,
    )
    t_izq.clear_updaters()
    t_der.clear_updaters()
    scene.play(FadeOut(t_der), FadeIn(dudas, scale=0.7), run_time=0.6)
    scene.play(FadeIn(diferenciable, shift=UP * 0.1),
               FadeIn(no_diferenciable, shift=UP * 0.1), run_time=0.6)
    scene.next_slide()
