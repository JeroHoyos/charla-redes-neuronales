import numpy as np
from manim import (
    DOWN,
    LEFT,
    UP,
    Arrow,
    Circle,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    LaggedStart,
    Line,
    MathTex,
    MoveAlongPath,
    Rotate,
    Transform,
    VGroup,
    there_and_back,
)

from componentes import texto
from componentes import titulo as hacer_titulo
from estilo import AMBAR, CLARO, FONDO, MORADO, PRIMARIO, ROJO, SECUNDARIO, VERDE

from . import _backprop

ZOOM = 3.4
Y_ROTULO_GRADIENTE = 1.55
TRAS_EL_PASO = 0.34

Y_NEURONA = 0.2
PASO_ENTRADA = 1.15
X_ENTRADA = -4.0
X_PERILLA = -3.2
X_MULT = -1.8
X_SUMA = 0.0
X_RELU = 1.8
X_PERDIDA = 3.8
ALTURAS_NEURONA = tuple(
    Y_NEURONA + PASO_ENTRADA - i * PASO_ENTRADA for i in range(3)
)


def _girar(perilla, angulo=-0.7):
    return Rotate(perilla[0][1], angle=angulo,
                  about_point=perilla[0][0].get_center())


def _restaurar_red(capas, conexiones):
    for capa in capas:
        for nodo in capa:
            nodo.set_stroke(color=SECUNDARIO, width=2.5, opacity=1.0)
            nodo.set_fill(FONDO, opacity=1.0)
    for grupo in conexiones:
        grupo.set_stroke(color=SECUNDARIO, width=1.5, opacity=0.4)


def _neurona():
    ys = ALTURAS_NEURONA

    entradas = VGroup(*[
        MathTex(f"x_{i + 1}", color=CLARO).scale(0.75).move_to(
            [X_ENTRADA, y, 0],
        )
        for i, y in enumerate(ys)
    ])
    perillas = VGroup(*[
        _backprop.perilla(f"w_{i + 1}").move_to([X_PERILLA, y - 0.62, 0])
        for i, y in enumerate(ys)
    ])
    multiplicadores = VGroup(*[
        VGroup(
            Circle(radius=0.24, color=SECUNDARIO, stroke_width=2.5)
            .set_fill(FONDO, opacity=1.0),
            MathTex(r"\times", color=SECUNDARIO).scale(0.7),
        ).move_to([X_MULT, y, 0])
        for y in ys
    ])
    suma = VGroup(
        Circle(radius=0.28, color=SECUNDARIO, stroke_width=2.5)
        .set_fill(FONDO, opacity=1.0),
        MathTex("+", color=SECUNDARIO).scale(0.8),
    ).move_to([X_SUMA, Y_NEURONA, 0])
    sesgo = _backprop.colgar(_backprop.perilla("b", lado=LEFT), suma, buff=1.35)

    relu = _backprop.caja(r"\mathrm{ReLU}", PRIMARIO, ancho=1.5, escala=0.55)
    relu.move_to([X_RELU, Y_NEURONA, 0])
    perdida = _backprop.caja("L", ROJO, ancho=0.95, escala=0.85)
    perdida.move_to([X_PERDIDA, Y_NEURONA, 0])

    cables_entrada = VGroup(*[
        Line([X_ENTRADA + 0.22, y, 0], [X_MULT - 0.24, y, 0],
             color=SECUNDARIO, stroke_width=2).set_stroke(opacity=0.7)
        for y in ys
    ])
    cables_peso = VGroup(*[
        Line(perillas[i][0].get_top(), [X_MULT - 0.17, y - 0.17, 0],
             color=AMBAR, stroke_width=2).set_stroke(opacity=0.7)
        for i, y in enumerate(ys)
    ])
    cables_suma = VGroup(*[
        Line([X_MULT + 0.24, y, 0], suma[0].get_center(),
             color=SECUNDARIO, stroke_width=2).set_stroke(opacity=0.7)
        for y in ys
    ])
    cable_sesgo = Line(
        sesgo[0].get_top(), suma[0].get_bottom(),
        color=AMBAR, stroke_width=2,
    ).set_stroke(opacity=0.7)
    flecha_z = Arrow(suma[0].get_right(), relu.get_left(), color=SECUNDARIO,
                     stroke_width=3, buff=0.12, tip_length=0.18)
    flecha_a = Arrow(relu.get_right(), perdida.get_left(), color=SECUNDARIO,
                     stroke_width=3, buff=0.12, tip_length=0.18)
    VGroup(flecha_z, flecha_a).set_stroke(opacity=0.85)

    etiquetas = VGroup(
        *[MathTex(f"p_{i + 1}", color=SECUNDARIO).scale(0.55).next_to(
            multiplicadores[i], UP, buff=0.12,
        ) for i in range(3)],
        MathTex("z", color=SECUNDARIO).scale(0.6).next_to(
            flecha_z, UP, buff=0.1),
        MathTex("a", color=SECUNDARIO).scale(0.6).next_to(
            flecha_a, UP, buff=0.1),
    )

    resto = VGroup(
        cables_entrada, cables_peso, cables_suma, cable_sesgo,
        flecha_z, flecha_a, entradas, multiplicadores, relu, perdida,
        perillas, sesgo, etiquetas,
    )
    tramos = (flecha_a, flecha_z, cables_suma, cables_peso, cable_sesgo)
    return suma, resto, perillas, sesgo, tramos


def construir(scene):
    encabezado_bp = hacer_titulo("Backpropagation")
    encabezado = hacer_titulo("Dentro de una neurona")
    encabezado_red = hacer_titulo("Toda la red")

    capas, conexiones = _backprop.red()
    red = VGroup(*conexiones, *capas)
    tubo = _backprop.tubo()
    rotulo_termo = texto("error", 19, color=ROJO).next_to(tubo, UP, buff=0.22)
    nivel = _backprop.liquido(0.02)

    nucleo, resto_neurona, perillas, sesgo, tramos = _neurona()
    flecha_a, flecha_z, cables_suma, cables_peso, cable_sesgo = tramos
    piezas_neurona = VGroup(nucleo, resto_neurona)

    gradientes = VGroup(*[
        MathTex(r"-\nabla w", color=MORADO).scale(0.75).move_to([
            (_backprop.x_capa(i) + _backprop.x_capa(i + 1)) / 2,
            Y_ROTULO_GRADIENTE, 0,
        ])
        for i in range(len(_backprop.CAPAS_RED) - 1)
    ])

    reuso = MathTex(
        r"\frac{\partial L}{\partial w_i}", "=",
        r"\frac{\partial L}{\partial z}", r"\cdot", "x_i",
    ).scale(0.9).move_to([0, -2.9, 0])
    reuso[0].set_color(AMBAR)
    reuso[2].set_color(MORADO)
    reuso[4].set_color(CLARO)

    parada_salida = np.array([(X_RELU + X_PERDIDA) / 2, Y_NEURONA, 0])
    parada_activa = np.array([(X_SUMA + X_RELU) / 2, Y_NEURONA, 0])
    parada_suma = np.array([X_SUMA - 0.62, Y_NEURONA, 0])
    paradas_mult = [np.array([X_MULT + 0.85, y, 0]) for y in ALTURAS_NEURONA]
    etiqueta_relu = MathTex(
        r"\cdot\ \frac{\partial a}{\partial z}", color=PRIMARIO,
    ).scale(0.6).move_to([X_RELU, Y_NEURONA + 0.95, 0])
    nodo_zoom = capas[1][_backprop.ARISTA_ELEGIDA % len(capas[1])]

    scene.play(FadeIn(encabezado_bp, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(red), run_time=0.9)
    scene.play(Create(tubo), FadeIn(rotulo_termo), run_time=0.9)
    _backprop.pasada(scene, capas, conexiones, VERDE, run_time=0.42)
    scene.add(nivel)
    scene.play(Transform(nivel, _backprop.liquido(_backprop.LLENO)),
               run_time=0.8)
    scene.next_slide()

    scene.play(
        FadeOut(encabezado_bp), FadeIn(encabezado, shift=DOWN * 0.2),
        nodo_zoom.animate.set_stroke(color=AMBAR, width=4.5),
        run_time=0.6,
    )
    scene.play(nodo_zoom.animate(rate_func=there_and_back).scale(1.35),
               run_time=0.6)
    scene.next_slide()

    foco = nodo_zoom.get_center()
    scene.play(
        red.animate.scale(ZOOM, about_point=foco).set_opacity(0),
        FadeOut(tubo), FadeOut(rotulo_termo), FadeOut(nivel),
        run_time=1.2,
    )
    scene.remove(red)
    scene.play(FadeIn(nucleo), FadeIn(resto_neurona), run_time=0.9)
    scene.next_slide()

    ficha = _backprop.ficha(r"\frac{\partial L}{\partial a}")
    ficha.move_to(parada_salida)
    scene.play(FadeIn(ficha, scale=0.6), run_time=0.6)
    _backprop.llevar(scene, [ficha], [parada_activa], [flecha_a])
    scene.play(FadeIn(etiqueta_relu, shift=DOWN * 0.1), run_time=0.4)
    scene.play(_backprop.convertir(ficha, r"\frac{\partial L}{\partial z}"),
               run_time=0.7)
    _backprop.llevar(scene, [ficha], [parada_suma], [flecha_z])
    scene.next_slide()

    ramas = [ficha.copy() for _ in ALTURAS_NEURONA]
    rama_sesgo = ficha.copy()
    scene.add(*ramas, rama_sesgo)
    scene.remove(ficha)
    _backprop.llevar(
        scene, ramas + [rama_sesgo],
        paradas_mult + [sesgo[0].get_center() + UP * 0.8],
        list(cables_suma) + [cable_sesgo], run_time=0.9,
    )
    scene.play(FadeIn(reuso, shift=UP * 0.12), run_time=0.7)

    scene.play(
        LaggedStart(*[
            _backprop.convertir(
                r, rf"\frac{{\partial L}}{{\partial w_{i + 1}}}",
            )
            for i, r in enumerate(ramas)
        ], lag_ratio=0.18),
        _backprop.convertir(rama_sesgo, r"\frac{\partial L}{\partial b}"),
        run_time=1.0,
    )
    scene.next_slide()

    _backprop.llevar(
        scene, ramas + [rama_sesgo],
        [p[0].get_center() for p in perillas] + [sesgo[0].get_center()],
        list(cables_peso), run_time=0.8,
    )
    scene.play(
        LaggedStart(*[FadeOut(r, scale=0.3) for r in ramas + [rama_sesgo]],
                    lag_ratio=0.12),
        LaggedStart(*[_girar(p) for p in perillas], lag_ratio=0.12),
        _girar(sesgo),
        run_time=1.0,
    )
    scene.next_slide()

    scene.play(FadeOut(piezas_neurona), FadeOut(reuso),
               FadeOut(etiqueta_relu), run_time=0.7)
    red.scale(1 / ZOOM, about_point=foco)
    _restaurar_red(capas, conexiones)
    scene.play(
        FadeIn(red), FadeIn(tubo), FadeIn(rotulo_termo), FadeIn(nivel),
        FadeOut(encabezado), FadeIn(encabezado_red, shift=DOWN * 0.2),
        run_time=0.7,
    )
    anterior = None
    for i in range(len(conexiones) - 1, -1, -1):
        grupo = conexiones[i]
        pulsos = [Dot(color=MORADO, radius=0.06).move_to(c.get_end())
                  for c in grupo]
        caminos = [Line(c.get_end(), c.get_start()) for c in grupo]
        scene.add(*pulsos)
        scene.play(
            *[MoveAlongPath(p, c) for p, c in zip(pulsos, caminos)],
            *([FadeOut(anterior, shift=DOWN * 0.3)] if anterior else []),
            run_time=0.6,
        )
        scene.play(
            *[p.animate.set_opacity(0) for p in pulsos],
            LaggedStart(*[_backprop.pulso(n, MORADO) for n in capas[i]],
                        lag_ratio=0.07),
            grupo.animate.set_stroke(color=AMBAR, opacity=0.8, width=1.8),
            FadeIn(gradientes[i], shift=DOWN * 0.3),
            run_time=0.6,
        )
        scene.remove(*pulsos)
        anterior = gradientes[i]
    scene.play(FadeOut(anterior, shift=DOWN * 0.3), run_time=0.45)
    scene.next_slide()

    _backprop.pasada(scene, capas, conexiones, VERDE, run_time=0.42)
    scene.play(Transform(nivel, _backprop.liquido(TRAS_EL_PASO)), run_time=1.0)
    scene.wait(0.4)

    scene.next_slide()
