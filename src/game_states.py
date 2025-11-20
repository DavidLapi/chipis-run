"""
game_states.py - Estados del juego Julia's Run

Este archivo gestiona los diferentes estados o pantallas del juego:
- Menú principal
- Jugando
- Game Over
- Pausa (TODO)

Conceptos de programación cubiertos:
- Máquina de estados
- Gestión de eventos
- Renderizado condicional
- Flujo de control del programa

Referencias útiles:
- pygame.font: https://www.pygame.org/docs/ref/font.html
- pygame.event: https://www.pygame.org/docs/ref/event.html
"""

import pygame
from settings import *

class GameStateManager:
    """
    Esta clase gestiona los diferentes estados del juego.
    
    Un juego típicamente tiene varios estados o pantallas:
    - Menú principal
    - Gameplay
    - Game Over
    - Pausa
    
    Esta clase se encarga de cambiar entre estos estados y
    asegurarse de que solo uno esté activo a la vez.
    """
    
    def __init__(self):
        """Constructor del gestor de estados."""
        self.current_state = STATE_MENU
        self.next_state = None
        
        #Inicializamos música
        pygame.mixer.init()

        # Inicializar fuentes para texto
        pygame.font.init()
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)

    
    def change_state(self, new_state):
        """
        Cambia a un nuevo estado.
        
        Args:
            new_state: El nuevo estado (ver constantes en settings.py)
        """
        self.next_state = new_state
    
    def update_state(self):
        """Actualiza el estado actual si hay un cambio pendiente."""
        if self.next_state:
            self.current_state = self.next_state
            self.next_state = None
    
    def get_current_state(self):
        """Obtiene el estado actual."""
        return self.current_state


class MenuState:
    """
    Estado del menú principal.
    
    Muestra el título del juego, instrucciones básicas y
    espera a que el jugador presione una tecla para empezar.
    """
    
    def __init__(self, state_manager):
        """
        Constructor del estado de menú.
        
        Args:
            state_manager: Referencia al gestor de estados
        """
        self.state_manager = state_manager
    
    def handle_events(self, events):
        """
        Maneja los eventos del menú.
        
        Args:
            events: Lista de eventos de pygame
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_SPACE or event.key == KEY_ENTER:
                    self.state_manager.change_state(STATE_PLAYING)
                elif event.key == KEY_ESCAPE:
                    return False  # Señal para salir del juego
        
        return True  # Continuar ejecutando
    
    def update(self):
        """Actualiza la lógica del menú (no hay mucho que hacer aquí)."""
        pass
    
    def draw(self, screen):
        """
        Dibuja el menú principal.
        
        Args:
            screen: Superficie de pygame donde dibujar
        """
        
        # Limpiar pantalla con color de fondo
        screen.fill(LIGHT_BLUE)
        
        # TODO 9: Añadir demo visual o animación de fondo
        # self.draw_background_animation(screen)
        fondo = pygame.image.load(SPRITE_BACKGROUND).convert()
        fondo_center = fondo.get_rect(center=(WINDOW_WIDTH//2, 350))
        screen.blit(fondo, fondo_center)


        # Título del juego
        # title_text = self.state_manager.font_large.render("Chipi's Run", True, BLACK)
        # title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, 150))
        # screen.blit(title_text, title_rect)
        
        # Subtítulo
        subtitle_text = self.state_manager.font_medium.render("La Aventura Épica Jamás Vista", True, PURPLE)
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH//2, 230))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Instrucciones
        instructions = [
            "Controles:",
            "Flechas → Mover",
            "Espacio → Lanzar cuchillo",
            "Esquiva obstáculos rojos",
            "Recoge power-ups de colores",
            "",
            "Presiona ESPACIO para comenzar",
            "ESC para salir"
        ]

        start_y = 280
        for i, instruction in enumerate(instructions):
            color = BLACK if instruction != "" else WHITE
            text = self.state_manager.font_small.render(instruction, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, start_y + i * 25))
            screen.blit(text, text_rect)
        
        


class PlayingState:
    """
    Estado principal del juego.
    
    Este es el estado donde ocurre toda la acción:
    - El jugador se mueve y lanza cuchillos
    - Aparecen obstáculos y power-ups
    - Se detectan colisiones
    - Se actualiza la puntuación
    """
    
    def __init__(self, state_manager):
        """Constructor del estado de juego."""
        self.state_manager = state_manager
    
    def handle_events(self, events, player, knife_cooldown):
        """
        Maneja los eventos durante el juego.
        
        Args:
            events: Lista de eventos de pygame
            player: Instancia del jugador
            knife_cooldown: Timer de cooldown para cuchillos
            
        Returns:
            list: Lista de nuevos cuchillos creados (si se lanzó alguno)
        """
        
        new_knives = []
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_SPACE:
                    # Lanzar cuchillo si no hay cooldown
                    if knife_cooldown.is_ready():
                        from entities import Knife  # Import local para evitar circular
                        new_knife = Knife(player.rect)
                        new_knives.append(new_knife)
                        knife_cooldown.start_cooldown()
                        
                        # TODO 4: Añadir sonido de lanzamiento
                        pygame.mixer.Sound(SOUND_THROW).play()
                
                elif event.key == KEY_P:
                    # ✅ IMPLEMENTADO: Implementar pausa
                    self.state_manager.change_state(STATE_PAUSED)
                    print("Juego pausado")  # Debug
                
                elif event.key == KEY_ESCAPE:
                    return new_knives, False  # Salir del juego
        
        return new_knives, True  # Continuar jugando
    
    def update(self, player, obstacles, knives, powerups, effects, knife_cooldown):
        """
        Actualiza toda la lógica del juego.
        
        Args:
            player: Instancia del jugador
            obstacles: Lista de obstáculos
            knives: Lista de cuchillos
            powerups: Lista de power-ups
            effects: Sistema de efectos de power-ups
            knife_cooldown: Timer de cooldown
            
        Returns:
            bool: True si el jugador sigue vivo, False si Game Over
        """
        
        # Actualizar timers
        knife_cooldown.update()
        effects.update(player)
        
        # Mover jugador según teclas presionadas
        keys = pygame.key.get_pressed()
        player.move(keys)
        
        # Actualizar obstáculos
        for obstacle in obstacles[:]:  # [:] crea una copia para iterar seguro
            if not obstacle.update():
                # Obstáculo salió de pantalla - dar puntos por esquivar
                obstacles.remove(obstacle)
                player.score += POINTS_PER_OBSTACLE_AVOIDED
        
        # Actualizar cuchillos
        for knife in knives[:]:
            if not knife.update():
                knives.remove(knife)
        
        # Actualizar power-ups
        for powerup in powerups[:]:
            if not powerup.update():
                powerups.remove(powerup)
        
        # Detectar colisiones jugador-obstáculos
        for obstacle in obstacles[:]:
            if player.rect.colliderect(obstacle.rect):
                obstacles.remove(obstacle)
                if not player.take_damage():
                    # Game Over
                    return False
                
                    # TODO 4: Añadir sonido de daño
                    # Iniciar música con mixer
                else:
                    pygame.mixer.Sound(SOUND_METAL_PIPE).play()
        
        # Detectar colisiones cuchillo-obstáculos
        for knife in knives[:]:
            for obstacle in obstacles[:]:
                if knife.rect.colliderect(obstacle.rect):
                    # Destruir ambos y dar puntos
                    knives.remove(knife)
                    obstacles.remove(obstacle)
                    player.score += POINTS_PER_OBSTACLE_DESTROYED
                    
                    # TODO 7: Crear efecto de explosión
                    # explosion = Explosion(obstacle.rect.center)
                    break
        
        # Detectar colisiones jugador-power-ups
        for powerup in powerups[:]:
            if player.rect.colliderect(powerup.rect):
                powerups.remove(powerup)
                player.score += POINTS_PER_POWERUP
                
                # Activar efecto según el tipo
                if powerup.type == 'vodka':
                    effects.activate_vodka_boost(player)
                elif powerup.type == 'tea':
                    effects.activate_tea_shield(player)
        
        return True  # Jugador sigue vivo
    
    def draw(self, screen, player, obstacles, knives, powerups, effects, knife_cooldown):
        """
        Dibuja todo el estado del juego.
        
        Args:
            screen: Superficie donde dibujar
            player: Instancia del jugador
            obstacles: Lista de obstáculos
            knives: Lista de cuchillos
            powerups: Lista de power-ups
            effects: Sistema de efectos
            knife_cooldown: Timer de cooldown
        """
        
        # Limpiar pantalla
        screen.fill(BLACK)

        
        # Dibujar todas las entidades
        player.draw(screen)
        
        for obstacle in obstacles:
            obstacle.draw(screen)
        
        for knife in knives:
            knife.draw(screen)
        
        for powerup in powerups:
            powerup.draw(screen)
        
        # Dibujar HUD (Heads-Up Display)
        self.draw_hud(screen, player, effects, knife_cooldown)
    
    def draw_hud(self, screen, player, effects, knife_cooldown):
        """
        Dibuja la interfaz de usuario (puntuación, vidas, etc.).
        
        Args:
            screen: Superficie donde dibujar
            player: Instancia del jugador
            effects: Sistema de efectos
            knife_cooldown: Timer de cooldown
        """
        
        # Puntuación
        score_text = self.state_manager.font_medium.render(f"Puntuación: {player.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Vidas
        lives_text = self.state_manager.font_medium.render(f"Vidas: {player.lives}", True, WHITE)
        screen.blit(lives_text, (10, 40))
        
        # Estado del escudo
        if player.has_shield:
            shield_text = self.state_manager.font_small.render("🛡️ ESCUDO ACTIVO", True, TEA_COLOR)
            screen.blit(shield_text, (10, 70))
        
        # ✅ IMPLEMENTADO: Barra de cooldown visual
        knife_cooldown.draw_cooldown_bar(screen)
        
        # ✅ IMPLEMENTADO: Efectos activos
        effects.draw_active_effects(screen, self.state_manager.font_small)


class GameOverState:
    """
    Estado de Game Over.
    
    Muestra la puntuación final, el récord y permite
    reiniciar el juego o volver al menú.
    """
    
    def __init__(self, state_manager):
        """Constructor del estado de Game Over."""
        self.state_manager = state_manager
        self.final_score = 0
        self.best_score = 0
        self.is_new_record = False
    
    def set_scores(self, final_score, best_score):
        """
        Establece las puntuaciones para mostrar.
        
        Args:
            final_score: Puntuación de la partida actual
            best_score: Mejor puntuación histórica
        """
        self.final_score = final_score
        self.best_score = best_score
        self.is_new_record = final_score > best_score
    
    def handle_events(self, events):
        """
        Maneja los eventos en la pantalla de Game Over.
        
        Args:
            events: Lista de eventos de pygame
        """
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_ENTER:
                    self.state_manager.change_state(STATE_PLAYING)
                elif event.key == KEY_ESCAPE:
                    return False  # Salir del juego
        
        return True
    
    def update(self):
        """Actualiza la lógica del Game Over."""
        pass
    
    def draw(self, screen):
        """
        Dibuja la pantalla de Game Over.
        
        Args:
            screen: Superficie donde dibujar
        """
        
        # Fondo semi-transparente
        screen.fill(BLACK)
        
        # Título
        game_over_text = self.state_manager.font_large.render("GAME OVER", True, RED)
        title_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, 150))
        screen.blit(game_over_text, title_rect)
        
        # Puntuación final
        score_text = self.state_manager.font_medium.render(f"Tu puntuación: {self.final_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, 220))
        screen.blit(score_text, score_rect)
        
        # Récord
        if self.is_new_record:
            record_text = self.state_manager.font_medium.render("¡NUEVO RÉCORD!", True, YELLOW)
        else:
            record_text = self.state_manager.font_medium.render(f"Récord: {self.best_score}", True, GRAY)
        
        record_rect = record_text.get_rect(center=(WINDOW_WIDTH//2, 260))
        screen.blit(record_text, record_rect)
        
        # Instrucciones
        restart_text = self.state_manager.font_small.render("Presiona ENTER para jugar de nuevo", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, 350))
        screen.blit(restart_text, restart_rect)
        
        exit_text = self.state_manager.font_small.render("ESC para salir", True, WHITE)
        exit_rect = exit_text.get_rect(center=(WINDOW_WIDTH//2, 380))
        screen.blit(exit_text, exit_rect)


# ✅ IMPLEMENTADO: Estado de pausa
class PausedState:
    """
    Estado cuando el juego está pausado.
    
    En este estado el juego se detiene pero se mantiene visible
    en el fondo con una indicación de pausa superpuesta.
    """
    
    def __init__(self, state_manager):
        """Constructor del estado de pausa."""
        self.state_manager = state_manager
        
        # ✅ IMPLEMENTADO: Efecto visual de pausa
        self.pulse_timer = 0  # Para efecto de pulso en el texto "PAUSED"
    
    def handle_events(self, events):
        """
        Maneja eventos en estado de pausa.
        
        Args:
            events: Lista de eventos de pygame
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_P:
                    # Reanudar el juego
                    self.state_manager.change_state(STATE_PLAYING)
                    print("Juego reanudado")  # Debug
                elif event.key == KEY_ESCAPE:
                    # Volver al menú principal
                    self.state_manager.change_state(STATE_MENU)
                    print("Volviendo al menú desde pausa")  # Debug
        return True
    
    def update(self):
        """Actualizar efectos visuales de la pausa."""
        self.pulse_timer += 1
    
    def draw(self, screen, game_surface=None):
        """
        Dibuja la pantalla de pausa.
        
        Args:
            screen: Superficie donde dibujar
            game_surface: Superficie del juego de fondo (opcional)
        """
        
        # ✅ IMPLEMENTADO: Mostrar el juego de fondo con overlay de pausa
        if game_surface:
            # Dibujar el juego de fondo ligeramente oscurecido
            dark_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            dark_surface.fill((0, 0, 0))
            dark_surface.set_alpha(128)  # Semi-transparente
            
            screen.blit(game_surface, (0, 0))
            screen.blit(dark_surface, (0, 0))
        else:
            # Si no hay superficie de fondo, usar color sólido
            screen.fill((50, 50, 50))  # Gris oscuro
        
        # ✅ IMPLEMENTADO: Texto "PAUSED" con efecto de pulso
        pulse_factor = abs(pygame.math.Vector2(1, 0).rotate(self.pulse_timer * 3).x)
        pulse_size = int(FONT_SIZE_LARGE + pulse_factor * 10)
        
        try:
            pulse_font = pygame.font.Font(None, pulse_size)
        except:
            pulse_font = self.state_manager.font_large
        
        paused_text = pulse_font.render("PAUSED", True, YELLOW)
        paused_rect = paused_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
        
        # Sombra del texto para mejor legibilidad
        shadow_text = pulse_font.render("PAUSED", True, BLACK)
        shadow_rect = shadow_text.get_rect(center=(paused_rect.centerx + 3, paused_rect.centery + 3))
        screen.blit(shadow_text, shadow_rect)
        screen.blit(paused_text, paused_rect)
        
        # Instrucciones
        instructions = [
            "Presiona P para continuar",
            "ESC para volver al menú"
        ]
        
        y_offset = WINDOW_HEIGHT//2 + 20
        for instruction in instructions:
            text = self.state_manager.font_medium.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, y_offset))
            
            # Fondo semi-transparente para las instrucciones
            bg_rect = pygame.Rect(text_rect.x - 10, text_rect.y - 5,
                                text_rect.width + 20, text_rect.height + 10)
            pygame.draw.rect(screen, BLACK, bg_rect)
            pygame.draw.rect(screen, WHITE, bg_rect, 1)
            
            screen.blit(text, text_rect)
            y_offset += 40


# TODO 1: Estado de pausa
# class PausedState:
#     """Estado cuando el juego está pausado."""
#     
#     def __init__(self, state_manager):
#         self.state_manager = state_manager
#     
#     def handle_events(self, events):
#         for event in events:
#             if event.type == pygame.KEYDOWN:
#                 if event.key == KEY_P:
#                     self.state_manager.change_state(STATE_PLAYING)
#         return True
#     
#     def update(self):
#         pass
#     
#     def draw(self, screen):
#         # Dibujar "PAUSED" en el centro
#         pass

# === NOTAS EDUCATIVAS ===
"""
Conceptos importantes sobre máquinas de estados:

1. SEPARACIÓN DE RESPONSABILIDADES:
   Cada estado maneja solo su propia lógica, lo que hace
   el código más organizado y fácil de mantener.

2. TRANSICIONES DE ESTADO:
   Los estados pueden cambiar a otros estados según eventos
   (teclas presionadas, condiciones del juego, etc.).

3. GESTIÓN DE EVENTOS:
   Cada estado decide cómo responder a eventos de teclado
   y ratón de manera apropiada para su contexto.

4. RENDERIZADO CONDICIONAL:
   Solo se dibuja lo que es relevante para el estado actual,
   mejorando el rendimiento y la claridad visual.

5. FLUJO DEL PROGRAMA:
   La máquina de estados define cómo el usuario navega
   por las diferentes pantallas del juego.

Ejercicio para estudiantes:
- Implementar el estado de pausa (TODO 1)
- Añadir un estado de opciones o configuración
- Crear transiciones animadas entre estados
"""