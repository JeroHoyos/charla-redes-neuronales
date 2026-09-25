import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Axes,
    Circle,
    Create,
    DashedLine,
    DecimalNumber,
    Dot,
    Ellipse,
    FadeIn,
    GrowFromEdge,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    Polygon,
    Rectangle,
    SurroundingRectangle,
    TransformFromCopy,
    ValueTracker,
    VGroup,
)

from componentes import texto
from componentes import titulo as hacer_titulo
from estilo import AMBAR, CLARO, FONDO, MORADO, PRIMARIO, ROJO, SECUNDARIO, VERDE

from . import _error

P_GATO = 0.7
Q_INICIAL, Q_EXCESO = 0.3, 0.95
OPACIDAD_P, OPACIDAD_Q = 0.7, 0.85

X_LEYENDA = -6.25
X_GLOSA = -5.45
Y_LEYENDA = (2.4, 2.0, 1.6)

X_GRUPOS = (-4.75, -2.45)
SEP_PAR = 0.36
ANCHO_BARRA = 0.58
Y_BASE = -1.45
ALTO_UNO = 2.5
Y_LETRAS = -1.78
Y_ICONOS = -2.35
ESCALA_VALOR = 0.5

Y_FORMULA = 2.05
CENTRO_CALCULO = [-3.4, -3.15, 0]
ESCALA_CALCULO = 0.6
HUECOS_P = (2, 8)
HUECOS_Q = (5, 11)
HUECO_TOTAL = 14

CENTRO_CURVA = [3.5, -1.05, 0]
ANCHO_CURVA, ALTO_CURVA = 5.0, 3.6
RANGO_Q = (0.25, 1.0)
RANGO_ERROR = (0.45, 1.1)
TRAMO_CURVA = (0.28, 0.96)


def _gato(escala=1.0):
    color = AMBAR
    orejas = VGroup(*[
        Polygon([s * 0.19, 0.1, 0], [s * 0.16, 0.34, 0], [s * 0.03, 0.2, 0])
        for s in (-1, 1)
    ]).set_stroke(color, width=2.5).set_fill(color, opacity=0.5)
    cabeza = Circle(radius=0.22, color=color, stroke_width=2.5)
    cabeza.set_fill(FONDO, opacity=1.0)
    ojos = VGroup(*[Dot([s * 0.08, 0.04, 0], radius=0.026, color=color)
                    for s in (-1, 1)])
    nariz = Polygon([-0.03, -0.02, 0], [0.03, -0.02, 0], [0, -0.06, 0])
    nariz.set_stroke(color, width=1.5).set_fill(color, opacity=1.0)
    bigotes = VGroup(*[
        Line([s * 0.07, -0.06, 0], [s * 0.27, y, 0], color=color,
             stroke_width=1.4)
        for s in (-1, 1) for y in (-0.02, -0.1)
    ])
    return VGroup(orejas, cabeza, ojos, nariz, bigotes).scale(escala)


def _perro(escala=1.0):
    color = MORADO
    cabeza = Circle(radius=0.22, color=color, stroke_width=2.5)
    cabeza.set_fill(FONDO, opacity=1.0)
    orejas = VGroup(*[
        Ellipse(width=0.14, height=0.32).rotate(s * 0.35)
        .move_to([s * 0.22, 0.0, 0])
        for s in (-1, 1)
    ]).set_stroke(color, width=2.5).set_fill(color, opacity=0.8)
    ojos = VGroup(*[Dot([s * 0.075, 0.05, 0], radius=0.026, color=color)
                    for s in (-1, 1)])
    nariz = Ellipse(width=0.11, height=0.075).move_to([0, -0.06, 0])
    nariz.set_stroke(color, width=1.5).set_fill(color, opacity=1.0)
    lengua = Ellipse(width=0.06, height=0.08).move_to([0, -0.14, 0])
    lengua.set_stroke(ROJO, width=1).set_fill(ROJO, opacity=0.9)
    return VGroup(cabeza, orejas, ojos, lengua, nariz).scale(escala)


def _probabilidades(q_gato):
    return (q_gato, 1 - q_gato)


P = _probabilidades(P_GATO)


def _error_total(q_gato):
    return float(sum(
        p * -np.log(q) for p, q in zip(P, _probabilidades(q_gato))
    ))


def _alto(prob):
    return max(prob * ALTO_UNO, 0.02)


def _x(k, lado):
    return X_GRUPOS[k] + lado * SEP_PAR


def _tope(k, lado, prob):
    return np.array([_x(k, lado), Y_BASE + _alto(prob), 0])


def _barras(probs, lado, color, opacidad):
    barras = VGroup()
    for k, prob in enumerate(probs):
        alto = _alto(prob)
        barras.add(Rectangle(
            width=ANCHO_BARRA, height=alto, stroke_width=0,
            fill_color=color, fill_opacity=opacidad,
        ).move_to([_x(k, lado), Y_BASE + alto / 2, 0]))
    return barras


def _valores(probs, lado, color):
    return VGroup(*[
        DecimalNumber(prob, num_decimal_places=2, color=color)
        .scale(ESCALA_VALOR).next_to(_tope(k, lado, prob), UP, buff=0.1)
        for k, prob in enumerate(probs)
    ])


def _letras(letra, lado, color):
    return VGroup(*[
        MathTex(letra, color=color).scale(0.6).move_to(
            [_x(k, lado), Y_LETRAS, 0],
        )
        for k in range(len(X_GRUPOS))
    ])


def _leyenda():
    filas = VGroup()
    for (letra, color, opacidad, glosa), y in zip(
        (("p", CLARO, OPACIDAD_P, "probabilidad real"),
         ("q", PRIMARIO, OPACIDAD_Q, "probabilidad predicha"),
         ("L", ROJO, OPACIDAD_Q, "función de error")),
        Y_LEYENDA,
    ):
        muestra = Rectangle(width=0.3, height=0.2, stroke_width=0,
                            fill_color=color, fill_opacity=opacidad)
        muestra.move_to([X_LEYENDA + 0.15, y, 0])
        simbolo = MathTex(letra, color=color).scale(0.65)
        simbolo.next_to(muestra, RIGHT, buff=0.18)
        nombre = texto(glosa, 15, color=color)
        nombre.move_to([X_GLOSA + nombre.width / 2, y, 0])
        filas.add(VGroup(muestra, simbolo, nombre))
    return filas


def _calculo(q_gato):
    q1, q2 = _probabilidades(q_gato)
    formula = MathTex(
        r"\text{error}", "=",
        f"{P[0]:.2f}", r"\cdot", "L(", f"{q1:.2f}", ")", "+",
        f"{P[1]:.2f}", r"\cdot", "L(", f"{q2:.2f}", ")",
        "=", f"{_error_total(q_gato):.2f}",
    ).scale(ESCALA_CALCULO).move_to(CENTRO_CALCULO)
    for indice in (0, 4, 6, 10, 12):
        formula[indice].set_color(ROJO)
    for indice in HUECOS_P:
        formula[indice].set_color(CLARO)
    return formula


def _vivo(hueco, valor, color):
    numero = DecimalNumber(valor, num_decimal_places=2, color=color)
    return numero.scale(ESCALA_CALCULO).move_to(hueco)


def _ejes_error():
    ejes = Axes(
        x_range=[*RANGO_Q, 0.25], y_range=[*RANGO_ERROR, 0.25],
        x_length=ANCHO_CURVA, y_length=ALTO_CURVA, axis_config=_error.EJES,
    ).move_to(CENTRO_CURVA)
    curva = ejes.plot(_error_total, x_range=[*TRAMO_CURVA, 0.005],
                      color=ROJO)
    curva.set_stroke(width=4)
    rot_x = MathTex(r"q_{\text{gato}}", color=PRIMARIO).scale(0.6)
    rot_x.next_to(ejes.c2p(RANGO_Q[1], RANGO_ERROR[0]), DOWN, buff=0.2)
    rot_y = MathTex(r"\text{error}", color=ROJO).scale(0.6)
    rot_y.next_to(ejes.c2p(RANGO_Q[0], RANGO_ERROR[1]), LEFT, buff=0.15)
    return VGroup(ejes, rot_x, rot_y), curva


def _seguir_barra(k, q):
    def actualizar(m):
        alto = _alto(_probabilidades(q.get_value())[k])
        m.stretch_to_fit_height(alto)
        m.move_to([_x(k, 1), Y_BASE + alto / 2, 0])

    return actualizar


def _seguir_valor(k, q):
    def actualizar(m):
        prob = _probabilidades(q.get_value())[k]
        m.set_value(prob)
        m.next_to(_tope(k, 1, prob), UP, buff=0.1)

    return actualizar


def construir(scene):
    encabezado = hacer_titulo("Error para clasificación")

    leyenda = _leyenda()
    suelo = Line(
        [X_GRUPOS[0] - 1.05, Y_BASE, 0], [X_GRUPOS[-1] + 1.05, Y_BASE, 0],
        color=SECUNDARIO, stroke_width=2,
    ).set_stroke(opacity=0.55)
    iconos = VGroup(
        _gato().move_to([X_GRUPOS[0], Y_ICONOS, 0]),
        _perro().move_to([X_GRUPOS[1], Y_ICONOS, 0]),
    )

    barras_p = _barras(P, -1, CLARO, OPACIDAD_P)
    valores_p = _valores(P, -1, CLARO)
    letras_p = _letras("p", -1, CLARO)

    q_inicial = _probabilidades(Q_INICIAL)
    barras_q = _barras(q_inicial, 1, PRIMARIO, OPACIDAD_Q)
    valores_q = _valores(q_inicial, 1, PRIMARIO)
    letras_q = _letras("q", 1, PRIMARIO)

    general = MathTex(
        r"\text{error}", "=", r"\sum_i", "p_i", r"\cdot", "L(", "q_i", ")",
    ).scale(0.8).move_to([0, Y_FORMULA, 0])
    general[0].set_color(ROJO)
    general[3].set_color(CLARO)
    general[5].set_color(ROJO)
    general[6].set_color(PRIMARIO)
    general[7].set_color(ROJO)
    caja = SurroundingRectangle(general, buff=0.22, corner_radius=0.12,
                                color=SECUNDARIO, stroke_width=2)

    calculo = _calculo(Q_INICIAL)
    huecos = set(HUECOS_P) | set(HUECOS_Q) | {HUECO_TOTAL - 1, HUECO_TOTAL}
    esqueleto = VGroup(*[
        parte for i, parte in enumerate(calculo) if i not in huecos
    ])
    vivos_q = VGroup(*[
        _vivo(calculo[i], prob, PRIMARIO)
        for i, prob in zip(HUECOS_Q, q_inicial)
    ])
    total = _vivo(calculo[HUECO_TOTAL], _error_total(Q_INICIAL), ROJO)

    ejes, curva = _ejes_error()
    punto = Dot(ejes[0].c2p(Q_INICIAL, _error_total(Q_INICIAL)), radius=0.09,
                color=ROJO)

    fondo_valle = ejes[0].c2p(P_GATO, _error_total(P_GATO))
    guia = DashedLine(
        ejes[0].c2p(P_GATO, RANGO_ERROR[0]), fondo_valle,
        color=VERDE, stroke_width=2, dash_length=0.08,
    ).set_stroke(opacity=0.8)
    igual = MathTex("q", "=", "p").scale(0.6)
    igual[0].set_color(PRIMARIO)
    igual[2].set_color(CLARO)
    igual.next_to(ejes[0].c2p(P_GATO, RANGO_ERROR[0]), DOWN, buff=0.2)
    minimo = texto("mínimo", 17, color=VERDE)
    minimo.next_to(fondo_valle, UP, buff=0.3)
    empates = VGroup(*[
        DashedLine(
            _tope(k, -1, prob) + LEFT * (ANCHO_BARRA / 2 + 0.08),
            _tope(k, 1, prob) + RIGHT * (ANCHO_BARRA / 2 + 0.08),
            color=VERDE, stroke_width=2.5, dash_length=0.08,
        )
        for k, prob in enumerate(P)
    ])

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(
        Create(suelo),
        LaggedStart(*[FadeIn(i, scale=0.6) for i in iconos], lag_ratio=0.2),
        run_time=0.8,
    )
    scene.play(
        FadeIn(leyenda[0], shift=RIGHT * 0.15),
        LaggedStart(*[GrowFromEdge(b, DOWN) for b in barras_p],
                    lag_ratio=0.2),
        FadeIn(letras_p),
        run_time=1.0,
    )
    scene.play(FadeIn(valores_p, shift=UP * 0.1), run_time=0.5)
    scene.next_slide()

    scene.play(
        FadeIn(leyenda[1], shift=RIGHT * 0.15),
        LaggedStart(*[GrowFromEdge(b, DOWN) for b in barras_q],
                    lag_ratio=0.2),
        FadeIn(letras_q),
        run_time=1.0,
    )
    scene.play(FadeIn(valores_q, shift=UP * 0.1), run_time=0.5)
    scene.next_slide()

    scene.play(
        FadeIn(general, shift=DOWN * 0.1), Create(caja),
        FadeIn(leyenda[2], shift=RIGHT * 0.15),
        run_time=1.0,
    )
    scene.play(FadeIn(esqueleto, shift=UP * 0.1), run_time=0.6)
    for k in range(len(P)):
        scene.play(
            TransformFromCopy(valores_p[k], calculo[HUECOS_P[k]]),
            TransformFromCopy(valores_q[k], vivos_q[k]),
            Indicate(iconos[k], scale_factor=1.15),
            run_time=1.0,
        )
    scene.play(
        FadeIn(VGroup(calculo[HUECO_TOTAL - 1], total), shift=LEFT * 0.1),
        run_time=0.6,
    )
    scene.next_slide()

    scene.play(FadeIn(ejes), run_time=0.6)
    scene.play(Create(curva), run_time=1.2)
    scene.play(FadeIn(punto, scale=0.5), Indicate(total, color=ROJO),
               run_time=0.8)
    scene.next_slide()

    q = ValueTracker(Q_INICIAL)
    for k, barra in enumerate(barras_q):
        barra.add_updater(_seguir_barra(k, q))
    for k, valor in enumerate(valores_q):
        valor.add_updater(_seguir_valor(k, q))
    for k, vivo in enumerate(vivos_q):
        vivo.add_updater(
            lambda m, k=k: m.set_value(_probabilidades(q.get_value())[k]),
        )
    total.add_updater(lambda m: m.set_value(_error_total(q.get_value())))
    punto.add_updater(lambda m: m.move_to(
        ejes[0].c2p(q.get_value(), _error_total(q.get_value())),
    ))
    scene.play(q.animate.set_value(Q_EXCESO), run_time=2.2)
    scene.play(q.animate.set_value(P_GATO), run_time=2.0)
    for m in (*barras_q, *valores_q, *vivos_q, total, punto):
        m.clear_updaters()

    scene.play(
        Create(guia), FadeIn(igual, shift=UP * 0.1),
        punto.animate.set_color(VERDE),
        LaggedStart(*[Create(e) for e in empates], lag_ratio=0.2),
        run_time=0.9,
    )
    scene.play(
        FadeIn(minimo, shift=DOWN * 0.1),
        total.animate.set_color(VERDE),
        run_time=0.6,
    )
    scene.next_slide()
