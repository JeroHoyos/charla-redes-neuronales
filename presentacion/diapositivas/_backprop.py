import numpy as np
from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    Circle,
    Dot,
    FadeOut,
    LaggedStart,
    Line,
    MathTex,
    MoveAlongPath,
    Rectangle,
    RoundedRectangle,
    Transform,
    VGroup,
    there_and_back,
)

from estilo import AMBAR, FONDO, MORADO, ROJO, SECUNDARIO

ANCHO_CAJA, ALTO_CAJA = 1.15, 0.95

CAPAS_RED = (3, 4, 4, 2)
X_RED = -2.0
Y_RED = -0.65
SEP_CAPA = 2.35
SEP_NODO = 0.95
RADIO_NODO = 0.28
ARISTA_ELEGIDA = 1

X_TERMO = 4.6
ANCHO_TERMO = 0.8
ALTO_TERMO = 3.2
Y_PIE_TERMO = -2.3
LLENO = 0.86


def perilla(nombre=None, angulo=np.pi / 2, radio=0.22, lado=LEFT):
    cuerpo = Circle(radius=radio, color=AMBAR, stroke_width=3)
    cuerpo.set_fill(FONDO, opacity=1.0)
    aguja = Line(
        ORIGIN, np.array([np.cos(angulo), np.sin(angulo), 0.0]) * radio * 0.74,
        color=AMBAR, stroke_width=3,
    )
    mando = VGroup(cuerpo, aguja)
    if nombre is None:
        return VGroup(mando)
    etiqueta = MathTex(nombre, color=AMBAR).scale(0.6)
    etiqueta.next_to(mando, lado, buff=0.14)
    return VGroup(mando, etiqueta)


def colgar(mando, de, buff):
    mando.next_to(de, DOWN, buff=buff)
    return mando.shift(
        RIGHT * (de.get_center()[0] - mando[0].get_center()[0]),
    )


def caja(etiqueta, color, ancho=ANCHO_CAJA, escala=0.8):
    marco = RoundedRectangle(
        width=ancho, height=ALTO_CAJA, corner_radius=0.16,
        stroke_color=color, stroke_width=3,
    ).set_fill(color, opacity=0.08)
    dentro = MathTex(etiqueta, color=color).scale(escala)
    return VGroup(marco, dentro.move_to(marco.get_center()))


def x_capa(i):
    return X_RED + (i - (len(CAPAS_RED) - 1) / 2) * SEP_CAPA


def red():
    capas = []
    for i, n in enumerate(CAPAS_RED):
        x = x_capa(i)
        alto = (n - 1) * SEP_NODO
        capas.append(VGroup(*[
            Circle(radius=RADIO_NODO, color=SECUNDARIO, stroke_width=2.5)
            .set_fill(FONDO, opacity=1.0)
            .move_to([x, Y_RED + alto / 2 - j * SEP_NODO, 0])
            for j in range(n)
        ]))

    conexiones = []
    for izquierda, derecha in zip(capas, capas[1:]):
        grupo = VGroup()
        for a in izquierda:
            for b in derecha:
                direccion = b.get_center() - a.get_center()
                direccion = direccion / np.linalg.norm(direccion)
                grupo.add(Line(
                    a.get_center() + direccion * RADIO_NODO,
                    b.get_center() - direccion * RADIO_NODO,
                    color=SECUNDARIO, stroke_width=1.5, stroke_opacity=0.4,
                ))
        conexiones.append(grupo)
    return capas, conexiones


def tubo():
    cristal = Rectangle(
        width=ANCHO_TERMO, height=ALTO_TERMO,
        stroke_color=SECUNDARIO, stroke_width=2,
    ).set_fill(FONDO, opacity=1.0)
    return cristal.move_to([X_TERMO, Y_PIE_TERMO + ALTO_TERMO / 2, 0])


def liquido(fraccion):
    llenado = max(ALTO_TERMO * fraccion, 0.04)
    barra = Rectangle(
        width=ANCHO_TERMO - 0.14, height=llenado,
        stroke_width=0, fill_color=ROJO, fill_opacity=0.8,
    )
    return barra.move_to([X_TERMO, Y_PIE_TERMO + llenado / 2, 0])


def ficha(expresion):
    formula = MathTex(expresion, color=MORADO).scale(0.55)
    borde = RoundedRectangle(
        width=formula.width + 0.26, height=formula.height + 0.2,
        corner_radius=0.09, stroke_color=MORADO, stroke_width=2,
    ).set_fill(FONDO, opacity=1.0)
    return VGroup(borde, formula.move_to(borde.get_center()))


def llevar(scene, fichas, destinos, cables=(), run_time=0.75):
    scene.play(
        *[f.animate.move_to(d) for f, d in zip(fichas, destinos)],
        *[c.animate.set_color(MORADO) for c in cables],
        run_time=run_time,
    )


def convertir(una_ficha, expresion):
    return Transform(una_ficha, ficha(expresion).move_to(una_ficha.get_center()))


def pulso(nodo, color, ancho=4.0):
    return nodo.animate(rate_func=there_and_back).set_stroke(
        color=color, width=ancho,
    )


def pasada(scene, capas, conexiones, color, run_time=0.45):
    scene.play(
        LaggedStart(*[pulso(n, color) for n in capas[0]], lag_ratio=0.08),
        run_time=0.5,
    )
    for grupo, destino in zip(conexiones, capas[1:]):
        pulsos = [Dot(color=color, radius=0.06).move_to(c.get_start())
                  for c in grupo]
        scene.add(*pulsos)
        scene.play(
            *[MoveAlongPath(p, c) for p, c in zip(pulsos, grupo)],
            grupo.animate(rate_func=there_and_back).set_stroke(
                color=color, opacity=0.9, width=2.2,
            ),
            run_time=run_time,
        )
        scene.play(
            *[FadeOut(p, scale=0.4) for p in pulsos],
            LaggedStart(*[pulso(n, color) for n in destino], lag_ratio=0.06),
            run_time=0.35,
        )
        scene.remove(*pulsos)


__all__ = [
    "perilla", "colgar", "caja", "x_capa", "red", "tubo", "liquido",
    "ficha", "llevar", "convertir", "pulso", "pasada",
    "CAPAS_RED", "X_RED", "Y_RED", "ARISTA_ELEGIDA", "LLENO",
]
