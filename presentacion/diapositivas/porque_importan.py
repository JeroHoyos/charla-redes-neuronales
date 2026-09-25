import numpy as np
from manim import (
    BOLD,
    DOWN,
    UP,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Flash,
    Group,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    MoveAlongPath,
    RoundedRectangle,
    VGroup,
)

from componentes import enmarcar, imagen, texto
from estilo import AMBAR, CLARO, FONDO, MORADO, PRIMARIO, SECUNDARIO, VERDE

EJEMPLOS = (
    ("youtube.jpg", "Sistemas de recomendación", "YouTube, Spotify", AMBAR),
    ("reconocimiento_facial.png", "Visión artificial", "desbloquear el celular", VERDE),
    ("chatgpt_claude.jpg", "LLMs", "ChatGPT, Claude", MORADO),
)

ANCHO_GRANDE = 4.8
ALTO_GRANDE = 2.74
MARGEN = 0.22
ESCALA_CHICA = 0.62
Y_GRANDE = -0.8
Y_FILA = 1.95
X_FILA = (-3.7, 0.0, 3.7)
ANCHO_ROTULO = 3.35
Y_CAJA = -1.72

CAPAS = (2, 4, 4, 2)
ANCHO_RED = 3.6
ALTO_RED = 1.6


def _tarjeta(archivo, color):
    marco = RoundedRectangle(
        width=ANCHO_GRANDE, height=ALTO_GRANDE, corner_radius=0.18,
        stroke_color=color, stroke_width=4,
        fill_color=FONDO, fill_opacity=1.0,
    )
    foto = imagen(archivo).scale_to_fit_height(ALTO_GRANDE - MARGEN)
    if foto.width > ANCHO_GRANDE - MARGEN:
        foto.scale_to_fit_width(ANCHO_GRANDE - MARGEN)
    foto.move_to(marco.get_center())
    return Group(marco, foto)


def _mini_red():
    paso = ALTO_RED / (max(CAPAS) - 1)
    columnas = []
    for i, n in enumerate(CAPAS):
        x = -ANCHO_RED / 2 + ANCHO_RED * i / (len(CAPAS) - 1)
        alto_capa = paso * (n - 1)
        columnas.append([
            np.array([x, alto_capa / 2 - paso * k, 0]) for k in range(n)
        ])

    tramos = VGroup(*[
        VGroup(*[
            Line(a, b, color=PRIMARIO, stroke_width=1.6, stroke_opacity=0.5)
            for a in izq for b in der
        ])
        for izq, der in zip(columnas, columnas[1:])
    ])
    capas = VGroup(*[
        VGroup(*[Dot(p, radius=0.075, color=PRIMARIO) for p in col])
        for col in columnas
    ])
    return tramos, capas


def construir(scene):
    pregunta = texto("¿Dónde has visto una red neuronal hoy?", 34, color=CLARO)
    scene.play(FadeIn(pregunta, shift=UP * 0.2), run_time=0.8)
    scene.next_slide()
    scene.play(pregunta.animate.scale(0.72).to_edge(UP, buff=0.5), run_time=0.8)

    rotulos = VGroup(*[
        texto(categoria, 20, color=color, weight=BOLD)
        for _, categoria, _, color in EJEMPLOS
    ])
    ancho_max = max(r.width for r in rotulos)
    if ancho_max > ANCHO_ROTULO:
        rotulos.scale(ANCHO_ROTULO / ancho_max)

    tarjetas = []
    for (archivo, categoria, ejemplo, color), x, rotulo in zip(EJEMPLOS, X_FILA, rotulos):
        tarjeta = _tarjeta(archivo, color).move_to([0, Y_GRANDE, 0])
        marco, foto = tarjeta
        pie = VGroup(
            texto(categoria, 30, color=color, weight=BOLD),
            texto(ejemplo, 20, color=SECUNDARIO),
        ).arrange(DOWN, buff=0.14)
        pie.next_to(tarjeta, DOWN, buff=0.35)

        scene.play(GrowFromCenter(marco), FadeIn(foto, scale=0.9), run_time=0.6)
        scene.play(FadeIn(pie, shift=UP * 0.12), run_time=0.4)
        scene.next_slide()

        rotulo.next_to([x, Y_FILA - ALTO_GRANDE * ESCALA_CHICA / 2, 0], DOWN, buff=0.28)
        scene.play(
            tarjeta.animate.scale(ESCALA_CHICA).move_to([x, Y_FILA, 0]),
            FadeOut(pie),
            run_time=0.9,
        )
        scene.play(FadeIn(rotulo), run_time=0.3)
        tarjetas.append(tarjeta)

    scene.next_slide()

    tramos, capas = _mini_red()
    etiqueta = texto("REDES NEURONALES", 22, color=PRIMARIO, weight=BOLD)
    contenido = VGroup(VGroup(tramos, capas), etiqueta).arrange(DOWN, buff=0.28)
    contenido.move_to([0, Y_CAJA, 0])
    caja_negra = enmarcar(contenido, margen=0.5)

    anclas = (-0.62, 0.0, 0.62)
    y_salida = rotulos.get_bottom()[1] - 0.12
    conexiones = VGroup()
    for x, ancla, (*_, color) in zip(X_FILA, anclas, EJEMPLOS):
        fin = np.array([ancla * caja_negra.width / 2, caja_negra.get_top()[1], 0])
        conexiones.add(Line(
            np.array([x, y_salida, 0]), fin,
            color=color, stroke_width=3, stroke_opacity=0.85,
        ))

    scene.play(
        LaggedStart(*[Create(c) for c in conexiones], lag_ratio=0.15),
        run_time=0.8,
    )
    pulsos = [
        Dot(color=color, radius=0.06).move_to(c.get_start())
        for c, (*_, color) in zip(conexiones, EJEMPLOS)
    ]
    scene.play(
        *[MoveAlongPath(p, c) for p, c in zip(pulsos, conexiones)],
        run_time=0.9,
    )
    scene.play(
        GrowFromCenter(caja_negra),
        *[FadeOut(p, scale=0.1) for p in pulsos],
        run_time=0.5,
    )
    scene.play(
        LaggedStart(*[GrowFromCenter(n) for capa in capas for n in capa],
                    lag_ratio=0.06),
        run_time=0.6,
    )
    scene.play(Create(tramos), FadeIn(etiqueta), run_time=0.7)
    scene.play(
        Flash(caja_negra, color=PRIMARIO, line_length=0.3, num_lines=18,
              flash_radius=caja_negra.width / 2 + 0.35),
        run_time=0.6,
    )
    scene.wait(0.4)

    scene.next_slide()

    diagrama = Group(pregunta, rotulos, contenido, caja_negra, conexiones, *tarjetas)
    scene.play(FadeOut(diagrama), run_time=0.5)

    tabla = imagen("computo_transformer.jpg").scale_to_fit_width(9.5)
    tabla.move_to([0, 0.1, 0])
    marco_tabla = enmarcar(tabla, margen=0.16)
    scene.play(FadeIn(tabla), Create(marco_tabla), run_time=0.7)
    scene.wait(0.5)

    F0, F1 = 0.633, 0.760
    izq = tabla.get_left()[0]
    x0, x1 = izq + F0 * tabla.width, izq + F1 * tabla.width
    resalte = RoundedRectangle(
        width=x1 - x0, height=tabla.height + 0.04, corner_radius=0.08,
        stroke_color=MORADO, stroke_width=4,
        fill_color=MORADO, fill_opacity=0.14,
    ).move_to([(x0 + x1) / 2, tabla.get_center()[1], 0])

    fuente = texto(
        "Fuente: Stephen Roller, ex Senior Staff Research Scientist "
        "en Google DeepMind",
        15, color=SECUNDARIO,
    )
    if fuente.width > 12.6:
        fuente.scale(12.6 / fuente.width)
    fuente.next_to(marco_tabla, DOWN, buff=0.3)

    scene.play(Create(resalte), run_time=0.5)
    scene.play(Indicate(resalte, color=MORADO, scale_factor=1.06), run_time=0.6)
    scene.play(FadeIn(fuente, shift=UP * 0.1), run_time=0.4)
    scene.wait(0.3)

    scene.next_slide()
