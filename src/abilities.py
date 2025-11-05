"""
abilities.py - Sistema de habilidades y efectos temporales

Este archivo gestiona los cooldowns de habilidades y los efectos temporales
de los power-ups en Julia's Run.

Conceptos de programación cubiertos:
- Gestión de tiempo en juegos
- Clases para funcionalidades específicas
- Efectos temporales
- Estados booleanos

Referencias útiles:
- pygame.time: https://www.pygame.org/docs/ref/time.html
"""

import pygame
from .settings import *

class CooldownTimer:
    """
    Esta clase gestiona el tiempo de cooldown entre lanzamientos de cuchillos.
    
    Un cooldown es un período de tiempo durante el cual una acción no puede
    realizarse de nuevo. Esto evita que el jugador dispare infinitos cuchillos
    instantáneamente, haciendo el juego más equilibrado.
    
    Atributos:
    - frames_remaining: Frames que faltan para poder usar la habilidad otra vez
    - max_cooldown: Duración total del cooldown en frames
    """
    
    def __init__(self, cooldown_frames):
        """
        Constructor del timer de cooldown.
        
        Args:
            cooldown_frames: Duración del cooldown en frames
        """
        self.max_cooldown = cooldown_frames
        self.frames_remaining = 0  # Empieza sin cooldown
    
    def start_cooldown(self):
        """Inicia el cooldown (llamar cuando se use la habilidad)."""
        self.frames_remaining = self.max_cooldown
    
    def update(self):
        """
        Actualiza el timer (llamar cada frame).
        Reduce el contador si está activo.
        """
        if self.frames_remaining > 0:
            self.frames_remaining -= 1
    
    def is_ready(self):
        """
        Comprueba si la habilidad está lista para usar.
        
        Returns:
            bool: True si no hay cooldown activo, False si aún está en cooldown
        """
        return self.frames_remaining <= 0
    
    def get_progress(self):
        """
        Obtiene el progreso del cooldown como porcentaje.
        Útil para dibujar barras de progreso.
        
        Returns:
            float: Valor entre 0.0 (cooldown completo) y 1.0 (listo para usar)
        """
        if self.max_cooldown == 0:
            return 1.0
        
        progress = 1.0 - (self.frames_remaining / self.max_cooldown)
        return max(0.0, min(1.0, progress))  # Asegurar que esté entre 0 y 1
    
    # TODO 2: Método para dibujar barra de cooldown
    def draw_cooldown_bar(self, screen, x, y, width, height):
        """
        Dibuja una barra visual del progreso del cooldown.
        
        Args:
            screen: Superficie donde dibujar
            x, y: Posición de la barra
            width, height: Tamaño de la barra
        """
        # Fondo de la barra (gris)
        background_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, GRAY, background_rect)
        
        # Progreso de la barra (verde)
        progress = self.get_progress()
        progress_width = int(width * progress)
        if progress_width > 0:
            progress_rect = pygame.Rect(x, y, progress_width, height)
            pygame.draw.rect(screen, GREEN, progress_rect)
        
        # Borde de la barra
        pygame.draw.rect(screen, BLACK, background_rect, 2)


class PowerUpEffect:
    """
    Esta clase gestiona los efectos temporales de los power-ups.
    
    Cuando el jugador recoge un power-up, se activa un efecto que dura
    un tiempo determinado. Esta clase maneja la duración y el estado
    de estos efectos.
    """
    
    def __init__(self):
        """Constructor del sistema de efectos de power-ups."""
        
        # Timers para cada tipo de power-up
        self.vodka_timer = 0      # Frames restantes del efecto Vodka Boost
        self.tea_timer = 0        # Frames restantes del efecto Té Mágico
        
        # Estado original del jugador (para restaurar después)
        self.original_speed = PLAYER_SPEED
    
    def activate_vodka_boost(self, player):
        """
        Activa el efecto Vodka Boost (aumenta velocidad).
        
        Args:
            player: Instancia del jugador para modificar su velocidad
        """
        
        self.vodka_timer = VODKA_DURATION
        
        # Aumentar la velocidad del jugador
        player.speed = int(self.original_speed * VODKA_SPEED_MULTIPLIER)
        
        # TODO 4: Añadir efecto sonoro
        # pygame.mixer.Sound(SOUND_POWERUP).play()
        
        print("¡Vodka Boost activado! Velocidad aumentada.")  # Debug
    
    def activate_tea_shield(self, player):
        """
        Activa el efecto Té Mágico (escudo protector).
        
        Args:
            player: Instancia del jugador para darle el escudo
        """
        
        self.tea_timer = TEA_DURATION
        
        # Activar escudo
        player.has_shield = True
        
        # TODO 4: Añadir efecto sonoro
        # pygame.mixer.Sound(SOUND_POWERUP).play()
        
        print("¡Té Mágico activado! Escudo protector obtenido.")  # Debug
    
    def update(self, player):
        """
        Actualiza todos los efectos activos (llamar cada frame).
        
        Args:
            player: Instancia del jugador para modificar sus atributos
        """
        
        # Actualizar Vodka Boost
        if self.vodka_timer > 0:
            self.vodka_timer -= 1
            
            # Si el efecto termina, restaurar velocidad normal
            if self.vodka_timer == 0:
                player.speed = self.original_speed
                print("Vodka Boost terminado. Velocidad normal restaurada.")  # Debug
        
        # Actualizar Té Mágico
        if self.tea_timer > 0:
            self.tea_timer -= 1
            
            # Si el efecto termina, quitar escudo
            if self.tea_timer == 0:
                player.has_shield = False
                print("Té Mágico terminado. Escudo desactivado.")  # Debug
    
    def is_vodka_active(self):
        """Comprueba si el efecto Vodka Boost está activo."""
        return self.vodka_timer > 0
    
    def is_tea_active(self):
        """Comprueba si el efecto Té Mágico está activo."""
        return self.tea_timer > 0
    
    def get_vodka_time_left(self):
        """Obtiene el tiempo restante del Vodka Boost en segundos."""
        return self.vodka_timer / FPS
    
    def get_tea_time_left(self):
        """Obtiene el tiempo restante del Té Mágico en segundos."""
        return self.tea_timer / FPS
    
    # TODO 6: Método para mostrar efectos activos en pantalla
    def draw_active_effects(self, screen, font):
        """
        Dibuja los efectos activos en la pantalla.
        
        Args:
            screen: Superficie donde dibujar
            font: Fuente para el texto
        """
        y_offset = 10
        
        if self.is_vodka_active():
            time_left = f"Vodka Boost: {self.get_vodka_time_left():.1f}s"
            text = font.render(time_left, True, VODKA_COLOR)
            screen.blit(text, (10, y_offset))
            y_offset += 25
        
        if self.is_tea_active():
            time_left = f"Té Mágico: {self.get_tea_time_left():.1f}s"
            text = font.render(time_left, True, TEA_COLOR)
            screen.blit(text, (10, y_offset))


# TODO 7: Clase para efectos de partículas
# class ParticleEffect:
#     """Sistema de partículas para efectos visuales."""
#     
#     def __init__(self, x, y, color, particle_count=10):
#         self.particles = []
#         for _ in range(particle_count):
#             # Crear partículas con velocidades aleatorias
#             pass
#     
#     def update(self):
#         # Actualizar posición de todas las partículas
#         pass
#     
#     def draw(self, screen):
#         # Dibujar todas las partículas
#         pass

# TODO 8: Sistema de combos
# class ComboSystem:
#     """Sistema para trackear combos de acciones consecutivas."""
#     
#     def __init__(self):
#         self.combo_count = 0
#         self.combo_timer = 0
#         self.max_combo_time = 120  # 2 segundos
#     
#     def add_hit(self):
#         # Añadir golpe al combo
#         pass
#     
#     def reset_combo(self):
#         # Resetear combo
#         pass

# === NOTAS EDUCATIVAS ===
"""
Conceptos importantes sobre gestión de tiempo en juegos:

1. FRAMES vs SEGUNDOS:
   - Los juegos se ejecutan a X frames por segundo (FPS)
   - Para efectos de tiempo, contamos frames y convertimos a segundos
   - Ejemplo: 60 frames = 1 segundo a 60 FPS

2. COOLDOWNS:
   - Previenen spam de acciones
   - Hacen el juego más estratégico
   - Se implementan con contadores de frames

3. EFECTOS TEMPORALES:
   - Modifican temporalmente las propiedades del jugador
   - Deben restaurar el estado original cuando terminan
   - Se pueden acumular o sobrescribir según el diseño

4. ESTADO TEMPORAL:
   - Importante guardar valores originales para restaurar
   - Usar flags booleanos para estados on/off
   - Considerar qué pasa si se recoge el mismo power-up dos veces

Ejercicio para estudiantes:
- Cambiar VODKA_DURATION y VODKA_SPEED_MULTIPLIER en settings.py
- Observar cómo afecta la jugabilidad
- ¿Qué valores hacen el juego más divertido?
"""