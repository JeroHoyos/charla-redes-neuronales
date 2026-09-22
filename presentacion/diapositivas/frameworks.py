import os

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    Group,
    ImageMobject,
    LaggedStart,
    RoundedRectangle,
    Text,
    VGroup,
)
from PIL import Image

from componentes import texto
from componentes import titulo as hacer_titulo
from estilo import (
    AMBAR,
    ASSETS,
    BLANCO,
    CLARO,
    FONT,
    MORADO,
    PRIMARIO,
    SECUNDARIO,
    VERDE,
)

LOGOS = (
    ("tensorflow-y-pytorch.png", (0.0, 0.5)),
    ("tensorflow-y-pytorch.png", (0.5, 1.0)),
    ("jax.png", None),
)

ANCHO_TARJETA, ALTO_TARJETA = 4.0, 1.9
MARGEN_TARJETA = 0.7
Y_TARJETAS = -0.6

CODIGO = (
    (0, "modelo = nn.Sequential(", None, None),
    (1, "nn.Linear(2, 8),", "la suma ponderada", PRIMARIO),
    (1, "nn.ReLU(),", "el umbral", VERDE),
    (1, "nn.Linear(8, 1),", None, None),
    (0, ")", None, None),
    (0, "", None, None),
    (0, "perdida = mse(modelo(x), y)", "medir el error", AMBAR),
    (0, "perdida.backward()", "backpropagation", MORADO),
    (0, "optimizador.step()", "bajar el valle", MORADO),
)

TINTES = {
    "nn": PRIMARIO, "Sequential": PRIMARIO, "Linear": PRIMARIO,
    "ReLU": PRIMARIO, "mse": PRIMARIO, "backward": PRIMARIO,
    "step": PRIMARIO,
    "2": AMBAR, "8": AMBAR, "1": AMBAR,
}

ANCHO_PANEL, ALTO_PANEL = 8.8, 5.2
Y_PANEL = -0.5
X_CODIGO = -3.75
SANGRIA = 0.45
X_COMENTARIO = 0.95
Y_PRIMERA = 1.15
PASO = 0.44
TAM_CODIGO = 20


def _logo(nombre, banda=None):
    imagen = Image.open(os.path.join(ASSETS, nombre)).convert("RGBA")
    if banda is not None:
        ancho, alto = imagen.size
        imagen = imagen.crop(
            (0, int(banda[0] * alto), ancho, int(banda[1] * alto)),
        )
    caja = imagen.getbbox()
    if caja:
        imagen = imagen.crop(caja)
    mob = ImageMobject(np.array(imagen))
    mob.receta_logo = (nombre, banda)
    return mob


def _tarjeta(logo):
    fondo = RoundedRectangle(
        width=ANCHO_TARJETA, height=ALTO_TARJETA, corner_radius=0.18,
        stroke_width=0,
    ).set_fill(BLANCO, opacity=1.0)
    logo.scale_to_fit_width(ANCHO_TARJETA - MARGEN_TARJETA)
    if logo.height > ALTO_TARJETA - MARGEN_TARJETA:
        logo.scale_to_fit_height(ALTO_TARJETA - MARGEN_TARJETA)
    return Group(fondo, logo.move_to(fondo.get_center()))


def construir(scene):
    encabezado = hacer_titulo("¿Y cómo se programa?")

    tarjetas = Group(*[_tarjeta(_logo(n, b)) for n, b in LOGOS])
    tarjetas.arrange(RIGHT, buff=0.45).set_y(Y_TARJETAS)

    panel = RoundedRectangle(
        width=ANCHO_PANEL, height=ALTO_PANEL, corner_radius=0.2,
        stroke_color=SECUNDARIO, stroke_width=2,
    ).set_fill(CLARO, opacity=0.035).move_to([0, Y_PANEL, 0])
    panel.set_stroke(opacity=0.35)
    pestana = VGroup(
        RoundedRectangle(
            width=1.5, height=0.42, corner_radius=0.1, stroke_width=0,
        ).set_fill(SECUNDARIO, opacity=0.16),
        texto("pytorch", 15, color=SECUNDARIO),
    )
    pestana[1].move_to(pestana[0].get_center())
    pestana.move_to([X_CODIGO + 0.55, Y_PANEL + ALTO_PANEL / 2 - 0.45, 0])

    lineas, comentarios = VGroup(), VGroup()
    for i, (sangria, linea, comentario, color) in enumerate(CODIGO):
        y = Y_PRIMERA - i * PASO
        if linea:
            lineas.add(Text(
                linea, font=FONT, font_size=TAM_CODIGO, color=CLARO,
                t2c=TINTES,
            ).move_to([X_CODIGO + sangria * SANGRIA, y, 0], aligned_edge=LEFT))
        if comentario:
            comentarios.add(texto(f"# {comentario}", 18, color=color).move_to(
                [X_COMENTARIO, y, 0], aligned_edge=LEFT,
            ))

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(
        LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tarjetas],
                    lag_ratio=0.3),
        run_time=1.4,
    )
    scene.next_slide()

    scene.play(FadeOut(tarjetas), run_time=0.6)
    scene.play(Create(panel), FadeIn(pestana), run_time=0.8)
    scene.play(
        LaggedStart(*[FadeIn(li, shift=RIGHT * 0.15) for li in lineas],
                    lag_ratio=0.3),
        run_time=1.8,
    )
    scene.next_slide()

    scene.play(
        LaggedStart(*[FadeIn(c, shift=LEFT * 0.15) for c in comentarios],
                    lag_ratio=0.4),
        run_time=1.6,
    )
    scene.wait(0.4)

    scene.next_slide()
