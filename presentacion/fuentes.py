import os

import manimpango

_DIR = os.path.join(os.path.dirname(__file__), "assets", "fonts")

_ARCHIVOS = (
    ("Press Start 2P", "PressStart2P-Regular.ttf"),
    ("JetBrains Mono", "JetBrainsMono-Regular.ttf"),
    ("JetBrains Mono", "JetBrainsMono-Bold.ttf"),
)

_registradas = False


def registrar():
    global _registradas
    if _registradas:
        return
    for _familia, archivo in _ARCHIVOS:
        manimpango.register_font(os.path.join(_DIR, archivo))
    _registradas = True


registrar()
