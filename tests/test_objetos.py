# test_objetos

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.entities import Player, Obstacle

def test_objects():
    # Crear dos jugadores diferentes
    chipi = Player()
    antonio = Player()

    # Son objetos diferentes aunque sean de la misma clase
    print("\nVidas de los jugadores:")
    print(f"Chipi Vidas: {chipi.lives}") # 3
    print(f"Antonio vidas: {antonio.lives}") # 3

    # Modificar una vida no afecta al otro
    print("\nAntonio pierde una vida...")
    antonio.take_damage()
    print(f"Chipi Vidas: {chipi.lives}") # 3 (sin cambios)
    print(f"Antonio vidas: {antonio.lives}") # 2

    # Crear obstáculos diferentes
    print("\nVelocidades de los enemigos:")
    chapa = Obstacle(1.0) # Normal
    chipiron = Obstacle(2.0) # Más dificil

    print(f"Velocidad Chapa: {chapa.speed}") # Velocidad normal
    print(f"Velocidad Chipiron: {chipiron.speed}") # Muy rápido
