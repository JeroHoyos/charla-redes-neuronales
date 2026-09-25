"""Lo que se deja listo al empezar: las constantes, las semillas y el estilo de las gráficas.

Importar este archivo deja el tema oscuro puesto para todo matplotlib.
"""

import random

import matplotlib.pyplot as plt
import numpy as np
import optuna
import torch
from torchvision import models

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
CLASS_NAMES = ("no hot dog", "hot dog")
WEIGHTS = models.ResNet18_Weights.DEFAULT     # ResNet-18 ya entrenada con ImageNet
EPOCHS = 20

BACKGROUND = "#010409"
PRIMARY = "#29c4d9"
SECONDARY = "#8dbccd"
LIGHT = "#eaf6fc"
AMBER = "#caa655"
PURPLE = "#ac94f1"
GREEN = "#48d0a5"
RED = "#e06c75"

CYCLE = [PRIMARY, AMBER, PURPLE, GREEN, RED]

plt.rcParams.update({
    "font.family": "monospace",
    "font.monospace": ["JetBrains Mono", "DejaVu Sans Mono"],
    "figure.facecolor": BACKGROUND,
    "axes.facecolor": BACKGROUND,
    "axes.edgecolor": SECONDARY,
    "axes.labelcolor": SECONDARY,
    "axes.labelsize": 10,
    "axes.titlecolor": LIGHT,
    "axes.titlesize": 13,
    "axes.titlepad": 14,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": SECONDARY,
    "grid.alpha": 0.15,
    "grid.linewidth": 0.8,
    "xtick.color": SECONDARY,
    "ytick.color": SECONDARY,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.facecolor": BACKGROUND,
    "legend.edgecolor": SECONDARY,
    "legend.labelcolor": LIGHT,
    "legend.framealpha": 0.9,
    "legend.fontsize": 9,
})


def color(i):
    """El color número `i` de la paleta, dando la vuelta si se acaban."""
    return CYCLE[i % len(CYCLE)]


def canvas(title="", x_label="", y_label="", size=(9, 5)):
    """Un eje vacío, ya con el título y los nombres puestos."""
    _, ax = plt.subplots(figsize=size)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    return ax


def set_seeds(seed=42):
    """Fija el azar de random, NumPy y PyTorch para que cada corrida dé lo mismo."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    optuna.logging.set_verbosity(optuna.logging.ERROR)  # oculta los mensajes de cada trial
