from manim import (
    DOWN,
    RIGHT,
    FadeIn,
)

from componentes import vinetas
from componentes import titulo as hacer_titulo


def construir(scene):
    encabezado = hacer_titulo("Título de la diapositiva")
    cuerpo = vinetas([
        "Idea uno",
        "Idea dos",
        "Idea tres",
    ]).shift(DOWN * 0.3)

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.7)
    for elemento in cuerpo:
        scene.play(FadeIn(elemento, shift=RIGHT * 0.2), run_time=0.35)
    scene.wait(0.5)

    scene.next_slide()
