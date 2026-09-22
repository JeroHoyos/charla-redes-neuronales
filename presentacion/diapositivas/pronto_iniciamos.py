from manim import (
    DOWN,
    UP,
    Circle,
    FadeIn,
    GrowFromCenter,
)

from componentes import imagen_circular, texto
from estilo import FONT_TITULO, PRIMARIO

Y_CIRCULO = 0.75
DIAMETRO = 4.4
OCUPACION = 0.62


def construir(scene):
    gato = imagen_circular("gato_tostada", diametro=DIAMETRO, ocupacion=OCUPACION)
    gato.move_to([0, Y_CIRCULO, 0])

    borde = Circle(radius=DIAMETRO / 2, color=PRIMARIO, stroke_width=7)
    borde.move_to(gato.get_center())

    mensaje = texto("PRONTO INICIAMOS", 32, color=PRIMARIO, font=FONT_TITULO)
    mensaje.next_to(borde, DOWN, buff=0.8)

    scene.play(FadeIn(gato, scale=0.85), GrowFromCenter(borde), run_time=0.9)
    scene.play(FadeIn(mensaje, shift=UP * 0.15), run_time=0.6)
    scene.wait(0.5)

    scene.next_slide()
