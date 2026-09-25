import numpy as np
from manim import (
    DOWN,
    TAU,
    UP,
    Create,
    FadeIn,
    LaggedStart,
    ValueTracker,
    VGroup,
    rate_functions,
)

from componentes import separador, texto
from estilo import CLARO, FONT_TITULO, PRIMARIO, SECUNDARIO

LINEAS = (
    ("¿QUE HACE BUENA", CLARO),
    ("A UNA FUNCION", CLARO),
    ("DE ERROR?", PRIMARIO),
)
TAM_PREGUNTA = 38
BUFF_LINEAS = 0.5
ANCHO_PREGUNTA = 8.4
Y_PREGUNTA = 0.45
LARGO_RAYA = 1.6
DY_RAYA = 0.8

GLIFOS = ("?", "¿")
TAMS = (26, 34, 44, 54, 64)
N_SIGNOS = 26
INTENTOS = 3000
SEMILLA = 23
X_LIMITE = 6.05
Y_LIMITE = 3.15
MARGEN_ZONA = 0.8
SEPARACION = 1.15
INCLINACION = 0.32
OPACIDAD_CERCA = 0.72
OPACIDAD_LEJOS = 0.26
PISO_BRILLO = 0.55
VAIVEN_X = (0.04, 0.12)
VAIVEN_Y = (0.10, 0.26)

VUELTA = 4.0


def _pregunta():
    lineas = VGroup(*[
        texto(contenido, TAM_PREGUNTA, color=color, font=FONT_TITULO)
        for contenido, color in LINEAS
    ]).arrange(DOWN, buff=BUFF_LINEAS)
    if lineas.width > ANCHO_PREGUNTA:
        lineas.scale(ANCHO_PREGUNTA / lineas.width)
    return lineas.move_to([0, Y_PREGUNTA, 0])


def _lugares(rng, ancho_zona, alto_zona, centro):
    puestos = []
    for _ in range(INTENTOS):
        if len(puestos) == N_SIGNOS:
            break
        punto = np.array([
            rng.uniform(-X_LIMITE, X_LIMITE),
            rng.uniform(-Y_LIMITE, Y_LIMITE),
            0.0,
        ])
        if (abs(punto[0] - centro[0]) < ancho_zona / 2
                and abs(punto[1] - centro[1]) < alto_zona / 2):
            continue
        if any(np.linalg.norm(punto - otro) < SEPARACION for otro in puestos):
            continue
        puestos.append(punto)
    return puestos


def _signos(ancho_zona, alto_zona, centro):
    rng = np.random.default_rng(SEMILLA)
    grupo = VGroup()
    for punto in _lugares(rng, ancho_zona, alto_zona, centro):
        tam = TAMS[rng.integers(len(TAMS))]
        signo = texto(
            GLIFOS[rng.integers(len(GLIFOS))],
            tam,
            color=PRIMARIO if rng.random() < 0.6 else SECUNDARIO,
            font=FONT_TITULO,
        )
        signo.rotate(rng.uniform(-INCLINACION, INCLINACION))
        signo.move_to(punto)
        signo.opacidad = float(np.interp(
            tam, (TAMS[0], TAMS[-1]), (OPACIDAD_CERCA, OPACIDAD_LEJOS),
        ))
        signo.set_opacity(signo.opacidad)
        signo.fase = rng.uniform(0.0, TAU)
        signo.vaiven = np.array([
            rng.uniform(*VAIVEN_X), rng.uniform(*VAIVEN_Y), 0.0,
        ])
        grupo.add(signo)
    return grupo


def _vaiven(signo, reloj):
    base = signo.get_center()
    fase, vaiven, opacidad = signo.fase, signo.vaiven, signo.opacidad

    def mover(mob):
        onda = TAU * reloj.get_value() + fase
        mob.move_to(base + vaiven * np.array([
            np.cos(onda), np.sin(onda), 0.0,
        ]))
        mob.set_opacity(opacidad * (
            PISO_BRILLO + (1 - PISO_BRILLO) * (0.5 + 0.5 * np.sin(onda))
        ))

    return mover


def construir(scene):
    pregunta = _pregunta()
    raya = separador(largo=LARGO_RAYA, grosor=3)
    raya.next_to(pregunta, DOWN, buff=DY_RAYA)

    bloque = VGroup(pregunta, raya)
    signos = _signos(
        bloque.width + MARGEN_ZONA * 2,
        bloque.height + MARGEN_ZONA * 2,
        bloque.get_center(),
    )

    scene.play(
        LaggedStart(*[FadeIn(linea, shift=UP * 0.2) for linea in pregunta],
                    lag_ratio=0.35),
        run_time=1.3,
    )
    scene.play(Create(raya), run_time=0.5)
    scene.play(
        LaggedStart(*[FadeIn(s, scale=0.5) for s in signos], lag_ratio=0.06),
        run_time=1.7,
    )

    reloj = ValueTracker(0.0)
    for signo in signos:
        signo.add_updater(_vaiven(signo, reloj))

    if hasattr(scene, "_base_slide_config"):
        scene._base_slide_config.auto_next = True
    scene.next_slide(loop=True, indicador=False)

    scene.play(
        reloj.animate.set_value(1.0),
        run_time=VUELTA,
        rate_func=rate_functions.linear,
    )

    scene.next_slide(indicador=False)
    for signo in signos:
        signo.clear_updaters()
