"""
Julia's Run - Un juego educativo de Python + Pygame

Este paquete contiene todos los módulos del juego Julia's Run,
diseñado para enseñar programación orientada a objetos.

Módulos:
- main: Punto de entrada y game loop principal
- settings: Configuración y constantes del juego
- entities: Clases de entidades (Player, Obstacle, etc.)
- abilities: Sistema de power-ups y cooldowns
- game_states: Estados del juego (menú, juego, game over)
- utils: Funciones auxiliares y utilidades

Para ejecutar el juego:
    python -m src.main

Versión: 1.0.0
Autor: Proyecto Educativo
"""

__version__ = "1.0.0"
__author__ = "Proyecto Educativo"

# Importaciones principales para facilitar el uso del paquete
from .main import JuliasRunGame
from .settings import *

# TODO: Añadir más exports cuando sea necesario