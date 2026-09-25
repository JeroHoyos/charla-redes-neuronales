from manim import (
    DOWN,
    RIGHT,
    UP,
    FadeIn,
    LaggedStart,
    MathTex,
    Transform,
    VGroup,
)

from componentes import texto
from componentes import titulo as hacer_titulo
from estilo import CLARO, PRIMARIO, ROJO, SECUNDARIO

from . import _error


def construir(scene):
    encabezado = hacer_titulo("Error para regresión")
    ys = _error.datos()
    mala = _error.ajuste_malo(ys)
    proporcion = _error.proporcion(ys, mala)

    mse = MathTex(
        r"L_{\mathrm{MSE}}", "=", r"\frac{1}{n}\sum",
        r"(", "y", "-", r"\hat{y}", ")^2",
    ).scale(1.1).move_to([0, _error.Y_FORMULA, 0])
    mse[0].set_color(ROJO)
    mse[4].set_color(CLARO)
    mse[6].set_color(PRIMARIO)
    leyenda = _error.leyenda((
        ("y", CLARO, "lo que era de verdad"),
        (r"\hat{y}", PRIMARIO, "lo que dijo el modelo"),
        ("n", SECUNDARIO, "cuántos ejemplos hay"),
    ))

    ejes = _error.ejes_datos(
        _error.CENTRO_GRAFICA_APOYO, _error.ANCHO_GRAFICA_APOYO,
        _error.ALTO_GRAFICA_APOYO,
    )
    puntos, curva_mala, cuad_mala = _error.dibujo_datos(
        ejes, ys, mala, "cuadrados", radio=0.055, grosor=2.6,
    )
    _, curva_buena, cuad_buena = _error.dibujo_datos(
        ejes, ys, _error.real, "cuadrados", radio=0.055, grosor=2.6,
    )
    tubo = _error.tubo_apoyo()
    rotulo = texto("error", 17, color=ROJO).next_to(tubo, UP, buff=0.2)
    nivel = _error.liquido_apoyo(_error.LLENO)

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(mse, shift=UP * 0.12), run_time=1.0)
    scene.play(
        LaggedStart(*[FadeIn(f, shift=RIGHT * 0.15) for f in leyenda],
                    lag_ratio=0.18),
        FadeIn(VGroup(ejes, puntos, curva_mala, tubo, rotulo)),
        run_time=1.2,
    )
    scene.play(
        LaggedStart(*[FadeIn(c, scale=0.4) for c in cuad_mala],
                    lag_ratio=0.12),
        FadeIn(nivel),
        run_time=1.0,
    )
    scene.next_slide()

    scene.play(
        Transform(curva_mala, curva_buena),
        Transform(cuad_mala, cuad_buena),
        Transform(nivel, _error.liquido_apoyo(_error.LLENO * proporcion)),
        run_time=1.4,
    )
    scene.next_slide()
