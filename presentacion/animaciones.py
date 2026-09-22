from manim import (
    RIGHT,
    FadeIn,
    FadeOut,
)


def limpiar_pantalla(scene):
    resto = [m for m in scene.mobjects if m is not getattr(scene, "marco", None)]
    for m in resto:
        m.clear_updaters()
    if resto:
        scene.play(*[FadeOut(m) for m in resto])


def aparecer_uno_a_uno(scene, grupo, run_time=0.4, shift=RIGHT * 0.2):
    for elemento in grupo:
        scene.play(FadeIn(elemento, shift=shift), run_time=run_time)
