"""
entities.py - Entidades del juego Julia's Run

Este archivo contiene todas las clases que representan los objetos del juego.
Cada clase encapsula los datos (atributos) y comportamientos (métodos) de una entidad.

Conceptos de POO cubiertos:
- Clases y objetos
- Atributos de instancia
- Métodos de instancia
- Encapsulación
- Uso de pygame.Rect para colisiones

Referencias útiles:
- pygame.Rect: https://www.pygame.org/docs/ref/rect.html
- pygame.draw: https://www.pygame.org/docs/ref/draw.html
"""

import pygame
import random
from .settings import *

class Player:
    """
    Esta clase representa al jugador (Julia).
    
    Atributos:
    - rect: Rectángulo para posición y colisiones (pygame.Rect)
    - lives: Número de vidas restantes
    - score: Puntuación actual
    - speed: Velocidad de movimiento actual
    - has_shield: Si tiene escudo activo del té mágico
    
    Métodos:
    - move(): Actualiza la posición según las teclas presionadas
    - draw(): Dibuja al jugador en la pantalla
    - take_damage(): Reduce una vida
    - reset_position(): Vuelve a la posición inicial
    """
    
    def __init__(self):
        """Constructor de la clase Player.
        Inicializa todos los atributos del jugador."""
        
        # pygame.Rect(x, y, width, height) - rectángulo para posición y colisiones
        self.rect = pygame.Rect(PLAYER_START_X, PLAYER_START_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        
        # Estado del jugador
        self.lives = PLAYER_LIVES
        self.score = 0
        self.speed = PLAYER_SPEED
        self.has_shield = False
        
        # TODO 5: Añadir atributo para animaciones de sprites
        # self.sprite_frame = 0
        # self.animation_timer = 0
    
    def move(self, keys_pressed):
        """
        Mueve al jugador según las teclas presionadas.
        
        Args:
            keys_pressed: Diccionario de teclas presionadas (pygame.key.get_pressed())
        """
        
        # Movimiento horizontal
        if keys_pressed[KEY_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys_pressed[KEY_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.speed
            
        # Movimiento vertical
        if keys_pressed[KEY_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys_pressed[KEY_DOWN] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += self.speed
    
    def draw(self, screen):
        """
        Dibuja al jugador en la pantalla.
        
        Args:
            screen: Superficie de pygame donde dibujar
        """
        
        # Color base del jugador
        color = PLAYER_COLOR
        
        # Si tiene escudo, cambiar color para indicarlo visualmente
        if self.has_shield:
            color = TEA_COLOR  # Verde cuando tiene escudo
        
        # pygame.draw.rect(superficie, color, rectángulo)
        pygame.draw.rect(screen, color, self.rect)
        
        # TODO 4: Reemplazar rectángulo con sprite real
        # screen.blit(self.sprite_image, self.rect)
    
    def take_damage(self):
        """
        El jugador recibe daño. Si tiene escudo, lo pierde.
        Si no tiene escudo, pierde una vida.
        
        Returns:
            bool: True si el jugador sigue vivo, False si se queda sin vidas
        """
        
        if self.has_shield:
            # El escudo absorbe el daño
            self.has_shield = False
            return True
        else:
            # Pierde una vida
            self.lives -= 1
            return self.lives > 0
    
    def reset_position(self):
        """Vuelve al jugador a su posición inicial."""
        self.rect.x = PLAYER_START_X
        self.rect.y = PLAYER_START_Y


class Obstacle:
    """
    Esta clase representa un obstáculo que cae del cielo.
    
    Los obstáculos aparecen en la parte superior de la pantalla
    y caen hacia abajo. Si tocan al jugador, le hacen daño.
    Si salen de la pantalla por abajo, dan puntos por ser esquivados.
    """
    
    def __init__(self):
        """Constructor del obstáculo. Aparece en posición aleatoria en la parte superior."""
        
        # Posición aleatoria en X, fija en Y (parte superior)
        start_x = random.randint(0, WINDOW_WIDTH - OBSTACLE_WIDTH)
        start_y = -OBSTACLE_HEIGHT  # Empieza justo arriba de la pantalla
        
        self.rect = pygame.Rect(start_x, start_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
        self.speed = OBSTACLE_SPEED
        
        # TODO 3: Añadir diferentes tipos de obstáculos
        # self.obstacle_type = random.choice(['normal', 'fast', 'big'])
    
    def update(self):
        """
        Actualiza la posición del obstáculo (lo hace caer).
        
        Returns:
            bool: False si el obstáculo salió de la pantalla, True si sigue visible
        """
        
        self.rect.y += self.speed
        
        # Retorna False si salió de la pantalla (por abajo)
        return self.rect.top < WINDOW_HEIGHT
    
    def draw(self, screen):
        """Dibuja el obstáculo en la pantalla."""
        pygame.draw.rect(screen, OBSTACLE_COLOR, self.rect)
        
        # TODO 4: Reemplazar con sprite
        # screen.blit(self.sprite_image, self.rect)


class Knife:
    """
    Esta clase representa un cuchillo lanzado por el jugador.
    
    Los cuchillos se mueven hacia arriba y pueden destruir obstáculos.
    Desaparecen cuando salen de la pantalla por arriba.
    """
    
    def __init__(self, player_rect):
        """
        Constructor del cuchillo. Aparece en la posición del jugador.
        
        Args:
            player_rect: Rectángulo del jugador para saber dónde aparecer
        """
        
        # El cuchillo aparece en el centro superior del jugador
        start_x = player_rect.centerx - KNIFE_WIDTH // 2
        start_y = player_rect.top
        
        self.rect = pygame.Rect(start_x, start_y, KNIFE_WIDTH, KNIFE_HEIGHT)
        self.speed = KNIFE_SPEED
    
    def update(self):
        """
        Actualiza la posición del cuchillo (lo hace subir).
        
        Returns:
            bool: False si el cuchillo salió de la pantalla, True si sigue visible
        """
        
        self.rect.y -= self.speed
        
        # Retorna False si salió de la pantalla (por arriba)
        return self.rect.bottom > 0
    
    def draw(self, screen):
        """Dibuja el cuchillo en la pantalla."""
        pygame.draw.rect(screen, KNIFE_COLOR, self.rect)
        
        # TODO 4: Reemplazar con sprite
        # screen.blit(self.sprite_image, self.rect)


class PowerUp:
    """
    Esta clase representa un power-up (Vodka Boost o Té Mágico).
    
    Los power-ups aparecen ocasionalmente y dan efectos especiales
    cuando el jugador los recoge.
    """
    
    def __init__(self, powerup_type):
        """
        Constructor del power-up.
        
        Args:
            powerup_type: Tipo de power-up ('vodka' o 'tea')
        """
        
        # Posición aleatoria en X, fija en Y (parte superior)
        start_x = random.randint(0, WINDOW_WIDTH - POWERUP_WIDTH)
        start_y = -POWERUP_HEIGHT
        
        self.rect = pygame.Rect(start_x, start_y, POWERUP_WIDTH, POWERUP_HEIGHT)
        self.type = powerup_type
        self.speed = POWERUP_SPEED
        
        # Color según el tipo
        if powerup_type == 'vodka':
            self.color = VODKA_COLOR
        else:  # 'tea'
            self.color = TEA_COLOR
    
    def update(self):
        """
        Actualiza la posición del power-up.
        
        Returns:
            bool: False si salió de la pantalla, True si sigue visible
        """
        
        self.rect.y += self.speed
        return self.rect.top < WINDOW_HEIGHT
    
    def draw(self, screen):
        """Dibuja el power-up en la pantalla."""
        pygame.draw.rect(screen, self.color, self.rect)
        
        # TODO 4: Reemplazar con sprites diferentes para cada tipo
        # if self.type == 'vodka':
        #     screen.blit(self.vodka_sprite, self.rect)
        # else:
        #     screen.blit(self.tea_sprite, self.rect)


# TODO 8: Crear clase Enemy para enemigos más complejos
# class Enemy(Obstacle):
#     """Enemigo que se mueve de forma más inteligente que un obstáculo simple."""
#     pass

# TODO 9: Crear clase Explosion para efectos visuales
# class Explosion:
#     """Efecto visual cuando se destruye un obstáculo."""
#     pass

# === NOTAS EDUCATIVAS ===
"""
Conceptos importantes de POO demostrados aquí:

1. ENCAPSULACIÓN: Cada clase mantiene sus propios datos (atributos)
   y los métodos que operan sobre esos datos.

2. RESPONSABILIDAD ÚNICA: Cada clase tiene una responsabilidad clara:
   - Player: Gestionar al jugador
   - Obstacle: Gestionar obstáculos
   - Knife: Gestionar proyectiles
   - PowerUp: Gestionar power-ups

3. PYGAME.RECT: Usamos pygame.Rect para:
   - Posición (x, y)
   - Tamaño (width, height)
   - Detección de colisiones
   - Límites de pantalla

4. MÉTODOS COMUNES: Todas las entidades móviles tienen:
   - update(): Actualizar lógica
   - draw(): Dibujar en pantalla

5. CONSTRUCTOR (__init__): Inicializa el estado de cada objeto
   cuando se crea una nueva instancia.

Para estudiantes: Experimenten cambiando los valores en settings.py
y vean cómo afecta el comportamiento de estas clases.
"""