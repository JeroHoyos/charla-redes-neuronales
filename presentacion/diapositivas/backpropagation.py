import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Circle,
    Create,
    FadeIn,
    FadeOut,
    LaggedStart,
    Line,
    MathTex,
    VGroup,
    Write,
)

from componentes import texto
from componentes import titulo as hacer_titulo
from estilo import AMBAR, CLARO, FONDO, PRIMARIO, ROJO, SECUNDARIO

from . import _backprop

Y_CADENA = 0.35
LARGO_FLECHA = 0.62

CENTRADO = -_backprop.X_RED
AMPLIACION = 1.25


def _flecha_corta(color=SECUNDARIO):
    return Arrow(
        LEFT * LARGO_FLECHA / 2, RIGHT * LARGO_FLECHA / 2, color=color,
        stroke_width=3, buff=0, tip_length=0.18,
    ).set_stroke(opacity=0.85)


def _cadena_funciones():
    entrada = MathTex("x", color=CLARO).scale(0.95)
    efes = [_backprop.caja(f"f_{i}", PRIMARIO) for i in (1, 2, 3)]
    perdida = _backprop.caja(r"\ell", ROJO)
    salida = MathTex("L", color=ROJO).scale(1.2)
    flechas = [_flecha_corta() for _ in range(5)]

    fila = VGroup(
        entrada, flechas[0], efes[0], flechas[1], efes[1], flechas[2],
        efes[2], flechas[3], perdida, flechas[4], salida,
    ).arrange(RIGHT, buff=0.24).move_to([0, Y_CADENA, 0])

    hs = VGroup(*[
        MathTex(f"h_{i}", color=SECUNDARIO).scale(0.65).next_to(
            flechas[i], UP, buff=0.12,
        )
        for i in (1, 2, 3)
    ])

    perilla = _backprop.colgar(
        _backprop.perilla("w", lado=LEFT), efes[0], buff=0.55,
    )
    cable = Line(
        efes[0].get_bottom(), perilla[0].get_top(),
        color=AMBAR, stroke_width=2,
    ).set_stroke(opacity=0.7)

    return fila, hs, VGroup(cable, perilla), efes, perdida


def _numerito(n, debajo_de):
    circulo = Circle(radius=0.16, color=SECUNDARIO, stroke_width=1.8)
    circulo.set_fill(FONDO, opacity=1.0)
    numero = texto(str(n), 13, color=SECUNDARIO).move_to(circulo.get_center())
    return VGroup(circulo, numero).next_to(debajo_de, DOWN, buff=0.16)


def construir(scene):
    encabezado = hacer_titulo("Una función dentro de otra")

    compuesta = MathTex(
        "L", "(", "w", ")", "=", "L", r"\big(", "f(x;", "w", ")", ",", "y",
        r"\big)",
    ).scale(1.05).move_to([0, 1.95, 0])
    for i in (0, 1, 3, 5, 6, 12):
        compuesta[i].set_color(ROJO)
    for i in (2, 8):
        compuesta[i].set_color(AMBAR)
    for i in (7, 9):
        compuesta[i].set_color(PRIMARIO)
    for i in (10, 11):
        compuesta[i].set_color(CLARO)

    fila, hs, mando, efes, caja_perdida = _cadena_funciones()

    cadena = MathTex(
        r"\frac{\partial L}{\partial w}", "=",
        r"\frac{\partial L}{\partial h_3}", r"\cdot",
        r"\frac{\partial h_3}{\partial h_2}", r"\cdot",
        r"\frac{\partial h_2}{\partial h_1}", r"\cdot",
        r"\frac{\partial h_1}{\partial w}",
    ).scale(1.0).move_to([0, -1.9, 0])
    cadena[0].set_color(AMBAR)
    cadena[2].set_color(ROJO)
    cadena[4].set_color(PRIMARIO)
    cadena[6].set_color(PRIMARIO)
    cadena[8].set_color(AMBAR)
    numeros = VGroup(*[
        _numerito(n, cadena[2 * n]) for n in (1, 2, 3, 4)
    ])

    capas, conexiones = _backprop.red()
    red = VGroup(*conexiones, *capas)
    centro_red = np.array([0.0, _backprop.Y_RED, 0.0])
    red.shift(RIGHT * CENTRADO).scale(AMPLIACION, about_point=centro_red)

    elegida = conexiones[0][_backprop.ARISTA_ELEGIDA]
    rot_elegida = MathTex("w", color=AMBAR).scale(0.7)
    rot_elegida.next_to(elegida.get_center(), UP + LEFT, buff=0.08)
    destino = _backprop.ARISTA_ELEGIDA % len(capas[1])
    abanico = [
        VGroup(*conexiones[1][destino * len(capas[2]):
                             (destino + 1) * len(capas[2])]),
        conexiones[2],
    ]

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(compuesta), run_time=0.8)
    scene.play(
        LaggedStart(*[FadeIn(p, shift=RIGHT * 0.2) for p in fila],
                    lag_ratio=0.12),
        run_time=1.8,
    )
    scene.play(FadeIn(hs), Create(mando), run_time=0.8)
    scene.next_slide()

    scene.play(Write(cadena), run_time=1.6)
    scene.play(
        LaggedStart(*[FadeIn(n, scale=0.5) for n in numeros], lag_ratio=0.2),
        run_time=1.0,
    )
    scene.next_slide()

    scene.play(
        FadeOut(compuesta), FadeOut(fila), FadeOut(hs), FadeOut(mando),
        FadeOut(cadena), FadeOut(numeros),
        run_time=0.8,
    )
    scene.play(FadeIn(red), run_time=0.9)
    scene.play(
        elegida.animate.set_stroke(color=AMBAR, opacity=1.0, width=3.5),
        FadeIn(rot_elegida),
        run_time=0.7,
    )
    for grupo in abanico:
        scene.play(grupo.animate.set_stroke(color=ROJO, opacity=0.75,
                                            width=2.2), run_time=0.6)
    scene.next_slide()
