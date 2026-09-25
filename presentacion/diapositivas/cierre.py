import numpy as np
from manim import (
    DOWN,
    RIGHT,
    UP,
    AnimationGroup,
    Arrow,
    Circle,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Group,
    GrowFromCenter,
    DEGREES,
    LaggedStart,
    Line,
    MathTex,
    MoveAlongPath,
    RoundedRectangle,
    ShowPassingFlash,
    Succession,
    VGroup,
    VMobject,
    there_and_back,
)

from componentes import imagen, texto
from estilo import (
    AMBAR,
    BLANCO,
    CLARO,
    FONT_TITULO,
    MORADO,
    PRIMARIO,
    SECUNDARIO,
    VERDE,
)

RELLENO_NODO = "#04121a"

Y_GRACIAS = 3.18
TAM_GRACIAS = 48
ANCHO_MAX_GRACIAS = 10.4

Y_RED = 0.55
TAM_CAPAS = (4, 6, 6, 3)
X_CAPAS = (-6.05, -4.35, -2.65, -0.95)
COLOR_CAPAS = (PRIMARIO, SECUNDARIO, SECUNDARIO, AMBAR)
RADIO_NODO = 0.15
PASO_NODO = 0.58
OPACIDAD_ARISTA = 0.26

X_JUNTA = 0.55

X_QR = 4.25
LADO_TARJETA = 2.9
MARGEN_QR = 0.3
Y_PIE_QR = -1.35

Y_TIRA = -2.55
ANCHO_PAPEL, ALTO_PAPEL = 2.6, 1.30
BUFF_PAPEL = 0.32
A_DIBUJO, H_DIBUJO = 0.92, 0.33
T_BOLA = 0.22
T_REBOTE = 0.74
MARGEN_HUECO = 0.05

GIRO_RECTA = 14 * DEGREES
ESTIRON_UMBRAL = 1.3
GIRO_ERROR = 8 * DEGREES

ALTURA_GRADIENTE = 0.16

Y_FIRMA = -3.62


def _red():
    capas = []
    for x, n, color in zip(X_CAPAS, TAM_CAPAS, COLOR_CAPAS):
        alto = (n - 1) * PASO_NODO
        capa = []
        for k in range(n):
            centro = np.array([x, Y_RED + alto / 2 - k * PASO_NODO, 0.0])
            nodo = Circle(radius=RADIO_NODO, color=color, stroke_width=2.6)
            capa.append(nodo.set_fill(RELLENO_NODO, opacity=1.0).move_to(centro))
        capas.append(capa)

    tramos = []
    for izquierda, derecha in zip(capas, capas[1:]):
        tramo = VGroup()
        for a in izquierda:
            for b in derecha:
                paso = b.get_center() - a.get_center()
                paso = paso / np.linalg.norm(paso)
                tramo.add(Line(
                    a.get_center() + paso * RADIO_NODO,
                    b.get_center() - paso * RADIO_NODO,
                    color=SECUNDARIO, stroke_width=1.1,
                ).set_stroke(opacity=OPACIDAD_ARISTA))
        tramos.append(tramo)
    return capas, tramos


def _desemboque(salidas):
    junta_centro = np.array([X_JUNTA, Y_RED, 0.0])
    junta = Dot(junta_centro, radius=0.08, color=PRIMARIO)

    convergencias = VGroup()
    for nodo in salidas:
        paso = junta_centro - nodo.get_center()
        paso = paso / np.linalg.norm(paso)
        convergencias.add(Line(
            nodo.get_center() + paso * RADIO_NODO,
            junta_centro - paso * 0.08,
            color=AMBAR, stroke_width=2.0,
        ).set_stroke(opacity=0.7))

    borde_qr = X_QR - LADO_TARJETA / 2
    tramo_final = (junta_centro + RIGHT * 0.1,
                   np.array([borde_qr - 0.12, Y_RED, 0.0]))
    salida = Arrow(
        *tramo_final, color=PRIMARIO, stroke_width=4, buff=0.0,
        max_tip_length_to_length_ratio=0.11,
    )
    riel = Line(*tramo_final)
    return junta, convergencias, salida, riel


def _oleada(tramo, nodos, color, reverso=False):
    rieles = [
        arista.copy().reverse_points() if reverso else arista.copy()
        for arista in tramo
    ]
    return AnimationGroup(
        AnimationGroup(*[
            ShowPassingFlash(
                riel.set_stroke(color, 3.5, 1.0), time_width=0.55,
            )
            for riel in rieles
        ]),
        AnimationGroup(*[
            nodo.animate(rate_func=there_and_back).set_stroke(color, 5.5)
            for nodo in nodos
        ]),
        lag_ratio=0.6,
    )


def _hacia_adelante(capas, tramos, junta, convergencias, riel, tarjeta):
    pasos = [
        _oleada(tramo, capas[i + 1], PRIMARIO)
        for i, tramo in enumerate(tramos)
    ]
    pasos.append(AnimationGroup(
        AnimationGroup(*[
            ShowPassingFlash(c.copy().set_stroke(AMBAR, 3.5, 1.0),
                             time_width=0.55)
            for c in convergencias
        ]),
        junta.animate(rate_func=there_and_back).scale(1.7),
        lag_ratio=0.6,
    ))
    pasos.append(AnimationGroup(
        ShowPassingFlash(riel.copy().set_stroke(PRIMARIO, 5.0, 1.0),
                         time_width=0.4),
        tarjeta.animate(rate_func=there_and_back).scale(1.045),
        lag_ratio=0.55,
    ))
    return LaggedStart(*pasos, lag_ratio=0.42)


def _hacia_atras(capas, tramos):
    return LaggedStart(*[
        _oleada(tramo, capas[i], MORADO, reverso=True)
        for i, tramo in reversed(list(enumerate(tramos)))
    ], lag_ratio=0.42)


def _gradientes(tramos):
    rotulos = VGroup()
    for tramo in tramos:
        cumbre = max((arista.get_center() for arista in tramo),
                     key=lambda punto: punto[1])
        rotulos.add(
            MathTex(r"-\nabla w", color=MORADO).scale(0.58)
            .next_to(cumbre, UP, buff=ALTURA_GRADIENTE)
        )
    return rotulos


def _boceto_recta():
    puntos = []
    for k, desvio in enumerate((0.10, -0.12, 0.08, -0.09, 0.11)):
        t = -1 + 2 * k / 4
        puntos.append(Dot([t * A_DIBUJO, t * H_DIBUJO + desvio, 0],
                          radius=0.045, color=SECUNDARIO))
    recta = Line([-A_DIBUJO, -H_DIBUJO, 0], [A_DIBUJO, H_DIBUJO, 0],
                 color=PRIMARIO, stroke_width=2.8)
    return VGroup(*puntos, recta)


def _boceto_umbral():
    eje = Line([-A_DIBUJO, -H_DIBUJO, 0], [A_DIBUJO, -H_DIBUJO, 0],
               color=SECUNDARIO, stroke_width=1.2).set_stroke(opacity=0.5)
    codo = VMobject(color=VERDE, stroke_width=2.8)
    codo.set_points_as_corners([
        [-A_DIBUJO, -H_DIBUJO, 0], [-0.04, -H_DIBUJO, 0],
        [A_DIBUJO * 0.88, H_DIBUJO, 0],
    ])
    return VGroup(eje, codo)


def _hueco(objetivo, prediccion):
    return DashedLine(
        objetivo + DOWN * MARGEN_HUECO, prediccion + UP * MARGEN_HUECO,
        color=AMBAR, stroke_width=2.4, dash_length=0.05,
    )


def _boceto_error():
    izq = np.array([-A_DIBUJO, -H_DIBUJO * 0.6, 0])
    der = np.array([A_DIBUJO, H_DIBUJO * 0.9, 0])
    modelo = Line(izq, der, color=SECUNDARIO,
                  stroke_width=1.6).set_stroke(opacity=0.5)

    prediccion = modelo.point_from_proportion(0.6)
    objetivo = prediccion + UP * H_DIBUJO * 1.15
    return VGroup(
        modelo,
        Dot(prediccion, radius=0.06, color=AMBAR),
        Dot(objetivo, radius=0.06, color=VERDE),
        _hueco(objetivo, prediccion),
    )


def _bajada(valle):
    return valle.copy().pointwise_become_partial(valle, T_BOLA, T_REBOTE)


def _boceto_descenso():
    xs = np.linspace(-A_DIBUJO, A_DIBUJO, 40)
    valle = VMobject(color=SECUNDARIO, stroke_width=1.8)
    valle.set_points_smoothly([
        [x, -H_DIBUJO + 2 * H_DIBUJO * (x / A_DIBUJO) ** 2, 0] for x in xs
    ])
    valle.set_stroke(opacity=0.55)

    bola = Dot(_bajada(valle).get_start(), radius=0.075, color=MORADO)
    rumbo = Arrow(
        bola.get_center() + np.array([0.12, -0.02, 0]),
        bola.get_center() + np.array([0.42, -0.20, 0]),
        color=MORADO, stroke_width=2.4, buff=0.0,
        max_tip_length_to_length_ratio=0.4,
    ).set_stroke(opacity=0.8)
    return VGroup(valle, bola, rumbo)


def _vive_recta(boceto):
    *puntos, recta = boceto
    return AnimationGroup(
        recta.animate(rate_func=there_and_back).rotate(
            GIRO_RECTA, about_point=recta.get_center()),
        LaggedStart(*[
            punto.animate(rate_func=there_and_back).scale(2.0)
            for punto in puntos
        ], lag_ratio=0.18),
    )


def _vive_umbral(boceto):
    _, codo = boceto
    return Succession(
        ShowPassingFlash(
            codo.copy().set_stroke(VERDE, 5.0, 1.0), time_width=0.45),
        codo.animate(rate_func=there_and_back).stretch(
            ESTIRON_UMBRAL, dim=1, about_point=codo.get_start()),
    )


def _vive_error(boceto):
    modelo, prediccion, objetivo, hueco = boceto
    hueco.add_updater(lambda m: m.become(
        _hueco(objetivo.get_center(), prediccion.get_center()),
    ))
    pivote = modelo.get_start()
    return AnimationGroup(
        modelo.animate(rate_func=there_and_back).rotate(
            GIRO_ERROR, about_point=pivote),
        prediccion.animate(rate_func=there_and_back).rotate(
            GIRO_ERROR, about_point=pivote),
        objetivo.animate(rate_func=there_and_back).scale(1.4),
    )


def _vive_descenso(boceto):
    valle, bola, rumbo = boceto
    return AnimationGroup(
        MoveAlongPath(bola, _bajada(valle), rate_func=there_and_back),
        rumbo.animate(rate_func=there_and_back).set_opacity(0.0),
    )


REPASO = (
    (_boceto_recta, _vive_recta),
    (_boceto_umbral, _vive_umbral),
    (_boceto_error, _vive_error),
    (_boceto_descenso, _vive_descenso),
)


def _dibujarse(boceto, lag=0.3):
    return LaggedStart(*[
        GrowFromCenter(pieza) if isinstance(pieza, Dot) else Create(pieza)
        for pieza in boceto
    ], lag_ratio=lag)


def _papel(dibujar):
    fondo = RoundedRectangle(
        width=ANCHO_PAPEL, height=ALTO_PAPEL, corner_radius=0.14,
        stroke_color=SECUNDARIO, stroke_width=1.6,
    ).set_fill(CLARO, opacity=0.03)
    fondo.set_stroke(opacity=0.3)
    return VGroup(fondo, dibujar().move_to(fondo.get_center()))


def construir(scene):
    gracias = VGroup(
        texto("MUCHAS", TAM_GRACIAS, color=CLARO, font=FONT_TITULO),
        texto("GRACIAS", TAM_GRACIAS, color=PRIMARIO, font=FONT_TITULO),
    ).arrange(RIGHT, buff=0.5)
    if gracias.width > ANCHO_MAX_GRACIAS:
        gracias.scale(ANCHO_MAX_GRACIAS / gracias.width)
    gracias.move_to([0, Y_GRACIAS, 0])

    capas, tramos = _red()

    papel_qr = RoundedRectangle(
        width=LADO_TARJETA, height=LADO_TARJETA, corner_radius=0.2,
        stroke_color=PRIMARIO, stroke_width=3,
    ).set_fill(BLANCO, opacity=1.0).move_to([X_QR, Y_RED, 0])
    codigo = imagen("qr_formulario.png")
    codigo.scale_to_fit_width(LADO_TARJETA - MARGEN_QR * 2)
    codigo.move_to(papel_qr.get_center())
    tarjeta = Group(papel_qr, codigo)

    junta, convergencias, salida, riel = _desemboque(capas[-1])

    pie_qr = VGroup(
        texto("Escanea el código", 15, color=CLARO),
        texto("Asistencia y recursos", 14, color=SECUNDARIO),
    ).arrange(DOWN, buff=0.12).move_to([X_QR, Y_PIE_QR, 0])

    tira = VGroup(*[_papel(dibujar) for dibujar, _ in REPASO])
    tira.arrange(RIGHT, buff=BUFF_PAPEL).move_to([0, Y_TIRA, 0])

    gradientes = _gradientes(tramos)

    firma = texto("Semillero de Data Science e IA  ·  Aperture", 15,
                  color=SECUNDARIO).move_to([0, Y_FIRMA, 0])

    scene.play(FadeIn(gracias[0], shift=UP * 0.18), run_time=0.5)
    scene.play(FadeIn(gracias[1], shift=UP * 0.18), run_time=0.5)

    scene.play(
        LaggedStart(*[
            AnimationGroup(*[GrowFromCenter(n) for n in capa])
            for capa in capas
        ], lag_ratio=0.35),
        run_time=1.0,
    )
    scene.play(
        LaggedStart(*[Create(t) for t in tramos], lag_ratio=0.35),
        run_time=1.1,
    )

    scene.play(
        LaggedStart(*[
            _oleada(tramo, capas[i + 1], PRIMARIO)
            for i, tramo in enumerate(tramos)
        ], lag_ratio=0.42),
        run_time=1.6,
    )
    scene.play(
        LaggedStart(*[Create(c) for c in convergencias], lag_ratio=0.15),
        GrowFromCenter(junta), run_time=0.6,
    )
    scene.play(Create(salida), run_time=0.45)
    scene.play(
        LaggedStart(GrowFromCenter(papel_qr), FadeIn(codigo, scale=0.85),
                    lag_ratio=0.55),
        run_time=0.95,
    )
    scene.play(FadeIn(pie_qr, shift=UP * 0.1), run_time=0.4)

    scene.play(
        LaggedStart(*[
            Succession(FadeIn(fondo, shift=UP * 0.18), _dibujarse(boceto))
            for fondo, boceto in tira
        ], lag_ratio=0.42),
        run_time=2.8,
    )
    scene.play(FadeIn(firma, shift=UP * 0.1), run_time=0.4)

    al_reves = list(gradientes)[::-1]
    if hasattr(scene, "_base_slide_config"):
        scene._base_slide_config.auto_next = True
    scene.next_slide(loop=True, indicador=False)
    scene.play(
        _hacia_adelante(capas, tramos, junta, convergencias, riel, tarjeta),
        LaggedStart(*[
            vivir(papel[1]) for (_, vivir), papel in zip(REPASO, tira)
        ], lag_ratio=0.22),
        run_time=2.4,
    )
    scene.play(
        _hacia_atras(capas, tramos),
        LaggedStart(*[FadeIn(g, shift=DOWN * 0.14) for g in al_reves],
                    lag_ratio=0.45),
        run_time=1.8,
    )
    scene.play(
        LaggedStart(*[FadeOut(g, shift=UP * 0.14) for g in al_reves],
                    lag_ratio=0.2),
        run_time=0.6,
    )
    scene.next_slide(indicador=False)
