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
import random
from settings import *

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
    
    # ✅ IMPLEMENTADO: Método para dibujar barra de cooldown
    def draw_cooldown_bar(self, screen, x=None, y=None, width=None, height=None):
        """
        Dibuja una barra visual del progreso del cooldown.
        
        Args:
            screen: Superficie donde dibujar
            x, y: Posición de la barra (opcional, usa valores por defecto de settings)
            width, height: Tamaño de la barra (opcional, usa valores por defecto)
        """
        # Usar valores por defecto de settings si no se especifican
        if x is None: x = COOLDOWN_BAR_X
        if y is None: y = COOLDOWN_BAR_Y  
        if width is None: width = COOLDOWN_BAR_WIDTH
        if height is None: height = COOLDOWN_BAR_HEIGHT
        
        # Fondo de la barra (gris)
        background_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, GRAY, background_rect)
        
        # Progreso de la barra
        progress = self.get_progress()
        
        # Color según el estado del cooldown
        if progress >= 1.0:
            # Listo para usar - verde brillante
            bar_color = GREEN
        elif progress >= 0.7:
            # Casi listo - amarillo
            bar_color = YELLOW
        else:
            # En cooldown - rojo
            bar_color = RED
        
        # Dibujar barra de progreso
        progress_width = int(width * progress)
        if progress_width > 0:
            progress_rect = pygame.Rect(x, y, progress_width, height)
            pygame.draw.rect(screen, bar_color, progress_rect)
        
        # Borde de la barra
        pygame.draw.rect(screen, BLACK, background_rect, 2)
        
        # ✅ IMPLEMENTADO: Texto indicativo
        if progress >= 1.0:
            # Mostrar "LISTO" cuando está disponible
            font = pygame.font.Font(None, 16)
            text = font.render("LISTO", True, WHITE)
            text_rect = text.get_rect(center=(x + width // 2, y - 12))
            screen.blit(text, text_rect)
        else:
            # Mostrar tiempo restante
            time_left = self.frames_remaining / FPS
            font = pygame.font.Font(None, 16)
            text = font.render(f"{time_left:.1f}s", True, WHITE)
            text_rect = text.get_rect(center=(x + width // 2, y - 12))
            screen.blit(text, text_rect)


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
    
    # ✅ IMPLEMENTADO: Método para mostrar efectos activos en pantalla
    def draw_active_effects(self, screen, font):
        """
        Dibuja los efectos activos en la pantalla.
        
        Args:
            screen: Superficie donde dibujar
            font: Fuente para el texto
        """
        y_offset = 140  # Posición inicial (debajo de la barra de cooldown)
        
        if self.is_vodka_active():
            # ✅ IMPLEMENTADO: Efecto visual para Vodka Boost
            time_left = f"⚡ Vodka Boost: {self.get_vodka_time_left():.1f}s"
            text = font.render(time_left, True, VODKA_COLOR)
            
            # Fondo semi-transparente para mejor legibilidad
            text_rect = text.get_rect()
            text_rect.x = 10
            text_rect.y = y_offset
            
            background_rect = pygame.Rect(text_rect.x - 2, text_rect.y - 2,
                                        text_rect.width + 4, text_rect.height + 4)
            pygame.draw.rect(screen, BLACK, background_rect)
            pygame.draw.rect(screen, VODKA_COLOR, background_rect, 1)
            
            screen.blit(text, text_rect)
            y_offset += 25
        
        if self.is_tea_active():
            # ✅ IMPLEMENTADO: Efecto visual para Té Mágico
            time_left = f"🛡️ Té Mágico: {self.get_tea_time_left():.1f}s"
            text = font.render(time_left, True, TEA_COLOR)
            
            # Fondo semi-transparente
            text_rect = text.get_rect()
            text_rect.x = 10
            text_rect.y = y_offset
            
            background_rect = pygame.Rect(text_rect.x - 2, text_rect.y - 2,
                                        text_rect.width + 4, text_rect.height + 4)
            pygame.draw.rect(screen, BLACK, background_rect)
            pygame.draw.rect(screen, TEA_COLOR, background_rect, 1)
            
            screen.blit(text, text_rect)
            y_offset += 25


# ✅ IMPLEMENTADO: Clase para efectos de partículas
class ParticleEffect:
    """
    Sistema de partículas para efectos visuales.
    
    Las partículas son pequeños elementos gráficos que se mueven
    y desaparecen para crear efectos como explosiones, chispas, etc.
    """
    
    def __init__(self, x, y, color, particle_count=10, effect_type="explosion"):
        """
        Constructor del sistema de partículas.
        
        Args:
            x, y: Posición inicial del efecto
            color: Color base de las partículas
            particle_count: Número de partículas a crear
            effect_type: Tipo de efecto ("explosion", "sparkle", "trail")
        """
        self.particles = []
        self.effect_type = effect_type
        
        for _ in range(particle_count):
            if effect_type == "explosion":
                # Partículas que salen en todas las direcciones
                angle = random.uniform(0, 2 * 3.14159)
                speed = random.uniform(1, 6)
            elif effect_type == "sparkle":
                # Partículas que suben lentamente
                angle = random.uniform(-0.5, 0.5)  # Principalmente hacia arriba
                speed = random.uniform(0.5, 2)
            else:  # "trail"
                # Partículas que caen
                angle = random.uniform(1.57 - 0.3, 1.57 + 0.3)  # Hacia abajo
                speed = random.uniform(1, 3)
            
            particle = {
                'x': x + random.uniform(-5, 5),
                'y': y + random.uniform(-5, 5),
                'vel_x': speed * pygame.math.Vector2(1, 0).rotate_rad(angle).x,
                'vel_y': speed * pygame.math.Vector2(1, 0).rotate_rad(angle).y,
                'size': random.randint(1, 4),
                'life': random.randint(20, 40),
                'max_life': 40,
                'color': color
            }
            self.particles.append(particle)
    
    def update(self):
        """
        Actualizar posición de todas las partículas.
        
        Returns:
            bool: False si todas las partículas expiraron, True si quedan activas
        """
        for particle in self.particles[:]:
            # Actualizar posición
            particle['x'] += particle['vel_x']
            particle['y'] += particle['vel_y']
            particle['life'] -= 1
            
            # Aplicar efectos físicos según el tipo
            if self.effect_type == "explosion":
                # Gravedad y fricción
                particle['vel_y'] += 0.1  # Gravedad
                particle['vel_x'] *= 0.98  # Fricción
            elif self.effect_type == "sparkle":
                # Flotación suave
                particle['vel_y'] -= 0.05  # Anti-gravedad
                particle['vel_x'] *= 0.99
            
            # Eliminar partículas muertas
            if particle['life'] <= 0:
                self.particles.remove(particle)
        
        return len(self.particles) > 0
    
    def draw(self, screen):
        """Dibujar todas las partículas."""
        for particle in self.particles:
            # Calcular alpha (transparencia) basada en vida restante
            alpha_factor = particle['life'] / particle['max_life']
            
            # Color que se desvanece
            faded_color = tuple(int(c * alpha_factor) for c in particle['color'])
            
            # Dibujar partícula
            if particle['size'] > 0:
                pygame.draw.circle(screen, faded_color,
                                 (int(particle['x']), int(particle['y'])),
                                 int(particle['size'] * alpha_factor))


# ✅ IMPLEMENTADO: Sistema de combos
class ComboSystem:
    """
    Sistema para trackear combos de acciones consecutivas.
    
    Un combo se forma cuando el jugador realiza acciones exitosas
    de manera consecutiva (ej: destruir obstáculos seguidos).
    """
    
    def __init__(self):
        """Constructor del sistema de combos."""
        self.combo_count = 0           # Número actual de combos
        self.combo_timer = 0           # Tiempo restante para mantener combo
        self.max_combo_time = 120      # 2 segundos para mantener combo activo
        self.best_combo = 0            # Mejor combo alcanzado en la partida
        self.combo_multiplier = 1.0    # Multiplicador de puntuación
    
    def add_hit(self):
        """
        Añadir golpe exitoso al combo.
        
        Se llama cuando el jugador destruye un obstáculo con un cuchillo.
        """
        self.combo_count += 1
        self.combo_timer = self.max_combo_time  # Resetear timer
        
        # Actualizar mejor combo
        if self.combo_count > self.best_combo:
            self.best_combo = self.combo_count
        
        # Calcular multiplicador (cada 5 combos aumenta 0.5x)
        self.combo_multiplier = 1.0 + (self.combo_count // 5) * 0.5
        
        print(f"¡Combo x{self.combo_count}! Multiplicador: {self.combo_multiplier:.1f}x")
    
    def add_miss(self):
        """
        El jugador falló o recibió daño - resetear combo.
        """
        if self.combo_count > 0:
            print(f"Combo perdido en x{self.combo_count}")
        self.reset_combo()
    
    def update(self):
        """Actualizar el sistema de combos cada frame."""
        if self.combo_timer > 0:
            self.combo_timer -= 1
            
            # Si se acaba el tiempo, resetear combo
            if self.combo_timer <= 0:
                self.reset_combo()
    
    def reset_combo(self):
        """Resetear combo actual."""
        self.combo_count = 0
        self.combo_timer = 0
        self.combo_multiplier = 1.0
    
    def get_combo_bonus_points(self, base_points):
        """
        Calcular puntos bonus por combo.
        
        Args:
            base_points: Puntos base de la acción
            
        Returns:
            int: Puntos totales incluyendo bonus de combo
        """
        return int(base_points * self.combo_multiplier)
    
    def draw_combo_display(self, screen, font):
        """
        Dibujar información del combo en pantalla.
        
        Args:
            screen: Superficie donde dibujar
            font: Fuente para el texto
        """
        if self.combo_count > 1:  # Solo mostrar si hay combo activo
            # Posición en la parte superior derecha
            combo_text = f"COMBO x{self.combo_count}"
            text = font.render(combo_text, True, YELLOW)
            
            # Calcular posición
            text_rect = text.get_rect()
            text_rect.right = WINDOW_WIDTH - 10
            text_rect.top = 10
            
            # Fondo semi-transparente
            background_rect = pygame.Rect(text_rect.x - 5, text_rect.y - 2,
                                        text_rect.width + 10, text_rect.height + 4)
            pygame.draw.rect(screen, BLACK, background_rect)
            pygame.draw.rect(screen, YELLOW, background_rect, 2)
            
            screen.blit(text, text_rect)
            
            # Multiplicador debajo
            if self.combo_multiplier > 1.0:
                mult_text = f"{self.combo_multiplier:.1f}x puntos"
                mult_surface = font.render(mult_text, True, GREEN)
                mult_rect = mult_surface.get_rect()
                mult_rect.right = WINDOW_WIDTH - 10
                mult_rect.top = text_rect.bottom + 2
                screen.blit(mult_surface, mult_rect)


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