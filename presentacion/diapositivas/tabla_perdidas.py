from manim import (
    DOWN,
    RIGHT,
    Create,
    FadeIn,
    Line,
    MathTex,
    VGroup,
)

from componentes import texto
from componentes import titulo as hacer_titulo
from estilo import CLARO, PRIMARIO, SECUNDARIO

FILAS = (
    ("Regresión", "MSE", r"\frac{1}{n}\sum (y - \hat{y})^2"),
    ("Clasificación", "Entropía cruzada",
     r"-\sum_i y_i \log \hat{y}_i"),
    ("LLM", "Perplejidad", r"e^{\,L_{\mathrm{CE}}}"),
    ("Reconocimiento facial", "Triplet", r"\max(0,\ d(a, p) - d(a, n) + m)"),
)
COLUMNAS = ("tarea", "pérdida", "fórmula")

X_TAREA = -6.0
X_PERDIDA = -1.3
X_FORMULA = 3.8
X_BORDE = 6.3
Y_CABECERA = 1.95
Y_PRIMERA = 0.95
PASO = 1.25


def _izquierda(mob, x, y):
    return mob.move_to([x + mob.width / 2, y, 0])


def _linea(y, color=SECUNDARIO, opacidad=0.35):
    return Line([X_TAREA - 0.2, y, 0], [X_BORDE, y, 0], color=color,
                stroke_width=1.5).set_stroke(opacity=opacidad)


def construir(scene):
    encabezado = hacer_titulo("Una pérdida para cada tarea")

    cabecera = VGroup(
        _izquierda(texto(COLUMNAS[0], 17, color=SECUNDARIO), X_TAREA,
                   Y_CABECERA),
        _izquierda(texto(COLUMNAS[1], 17, color=SECUNDARIO), X_PERDIDA,
                   Y_CABECERA),
        texto(COLUMNAS[2], 17, color=SECUNDARIO).move_to(
            [X_FORMULA, Y_CABECERA, 0],
        ),
    )
    bajo_cabecera = _linea(Y_CABECERA - 0.4, PRIMARIO, 0.8)

    filas = VGroup()
    separadores = VGroup()
    for k, (tarea, perdida, formula) in enumerate(FILAS):
        y = Y_PRIMERA - k * PASO
        filas.add(VGroup(
            _izquierda(texto(tarea, 22, color=CLARO), X_TAREA, y),
            _izquierda(texto(perdida, 22, color=PRIMARIO), X_PERDIDA, y),
            MathTex(formula, color=CLARO).scale(0.75).move_to([X_FORMULA, y, 0]),
        ))
        if k < len(FILAS) - 1:
            separadores.add(_linea(y - PASO / 2))

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(cabecera), Create(bajo_cabecera), run_time=0.6)
    for k, fila in enumerate(filas):
        animaciones = [FadeIn(fila, shift=RIGHT * 0.2)]
        if k > 0:
            animaciones.append(Create(separadores[k - 1]))
        scene.play(*animaciones, run_time=0.6)
    scene.next_slide()
