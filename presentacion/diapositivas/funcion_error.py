import numpy as np
from manim import (
    DOWN,
    LEFT,
    UP,
    Create,
    DecimalNumber,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    ManimColor,
    MathTex,
    Rectangle,
    RoundedRectangle,
    Transform,
    ValueTracker,
    VGroup,
    always_redraw,
    interpolate_color,
    linear,
    smooth,
)

from componentes import texto
from componentes import titulo as hacer_titulo
from estilo import CLARO, FONDO, PRIMARIO, ROJO, SECUNDARIO, VERDE

from . import _error

CENTRO_GRAFICA = [-2.5, -0.4, 0]
ANCHO_GRAFICA = 6.4
ALTO_GRAFICA = 3.9
RADIO_PUNTO = 0.085

CENTRO_PANEL = np.array([3.95, -0.4, 0])
ANCHO_PANEL = 4.2
ALTO_PANEL = 3.9
Y_CABECERA = 1.2
Y_RAYA = 0.88
X_LECTURA = 3.2
Y_FORMULA = 0.2
Y_VALOR = -0.65
ANCLA_ESTADO = np.array([2.2, -1.8, 0])

X_TERMO = 5.3
ANCHO_TERMO = 0.55
ALTO_TERMO = 2.3
Y_PIE_TERMO = -2.0

INICIO_BARRIDO = 0.1
FIN_BARRIDO = 4.0
Y_TOPE_HAZ = 4.0
DURACION_BARRIDO = 3.2
RAMPA = 0.25
ANCHO_DESTELLO = 0.12
BRILLOS = ((0.7, 0.05), (0.36, 0.08), (0.14, 0.12))


def _detectado(t, x):
    return smooth(float(np.clip((t - x) / RAMPA, 0.0, 1.0)))


def _destello(t, x):
    return float(np.exp(-(((t - x) / ANCHO_DESTELLO) ** 2)))


def _cuadrados(ys, funcion):
    return (ys - funcion(np.array(_error.XS))) ** 2


def _acumulado(t, cuadrados):
    return sum(
        _detectado(t, x) * c for x, c in zip(_error.XS, cuadrados)
    ) / len(_error.XS)


def _haz(ejes):
    abajo = ejes.c2p(0, 0)[1]
    arriba = ejes.c2p(0, Y_TOPE_HAZ)[1]
    brillos = VGroup(*[
        Rectangle(
            width=ancho, height=arriba - abajo, stroke_width=0,
            fill_color=ROJO, fill_opacity=opacidad,
        ).move_to([0, (arriba + abajo) / 2, 0])
        for ancho, opacidad in BRILLOS
    ])
    linea = Line([0, abajo, 0], [0, arriba, 0], color=ROJO, stroke_width=2.5)
    marco = RoundedRectangle(
        width=0.52, height=0.42, corner_radius=0.1,
        stroke_color=ROJO, stroke_width=2.5,
    ).set_fill(FONDO, opacity=1.0)
    letra = MathTex("L", color=ROJO).scale(0.6).move_to(marco.get_center())
    cabeza = VGroup(marco, letra).next_to(linea, UP, buff=0)
    return VGroup(brillos, linea, cabeza)


def _panel():
    marco = RoundedRectangle(
        width=ANCHO_PANEL, height=ALTO_PANEL, corner_radius=0.2,
        stroke_color=SECUNDARIO, stroke_width=2,
    ).set_stroke(opacity=0.55).set_fill(FONDO, opacity=0.9)
    marco.move_to(CENTRO_PANEL)
    cabecera = texto("función de error", 18, color=SECUNDARIO)
    cabecera.move_to([CENTRO_PANEL[0], Y_CABECERA, 0])
    raya = Line(
        [marco.get_left()[0] + 0.25, Y_RAYA, 0],
        [marco.get_right()[0] - 0.25, Y_RAYA, 0],
        color=SECUNDARIO, stroke_width=1.5,
    ).set_stroke(opacity=0.4)
    formula = MathTex("L", "(", r"\hat{y}", ",", "y", ")").scale(0.95)
    formula.set_color(CLARO)
    formula[0].set_color(ROJO)
    formula[2].set_color(PRIMARIO)
    formula.move_to([X_LECTURA, Y_FORMULA, 0])
    return VGroup(marco, cabecera, raya, formula)


def _estado(mensaje, color):
    punto = Dot(radius=0.07, color=color)
    rotulo = texto(mensaje, 16, color=SECUNDARIO)
    return VGroup(punto, rotulo).arrange(buff=0.16).move_to(
        ANCLA_ESTADO, aligned_edge=LEFT,
    )


def _cambiar(viejo, nuevo):
    viejo.clear_updaters()
    return [FadeOut(viejo, shift=UP * 0.12), FadeIn(nuevo, shift=UP * 0.12)]


def _escaneando(barrido):
    estado = _estado("escaneando", ROJO)
    estado[0].add_updater(lambda m: m.set_opacity(
        0.3 + 0.7 * abs(np.cos(4 * barrido.get_value())),
    ))
    return estado


def _seguir_distancias(distancias, barrido):
    for linea, x in zip(distancias, _error.XS):
        linea.add_updater(lambda m, x=x: m.set_stroke(
            opacity=_detectado(barrido.get_value(), x),
            width=4 + 3 * _destello(barrido.get_value(), x),
        ), call_updater=True)


def _seguir_puntos(puntos, barrido):
    claro, rojo = ManimColor(CLARO), ManimColor(ROJO)
    for punto, x in zip(puntos, _error.XS):
        def latir(m, x=x):
            brillo = _destello(barrido.get_value(), x)
            m.set_width(2 * RADIO_PUNTO * (1 + 0.9 * brillo))
            m.set_color(interpolate_color(claro, rojo, brillo))
        punto.add_updater(latir)


def _escanear(scene, barrido, haz, estado, valor):
    haz.update()
    activo = _escaneando(barrido)
    scene.play(FadeIn(haz), *_cambiar(estado, activo), run_time=0.5)
    scene.play(barrido.animate(rate_func=linear).set_value(FIN_BARRIDO),
               run_time=DURACION_BARRIDO)
    listo = _estado("listo", VERDE)
    scene.play(*_cambiar(activo, listo), FadeOut(haz),
               Indicate(valor, color=ROJO), run_time=0.7)
    return listo


def construir(scene):
    encabezado = hacer_titulo("¿Cómo calificamos el modelo?")
    ys = _error.datos()
    mala = _error.ajuste_malo(ys)

    ejes = _error.ejes_datos(CENTRO_GRAFICA, ANCHO_GRAFICA, ALTO_GRAFICA)
    puntos, curva, dist_mala = _error.dibujo_datos(
        ejes, ys, mala, "distancias", radio=RADIO_PUNTO,
    )
    _, curva_buena, dist_buena = _error.dibujo_datos(
        ejes, ys, _error.real, "distancias", radio=RADIO_PUNTO,
    )
    puntos.set_z_index(2)

    barrido = ValueTracker(INICIO_BARRIDO)
    lectura = {"cuadrados": _cuadrados(ys, mala)}
    tope = _acumulado(FIN_BARRIDO, lectura["cuadrados"])

    def error_actual():
        return _acumulado(barrido.get_value(), lectura["cuadrados"])

    haz = _haz(ejes).set_z_index(1)
    haz.add_updater(lambda m: m.set_x(ejes.c2p(barrido.get_value(), 0)[0]))

    panel = _panel()
    valor = DecimalNumber(0, num_decimal_places=2, font_size=64, color=ROJO)
    valor.move_to([X_LECTURA, Y_VALOR, 0])
    valor.add_updater(lambda m: m.set_value(error_actual()))
    tubo = _error.tubo(X_TERMO, Y_PIE_TERMO, ANCHO_TERMO, ALTO_TERMO)
    rotulo_termo = texto("error", 16, color=ROJO).next_to(tubo, UP, buff=0.18)
    nivel = always_redraw(lambda: _error.liquido(
        X_TERMO, Y_PIE_TERMO, ANCHO_TERMO, ALTO_TERMO,
        _error.LLENO * error_actual() / tope,
    ))
    estado = _estado("en espera", SECUNDARIO)

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(Create(ejes), run_time=0.7)
    scene.play(
        LaggedStart(*[FadeIn(p, scale=0.5) for p in puntos], lag_ratio=0.08),
        run_time=0.9,
    )
    scene.play(Create(curva), run_time=0.8)
    scene.play(
        FadeIn(panel), FadeIn(valor), FadeIn(tubo), FadeIn(rotulo_termo),
        FadeIn(estado),
        run_time=0.8,
    )
    scene.add(nivel)
    scene.next_slide()

    _seguir_puntos(puntos, barrido)
    _seguir_distancias(dist_mala, barrido)
    scene.add(dist_mala)
    estado = _escanear(scene, barrido, haz, estado, valor)
    scene.next_slide()

    espera = _estado("en espera", SECUNDARIO)
    scene.play(
        barrido.animate(rate_func=smooth).set_value(INICIO_BARRIDO),
        *_cambiar(estado, espera),
        run_time=0.9,
    )
    dist_mala.clear_updaters()
    scene.remove(dist_mala)
    lectura["cuadrados"] = _cuadrados(ys, _error.real)
    _seguir_distancias(dist_buena, barrido)
    scene.add(dist_buena)
    scene.play(Transform(curva, curva_buena), run_time=1.2)
    _escanear(scene, barrido, haz, espera, valor)
    scene.next_slide()
