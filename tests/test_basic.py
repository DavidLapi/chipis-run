# test_basic

import sys
import os

# Obtener la ruta del directorio padre (chipis-run/)
ruta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Añadir al path
sys.path.append(ruta_proyecto)

# Importar entities
from src.entities import Player

def test_player_starts_with_three_lives():
       player = Player()
       assert player.lives == 3