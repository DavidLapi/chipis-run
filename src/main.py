"""
main.py - Punto de entrada de Julia's Run

Este es el archivo principal del juego. Contiene el game loop principal
y la inicialización de todos los sistemas del juego.

Conceptos de programación cubiertos:
- Game loop (bucle principal del juego)
- Inicialización de sistemas
- Gestión de tiempo (FPS)
- Integración de todos los módulos

Para ejecutar el juego:
    python -m src.main

Referencias útiles:
- pygame.init(): https://www.pygame.org/docs/ref/pygame.html#pygame.init
- pygame.time.Clock: https://www.pygame.org/docs/ref/time.html#pygame.time.Clock
"""

import sys
import pygame
import random

# Importar nuestros módulos
from .settings import *
from .entities import Player, Obstacle, Knife, PowerUp
from .abilities import CooldownTimer, PowerUpEffect
from .game_states import GameStateManager, MenuState, PlayingState, GameOverState
from .utils import (
    load_best_score, save_best_score, should_spawn_obstacle, 
    should_spawn_powerup, get_random_powerup_type
)

class JuliasRunGame:
    """
    Clase principal del juego Julia's Run.
    
    Esta clase encapsula todo el juego: inicialización, game loop,
    y gestión de todos los sistemas del juego.
    
    El patrón usado aquí es común en programación de juegos:
    - Inicialización una vez
    - Game loop que se ejecuta continuamente
    - Cleanup al salir
    """
    
    def __init__(self):
        """Inicializa el juego y todos sus sistemas."""
        
        # Inicializar Pygame
        pygame.init()
        
        # Crear la ventana del juego
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Julia's Run - ¡Esquiva y Sobrevive!")
        
        # Control de tiempo (FPS)
        self.clock = pygame.time.Clock()
        
        # Gestor de estados del juego
        self.state_manager = GameStateManager()
        self.menu_state = MenuState(self.state_manager)
        self.playing_state = PlayingState(self.state_manager)
        self.game_over_state = GameOverState(self.state_manager)
        
        # Variables del juego
        self.running = True
        self.frame_count = 0
        
        # Inicializar componentes del juego
        self.reset_game()
    
    def reset_game(self):
        """
        Reinicia el juego a su estado inicial.
        
        Esta función se llama al inicio y cada vez que se reinicia una partida.
        Es importante resetear TODOS los componentes para evitar bugs.
        """
        
        # Crear jugador
        self.player = Player()
        
        # Listas de entidades del juego
        self.obstacles = []      # Lista de obstáculos en pantalla
        self.knives = []         # Lista de cuchillos lanzados
        self.powerups = []       # Lista de power-ups en pantalla
        
        # Sistemas de juego
        self.knife_cooldown = CooldownTimer(KNIFE_COOLDOWN)
        self.powerup_effects = PowerUpEffect()
        
        # Contadores
        self.frame_count = 0
        
        # Cargar mejor puntuación
        self.best_score = load_best_score()
        
        print("Juego reiniciado. ¡Buena suerte!")  # Debug
    
    def handle_events(self):
        """
        Maneja todos los eventos del juego (teclado, ratón, etc.).
        
        Returns:
            bool: False si se debe salir del juego, True para continuar
        """
        
        # Obtener todos los eventos de esta frame
        events = pygame.event.get()
        
        # Revisar eventos especiales (cerrar ventana)
        for event in events:
            if event.type == pygame.QUIT:
                return False
        
        # Delegar el manejo de eventos al estado actual
        current_state = self.state_manager.get_current_state()
        
        if current_state == STATE_MENU:
            return self.menu_state.handle_events(events)
        
        elif current_state == STATE_PLAYING:
            new_knives, continue_playing = self.playing_state.handle_events(
                events, self.player, self.knife_cooldown
            )
            # Añadir nuevos cuchillos a la lista
            self.knives.extend(new_knives)
            return continue_playing
        
        elif current_state == STATE_GAME_OVER:
            return self.game_over_state.handle_events(events)
        
        return True
    
    def update(self):
        """
        Actualiza toda la lógica del juego.
        
        Esta función se llama una vez por frame y contiene toda la lógica
        del juego: movimiento, colisiones, spawn de entidades, etc.
        """
        
        # Actualizar el gestor de estados
        self.state_manager.update_state()
        
        current_state = self.state_manager.get_current_state()
        
        if current_state == STATE_MENU:
            self.menu_state.update()
        
        elif current_state == STATE_PLAYING:
            # Incrementar contador de frames
            self.frame_count += 1
            
            # Spawn de nuevos obstáculos
            if should_spawn_obstacle(self.frame_count):
                new_obstacle = Obstacle()
                self.obstacles.append(new_obstacle)
            
            # Spawn de power-ups (menos frecuente)
            if should_spawn_powerup(self.frame_count):
                powerup_type = get_random_powerup_type()
                new_powerup = PowerUp(powerup_type)
                self.powerups.append(new_powerup)
            
            # Actualizar lógica del juego
            player_alive = self.playing_state.update(
                self.player, self.obstacles, self.knives, 
                self.powerups, self.powerup_effects, self.knife_cooldown
            )
            
            # Comprobar Game Over
            if not player_alive:
                self.handle_game_over()
        
        elif current_state == STATE_GAME_OVER:
            self.game_over_state.update()
    
    def handle_game_over(self):
        """
        Maneja la transición a Game Over.
        
        Se llama cuando el jugador se queda sin vidas.
        Guarda la puntuación y cambia al estado correspondiente.
        """
        
        # Guardar nueva mejor puntuación si corresponde
        if self.player.score > self.best_score:
            save_best_score(self.player.score)
            self.best_score = self.player.score
        
        # Configurar el estado de Game Over
        self.game_over_state.set_scores(self.player.score, self.best_score)
        
        # Cambiar al estado de Game Over
        self.state_manager.change_state(STATE_GAME_OVER)
        
        print(f"Game Over! Puntuación final: {self.player.score}")  # Debug
    
    def draw(self):
        """
        Dibuja todo el contenido del juego en la pantalla.
        
        Esta función se llama una vez por frame y se encarga de
        renderizar todos los elementos visuales del juego.
        """
        
        current_state = self.state_manager.get_current_state()
        
        if current_state == STATE_MENU:
            self.menu_state.draw(self.screen)
        
        elif current_state == STATE_PLAYING:
            self.playing_state.draw(
                self.screen, self.player, self.obstacles, 
                self.knives, self.powerups, self.powerup_effects, 
                self.knife_cooldown
            )
        
        elif current_state == STATE_GAME_OVER:
            self.game_over_state.draw(self.screen)
        
        # Actualizar la pantalla (hacer visible lo dibujado)
        pygame.display.flip()
    
    def run(self):
        """
        Game loop principal.
        
        Este es el corazón del juego: un bucle que se ejecuta continuamente
        hasta que el jugador decide salir. En cada iteración:
        1. Maneja eventos
        2. Actualiza lógica
        3. Dibuja en pantalla
        4. Controla el framerate
        """
        
        print("¡Iniciando Julia's Run!")
        print("Usa las flechas para mover, ESPACIO para lanzar cuchillos.")
        print("¡Buena suerte!")
        
        # Game loop principal
        while self.running:
            # 1. Manejar eventos (input del usuario)
            self.running = self.handle_events()
            
            # 2. Actualizar lógica del juego
            if self.running:
                self.update()
            
            # 3. Dibujar todo en pantalla
            if self.running:
                self.draw()
            
            # 4. Controlar framerate (mantener FPS constantes)
            self.clock.tick(FPS)
            
            # Comprobar si necesitamos reiniciar el juego
            if (self.state_manager.get_current_state() == STATE_PLAYING and 
                self.state_manager.next_state == STATE_PLAYING):
                # El estado cambió a PLAYING desde otro estado - reiniciar
                self.reset_game()
                self.state_manager.next_state = None
        
        # Cleanup al salir
        self.cleanup()
    
    def cleanup(self):
        """
        Limpia recursos antes de salir del juego.
        
        Es una buena práctica limpiar recursos (sonidos, fuentes, etc.)
        antes de terminar el programa.
        """
        
        print("¡Gracias por jugar Julia's Run!")
        pygame.quit()


def main():
    """
    Función principal del programa.
    
    Esta función se ejecuta cuando se llama al módulo directamente.
    Maneja errores generales y asegura un cierre limpio del programa.
    """
    
    try:
        # Crear e iniciar el juego
        game = JuliasRunGame()
        game.run()
    
    except KeyboardInterrupt:
        # El usuario presionó Ctrl+C
        print("\nJuego interrumpido por el usuario.")
    
    except Exception as e:
        # Error inesperado
        print(f"Error inesperado: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Asegurar que pygame se cierre correctamente
        pygame.quit()
        sys.exit()


# TODO 1: Añadir sistema de pausa
# - Modificar el game loop para manejar el estado PAUSED
# - Pausar actualizaciones pero mantener el renderizado

# TODO 2: Implementar barra de cooldown visual
# - Llamar al método draw_cooldown_bar() del CooldownTimer

# TODO 3: Añadir dificultad progresiva
# - Usar get_difficulty_multiplier() de utils.py
# - Aumentar velocidad de obstáculos según puntuación

# TODO 4: Integrar sprites y sonidos
# - Cargar assets al inicializar
# - Reemplazar rectángulos con sprites reales

# TODO 5: Añadir más efectos visuales
# - Partículas al destruir obstáculos
# - Animaciones de power-ups

# TODO 6: Mejorar el HUD
# - Mostrar tiempo de efectos activos
# - Añadir mini-mapa o indicadores

# TODO 7: Sistema de logros
# - Tracking de estadísticas de juego
# - Desbloquear logros por acciones específicas

# TODO 8: Opciones de configuración
# - Volumen de sonidos
# - Dificultad inicial
# - Controles personalizables

# TODO 9: Multijugador local
# - Segundo jugador con teclas diferentes
# - Competencia por puntuación más alta

# TODO 10: Efectos de pantalla
# - Screen shake al recibir daño
# - Fade in/out entre estados

# Esta condición verifica si el archivo se está ejecutando directamente
# (no siendo importado como módulo)
if __name__ == "__main__":
    main()

# === NOTAS EDUCATIVAS ===
"""
Conceptos importantes del game loop:

1. GAME LOOP PATTERN:
   El patrón fundamental de los videojuegos:
   - Input → Update → Render → Repeat
   
2. FRAMERATE:
   - FPS (Frames Per Second) determina qué tan suave se ve el juego
   - 60 FPS es el estándar para juegos fluidos
   - pygame.time.Clock.tick() controla el framerate

3. SEPARACIÓN DE RESPONSABILIDADES:
   - main.py orquesta todo pero no implementa lógica específica
   - Cada módulo tiene su responsabilidad bien definida
   - Fácil de mantener y expandir

4. GESTIÓN DE ESTADOS:
   - Solo el estado actual procesa input y se actualiza
   - Transiciones claras entre diferentes pantallas del juego

5. GESTIÓN DE MEMORIA:
   - Listas de entidades que se crean y destruyen dinámicamente
   - Importante limpiar entidades que salen de pantalla

6. ERROR HANDLING:
   - try/except para manejar errores graciosamente
   - finally para asegurar cleanup correcto

Ejercicio para estudiantes:
- Ejecutar el juego y experimentar con los controles
- Modificar valores en settings.py y ver cómo afecta el juego
- Implementar algunos de los TODOs listados
- Añadir debugging prints para entender el flujo del programa
"""