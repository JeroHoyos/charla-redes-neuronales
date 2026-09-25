"""El tic-tac-toe del cuaderno 04: las reglas y un tablero para jugarle a la red.

El tablero son 9 casillas y siempre se ve desde quien tiene el turno:
1 es suyo, -1 del rival y 0 está libre.
"""

import ipywidgets as widgets
import torch

from .configuracion import AMBER, LIGHT, PRIMARY, SECONDARY

EMPTY = (0,) * 9

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

ROTATION = (6, 3, 0, 7, 4, 1, 8, 5, 2)    # dónde cae cada casilla al girar el tablero
MIRROR = (2, 1, 0, 5, 4, 3, 8, 7, 6)      # y al reflejarlo


def free_cells(board):
    return [cell for cell, value in enumerate(board) if value == 0]


def has_winner(board):
    return any(board[a] != 0 and board[a] == board[b] == board[c] for a, b, c in LINES)


def step(board, cell):
    """Juega en `cell`. Devuelve el tablero visto por el rival, la recompensa y si se acabó."""
    next_board = list(board)
    next_board[cell] = 1
    won = has_winner(next_board)
    return tuple(-value for value in next_board), float(won), won or not free_cells(next_board)


def symmetries(move):
    """La misma jugada girada y reflejada: 8 versiones del mismo juego."""
    board, cell, reward, next_board, done = move
    versions = []
    for _ in range(4):
        for order in (range(9), MIRROR):
            versions.append((tuple(board[i] for i in order), list(order).index(cell),
                             reward, tuple(next_board[i] for i in order), done))
        board = tuple(board[i] for i in ROTATION)
        next_board = tuple(next_board[i] for i in ROTATION)
        cell = ROTATION.index(cell)
    return versions


def play_against(model):
    """Tú eres X y empiezas. El tablero aparece debajo de la celda."""
    board = [0] * 9                        # 1 es tuya, -1 de la red
    status = widgets.HTML()
    buttons = [widgets.Button(layout=widgets.Layout(width="80px", height="80px"))
               for _ in range(9)]
    for button in buttons:
        button.style.button_color = "#0b1622"
        button.style.font_family = "Consolas, monospace"
        button.style.font_size = "40px"
        button.style.font_weight = "bold"

    def say(text, color=SECONDARY):
        status.value = f'<span style="font-family: Consolas, monospace; font-size: 16px; color: {color}">{text}</span>'

    def place(cell, value):
        """Pone la ficha y dice si se acabó la partida."""
        board[cell] = value
        buttons[cell].description = "X" if value == 1 else "O"
        buttons[cell].style.text_color = PRIMARY if value == 1 else AMBER
        if has_winner(board) and value == 1:
            say("¡Ganaste!", PRIMARY)
        elif has_winner(board):
            say("Gana la red", AMBER)
        elif not free_cells(board):
            say("Empate")
        else:
            return False
        return True

    @torch.no_grad()
    def model_move():
        q = model(torch.tensor([-value for value in board], dtype=torch.float32))
        place(max(free_cells(board), key=lambda cell: q[cell]), -1)

    def click(cell):
        if board[cell] == 0 and not has_winner(board) and not place(cell, 1):
            model_move()

    def new_game(_=None):
        board[:] = [0] * 9
        for button in buttons:
            button.description = ""
        say("Tu turno")

    for cell, button in enumerate(buttons):
        button.on_click(lambda _, cell=cell: click(cell))

    again = widgets.Button(description="otra partida", layout=widgets.Layout(width="252px"))
    again.style.button_color = "#10202d"
    again.style.text_color = LIGHT
    again.on_click(new_game)

    new_game()
    grid = widgets.GridBox(buttons, layout=widgets.Layout(
        grid_template_columns="repeat(3, 80px)", grid_gap="6px"))
    return widgets.VBox([grid, status, again], layout=widgets.Layout(padding="10px"))
