import numpy as np
from manim import (
    DOWN,
    RIGHT,
    UP,
    Arrow,
    Circle,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    FadeTransform,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    MoveAlongPath,
    ReplacementTransform,
    RoundedRectangle,
    VGroup,
    linear,
)

from componentes import texto
from componentes import titulo as hacer_titulo
from estilo import AMBAR, CLARO, FONDO, MORADO, PRIMARIO, SECUNDARIO, VERDE

X_ENTRADAS = -4.3
X_CUERPO = 0.0
X_SALIDA = 3.9
Y_EJE = 0.4
RADIO_CUERPO = 0.85
RADIO_NODO = 0.32
Y_ROTULOS = -1.75
Y_FORMULA = -2.7

FILAS = ((1.7, "x_1", "w_1"), (0.4, "x_2", "w_2"), (-0.9, "x_n", "w_n"))

EJEMPLO_X = (2, 1, 3)
EJEMPLO_W = (3, -2, 1)
EJEMPLO_B = 1
POS_ROTULO_EJEMPLO = [-5.55, 2.5, 0]


def _m(tex, color, escala=0.6):
    return MathTex(tex, color=color).scale(escala)


def _nodo(centro, radio, color):
    nodo = Circle(radius=radio, color=color, stroke_width=3.5)
    return nodo.set_fill(FONDO, opacity=1.0).move_to(centro)


def _entradas():
    centro = np.array([X_CUERPO, Y_EJE, 0.0])
    nodos, etiquetas_x, aristas, pesos = [], [], [], []
    for y, nombre_x, nombre_w in FILAS:
        nodo = _nodo([X_ENTRADAS, y, 0], RADIO_NODO, VERDE)
        nodos.append(nodo)
        etiquetas_x.append(_m(nombre_x, CLARO, 0.55).move_to(nodo.get_center()))

        direccion = centro - nodo.get_center()
        direccion = direccion / np.linalg.norm(direccion)
        arista = Line(
            nodo.get_center() + direccion * RADIO_NODO,
            centro - direccion * RADIO_CUERPO,
            color=SECUNDARIO, stroke_width=2.5,
        )
        aristas.append(arista)
        pesos.append(_m(nombre_w, VERDE, 0.5).move_to(
            arista.point_from_proportion(0.42) + UP * 0.26
        ))
    puntos_suspensivos = _m(r"\vdots", SECUNDARIO, 0.6)
    puntos_suspensivos.move_to([X_ENTRADAS, -0.28, 0])
    return nodos, etiquetas_x, aristas, pesos, puntos_suspensivos


def _cuerpo():
    centro = np.array([X_CUERPO, Y_EJE, 0.0])
    cuerpo = _nodo(centro, RADIO_CUERPO, PRIMARIO)
    cuerpo.set_stroke(width=4.5)
    sigma = _m(r"\Sigma", CLARO, 1.1).move_to(centro)
    return cuerpo, sigma


def _factor(valor):
    return f"({valor})" if valor < 0 else f"{valor}"


def _suma(valores):
    cuenta = f"{valores[0]}"
    for valor in valores[1:]:
        cuenta += f" - {-valor}" if valor < 0 else f" + {valor}"
    return cuenta


def _rotulo_ejemplo():
    nombre = texto("ejemplo", 17, color=SECUNDARIO)
    borde = RoundedRectangle(
        width=nombre.width + 0.4, height=nombre.height + 0.24,
        corner_radius=0.12, stroke_color=SECUNDARIO, stroke_width=2,
    )
    return VGroup(borde, nombre).move_to(POS_ROTULO_EJEMPLO)


def _rotulo_biologico(nombre, color, x, ancla):
    etiqueta = texto(nombre, 19, color=color)
    etiqueta.move_to([x, Y_ROTULOS, 0])
    guia = DashedLine(
        etiqueta.get_top() + UP * 0.1, ancla,
        color=color, stroke_width=2, stroke_opacity=0.45, dash_length=0.09,
    )
    return etiqueta, guia


def construir(scene):
    encabezado = hacer_titulo("El perceptrón")
    centro = np.array([X_CUERPO, Y_EJE, 0.0])

    nodos, etiquetas_x, aristas, pesos, puntos_suspensivos = _entradas()
    cuerpo, sigma = _cuerpo()

    centro_bias = np.array([X_CUERPO, 2.15, 0.0])
    nodo_bias = _nodo(centro_bias, 0.28, MORADO)
    etiqueta_bias = _m("b", MORADO, 0.55).move_to(centro_bias)
    direccion_bias = centro - centro_bias
    direccion_bias = direccion_bias / np.linalg.norm(direccion_bias)
    arista_bias = Line(
        centro_bias + direccion_bias * 0.28,
        centro - direccion_bias * RADIO_CUERPO,
        color=MORADO, stroke_width=2.5, stroke_opacity=0.9,
    )

    flecha = Arrow(
        centro + RIGHT * RADIO_CUERPO, [X_SALIDA - 0.38, Y_EJE, 0],
        color=AMBAR, stroke_width=4, buff=0.05,
        max_tip_length_to_length_ratio=0.13,
    )
    salida = _nodo([X_SALIDA, Y_EJE, 0], 0.34, AMBAR)
    etiqueta_salida = _m(r"\hat{y}", AMBAR, 0.62).move_to(salida.get_center())

    rot_dendritas, guia_dendritas = _rotulo_biologico(
        "dendritas", VERDE, X_ENTRADAS, [X_ENTRADAS, -0.9 - RADIO_NODO, 0],
    )
    rot_soma, guia_soma = _rotulo_biologico(
        "soma", PRIMARIO, X_CUERPO, [X_CUERPO, Y_EJE - RADIO_CUERPO, 0],
    )
    rot_axon, guia_axon = _rotulo_biologico(
        "axón", AMBAR, X_SALIDA, [X_SALIDA, Y_EJE - 0.34, 0],
    )

    suma = MathTex(
        r"\hat{y}", "=", "x_1 w_1", "+", "x_2 w_2", "+", r"\cdots", "+",
        "x_n w_n", "+", "b",
    ).scale(0.85).move_to([0, Y_FORMULA, 0])
    suma[0].set_color(AMBAR)
    suma[10].set_color(MORADO)

    compacta = MathTex(
        r"\hat{y}", "=", r"\sum_i x_i w_i", "+", "b",
    ).scale(0.95).move_to([0, Y_FORMULA, 0])
    compacta[0].set_color(AMBAR)
    compacta[2].set_color(CLARO)
    compacta[4].set_color(MORADO)

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(
        LaggedStart(*[GrowFromCenter(VGroup(n, e))
                      for n, e in zip(nodos, etiquetas_x)], lag_ratio=0.2),
        FadeIn(puntos_suspensivos),
        run_time=0.9,
    )
    scene.next_slide()

    scene.play(
        LaggedStart(*[Create(a) for a in aristas], lag_ratio=0.2),
        run_time=0.9,
    )
    scene.play(
        LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in pesos], lag_ratio=0.2),
        run_time=0.7,
    )
    scene.play(GrowFromCenter(cuerpo), FadeIn(sigma), run_time=0.7)
    scene.next_slide()

    scene.play(
        GrowFromCenter(VGroup(nodo_bias, etiqueta_bias)), Create(arista_bias),
        run_time=0.6,
    )
    scene.play(Create(flecha), run_time=0.5)
    scene.play(GrowFromCenter(VGroup(salida, etiqueta_salida)), run_time=0.5)
    scene.next_slide()

    scene.play(
        LaggedStart(
            *[FadeIn(r) for r in (rot_dendritas, rot_soma, rot_axon)],
            *[Create(g) for g in (guia_dendritas, guia_soma, guia_axon)],
            lag_ratio=0.12,
        ),
        run_time=1.1,
    )
    scene.next_slide()

    scene.play(FadeIn(VGroup(suma[0], suma[1])), run_time=0.4)

    for arista, peso, trozos in zip(aristas, pesos, ([2], [3, 4], [5, 6, 7, 8])):
        pulso = Dot(color=VERDE, radius=0.07).move_to(arista.get_start())
        scene.add(pulso)
        scene.play(
            Indicate(peso, color=CLARO, scale_factor=1.35),
            MoveAlongPath(pulso, arista), run_time=0.55, rate_func=linear,
        )
        scene.play(
            Indicate(cuerpo, color=PRIMARIO, scale_factor=1.06),
            FadeOut(pulso, scale=0.2),
            FadeIn(VGroup(*[suma[t] for t in trozos]), shift=UP * 0.12),
            run_time=0.5,
        )

    pulso_bias = Dot(color=MORADO, radius=0.07).move_to(arista_bias.get_start())
    scene.add(pulso_bias)
    scene.play(MoveAlongPath(pulso_bias, arista_bias), run_time=0.45,
               rate_func=linear)
    scene.play(
        Indicate(cuerpo, color=PRIMARIO, scale_factor=1.06),
        FadeOut(pulso_bias, scale=0.2),
        FadeIn(VGroup(suma[9], suma[10]), shift=UP * 0.12),
        run_time=0.5,
    )

    pulso_salida = Dot(color=AMBAR, radius=0.07).move_to(flecha.get_start())
    scene.add(pulso_salida)
    scene.play(MoveAlongPath(pulso_salida, flecha), run_time=0.5,
               rate_func=linear)
    scene.play(
        FadeOut(pulso_salida, scale=0.2),
        Indicate(VGroup(salida, etiqueta_salida), color=AMBAR),
        run_time=0.45,
    )
    scene.next_slide()

    scene.play(
        Indicate(sigma, color=PRIMARIO, scale_factor=1.4),
        ReplacementTransform(suma[0], compacta[0]),
        ReplacementTransform(suma[1], compacta[1]),
        ReplacementTransform(VGroup(*suma[2:9]), compacta[2]),
        ReplacementTransform(suma[9], compacta[3]),
        ReplacementTransform(suma[10], compacta[4]),
        run_time=1.3,
    )
    scene.wait(0.4)
    scene.next_slide()

    _ejemplo(
        scene, nodos, etiquetas_x, aristas, pesos, cuerpo, etiqueta_bias,
        arista_bias, flecha, salida, etiqueta_salida, compacta,
        VGroup(
            rot_dendritas, rot_soma, rot_axon,
            guia_dendritas, guia_soma, guia_axon, puntos_suspensivos,
        ),
    )


def _ejemplo(scene, nodos, etiquetas_x, aristas, pesos, cuerpo, etiqueta_bias,
             arista_bias, flecha, salida, etiqueta_salida, compacta, sobrantes):
    productos = [x * w for x, w in zip(EJEMPLO_X, EJEMPLO_W)]
    resultado = sum(productos) + EJEMPLO_B

    numeros_x = [
        _m(f"{x}", CLARO, 0.6).move_to(nodo.get_center())
        for nodo, x in zip(nodos, EJEMPLO_X)
    ]
    numeros_w = [
        _m(f"{w}", VERDE, 0.55).move_to(peso.get_center())
        for peso, w in zip(pesos, EJEMPLO_W)
    ]
    numero_b = _m(f"{EJEMPLO_B}", MORADO, 0.55)
    numero_b.move_to(etiqueta_bias.get_center())
    numero_salida = _m(f"{resultado}", AMBAR, 0.62)
    numero_salida.move_to(salida.get_center())

    partes, trozos = [r"\hat{y}", "="], []
    for k, (x, w) in enumerate(zip(EJEMPLO_X, EJEMPLO_W)):
        inicio = len(partes)
        partes += (["+"] if k else []) + [f"{x}", r"\cdot", _factor(w)]
        trozos.append(range(inicio, len(partes)))
    sesgo = range(len(partes), len(partes) + 2)
    partes += ["+", _factor(EJEMPLO_B)]
    sumandos = range(len(partes), len(partes) + 2)
    partes += ["=", _suma([*productos, EJEMPLO_B])]
    total = range(len(partes), len(partes) + 2)
    partes += ["=", f"{resultado}"]

    cuenta = MathTex(*partes).scale(0.85).move_to([0, Y_FORMULA, 0])
    cuenta[0].set_color(AMBAR)
    for trozo in trozos:
        cuenta[trozo[-1]].set_color(VERDE)
    cuenta[sesgo[-1]].set_color(MORADO)
    cuenta[total[-1]].set_color(AMBAR)

    def tramo(indices):
        return VGroup(*[cuenta[i] for i in indices])

    scene.play(
        FadeOut(sobrantes),
        FadeIn(_rotulo_ejemplo(), shift=RIGHT * 0.15),
        run_time=0.7,
    )
    scene.play(
        *[FadeTransform(e, n) for e, n in zip(etiquetas_x, numeros_x)],
        *[FadeTransform(p, n) for p, n in zip(pesos, numeros_w)],
        FadeTransform(etiqueta_bias, numero_b),
        run_time=1.0,
    )
    scene.next_slide()

    scene.play(FadeOut(compacta), FadeIn(tramo(range(2))), run_time=0.5)
    for arista, peso, trozo in zip(aristas, numeros_w, trozos):
        pulso = Dot(color=VERDE, radius=0.07).move_to(arista.get_start())
        scene.add(pulso)
        scene.play(
            Indicate(peso, color=VERDE, scale_factor=1.35),
            MoveAlongPath(pulso, arista), run_time=0.55, rate_func=linear,
        )
        scene.play(
            Indicate(cuerpo, color=PRIMARIO, scale_factor=1.06),
            FadeOut(pulso, scale=0.2),
            FadeIn(tramo(trozo), shift=UP * 0.12),
            run_time=0.5,
        )

    pulso_bias = Dot(color=MORADO, radius=0.07).move_to(arista_bias.get_start())
    scene.add(pulso_bias)
    scene.play(MoveAlongPath(pulso_bias, arista_bias), run_time=0.45,
               rate_func=linear)
    scene.play(
        Indicate(cuerpo, color=PRIMARIO, scale_factor=1.06),
        FadeOut(pulso_bias, scale=0.2),
        FadeIn(tramo(sesgo), shift=UP * 0.12),
        run_time=0.5,
    )
    scene.play(FadeIn(tramo(sumandos), shift=RIGHT * 0.12), run_time=0.5)
    scene.play(FadeIn(tramo(total), shift=RIGHT * 0.12), run_time=0.5)

    pulso_salida = Dot(color=AMBAR, radius=0.07).move_to(flecha.get_start())
    scene.add(pulso_salida)
    scene.play(MoveAlongPath(pulso_salida, flecha), run_time=0.5,
               rate_func=linear)
    scene.play(
        FadeOut(pulso_salida, scale=0.2),
        FadeTransform(etiqueta_salida, numero_salida),
        Indicate(salida, color=AMBAR),
        run_time=0.6,
    )
    scene.wait(0.4)
    scene.next_slide()
