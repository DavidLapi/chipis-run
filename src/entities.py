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
import os
from settings import *

# === GESTIÓN DE SPRITES ===
"""
Este módulo incluye la carga y renderizado de sprites (imágenes) en lugar de rectángulos.

Conceptos importantes sobre sprites en pygame:
1. pygame.image.load() - Carga una imagen desde archivo
2. convert_alpha() - Optimiza la imagen para mejor rendimiento y soporte de transparencia
3. transform.scale() - Redimensiona la imagen al tamaño deseado
4. screen.blit() - Dibuja la imagen en la pantalla en una posición específica

Diferencias entre pygame.draw y blit:
- pygame.draw: Dibuja formas geométricas (rectángulos, círculos, líneas)
- screen.blit: Dibuja imágenes/sprites cargados desde archivos

¿Por qué usar convert_alpha()?
- Mejora significativamente el rendimiento al dibujar
- Preserva la transparencia del fondo (canal alpha)
- Adapta el formato de píxeles al de la pantalla

Gestión de errores:
- Siempre incluimos fallbacks en caso de que las imágenes no existan
- El juego debe funcionar correctamente aunque falten sprites
"""

def load_sprite_with_fallback(sprite_path, fallback_color, width, height):
    """
    Función auxiliar para cargar sprites con fallback seguro.
    
    Args:
        sprite_path: Ruta al archivo de imagen
        fallback_color: Color a usar si la imagen no se encuentra
        width, height: Dimensiones para escalar la imagen
    
    Returns:
        tuple: (imagen_cargada, es_fallback_boolean)
    """
    try:
        if os.path.exists(sprite_path):
            # Cargar imagen original
            image = pygame.image.load(sprite_path)
            
            # convert_alpha() optimiza la imagen y preserva transparencia
            image = image.convert_alpha()
            
            # Escalar al tamaño deseado - pygame.transform.scale()
            image = pygame.transform.scale(image, (width, height))
            
            return image, False  # Imagen cargada exitosamente
        else:
            # Crear sprite fallback si no existe la imagen
            return create_fallback_sprite(fallback_color, width, height), True
            
    except (pygame.error, FileNotFoundError, OSError) as e:
        print(f"⚠️ Error cargando sprite {sprite_path}: {e}")
        print(f"   Usando fallback de color {fallback_color}")
        return create_fallback_sprite(fallback_color, width, height), True

def create_fallback_sprite(color, width, height):
    """
    Crea un sprite de fallback (rectángulo de color) cuando la imagen no está disponible.
    
    Args:
        color: Color RGB del fallback
        width, height: Dimensiones del sprite
    
    Returns:
        pygame.Surface: Superficie con el color especificado
    """
    # Crear una superficie con transparencia
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Rellenar con el color especificado
    surface.fill(color)
    
    # Añadir un borde para distinguir que es un fallback
    pygame.draw.rect(surface, WHITE, surface.get_rect(), 2)
    
    return surface

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
        
        # === CARGA DE SPRITE PARA JULIA ===
        # Intentar cargar sprite de Julia
        sprite_path = os.path.join("assets", "sprites", "julia_pixelart.jpg")
        self.sprite, self.using_fallback = load_sprite_with_fallback(
            sprite_path, 
            PLAYER_COLOR,  # Color fallback si no hay imagen
            PLAYER_WIDTH, 
            PLAYER_HEIGHT
        )
        
        # ✅ IMPLEMENTADO: Atributos para animaciones de sprites
        self.sprite_frame = 0          # Frame actual de animación
        self.animation_timer = 0       # Contador para cambio de frames
        self.facing_direction = 1      # 1 = derecha, -1 = izquierda
        
        # ✅ IMPLEMENTADO: Efectos visuales
        self.hit_flash_timer = 0       # Timer para efecto de parpadeo al recibir daño
        self.invulnerability_timer = 0 # Frames de invulnerabilidad después de recibir daño
        
        # Debug info para desarrollo
        if self.using_fallback:
            print("🎮 Player: Usando rectángulo fallback (imagen no encontrada)")
        else:
            print("🎮 Player: Sprite cargado exitosamente desde", sprite_path)
    
    def move(self, keys_pressed):
        """
        Mueve al jugador según las teclas presionadas.
        
        Args:
            keys_pressed: Diccionario de teclas presionadas (pygame.key.get_pressed())
        """
        
        # ✅ IMPLEMENTADO: Actualizar animación
        self.animation_timer += 1
        if self.animation_timer >= SPRITE_ANIMATION_SPEED:
            self.sprite_frame = (self.sprite_frame + 1) % 4  # 4 frames de animación
            self.animation_timer = 0
        
        # ✅ IMPLEMENTADO: Actualizar timers de efectos
        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= 1
        if self.invulnerability_timer > 0:
            self.invulnerability_timer -= 1
        
        # Variable para detectar si se está moviendo (para animación)
        is_moving = False
        
        # Movimiento horizontal
        if keys_pressed[KEY_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.facing_direction = -1  # Mirando hacia la izquierda
            is_moving = True
        if keys_pressed[KEY_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.speed
            self.facing_direction = 1   # Mirando hacia la derecha
            is_moving = True
            
        # Movimiento vertical
        if keys_pressed[KEY_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
            is_moving = True
        if keys_pressed[KEY_DOWN] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += self.speed
            is_moving = True
        
        # ✅ IMPLEMENTADO: Resetear animación si no se mueve
        if not is_moving:
            self.sprite_frame = 0  # Frame estático cuando no se mueve
    
    def draw(self, screen):
        """
        Dibuja al jugador en la pantalla.
        
        Args:
            screen: Superficie de pygame donde dibujar
        """
        
        # ✅ IMPLEMENTADO: Efecto de parpadeo cuando recibe daño
        if self.hit_flash_timer > 0 and self.hit_flash_timer % 4 < 2:
            return  # No dibujar cada 2 frames para crear efecto de parpadeo
        
        # === RENDERIZADO DE SPRITE O FALLBACK ===
        if self.using_fallback:
            # Si usamos fallback, dibujar rectángulo mejorado
            # Color base del jugador
            color = PLAYER_COLOR
            
            # Si tiene escudo, cambiar color para indicarlo visualmente
            if self.has_shield:
                color = TEA_COLOR  # Verde cuando tiene escudo
                
                # ✅ IMPLEMENTADO: Efecto de pulso para el escudo
                pulse = abs((pygame.time.get_ticks() // 200) % 2)  # Cambia cada 200ms
                if pulse:
                    # Hacer el color más brillante
                    color = tuple(min(255, c + 50) for c in color)
            
            # pygame.draw.rect(superficie, color, rectángulo)
            pygame.draw.rect(screen, color, self.rect)
            
            # ✅ IMPLEMENTADO: Dibujar dirección con un pequeño indicador
            # Pequeño triángulo para mostrar hacia dónde mira
            if self.facing_direction == 1:  # Derecha
                points = [(self.rect.right, self.rect.centery),
                         (self.rect.right - 8, self.rect.centery - 4),
                         (self.rect.right - 8, self.rect.centery + 4)]
            else:  # Izquierda
                points = [(self.rect.left, self.rect.centery),
                         (self.rect.left + 8, self.rect.centery - 4),
                         (self.rect.left + 8, self.rect.centery + 4)]
            
            pygame.draw.polygon(screen, WHITE, points)
        
        else:
            # === RENDERIZADO DE SPRITE REAL ===
            sprite_to_draw = self.sprite
            
            # Si está mirando hacia la izquierda, voltear el sprite
            if self.facing_direction == -1:
                sprite_to_draw = pygame.transform.flip(self.sprite, True, False)
            
            # Si tiene escudo, aplicar tinte verdoso
            if self.has_shield:
                # Crear una copia del sprite con tinte
                sprite_to_draw = sprite_to_draw.copy()
                
                # Crear superficie de tinte
                tint_surface = pygame.Surface(sprite_to_draw.get_size(), pygame.SRCALPHA)
                tint_surface.fill((*TEA_COLOR, 100))  # Verde semi-transparente
                
                # Aplicar tinte al sprite
                sprite_to_draw.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
            
            # Dibujar el sprite en la posición del rectángulo
            screen.blit(sprite_to_draw, self.rect)
        
        # ✅ IMPLEMENTADO: Borde adicional si es invulnerable
        if self.invulnerability_timer > 0:
            # Dibujar borde de invulnerabilidad
            border_rect = pygame.Rect(self.rect.x - 2, self.rect.y - 2, 
                                    self.rect.width + 4, self.rect.height + 4)
            pygame.draw.rect(screen, YELLOW, border_rect, 2)
    
    def take_damage(self):
        """
        El jugador recibe daño. Si tiene escudo, lo pierde.
        Si no tiene escudo, pierde una vida.
        
        Returns:
            bool: True si el jugador sigue vivo, False si se queda sin vidas
        """
        
        # ✅ IMPLEMENTADO: No recibir daño si está en período de invulnerabilidad
        if self.invulnerability_timer > 0:
            return True  # Aún invulnerable, no recibir daño
        
        if self.has_shield:
            # El escudo absorbe el daño
            self.has_shield = False
            # ✅ IMPLEMENTADO: Efecto visual al perder escudo
            self.hit_flash_timer = 20  # 20 frames de parpadeo
            print("¡Escudo perdido!")  # Mensaje educativo para debug
            return True
        else:
            # Pierde una vida
            self.lives -= 1
            # ✅ IMPLEMENTADO: Período de invulnerabilidad tras recibir daño
            self.invulnerability_timer = 60  # 1 segundo de invulnerabilidad
            self.hit_flash_timer = 30        # 30 frames de parpadeo
            print(f"¡Vida perdida! Vidas restantes: {self.lives}")  # Debug educativo
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
    
    def __init__(self, difficulty_multiplier=1.0):
        """Constructor del obstáculo. Aparece en posición aleatoria en la parte superior."""
        
        # Posición aleatoria en X, fija en Y (parte superior)
        start_x = random.randint(0, WINDOW_WIDTH - OBSTACLE_WIDTH)
        start_y = -OBSTACLE_HEIGHT  # Empieza justo arriba de la pantalla
        
        self.rect = pygame.Rect(start_x, start_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
        
        # ✅ IMPLEMENTADO: Diferentes tipos de obstáculos
        self.obstacle_type = random.choice(['normal', 'fast', 'big'])
        
        # Ajustar propiedades según el tipo
        if self.obstacle_type == 'fast':
            self.speed = int(OBSTACLE_SPEED * 1.5 * difficulty_multiplier)
            self.color = RED
            # Los rápidos son más pequeños
            self.rect.width = OBSTACLE_WIDTH - 5
            self.rect.height = OBSTACLE_HEIGHT - 5
            
        elif self.obstacle_type == 'big':
            self.speed = int(OBSTACLE_SPEED * 0.7 * difficulty_multiplier)
            # Los grandes son más lentos pero más difíciles de esquivar
            self.rect.width = OBSTACLE_WIDTH + 15
            self.rect.height = OBSTACLE_HEIGHT + 15
            self.color = (150, 0, 0)  # Rojo más oscuro
            
        else:  # 'normal'
            self.speed = int(OBSTACLE_SPEED * difficulty_multiplier)
            self.color = OBSTACLE_COLOR
        
        # === CARGA DE SPRITE PARA CACHOPO (OBSTÁCULO) ===
        # Intentar cargar sprite del cachopo
        sprite_path = os.path.join("assets", "sprites", "cachopo_pixelart.jpg")
        self.sprite, self.using_fallback = load_sprite_with_fallback(
            sprite_path, 
            self.color,  # Color fallback específico del tipo
            self.rect.width, 
            self.rect.height
        )
        
        # ✅ IMPLEMENTADO: Efectos visuales
        self.rotation = 0  # Para rotación visual
        self.pulse_timer = random.randint(0, 60)  # Para efecto de pulso
        
        # Debug info para desarrollo
        if self.using_fallback:
            print(f"🍖 Obstacle ({self.obstacle_type}): Usando rectángulo fallback")
        else:
            print(f"🍖 Obstacle ({self.obstacle_type}): Sprite cargado desde", sprite_path)
    
    def update(self):
        """
        Actualiza la posición del obstáculo (lo hace caer).
        
        Returns:
            bool: False si el obstáculo salió de la pantalla, True si sigue visible
        """
        
        self.rect.y += self.speed
        
        # ✅ IMPLEMENTADO: Actualizar efectos visuales
        self.rotation += 2  # Rotación lenta para efecto visual
        self.pulse_timer += 1
        
        # Retorna False si salió de la pantalla (por abajo)
        return self.rect.top < WINDOW_HEIGHT
    
    def draw(self, screen):
        """Dibuja el obstáculo en la pantalla."""
        
        # === RENDERIZADO DE SPRITE O FALLBACK ===
        if self.using_fallback:
            # Si usamos fallback, dibujar rectángulo mejorado
            # ✅ IMPLEMENTADO: Efecto de pulso para obstáculos
            base_color = self.color
            pulse_offset = int(abs(pygame.math.Vector2(1, 0).rotate(self.pulse_timer * 6).x) * 20)
            pulse_color = tuple(min(255, max(0, c + pulse_offset)) for c in base_color)
            
            # Dibujar el obstáculo principal
            pygame.draw.rect(screen, pulse_color, self.rect)
            
            # ✅ IMPLEMENTADO: Indicador visual del tipo de obstáculo
            if self.obstacle_type == 'fast':
                # Líneas para indicar velocidad
                for i in range(3):
                    line_y = self.rect.centery - 6 + i * 6
                    pygame.draw.line(screen, WHITE, 
                                   (self.rect.left + 2, line_y), 
                                   (self.rect.right - 2, line_y), 1)
            
            elif self.obstacle_type == 'big':
                # Cruz para indicar peligro
                pygame.draw.line(screen, WHITE,
                               (self.rect.left + 3, self.rect.top + 3),
                               (self.rect.right - 3, self.rect.bottom - 3), 2)
                pygame.draw.line(screen, WHITE,
                               (self.rect.right - 3, self.rect.top + 3),
                               (self.rect.left + 3, self.rect.bottom - 3), 2)
            
            # Borde del obstáculo
            pygame.draw.rect(screen, BLACK, self.rect, 1)
            
        else:
            # === RENDERIZADO DE SPRITE REAL ===
            sprite_to_draw = self.sprite
            
            # Aplicar rotación visual si el obstáculo está cayendo
            if self.rotation != 0:
                # Rotar sprite alrededor de su centro
                sprite_to_draw = pygame.transform.rotate(self.sprite, self.rotation)
                
                # Calcular nueva posición para que el centro se mantenga
                old_center = self.rect.center
                new_rect = sprite_to_draw.get_rect()
                new_rect.center = old_center
                
                # Dibujar sprite rotado
                screen.blit(sprite_to_draw, new_rect)
            else:
                # Dibujar sprite normal
                screen.blit(sprite_to_draw, self.rect)
            
            # ✅ IMPLEMENTADO: Indicadores sobre el sprite para diferentes tipos
            if self.obstacle_type == 'fast':
                # Efecto de velocidad: líneas semi-transparentes
                for i in range(3):
                    line_y = self.rect.centery - 6 + i * 6
                    pygame.draw.line(screen, (255, 255, 255, 150), 
                                   (self.rect.left - 10, line_y), 
                                   (self.rect.left - 5, line_y), 2)
            
            elif self.obstacle_type == 'big':
                # Indicador de peligro: borde rojo
                pygame.draw.rect(screen, RED, self.rect, 3)


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
        
        # === CARGA DE SPRITE PARA CUCHILLO ===
        # Intentar cargar sprite del cuchillo
        sprite_path = os.path.join("assets", "sprites", "knife__pixelart.jpg")
        self.sprite, self.using_fallback = load_sprite_with_fallback(
            sprite_path, 
            KNIFE_COLOR,  # Color fallback
            KNIFE_WIDTH, 
            KNIFE_HEIGHT
        )
        
        # Efectos visuales para el cuchillo
        self.rotation = 0  # Para rotación durante el vuelo
        
        # Debug info para desarrollo
        if self.using_fallback:
            print("🔪 Knife: Usando rectángulo fallback (imagen no encontrada)")
        else:
            print("🔪 Knife: Sprite cargado exitosamente desde", sprite_path)
    
    def update(self):
        """
        Actualiza la posición del cuchillo (lo hace subir).
        
        Returns:
            bool: False si el cuchillo salió de la pantalla, True si sigue visible
        """
        
        self.rect.y -= self.speed
        
        # Efecto de rotación durante el vuelo
        self.rotation += 10  # Rotación rápida para efecto dinámico
        
        # Retorna False si salió de la pantalla (por arriba)
        return self.rect.bottom > 0
    
    def draw(self, screen):
        """Dibuja el cuchillo en la pantalla."""
        
        # === RENDERIZADO DE SPRITE O FALLBACK ===
        if self.using_fallback:
            # Dibujar rectángulo fallback
            pygame.draw.rect(screen, KNIFE_COLOR, self.rect)
            
            # Añadir una punta para que parezca más un cuchillo
            tip_points = [(self.rect.centerx, self.rect.top - 3),
                         (self.rect.left + 2, self.rect.top + 3),
                         (self.rect.right - 2, self.rect.top + 3)]
            pygame.draw.polygon(screen, KNIFE_COLOR, tip_points)
            
        else:
            # === RENDERIZADO DE SPRITE REAL ===
            sprite_to_draw = self.sprite
            
            # Aplicar rotación al sprite
            if self.rotation != 0:
                # Rotar sprite alrededor de su centro
                sprite_to_draw = pygame.transform.rotate(self.sprite, self.rotation)
                
                # Calcular nueva posición para que el centro se mantenga
                old_center = self.rect.center
                new_rect = sprite_to_draw.get_rect()
                new_rect.center = old_center
                
                # Dibujar sprite rotado
                screen.blit(sprite_to_draw, new_rect)
            else:
                # Dibujar sprite normal
                screen.blit(sprite_to_draw, self.rect)


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
            self.symbol = "V"  # Símbolo para identificar visualmente
            # === CARGA DE SPRITE PARA VODKA ===
            sprite_path = os.path.join("assets", "sprites", "vodka_pixelart.jpg")
        else:  # 'tea'
            self.color = TEA_COLOR
            self.symbol = "T"
            # Para el té, usar el mismo sprite de vodka como placeholder
            # (en un juego real tendrías un sprite específico para cada power-up)
            sprite_path = os.path.join("assets", "sprites", "vodka_pixelart.jpg")
        
        # Cargar sprite del power-up
        self.sprite, self.using_fallback = load_sprite_with_fallback(
            sprite_path, 
            self.color,  # Color fallback específico del tipo
            POWERUP_WIDTH, 
            POWERUP_HEIGHT
        )
        
        # ✅ IMPLEMENTADO: Efectos visuales para power-ups
        self.pulse_timer = 0           # Para efecto de pulso
        self.float_offset = 0          # Para efecto de flotación
        self.sparkle_timer = 0         # Para efecto de brillo
        self.original_y = start_y      # Posición Y original para flotación
        
        # Debug info para desarrollo
        if self.using_fallback:
            print(f"🍺 PowerUp ({powerup_type}): Usando rectángulo fallback")
        else:
            print(f"🍺 PowerUp ({powerup_type}): Sprite cargado desde", sprite_path)
    
    def update(self):
        """
        Actualiza la posición del power-up.
        
        Returns:
            bool: False si salió de la pantalla, True si sigue visible
        """
        
        # ✅ IMPLEMENTADO: Movimiento principal + efecto de flotación
        self.rect.y += self.speed
        
        # Actualizar timers de efectos
        self.pulse_timer += 1
        self.sparkle_timer += 1
        
        # Efecto de flotación sutil (movimiento ondulante)
        self.float_offset = pygame.math.Vector2(1, 0).rotate(self.pulse_timer * 3).y * 2
        
        return self.rect.top < WINDOW_HEIGHT
    
    def draw(self, screen):
        """Dibuja el power-up en la pantalla."""
        
        # ✅ IMPLEMENTADO: Posición con efecto de flotación
        draw_rect = pygame.Rect(self.rect.x, self.rect.y + self.float_offset, 
                               self.rect.width, self.rect.height)
        
        # === RENDERIZADO DE SPRITE O FALLBACK ===
        if self.using_fallback:
            # ✅ IMPLEMENTADO: Efecto de pulso en el color
            pulse_intensity = abs(pygame.math.Vector2(1, 0).rotate(self.pulse_timer * POWERUP_PULSE_SPEED).x)
            base_color = self.color
            pulse_color = tuple(int(c * (0.7 + 0.3 * pulse_intensity)) for c in base_color)
            
            # Dibujar el power-up principal
            pygame.draw.rect(screen, pulse_color, draw_rect)
            
            # ✅ IMPLEMENTADO: Borde brillante
            border_color = tuple(min(255, c + 50) for c in base_color)
            pygame.draw.rect(screen, border_color, draw_rect, 2)
            
            # ✅ IMPLEMENTADO: Símbolo identificativo en el centro
            font = pygame.font.Font(None, 20)
            text = font.render(self.symbol, True, WHITE)
            text_rect = text.get_rect(center=draw_rect.center)
            screen.blit(text, text_rect)
            
        else:
            # === RENDERIZADO DE SPRITE REAL ===
            sprite_to_draw = self.sprite
            
            # Aplicar efecto de pulso escalando el sprite
            pulse_intensity = abs(pygame.math.Vector2(1, 0).rotate(self.pulse_timer * POWERUP_PULSE_SPEED).x)
            scale_factor = 0.9 + 0.2 * pulse_intensity  # Escala entre 0.9 y 1.1
            
            if scale_factor != 1.0:
                # Escalar sprite para efecto de pulso
                scaled_size = (int(self.rect.width * scale_factor), 
                              int(self.rect.height * scale_factor))
                sprite_to_draw = pygame.transform.scale(self.sprite, scaled_size)
                
                # Calcular posición centrada
                scaled_rect = sprite_to_draw.get_rect()
                scaled_rect.center = draw_rect.center
                
                # Dibujar sprite escalado
                screen.blit(sprite_to_draw, scaled_rect)
            else:
                # Dibujar sprite normal
                screen.blit(sprite_to_draw, draw_rect)
            
            # Aplicar tinte de color según el tipo (para distinguir vodka de té)
            if self.type == 'tea':
                # Crear superficie de tinte para el té
                tint_surface = pygame.Surface(draw_rect.size, pygame.SRCALPHA)
                tint_surface.fill((*TEA_COLOR, 80))  # Verde semi-transparente
                screen.blit(tint_surface, draw_rect, special_flags=pygame.BLEND_ALPHA_SDL2)
        
        # ✅ IMPLEMENTADO: Efecto de brillo ocasional (para ambos casos)
        if self.sparkle_timer % 30 < 5:  # Brilla cada 30 frames durante 5 frames
            # Pequeñas estrellas alrededor del power-up
            sparkle_points = [
                (draw_rect.centerx, draw_rect.top - 3),
                (draw_rect.right + 3, draw_rect.centery),
                (draw_rect.centerx, draw_rect.bottom + 3),
                (draw_rect.left - 3, draw_rect.centery)
            ]
            for point in sparkle_points:
                pygame.draw.circle(screen, WHITE, point, 1)


# ✅ IMPLEMENTADO: Clase Enemy para enemigos más complejos
class Enemy(Obstacle):
    """
    Enemigo que se mueve de forma más inteligente que un obstáculo simple.
    
    Los enemigos pueden seguir al jugador o moverse en patrones específicos.
    Esta clase demuestra herencia de la clase Obstacle.
    """
    
    def __init__(self, player_x, difficulty_multiplier=1.0):
        """
        Constructor del enemigo.
        
        Args:
            player_x: Posición X del jugador para seguimiento
            difficulty_multiplier: Multiplicador de dificultad
        """
        super().__init__(difficulty_multiplier)  # Llamar al constructor padre
        
        # Configuración específica del enemigo
        self.color = (150, 0, 150)  # Color púrpura para distinguir
        self.obstacle_type = 'enemy'
        self.target_x = player_x    # Posición objetivo (jugador)
        self.horizontal_speed = 1   # Velocidad de seguimiento horizontal
    
    def update(self, player_x):
        """
        Actualizar enemigo con seguimiento del jugador.
        
        Args:
            player_x: Posición X actual del jugador
        """
        # Actualizar posición vertical (como obstáculo normal)
        self.rect.y += self.speed
        
        # ✅ IMPLEMENTADO: Seguimiento horizontal del jugador
        self.target_x = player_x
        if self.rect.centerx < self.target_x:
            self.rect.x += self.horizontal_speed
        elif self.rect.centerx > self.target_x:
            self.rect.x -= self.horizontal_speed
        
        # Mantener dentro de los límites de pantalla
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(WINDOW_WIDTH, self.rect.right)
        
        # Efectos visuales
        self.rotation += 3  # Rotar más rápido que obstáculos normales
        self.pulse_timer += 1
        
        return self.rect.top < WINDOW_HEIGHT
    
    def draw(self, screen):
        """Dibujar enemigo con indicadores especiales."""
        # Color base con pulso
        base_color = self.color
        pulse_offset = int(abs(pygame.math.Vector2(1, 0).rotate(self.pulse_timer * 4).x) * 30)
        pulse_color = tuple(min(255, max(0, c + pulse_offset)) for c in base_color)
        
        # Dibujar enemigo
        pygame.draw.rect(screen, pulse_color, self.rect)
        
        # Indicador de que es un enemigo (ojos)
        eye_size = 3
        left_eye = (self.rect.left + 6, self.rect.top + 6)
        right_eye = (self.rect.right - 6, self.rect.top + 6)
        pygame.draw.circle(screen, WHITE, left_eye, eye_size)
        pygame.draw.circle(screen, WHITE, right_eye, eye_size)
        pygame.draw.circle(screen, RED, left_eye, 1)
        pygame.draw.circle(screen, RED, right_eye, 1)
        
        # Borde amenazante
        pygame.draw.rect(screen, RED, self.rect, 2)


# ✅ IMPLEMENTADO: Clase Explosion para efectos visuales
class Explosion:
    """
    Efecto visual cuando se destruye un obstáculo.
    
    Esta clase demuestra cómo crear efectos temporales que se
    dibujan durante un tiempo limitado y luego desaparecen.
    """
    
    def __init__(self, x, y, color=YELLOW):
        """
        Constructor de la explosión.
        
        Args:
            x, y: Posición central de la explosión
            color: Color base de la explosión
        """
        self.x = x
        self.y = y
        self.color = color
        self.particles = []
        self.life = PARTICLE_LIFE  # Vida total del efecto
        
        # ✅ IMPLEMENTADO: Crear partículas individuales
        for _ in range(PARTICLE_COUNT):
            # Cada partícula tiene posición, velocidad y tamaño aleatorio
            angle = random.uniform(0, 2 * 3.14159)  # Ángulo aleatorio
            speed = random.uniform(2, 8)             # Velocidad aleatoria
            
            particle = {
                'x': x,
                'y': y,
                'vel_x': pygame.math.Vector2(speed, 0).rotate_rad(angle).x,
                'vel_y': pygame.math.Vector2(speed, 0).rotate_rad(angle).y,
                'size': random.randint(2, 5),
                'life': random.randint(15, PARTICLE_LIFE)
            }
            self.particles.append(particle)
    
    def update(self):
        """
        Actualizar todas las partículas de la explosión.
        
        Returns:
            bool: False si la explosión terminó, True si sigue activa
        """
        self.life -= 1
        
        # Actualizar cada partícula
        for particle in self.particles[:]:  # [:] para iterar copia segura
            particle['x'] += particle['vel_x']
            particle['y'] += particle['vel_y']
            particle['life'] -= 1
            
            # Aplicar gravedad y fricción
            particle['vel_y'] += 0.2  # Gravedad
            particle['vel_x'] *= 0.98  # Fricción
            
            # Eliminar partículas que expiraron
            if particle['life'] <= 0:
                self.particles.remove(particle)
        
        # La explosión termina cuando no quedan partículas o se acaba el tiempo
        return len(self.particles) > 0 and self.life > 0
    
    def draw(self, screen):
        """Dibujar todas las partículas de la explosión."""
        for particle in self.particles:
            # Color que se desvanece con el tiempo
            alpha_factor = particle['life'] / PARTICLE_LIFE
            particle_color = tuple(int(c * alpha_factor) for c in self.color)
            
            # Dibujar partícula como círculo
            pygame.draw.circle(screen, particle_color, 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])


# ✅ IMPLEMENTADO: Clase para efectos de pantalla
class ScreenEffect:
    """
    Efectos que afectan a toda la pantalla como screen shake.
    """
    
    def __init__(self):
        """Constructor del sistema de efectos de pantalla."""
        self.shake_intensity = 0
        self.shake_duration = 0
        self.shake_offset_x = 0
        self.shake_offset_y = 0
    
    def start_screen_shake(self, intensity=SCREEN_SHAKE_INTENSITY, duration=SCREEN_SHAKE_DURATION):
        """
        Iniciar efecto de screen shake.
        
        Args:
            intensity: Intensidad del temblor
            duration: Duración en frames
        """
        self.shake_intensity = intensity
        self.shake_duration = duration
    
    def update(self):
        """Actualizar efectos de pantalla."""
        if self.shake_duration > 0:
            self.shake_duration -= 1
            
            # Calcular offset aleatorio para el shake
            if self.shake_duration > 0:
                self.shake_offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
                self.shake_offset_y = random.randint(-self.shake_intensity, self.shake_intensity)
            else:
                self.shake_offset_x = 0
                self.shake_offset_y = 0
    
    def get_screen_offset(self):
        """
        Obtener el offset actual de la pantalla.
        
        Returns:
            tuple: (offset_x, offset_y) para aplicar a la cámara
        """
        return (self.shake_offset_x, self.shake_offset_y)


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