import numpy as np
from manim import (
    DOWN,
    PI,
    TAU,
    UP,
    Create,
    Dot,
    Ellipse,
    FadeIn,
    FadeOut,
    Line,
    Star,
    ValueTracker,
    VGroup,
    linear,
)

from componentes import titulo as hacer_titulo
from estilo import AMBAR, CLARO, PRIMARIO, ROJO, VERDE

from . import _error

X_IZQ, X_DER = _error.X_COLUMNAS
RADIO_PUNTA, RADIO_HUECO = 1.55, 0.66
CAMINO_ESTRELLA = 0.8
SEPARACION_INICIAL, SEPARACION_FINAL = 0.5, 0.2
ACERCAMIENTO = 0.3
CAMINOS_ELIPSE = ((1.4, 0.9), (0.95, 0.6))
RADIO_BOLA = 0.13
DURACION_PASEO = 6.0

CLAVES_CUENCO = ((1.0, 2.0), (0.8, 4.2), (3.5, 5.4), (1.2, 4.6))
CLAVES_VALLES = ((0.5, 1.6), (0.9, 3.2), (4.4, 5.5), (1.0, 5.0))


def _figura(mob):
    return mob.set_stroke(PRIMARIO, width=3).set_fill(PRIMARIO, opacity=0.12)


def _vertices_estrella(centro, escala=1.0):
    vertices = []
    for i in range(10):
        radio = RADIO_PUNTA if i % 2 == 0 else RADIO_HUECO
        angulo = PI / 2 + i * TAU / 10
        vertices.append(
            centro + escala * radio * np.array([np.cos(angulo), np.sin(angulo), 0]),
        )
    return vertices


def _sobre_estrella(centro, s):
    vertices = _vertices_estrella(centro, CAMINO_ESTRELLA)
    s = (s % 1.0) * len(vertices)
    i = int(s)
    a, b = vertices[i], vertices[(i + 1) % len(vertices)]
    return a + (b - a) * (s - i)


def _separacion(t):
    avance = min(t / ACERCAMIENTO, 1.0)
    suave = avance * avance * (3 - 2 * avance)
    return SEPARACION_FINAL + (SEPARACION_INICIAL - SEPARACION_FINAL) * (1 - suave)


def _sobre_elipse(centro, camino, angulo):
    ancho, alto = CAMINOS_ELIPSE[camino]
    return centro + np.array([ancho * np.cos(angulo), alto * np.sin(angulo), 0])


def _dentro(punto, vertices):
    x, y = punto[0], punto[1]
    dentro = False
    for a, b in zip(vertices, vertices[1:] + vertices[:1]):
        if (a[1] > y) != (b[1] > y):
            if x < a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1]):
                dentro = not dentro
    return dentro


def _segmento_dentro(a, b, vertices):
    return all(_dentro(a + (b - a) * s, vertices) for s in np.linspace(0, 1, 60))


def _cuerda_encima(funcion, a, b):
    xs = np.linspace(a, b, 80)
    recta = funcion(a) + (funcion(b) - funcion(a)) * (xs - a) / (b - a)
    return bool(np.all(recta >= funcion(xs) - 1e-6))


def _recorrido(claves, t):
    tramos = len(claves) - 1
    i = min(int(t * tramos), tramos - 1)
    local = t * tramos - i
    suave = local * local * (3 - 2 * local)
    a, b = np.array(claves[i]), np.array(claves[i + 1])
    return a + (b - a) * suave


def _cuerda(a, b, color):
    return VGroup(
        Line(a, b, color=color, stroke_width=4),
        Dot(a, radius=0.08, color=CLARO),
        Dot(b, radius=0.08, color=CLARO),
    )


def _cuenco(x):
    return 0.32 * (x - 3) ** 2 + 0.25


def _dos_valles(x):
    u = x - 3
    return 0.1 * (u ** 2 - 4) ** 2 + 0.3 * u + 0.8


def _minimo(funcion, desde, hasta):
    xs = np.linspace(desde, hasta, 2001)
    return float(xs[np.argmin(funcion(xs))])


def _bola(ejes, funcion, x):
    punto = ejes.c2p(x, funcion(x))
    delta = 1e-3
    tangente = ejes.c2p(x + delta, funcion(x + delta)) - ejes.c2p(
        x - delta, funcion(x - delta),
    )
    normal = np.array([-tangente[1], tangente[0], 0.0])
    normal = normal / np.linalg.norm(normal)
    return Dot(punto + normal * RADIO_BOLA, radius=RADIO_BOLA, color=AMBAR)


def construir(scene):
    encabezado = hacer_titulo("Convexidad")
    centro_izq = np.array([X_IZQ, _error.Y_COLUMNA, 0.0])
    centro_der = np.array([X_DER, _error.Y_COLUMNA, 0.0])

    elipse = _figura(Ellipse(width=3.8, height=2.6)).move_to(centro_izq)
    estrella = _figura(Star(
        n=5, outer_radius=RADIO_PUNTA, inner_radius=RADIO_HUECO,
        start_angle=PI / 2,
    )).move_to(centro_der)
    borde_estrella = _vertices_estrella(centro_der)
    paseo = ValueTracker(0.0)

    def cuerda_elipse_en():
        t = paseo.get_value()
        return _cuerda(_sobre_elipse(centro_izq, 0, 2.8 + TAU * t),
                       _sobre_elipse(centro_izq, 1, -0.45 - 0.7 * TAU * t),
                       VERDE)

    def cuerda_estrella_en():
        t = paseo.get_value()
        a = _sobre_estrella(centro_der, t)
        b = _sobre_estrella(centro_der, t + _separacion(t))
        return _cuerda(a, b, VERDE if _segmento_dentro(a, b, borde_estrella)
                       else ROJO)

    cuerda_elipse = cuerda_elipse_en()
    cuerda_estrella = cuerda_estrella_en()

    convexa = _error.etiqueta(True, "convexa", X_IZQ)
    no_convexa = _error.etiqueta(False, "no convexa", X_DER)

    ejes_izq = _error.ejes_columna(X_IZQ)
    ejes_der = _error.ejes_columna(X_DER)
    cuenco = ejes_izq.plot(_cuenco, x_range=[0.4, 5.6, 0.05], color=PRIMARIO)
    valles = ejes_der.plot(_dos_valles, x_range=[0.3, 5.7, 0.05],
                           color=PRIMARIO)
    VGroup(cuenco, valles).set_stroke(width=3.5)
    recorrido = ValueTracker(0.0)

    def cuerda_sobre(ejes, funcion, claves):
        a, b = _recorrido(claves, recorrido.get_value())
        color = VERDE if _cuerda_encima(funcion, a, b) else ROJO
        return _cuerda(ejes.c2p(a, funcion(a)), ejes.c2p(b, funcion(b)), color)

    def cuerda_cuenco_en():
        return cuerda_sobre(ejes_izq, _cuenco, CLAVES_CUENCO)

    def cuerda_valles_en():
        return cuerda_sobre(ejes_der, _dos_valles, CLAVES_VALLES)

    cuerda_cuenco = cuerda_cuenco_en()
    cuerda_valles = cuerda_valles_en()

    fondo_cuenco = _minimo(_cuenco, 0.4, 5.6)
    fondo_falso = _minimo(_dos_valles, 3.5, 5.7)
    fondo_real = _minimo(_dos_valles, 0.3, 3.0)
    x_izq, x_der = ValueTracker(5.3), ValueTracker(5.6)
    bola_izq = _bola(ejes_izq, _cuenco, x_izq.get_value())
    bola_der = _bola(ejes_der, _dos_valles, x_der.get_value())
    mejor = Dot(ejes_der.c2p(fondo_real, _dos_valles(fondo_real)),
                radius=0.09, color=VERDE)

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(elipse), FadeIn(estrella), run_time=0.8)
    scene.play(Create(cuerda_elipse), Create(cuerda_estrella), run_time=1.0)
    cuerda_elipse.add_updater(lambda m: m.become(cuerda_elipse_en()))
    cuerda_estrella.add_updater(lambda m: m.become(cuerda_estrella_en()))
    scene.play(paseo.animate.set_value(1.0), run_time=DURACION_PASEO,
               rate_func=linear)
    cuerda_elipse.clear_updaters()
    cuerda_estrella.clear_updaters()
    scene.play(FadeIn(convexa, shift=UP * 0.1),
               FadeIn(no_convexa, shift=UP * 0.1), run_time=0.6)
    scene.next_slide()

    scene.play(
        FadeOut(VGroup(elipse, estrella, cuerda_elipse, cuerda_estrella)),
        run_time=0.6,
    )
    scene.play(Create(ejes_izq), Create(ejes_der), run_time=0.7)
    scene.play(Create(cuenco), Create(valles), run_time=1.0)
    scene.play(Create(cuerda_cuenco), Create(cuerda_valles), run_time=1.0)
    cuerda_cuenco.add_updater(lambda m: m.become(cuerda_cuenco_en()))
    cuerda_valles.add_updater(lambda m: m.become(cuerda_valles_en()))
    scene.play(recorrido.animate.set_value(1.0), run_time=DURACION_PASEO,
               rate_func=linear)
    cuerda_cuenco.clear_updaters()
    cuerda_valles.clear_updaters()
    scene.next_slide()

    scene.play(FadeOut(cuerda_cuenco), FadeOut(cuerda_valles),
               FadeIn(bola_izq, scale=0.5), FadeIn(bola_der, scale=0.5),
               run_time=0.6)
    bola_izq.add_updater(
        lambda m: m.become(_bola(ejes_izq, _cuenco, x_izq.get_value())),
    )
    bola_der.add_updater(
        lambda m: m.become(_bola(ejes_der, _dos_valles, x_der.get_value())),
    )
    scene.play(
        x_izq.animate.set_value(fondo_cuenco),
        x_der.animate.set_value(fondo_falso),
        run_time=1.8,
    )
    bola_izq.clear_updaters()
    bola_der.clear_updaters()
    scene.play(FadeIn(mejor, scale=0.5), run_time=0.6)
    scene.next_slide()
