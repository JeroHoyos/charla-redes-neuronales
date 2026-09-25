import numpy as np
from manim import (
    RIGHT,
    Axes,
    DashedLine,
    Dot,
    MathTex,
    Rectangle,
    Square,
    VGroup,
)

from componentes import aspa, texto, visto
from estilo import CLARO, FONDO, PRIMARIO, ROJO, SECUNDARIO, VERDE

XS = (0.4, 1.05, 1.7, 2.35, 3.0, 3.65)
RUIDO = (0.1, -0.12, 0.08, -0.1, 0.12, -0.08)
LLENO = 0.9

Y_FORMULA = 0.8
Y_LEYENDA = -0.85
CENTRO_GRAFICA_APOYO = [2.35, -1.5, 0]
ANCHO_GRAFICA_APOYO = 4.3
ALTO_GRAFICA_APOYO = 2.5
X_TERMO_APOYO = 5.5
ANCHO_TERMO_APOYO = 0.5
ALTO_TERMO_APOYO = 2.1
Y_PIE_TERMO_APOYO = -2.6

EJES = {
    "color": SECUNDARIO, "stroke_width": 2.2,
    "include_ticks": False, "tip_width": 0.14, "tip_height": 0.14,
}

X_COLUMNAS = (-3.4, 3.4)
Y_COLUMNA = 0.3
ANCHO_COLUMNA, ALTO_COLUMNA = 5.0, 3.0
Y_ETIQUETA = -2.2


def real(x):
    return 2.1 + 1.15 * np.sin(1.75 * np.asarray(x) - 0.7)


def datos():
    return real(XS) + np.array(RUIDO)


def ajuste_malo(ys):
    pendiente, ordenada = np.polyfit(XS, ys, 1)

    def recta(x):
        return pendiente * np.asarray(x) + ordenada

    return recta


def proporcion(ys, malo):
    return float(np.mean((ys - real(XS)) ** 2) / np.mean((ys - malo(XS)) ** 2))


def leyenda(entradas, x_simbolo=-5.5, paso=0.6):
    grupo = VGroup()
    for fila, (simbolo, color, glosa) in enumerate(entradas):
        y = Y_LEYENDA - fila * paso
        grupo.add(
            MathTex(simbolo, color=color).scale(0.8).move_to([x_simbolo, y, 0]),
            texto(glosa, 19, color=SECUNDARIO).next_to(
                np.array([x_simbolo + 0.45, y, 0]), RIGHT, buff=0,
            ),
        )
    return grupo


def tubo(x, y_pie, ancho, alto):
    cristal = Rectangle(
        width=ancho, height=alto,
        stroke_color=SECUNDARIO, stroke_width=2,
    ).set_fill(FONDO, opacity=1.0)
    return cristal.move_to([x, y_pie + alto / 2, 0])


def liquido(x, y_pie, ancho, alto, fraccion, color=ROJO):
    llenado = max(alto * fraccion, 0.03)
    barra = Rectangle(
        width=ancho - 0.13, height=llenado,
        stroke_width=0, fill_color=color, fill_opacity=0.8,
    )
    return barra.move_to([x, y_pie + llenado / 2, 0])


def tubo_apoyo():
    return tubo(X_TERMO_APOYO, Y_PIE_TERMO_APOYO,
                ANCHO_TERMO_APOYO, ALTO_TERMO_APOYO)


def liquido_apoyo(fraccion, color=ROJO):
    return liquido(X_TERMO_APOYO, Y_PIE_TERMO_APOYO, ANCHO_TERMO_APOYO,
                   ALTO_TERMO_APOYO, fraccion, color)


def ejes_datos(centro, ancho, alto):
    return Axes(
        x_range=[0, 4.1, 1], y_range=[0, 4.2, 1],
        x_length=ancho, y_length=alto,
        axis_config={
            "color": SECUNDARIO, "stroke_width": 2.2,
            "include_ticks": False, "tip_width": 0.14, "tip_height": 0.14,
        },
    ).move_to(centro)


def dibujo_datos(ejes, ys, funcion, forma, radio=0.085, grosor=4):
    puntos = VGroup(*[
        Dot(ejes.c2p(x, y), radius=radio, color=CLARO) for x, y in zip(XS, ys)
    ])
    curva = ejes.plot(
        lambda x: float(funcion(x)), x_range=[0.15, 3.9], color=PRIMARIO,
    ).set_stroke(width=grosor)

    alto_unidad = ejes.c2p(0, 1)[1] - ejes.c2p(0, 0)[1]
    errores = VGroup()
    for x, y in zip(XS, ys):
        prediccion = float(funcion(x))
        if forma == "distancias":
            errores.add(DashedLine(
                ejes.c2p(x, y), ejes.c2p(x, prediccion),
                color=ROJO, stroke_width=grosor, dash_length=0.11,
            ))
            continue
        lado = max(abs(y - prediccion) * alto_unidad, 0.02)
        cuadrado = Square(
            side_length=lado, stroke_color=ROJO, stroke_width=grosor * 0.55,
            fill_color=ROJO, fill_opacity=0.25,
        )
        cuadrado.move_to([
            ejes.c2p(x, 0)[0] + lado / 2,
            ejes.c2p(x, min(y, prediccion))[1] + lado / 2, 0,
        ])
        errores.add(cuadrado)
    return puntos, curva, errores


def ejes_columna(x_centro, y_max=3.2):
    return Axes(
        x_range=[0, 6, 1], y_range=[0, y_max, 1],
        x_length=ANCHO_COLUMNA, y_length=ALTO_COLUMNA,
        axis_config={
            "color": SECUNDARIO, "stroke_width": 2.2,
            "include_ticks": False, "tip_width": 0.14, "tip_height": 0.14,
        },
    ).move_to([x_centro, Y_COLUMNA, 0])


def etiqueta(bien, nombre, x_centro):
    marca = visto(VERDE) if bien else aspa(ROJO)
    rotulo = texto(nombre, 24, color=CLARO)
    return VGroup(marca, rotulo).arrange(RIGHT, buff=0.25).move_to(
        [x_centro, Y_ETIQUETA, 0],
    )


__all__ = [
    "XS", "LLENO", "Y_FORMULA", "EJES", "CENTRO_GRAFICA_APOYO",
    "ANCHO_GRAFICA_APOYO", "ALTO_GRAFICA_APOYO", "X_COLUMNAS",
    "real", "datos", "ajuste_malo", "proporcion", "leyenda", "tubo",
    "liquido", "tubo_apoyo", "liquido_apoyo", "ejes_datos", "dibujo_datos",
    "ejes_columna", "etiqueta",
]
