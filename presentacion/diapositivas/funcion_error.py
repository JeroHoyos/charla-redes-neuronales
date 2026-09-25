from manim import (
    DOWN,
    UP,
    Create,
    FadeIn,
    LaggedStart,
    Transform,
)

from componentes import texto
from componentes import titulo as hacer_titulo
from estilo import ROJO

from . import _error

X_TERMO = 4.35
ANCHO_TERMO = 0.75
ALTO_TERMO = 3.1
Y_PIE_TERMO = -2.05


def construir(scene):
    encabezado = hacer_titulo("¿Cómo calificamos el modelo?")
    ys = _error.datos()
    mala = _error.ajuste_malo(ys)
    proporcion = _error.proporcion(ys, mala)

    ejes = _error.ejes_datos([-1.7, -0.35, 0], 7.4, 3.9)
    puntos, curva_mala, dist_mala = _error.dibujo_datos(
        ejes, ys, mala, "distancias",
    )
    _, curva_buena, dist_buena = _error.dibujo_datos(
        ejes, ys, _error.real, "distancias",
    )

    tubo = _error.tubo(X_TERMO, Y_PIE_TERMO, ANCHO_TERMO, ALTO_TERMO)
    rotulo_termo = texto("error", 20, color=ROJO).next_to(tubo, UP, buff=0.24)
    nivel = _error.liquido(X_TERMO, Y_PIE_TERMO, ANCHO_TERMO, ALTO_TERMO,
                           _error.LLENO)

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)

    scene.play(Create(ejes), run_time=0.7)
    scene.play(
        LaggedStart(*[FadeIn(p, scale=0.5) for p in puntos], lag_ratio=0.08),
        run_time=0.9,
    )
    scene.play(Create(tubo), FadeIn(rotulo_termo), run_time=0.6)
    scene.play(Create(curva_mala), run_time=0.8)
    scene.play(
        LaggedStart(*[Create(d) for d in dist_mala], lag_ratio=0.1),
        FadeIn(nivel),
        run_time=1.1,
    )
    scene.next_slide()

    scene.play(
        Transform(curva_mala, curva_buena),
        Transform(dist_mala, dist_buena),
        Transform(nivel, _error.liquido(X_TERMO, Y_PIE_TERMO, ANCHO_TERMO,
                                        ALTO_TERMO, _error.LLENO * proporcion)),
        run_time=1.5,
    )
    scene.next_slide()
