import numpy as np
from manim import (
    DOWN,
    RIGHT,
    UP,
    Axes,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    LaggedStart,
    MathTex,
    Transform,
    VGroup,
)

from componentes import texto
from componentes import titulo as hacer_titulo
from estilo import CLARO, PRIMARIO, ROJO, VERDE

from . import _error

P_MALA, P_BUENA = 0.1, 0.9


def _ejes_log(centro, ancho, alto):
    ejes = Axes(
        x_range=[0, 1.05, 0.25], y_range=[0, 3.2, 1],
        x_length=ancho, y_length=alto, axis_config=_error.EJES,
    ).move_to(centro)
    curva = ejes.plot(lambda p: -np.log(p), x_range=[0.043, 1.0, 0.01],
                      color=ROJO).set_stroke(width=3.5)
    rot_x = MathTex(r"\hat{y}", color=PRIMARIO).scale(0.65)
    rot_x.next_to(ejes.c2p(1.05, 0), DOWN, buff=0.2)
    return VGroup(ejes, rot_x), curva


def _marca_log(ejes, p, color):
    coste = -np.log(p)
    return VGroup(
        DashedLine(ejes.c2p(p, 0), ejes.c2p(p, coste), color=color,
                   stroke_width=2, dash_length=0.08).set_stroke(opacity=0.7),
        Dot(ejes.c2p(p, coste), radius=0.085, color=color),
        texto(f"{p}", 18, color=color).next_to(
            ejes.c2p(p, 0), DOWN, buff=0.14,
        ),
    )


def construir(scene):
    encabezado = hacer_titulo("Entropía cruzada")

    entropia = MathTex(
        r"L_{\mathrm{CE}}", "=", "-", r"\sum_i", "y_i", r"\log(",
        r"\hat{y}_i", ")",
    ).scale(1.0).move_to([0, _error.Y_FORMULA, 0])
    for i in (0, 2):
        entropia[i].set_color(ROJO)
    entropia[4].set_color(CLARO)
    entropia[6].set_color(PRIMARIO)
    leyenda = _error.leyenda((
        ("y_i", CLARO, "1 si es la correcta, si no 0"),
        (r"\hat{y}_i", PRIMARIO, "la probabilidad del modelo"),
    ))

    ejes, curva = _ejes_log(
        _error.CENTRO_GRAFICA_APOYO, _error.ANCHO_GRAFICA_APOYO,
        _error.ALTO_GRAFICA_APOYO,
    )
    marca_mala = _marca_log(ejes[0], P_MALA, ROJO)
    marca_buena = _marca_log(ejes[0], P_BUENA, VERDE)
    tubo = _error.tubo_apoyo()
    rotulo = texto("error", 17, color=ROJO).next_to(tubo, UP, buff=0.2)
    nivel = _error.liquido_apoyo(_error.LLENO, ROJO)
    nivel_bajo = _error.liquido_apoyo(
        _error.LLENO * float(np.log(P_BUENA) / np.log(P_MALA)), VERDE,
    )

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(entropia, shift=UP * 0.12), run_time=1.0)
    scene.play(
        LaggedStart(*[FadeIn(f, shift=RIGHT * 0.15) for f in leyenda],
                    lag_ratio=0.18),
        FadeIn(ejes), FadeIn(tubo), FadeIn(rotulo),
        run_time=1.1,
    )
    scene.play(Create(curva), run_time=0.9)
    scene.play(FadeIn(marca_mala), FadeIn(nivel), run_time=0.9)
    scene.next_slide()

    scene.play(
        Transform(marca_mala, marca_buena),
        Transform(nivel, nivel_bajo),
        run_time=1.4,
    )
    scene.wait(0.4)

    scene.next_slide()
