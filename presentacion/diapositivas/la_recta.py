"""Diapositiva 7 — Del diagrama a las matemáticas: la recta.

Dos columnas: a la izquierda el modelo escrito, a la derecha lo que ese modelo
dibuja sobre los datos. El álgebra va creciendo y la gráfica va respondiendo.

  1. Una entrada: ``ŷ = w x + b`` es, literalmente, la ecuación de una recta.
     Debajo, la neurona que la calcula; a la derecha, la recta que dibuja.
  2. n entradas y m muestras: la suma se contrae hasta ``Ŷ = X W + b``, con un
     bloque por matriz y su forma debajo.
  3. Más neuronas: dos capas lineales encadenadas, y el álgebra las colapsa en
     ``X W' + b'``. Cambian los parámetros, gira la recta, pero sigue siendo
     una recta.
  4. Los puntos se curvan y ya ninguna recta los ajusta: los residuos en ámbar
     lo dejan ver. Deja el terreno listo para "Falta algo".

Código de color heredado de la 6: entradas en verde, pesos en cian, sesgo en
morado, salida en ámbar.
"""

import numpy as np
from manim import (
    DOWN,
    RIGHT,
    UP,
    Axes,
    Circle,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    ReplacementTransform,
    RoundedRectangle,
    Transform,
    VGroup,
)

from componentes import enmarcar, texto
from componentes import titulo as hacer_titulo
from estilo import AMBAR, CLARO, FONDO, MORADO, PRIMARIO, SECUNDARIO, VERDE

PENDIENTE = 0.5
ORDENADA = 0.75
VERTICE = 2.6        # centro de la parábola, en coordenadas de datos
NIVEL_PLANO = 1.45   # mejor recta posible para la parábola: casi horizontal
X_TRAZO = (0.15, 5.05)   # tramo de x donde se dibujan las rectas

# Columna derecha: lo que el modelo dibuja.
CENTRO_GRAFICA = [3.75, -0.35, 0]

# Columna izquierda: el modelo escrito.
X_MATE = -3.5
ANCHO_MATE = 6.2     # tope para que el álgebra no invada la gráfica

# Bloques de la expresión matricial: una medida por dimensión, así los lados
# que tienen que coincidir (las n de X y de W) coinciden también en pantalla.
UNIDAD_M = 1.3       # m muestras
UNIDAD_N = 0.95      # n entradas
UNIDAD_1 = 0.42      # la única salida

# Neurona de la primera pausa: una entrada, un peso, un sesgo y la salida.
X_NEURONA = (-5.15, -3.5, -1.85)
Y_NEURONA = -1.05
Y_SESGO = -2.05          # el sesgo entra por debajo, como en la 6
RADIO_NEURONA = 0.26
RADIO_CUERPO = 0.44
RADIO_SESGO = 0.18

# Red compacta de la composición: entradas, capa oculta y salida.
X_RED = (-4.85, -3.5, -2.15)
TAMANOS_RED = (2, 3, 1)
Y_RED = 1.85
PASO_RED = 0.52
RADIO_RED = 0.15


def _datos():
    """Los mismos puntos, primero alineados y después curvados."""
    rng = np.random.default_rng(11)
    xs = np.linspace(0.35, 4.85, 11)
    ruido = rng.normal(0, 0.14, xs.size)
    return (xs,
            PENDIENTE * xs + ORDENADA + ruido,
            0.4 * (xs - VERTICE) ** 2 + 0.55 + ruido)


def _ajustar(mob, ancho=ANCHO_MATE):
    """Encoge lo que se salga de la columna izquierda."""
    if mob.width > ancho:
        mob.scale(ancho / mob.width)
    return mob


def _pintar(formula, colores):
    """Colorea tokens sueltos de un ``MathTex`` por su índice."""
    for indice, color in colores:
        formula[indice].set_color(color)
    return formula


# --- Columna izquierda: el modelo escrito ----------------------------------
def _bloque(ancho, alto, etiqueta, color):
    """Rectángulo con el nombre de la matriz dentro: la forma se ve de un vistazo."""
    caja = RoundedRectangle(
        width=ancho, height=alto, corner_radius=0.08,
        stroke_color=color, stroke_width=3,
        fill_color=color, fill_opacity=0.1,
    )
    letra = MathTex(etiqueta, color=color).scale(0.65)
    if letra.width > ancho * 0.7:
        letra.scale(ancho * 0.7 / letra.width)
    return VGroup(caja, letra.move_to(caja))


def _matricial():
    """``Ŷ = X W + b`` dibujado como bloques, con la forma de cada matriz.

    Las formas se cuelgan después de colocar la fila y todas a la misma
    altura: los bloques tienen altos distintos, y si cada etiqueta colgara del
    suyo la fila quedaría en escalera.
    """
    salida = _bloque(UNIDAD_1, UNIDAD_M, r"\hat{Y}", AMBAR)
    entradas = _bloque(UNIDAD_N, UNIDAD_M, "X", VERDE)
    pesos = _bloque(UNIDAD_1, UNIDAD_N, "W", PRIMARIO)
    sesgo = _bloque(UNIDAD_1, UNIDAD_1, "b", MORADO)

    producto = VGroup(entradas, pesos).arrange(RIGHT, buff=0.26)
    fila = VGroup(
        salida,
        MathTex("=", color=SECUNDARIO).scale(0.9),
        producto,
        MathTex("+", color=SECUNDARIO).scale(0.9),
        sesgo,
    ).arrange(RIGHT, buff=0.3)

    formas = VGroup()
    for bloque, forma in ((salida, "m x 1"), (entradas, "m x n"),
                          (pesos, "n x 1"), (sesgo, "1 x 1")):
        etiqueta = texto(forma, 14, color=SECUNDARIO)
        formas.add(etiqueta.next_to(fila, DOWN, buff=0.16).set_x(bloque.get_x()))
    return VGroup(fila, formas)


def _composicion():
    """Las tres líneas del colapso: dos capas lineales caben en una.

    Devuelve también la última línea, que es la que se enmarca y la que la
    diapositiva señala cuando los datos dejan de ser rectos.
    """
    linea1 = _pintar(
        MathTex(r"\hat{Y}", "=", "(", "X", "W_1", "+", "b_1", ")",
                "W_2", "+", "b_2"),
        ((0, AMBAR), (3, VERDE), (4, PRIMARIO), (6, MORADO),
         (8, PRIMARIO), (10, MORADO)),
    )
    linea2 = _pintar(
        MathTex("=", "X", "(", "W_1 W_2", ")", "+", "(", "b_1 W_2 + b_2", ")"),
        ((1, VERDE), (3, PRIMARIO), (7, MORADO)),
    )
    linea3 = _pintar(
        MathTex("=", "X", "W'", "+", "b'"),
        ((1, VERDE), (2, PRIMARIO), (4, MORADO)),
    )

    bloque = VGroup(linea1, linea2, linea3).arrange(DOWN, buff=0.42).scale(0.85)
    # Los "=" de las tres líneas, en la misma vertical.
    for linea in (linea2, linea3):
        linea.shift(
            RIGHT * (linea1[1].get_center()[0] - linea[0].get_center()[0])
        )
    return _ajustar(bloque), linea3


def _nodo(centro, color, radio=RADIO_RED):
    """Círculo relleno del fondo para que las aristas no se vean por debajo."""
    nodo = Circle(radius=radio, color=color, stroke_width=3)
    return nodo.set_fill(FONDO, opacity=1.0).move_to(centro)


def _arista(origen, destino, radio_origen=RADIO_RED, radio_destino=RADIO_RED,
            color=SECUNDARIO, grosor=1.8):
    """Conexión recortada en el borde de los dos nodos que une."""
    direccion = destino - origen
    direccion = direccion / np.linalg.norm(direccion)
    linea = Line(
        origen + direccion * radio_origen, destino - direccion * radio_destino,
        color=color, stroke_width=grosor,
    )
    return linea.set_stroke(opacity=0.6)


def _neurona_simple():
    """La ecuación de arriba, dibujada: entrada por un peso, más el sesgo."""
    entrada, cuerpo, salida = [
        np.array([x, Y_NEURONA, 0.0]) for x in X_NEURONA
    ]
    sesgo = np.array([X_NEURONA[1], Y_SESGO, 0.0])

    aristas = VGroup(
        _arista(entrada, cuerpo, RADIO_NEURONA, RADIO_CUERPO, grosor=2.4),
        _arista(sesgo, cuerpo, RADIO_SESGO, RADIO_CUERPO, MORADO, grosor=2.4),
        _arista(cuerpo, salida, RADIO_CUERPO, RADIO_NEURONA, AMBAR, grosor=2.4),
    )
    nodos = VGroup(
        _nodo(entrada, VERDE, RADIO_NEURONA),
        _nodo(sesgo, MORADO, RADIO_SESGO),
        _nodo(cuerpo, PRIMARIO, RADIO_CUERPO),
        _nodo(salida, AMBAR, RADIO_NEURONA),
    )
    etiquetas = VGroup(
        MathTex("x", color=VERDE).scale(0.6).move_to(entrada),
        MathTex("b", color=MORADO).scale(0.5).move_to(sesgo),
        MathTex(r"\hat{y}", color=AMBAR).scale(0.5).move_to(salida),
        MathTex("w", color=PRIMARIO).scale(0.6).move_to(
            (entrada + cuerpo) / 2 + UP * 0.33),
    )
    return VGroup(aristas, nodos, etiquetas)


def _red_compacta():
    """Dos capas seguidas: la excusa para tener un W_1 y un W_2 que componer."""
    capas = [
        [np.array([x, Y_RED + (n - 1) / 2 * PASO_RED - k * PASO_RED, 0.0])
         for k in range(n)]
        for x, n in zip(X_RED, TAMANOS_RED)
    ]
    nodos = VGroup(*[
        _nodo(centro, color)
        for capa, color in zip(capas, (VERDE, PRIMARIO, AMBAR))
        for centro in capa
    ])
    aristas = VGroup(*[
        _arista(origen, destino)
        for izquierda, derecha in zip(capas, capas[1:])
        for origen in izquierda for destino in derecha
    ])
    etiquetas = VGroup(*[
        MathTex(nombre, color=PRIMARIO).scale(0.55).move_to(
            [(X_RED[i] + X_RED[i + 1]) / 2, Y_RED + 0.8, 0])
        for i, nombre in enumerate(("W_1", "W_2"))
    ])
    return VGroup(aristas, nodos, etiquetas)


# --- Columna derecha: lo que el modelo dibuja ------------------------------
def _recta(ejes, funcion, color):
    """Recta con resplandor detrás: da cuerpo sin engordar el trazo."""
    resplandor = ejes.plot(funcion, x_range=X_TRAZO, color=color)
    resplandor.set_stroke(width=13, opacity=0.16)
    linea = ejes.plot(funcion, x_range=X_TRAZO, color=color)
    linea.set_stroke(width=4.5)
    return VGroup(resplandor, linea)


def _residuos(ejes, xs, ys, funcion):
    """Segmentos verticales del punto a la recta: el error, hecho visible."""
    return VGroup(*[
        DashedLine(
            ejes.c2p(x, y), ejes.c2p(x, funcion(x)),
            color=AMBAR, stroke_width=2.5, dash_length=0.09,
        )
        for x, y in zip(xs, ys)
    ])


def construir(scene):
    encabezado = hacer_titulo("Llevémoslo a las matemáticas")

    ejes = Axes(
        x_range=[0, 5.2, 1], y_range=[0, 3.8, 1],
        x_length=5.4, y_length=4.0,
        axis_config={
            "color": SECUNDARIO, "stroke_width": 2.5, "stroke_opacity": 0.7,
            "include_ticks": False, "tip_width": 0.18, "tip_height": 0.18,
        },
    ).move_to(CENTRO_GRAFICA)

    xs, ys_lineal, ys_curva = _datos()
    puntos = VGroup(*[
        Dot(ejes.c2p(x, y), radius=0.08, color=CLARO)
        for x, y in zip(xs, ys_lineal)
    ])

    def ajuste(x):
        return PENDIENTE * x + ORDENADA

    # ---------------------- 1: una entrada, una recta -----------------------
    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(Create(ejes), run_time=0.8)
    scene.play(
        LaggedStart(*[FadeIn(p, scale=0.5) for p in puntos], lag_ratio=0.08),
        run_time=0.9,
    )

    escalar = _pintar(
        MathTex(r"\hat{y}", "=", "w", "x", "+", "b"),
        ((0, AMBAR), (2, PRIMARIO), (3, VERDE), (5, MORADO)),
    ).scale(1.35).move_to([X_MATE, 0.95, 0])
    scene.play(FadeIn(escalar, shift=UP * 0.15), run_time=0.6)

    # La misma ecuación, dibujada: es una sola neurona.
    neurona = _neurona_simple()
    scene.play(FadeIn(neurona, scale=0.9), run_time=0.8)

    recta = _recta(ejes, ajuste, VERDE)
    scene.play(Create(recta), run_time=1.0)
    scene.next_slide()

    # ---------------------- 2: n entradas -----------------------------------
    expandida = _pintar(
        MathTex(r"\hat{y}", "=", "w_1", "x_1", "+", "w_2", "x_2", "+",
                r"\cdots", "+", "w_n", "x_n", "+", "b"),
        ((0, AMBAR), (2, PRIMARIO), (3, VERDE), (5, PRIMARIO), (6, VERDE),
         (10, PRIMARIO), (11, VERDE), (13, MORADO)),
    ).scale(0.8)
    _ajustar(expandida).move_to([X_MATE, 1.95, 0])
    pie = texto("una muestra, n entradas", 18, color=SECUNDARIO)
    pie.next_to(expandida, DOWN, buff=0.3)

    scene.play(
        FadeOut(neurona, shift=DOWN * 0.15),
        ReplacementTransform(escalar, expandida),
        run_time=0.9,
    )
    scene.play(FadeIn(pie), run_time=0.5)
    scene.next_slide()

    # ---------------------- 3: todas las muestras a la vez ------------------
    matricial = _pintar(
        MathTex(r"\hat{Y}", "=", "X", "W", "+", "b"),
        ((0, AMBAR), (2, VERDE), (3, PRIMARIO), (5, MORADO)),
    ).scale(1.2).move_to([X_MATE, 0.35, 0])
    bloques = _matricial().move_to([X_MATE, -1.6, 0])
    leyenda = texto("m muestras, n entradas", 18, color=SECUNDARIO)
    leyenda.move_to([X_MATE, -2.95, 0])

    scene.play(FadeIn(matricial, shift=UP * 0.15), run_time=0.7)
    scene.play(
        LaggedStart(*[GrowFromCenter(b) for b in bloques[0]], lag_ratio=0.15),
        run_time=1.1,
    )
    scene.play(FadeIn(bloques[1]), FadeIn(leyenda), run_time=0.6)
    scene.next_slide()

    # ---------------------- 4: más neuronas, la misma recta -----------------
    # Dos capas lineales encadenadas se multiplican entre sí y vuelven a caber
    # en un solo peso y un solo sesgo: la forma de la ecuación no cambia.
    columna = VGroup(expandida, pie, matricial, bloques, leyenda)
    red = _red_compacta()
    algebra, final = _composicion()
    algebra.move_to([X_MATE, -0.55, 0])
    caja = enmarcar(final, margen=0.35)
    remate = texto("componer lineales da otra lineal", 20, color=CLARO)
    remate.move_to([X_MATE, -2.4, 0])

    scene.play(FadeOut(columna, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(red, scale=0.9), run_time=0.7)
    scene.play(FadeIn(algebra[0], shift=UP * 0.1), run_time=0.6)
    scene.play(FadeIn(algebra[1], shift=UP * 0.1), run_time=0.7)
    scene.play(FadeIn(algebra[2], shift=UP * 0.1), Create(caja), run_time=0.7)
    scene.play(FadeIn(remate), run_time=0.5)

    # Cambian los parámetros, gira la recta, y sigue siendo una recta.
    for pendiente, altura in ((-0.42, 1.95), (0.6, 1.9)):
        def girada(x, m=pendiente, c=altura):
            return m * (x - VERTICE) + c

        scene.play(
            Transform(recta, _recta(ejes, girada, PRIMARIO)), run_time=0.7,
        )
    scene.play(Transform(recta, _recta(ejes, ajuste, VERDE)), run_time=0.7)
    scene.next_slide()

    # ---------------------- 5: datos no lineales ----------------------------
    scene.play(
        *[p.animate.move_to(ejes.c2p(x, y))
          for p, x, y in zip(puntos, xs, ys_curva)],
        run_time=1.3,
    )
    scene.next_slide()

    # El modelo hace lo único que puede: aplanar la recta. Y aun así falla.
    scene.play(
        Transform(recta, _recta(ejes, lambda x: NIVEL_PLANO, AMBAR)),
        run_time=0.9,
    )
    residuos = _residuos(ejes, xs, ys_curva, lambda x: NIVEL_PLANO)
    scene.play(
        LaggedStart(*[Create(r) for r in residuos], lag_ratio=0.06),
        run_time=1.0,
    )

    for pendiente, altura in ((-0.42, 1.95), (0.55, 1.15), (0.12, 1.5)):
        def girada(x, m=pendiente, c=altura):
            return m * (x - VERTICE) + c

        scene.play(
            Transform(recta, _recta(ejes, girada, AMBAR)),
            Transform(residuos, _residuos(ejes, xs, ys_curva, girada)),
            run_time=0.85,
        )

    aviso = texto("ninguna recta encaja", 20, color=AMBAR)
    aviso.move_to([CENTRO_GRAFICA[0], -3.05, 0])
    scene.play(
        LaggedStart(*[Indicate(r, color=AMBAR, scale_factor=1.15)
                      for r in residuos], lag_ratio=0.05),
        Indicate(caja, color=AMBAR, scale_factor=1.04),
        FadeIn(aviso),
        run_time=0.9,
    )
    scene.wait(0.3)

    scene.next_slide()
