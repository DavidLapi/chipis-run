"""
utils.py - Funciones auxiliares para Julia's Run

Este archivo contiene funciones de utilidad que se usan en diferentes
partes del juego. Mantener estas funciones separadas hace el código
más modular y reutilizable.

Conceptos de programación cubiertos:
- Funciones puras
- Manejo de archivos JSON
- Generación de números aleatorios
- Validación de datos
- Manejo de excepciones

Referencias útiles:
- json module: https://docs.python.org/3/library/json.html
- random module: https://docs.python.org/3/library/random.html
"""

import json
import random
import os
from settings import *

def load_best_score():
    """
    Carga la mejor puntuación desde el archivo JSON.
    
    Esta función demuestra:
    - Manejo de archivos
    - Manejo de excepciones
    - Valores por defecto
    
    Returns:
        int: La mejor puntuación guardada, o 0 si no existe el archivo
    """
    
    try:
        # Verificar si el archivo existe
        if os.path.exists(SCORE_FILE):
            with open(SCORE_FILE, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data.get('best_score', 0)  # get() con valor por defecto
        else:
            # Si no existe el archivo, la mejor puntuación es 0
            return 0
    
    except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
        # Si hay algún error leyendo el archivo, imprimir info para debug
        print(f"Error cargando puntuación: {e}")
        return 0
    
    except Exception as e:
        # Cualquier otro error inesperado
        print(f"Error inesperado cargando puntuación: {e}")
        return 0


def save_best_score(score):
    """
    Guarda una nueva mejor puntuación en el archivo JSON.
    
    Args:
        score (int): La puntuación a guardar
    
    Returns:
        bool: True si se guardó correctamente, False si hubo error
    """
    
    try:
        # Cargar la puntuación actual para compararla
        current_best = load_best_score()
        
        # Solo guardar si es realmente mejor
        if score > current_best:
            data = {
                'best_score': score,
                'timestamp': get_current_timestamp()  # Cuándo se logró
            }
            
            with open(SCORE_FILE, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2)  # indent=2 hace el JSON más legible
            
            print(f"¡Nueva mejor puntuación guardada: {score}!")
            return True
        else:
            # No es un nuevo récord, no guardar
            return False
    
    except Exception as e:
        print(f"Error guardando puntuación: {e}")
        return False


def get_current_timestamp():
    """
    Obtiene la fecha y hora actual como string.
    
    Returns:
        str: Timestamp en formato legible
    """
    
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def should_spawn_obstacle(frame_count):
    """
    Determina si debe aparecer un nuevo obstáculo en este frame.
    
    Esta función demuestra cómo crear patrones de aparición usando módulo.
    
    Args:
        frame_count (int): Número de frame actual del juego
    
    Returns:
        bool: True si debe aparecer un obstáculo
    """
    
    # Usar módulo para crear un patrón regular
    return frame_count % OBSTACLE_SPAWN_RATE == 0


def should_spawn_powerup(frame_count):
    """
    Determina si debe aparecer un power-up en este frame.
    
    Args:
        frame_count (int): Número de frame actual del juego
    
    Returns:
        bool: True si debe aparecer un power-up
    """
    
    return frame_count % POWERUP_SPAWN_RATE == 0


def get_random_powerup_type():
    """
    Selecciona aleatoriamente un tipo de power-up.
    
    Returns:
        str: 'vodka' o 'tea'
    """
    
    return random.choice(['vodka', 'tea'])


def clamp(value, min_value, max_value):
    """
    Limita un valor entre un mínimo y máximo.
    
    Esta es una función de utilidad muy común en programación de juegos
    para asegurar que los valores estén dentro de rangos válidos.
    
    Args:
        value: El valor a limitar
        min_value: Valor mínimo permitido
        max_value: Valor máximo permitido
    
    Returns:
        El valor limitado al rango [min_value, max_value]
    
    Ejemplo:
        clamp(150, 0, 100) → 100
        clamp(-10, 0, 100) → 0
        clamp(50, 0, 100) → 50
    """
    
    return max(min_value, min(value, max_value))


def distance(pos1, pos2):
    """
    Calcula la distancia entre dos puntos.
    
    Args:
        pos1 (tuple): Primera posición (x, y)
        pos2 (tuple): Segunda posición (x, y)
    
    Returns:
        float: Distancia entre los puntos
    """
    
    import math
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    return math.sqrt(dx * dx + dy * dy)


def is_point_in_rect(point, rect):
    """
    Comprueba si un punto está dentro de un rectángulo.
    
    Args:
        point (tuple): Coordenadas (x, y) del punto
        rect (pygame.Rect): Rectángulo a comprobar
    
    Returns:
        bool: True si el punto está dentro del rectángulo
    """
    
    x, y = point
    return (rect.left <= x <= rect.right and 
            rect.top <= y <= rect.bottom)


def format_score(score):
    """
    Formatea una puntuación para mostrar en pantalla.
    
    Args:
        score (int): Puntuación a formatear
    
    Returns:
        str: Puntuación formateada con separadores de miles
    
    Ejemplo:
        format_score(1234) → "1,234"
        format_score(567890) → "567,890"
    """
    
    return f"{score:,}"


def get_difficulty_multiplier(score):
    """
    Calcula un multiplicador de dificultad basado en la puntuación.
    
    Esto permite que el juego se vuelva más difícil progresivamente.
    
    Args:
        score (int): Puntuación actual del jugador
    
    Returns:
        float: Multiplicador de dificultad (1.0 = normal, >1.0 = más difícil)
    """
    
    # ✅ IMPLEMENTADO: Dificultad progresiva
    # Cada DIFFICULTY_INCREASE_INTERVAL puntos aumenta la dificultad
    difficulty_level = score // DIFFICULTY_INCREASE_INTERVAL
    
    # Fórmula: 1.0 + (nivel * 0.1), con un máximo razonable
    multiplier = 1.0 + (difficulty_level * 0.1)
    
    # Limitar la dificultad máxima para mantener el juego jugable
    max_multiplier = 3.0  # Máximo 3x la dificultad original
    
    return min(multiplier, max_multiplier)


def create_random_color():
    """
    Genera un color RGB aleatorio.
    
    Returns:
        tuple: Color RGB aleatorio (r, g, b)
    """
    
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)


def lerp(start, end, t):
    """
    Interpolación lineal entre dos valores.
    
    LERP (Linear Interpolation) es muy útil para animaciones suaves.
    
    Args:
        start: Valor inicial
        end: Valor final
        t: Factor de interpolación (0.0 a 1.0)
    
    Returns:
        Valor interpolado
    
    Ejemplo:
        lerp(0, 100, 0.5) → 50
        lerp(0, 100, 0.25) → 25
    """
    
    return start + (end - start) * t


# ✅ IMPLEMENTADO: Funciones para gestión de sprites
def load_sprite(filename, scale=1.0):
    """
    Carga y escala un sprite.
    
    Args:
        filename: Ruta del archivo de imagen
        scale: Factor de escala (1.0 = tamaño original)
    
    Returns:
        pygame.Surface: Imagen cargada y escalada, o None si hay error
    """
    try:
        import pygame
        image = pygame.image.load(filename)
        
        if scale != 1.0:
            # Calcular nuevo tamaño
            width = int(image.get_width() * scale)
            height = int(image.get_height() * scale)
            image = pygame.transform.scale(image, (width, height))
        
        # Convertir para mejor rendimiento
        return image.convert_alpha()
        
    except (pygame.error, FileNotFoundError) as e:
        print(f"Error cargando sprite {filename}: {e}")
        return None

def create_sprite_sheet_loader(filename, sprite_width, sprite_height):
    """
    Carga una hoja de sprites y permite extraer frames individuales.
    
    Args:
        filename: Ruta del archivo de sprite sheet
        sprite_width: Ancho de cada sprite individual
        sprite_height: Alto de cada sprite individual
    
    Returns:
        function: Función para extraer sprites por coordenadas
    """
    try:
        import pygame
        sprite_sheet = pygame.image.load(filename).convert_alpha()
        
        def get_sprite(x, y):
            """Extrae un sprite específico de la hoja."""
            rect = pygame.Rect(x * sprite_width, y * sprite_height, 
                             sprite_width, sprite_height)
            sprite = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
            sprite.blit(sprite_sheet, (0, 0), rect)
            return sprite
        
        return get_sprite
        
    except (pygame.error, FileNotFoundError) as e:
        print(f"Error cargando sprite sheet {filename}: {e}")
        return None

# ✅ IMPLEMENTADO: Funciones para efectos de sonido
def play_sound(sound_file, volume=1.0):
    """
    Reproduce un efecto de sonido con el volumen especificado.
    
    Args:
        sound_file: Ruta del archivo de sonido
        volume: Volumen (0.0 a 1.0)
    """
    try:
        import pygame
        if pygame.mixer.get_init():  # Verificar que el mixer esté inicializado
            sound = pygame.mixer.Sound(sound_file)
            sound.set_volume(volume)
            sound.play()
    except (pygame.error, FileNotFoundError) as e:
        print(f"Error reproduciendo sonido {sound_file}: {e}")

# ✅ IMPLEMENTADO: Funciones para partículas y efectos visuales
def create_particle_explosion(x, y, color, particle_count=10):
    """
    Crea un efecto de explosión de partículas en la posición dada.
    
    Args:
        x, y: Posición central de la explosión
        color: Color de las partículas
        particle_count: Número de partículas
    
    Returns:
        dict: Datos de la explosión para ser procesados
    """
    particles = []
    
    for _ in range(particle_count):
        # Ángulo aleatorio en radianes
        angle = random.uniform(0, 2 * 3.14159)
        speed = random.uniform(2, 8)
        
        particle = {
            'x': x,
            'y': y,
            'vel_x': speed * (random.uniform(-1, 1)),
            'vel_y': speed * (random.uniform(-1, 1)),
            'size': random.randint(2, 5),
            'life': random.randint(15, 30),
            'color': color
        }
        particles.append(particle)
    
    return {
        'particles': particles,
        'active': True
    }

# ✅ IMPLEMENTADO: Funciones para configuración del juego
def load_game_settings():
    """
    Carga configuración del usuario desde un archivo.
    
    Returns:
        dict: Configuración cargada o valores por defecto
    """
    default_settings = {
        'master_volume': 0.7,
        'sfx_volume': 0.8,
        'music_volume': 0.6,
        'fullscreen': False,
        'difficulty': 'normal',
        'controls': {
            'left': 'LEFT',
            'right': 'RIGHT', 
            'up': 'UP',
            'down': 'DOWN',
            'shoot': 'SPACE',
            'pause': 'p',
            'instruccions': 'i'
        }
    }
    
    try:
        if os.path.exists('game_settings.json'):
            with open('game_settings.json', 'r', encoding='utf-8') as file:
                settings = json.load(file)
                # Combinar con defaults para asegurar que todas las claves existen
                for key, value in default_settings.items():
                    if key not in settings:
                        settings[key] = value
                return settings
    except Exception as e:
        print(f"Error cargando configuración: {e}")
    
    return default_settings

def save_game_settings(settings_dict):
    """
    Guarda configuración del usuario en un archivo.
    
    Args:
        settings_dict: Diccionario con la configuración a guardar
    
    Returns:
        bool: True si se guardó correctamente
    """
    try:
        with open('game_settings.json', 'w', encoding='utf-8') as file:
            json.dump(settings_dict, file, indent=2)
        return True
    except Exception as e:
        print(f"Error guardando configuración: {e}")
        return False

# ✅ IMPLEMENTADO: Funciones para estadísticas del juego
def update_play_statistics(score, time_played):
    """
    Actualiza estadísticas de juego (partidas jugadas, tiempo total, etc.).
    
    Args:
        score: Puntuación de la partida
        time_played: Tiempo jugado en segundos
    """
    stats_file = 'game_stats.json'
    
    # Cargar estadísticas existentes
    try:
        if os.path.exists(stats_file):
            with open(stats_file, 'r', encoding='utf-8') as file:
                stats = json.load(file)
        else:
            stats = {
                'games_played': 0,
                'total_time': 0,
                'total_score': 0,
                'best_score': 0,
                'average_score': 0,
                'total_obstacles_destroyed': 0,
                'total_powerups_collected': 0
            }
    except Exception:
        stats = {}
    
    # Actualizar estadísticas
    stats['games_played'] = stats.get('games_played', 0) + 1
    stats['total_time'] = stats.get('total_time', 0) + time_played
    stats['total_score'] = stats.get('total_score', 0) + score
    stats['best_score'] = max(stats.get('best_score', 0), score)
    stats['average_score'] = stats['total_score'] / stats['games_played']
    
    # Guardar estadísticas actualizadas
    try:
        with open(stats_file, 'w', encoding='utf-8') as file:
            json.dump(stats, file, indent=2)
    except Exception as e:
        print(f"Error guardando estadísticas: {e}")

# ✅ IMPLEMENTADO: Funciones para debug y desarrollo
def debug_print(*args, debug_mode=False):
    """
    Imprime mensajes solo si el modo debug está activado.
    
    Args:
        *args: Argumentos a imprimir
        debug_mode: Si está en modo debug
    """
    if debug_mode:
        print("[DEBUG]", *args)

def get_fps_color(fps):
    """
    Devuelve un color según el FPS actual para debug visual.
    
    Args:
        fps: FPS actual
    
    Returns:
        tuple: Color RGB según rendimiento
    """
    if fps >= 55:
        return GREEN    # Buen rendimiento
    elif fps >= 45:
        return YELLOW   # Rendimiento aceptable
    elif fps >= 30:
        return (255, 165, 0)  # Naranja - rendimiento bajo
    else:
        return RED      # Rendimiento muy bajo


# TODO 5: Funciones para gestión de sprites
# def load_sprite(filename, scale=1.0):
#     """Carga y escala un sprite."""
#     pass

# def create_sprite_sheet_loader(filename, sprite_width, sprite_height):
#     """Carga una hoja de sprites y permite extraer frames individuales."""
#     pass

# TODO 6: Funciones para efectos de sonido
# def play_sound(sound_file, volume=1.0):
#     """Reproduce un efecto de sonido con el volumen especificado."""
#     pass

# TODO 7: Funciones para partículas y efectos visuales
# def create_particle_explosion(x, y, color, particle_count=10):
#     """Crea un efecto de explosión de partículas en la posición dada."""
#     pass

# TODO 8: Funciones para configuración del juego
# def load_game_settings():
#     """Carga configuración del usuario desde un archivo."""
#     pass
# 
# def save_game_settings(settings_dict):
#     """Guarda configuración del usuario en un archivo."""
#     pass

# TODO 9: Funciones para estadísticas del juego
# def update_play_statistics(score, time_played):
#     """Actualiza estadísticas de juego (partidas jugadas, tiempo total, etc.)."""
#     pass

# TODO 10: Funciones para debug y desarrollo
# def debug_print(*args, debug_mode=False):
#     """Imprime mensajes solo si el modo debug está activado."""
#     if debug_mode:
#         print("[DEBUG]", *args)

# === NOTAS EDUCATIVAS ===
"""
Conceptos importantes sobre funciones auxiliares:

1. FUNCIONES PURAS:
   Funciones que siempre devuelven el mismo resultado para los mismos
   parámetros y no tienen efectos secundarios. Ejemplo: clamp(), distance().

2. MANEJO DE ERRORES:
   Usar try/except para manejar errores graciosamente. El programa
   no debe crashear por archivos corruptos o faltantes.

3. SEPARACIÓN DE RESPONSABILIDADES:
   Cada función tiene una tarea específica y bien definida.
   Esto hace el código más testeable y reutilizable.

4. DOCUMENTACIÓN:
   Cada función está documentada con docstrings que explican:
   - Qué hace la función
   - Qué parámetros acepta
   - Qué devuelve
   - Ejemplos de uso

5. VALORES POR DEFECTO:
   Usar valores sensatos cuando los datos están corruptos o faltantes.

6. VALIDACIÓN:
   Comprobar que los datos están en el formato y rango esperados.

Ejercicio para estudiantes:
- Implementar las funciones marcadas como TODO
- Crear tests para verificar que las funciones funcionan correctamente
- Experimentar con diferentes algoritmos de spawn de obstáculos
"""