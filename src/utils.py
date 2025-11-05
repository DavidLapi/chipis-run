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
from .settings import *

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
    
    # TODO 3: Implementar dificultad progresiva
    # Ejemplo: cada 10 puntos aumenta la dificultad en 10%
    # return 1.0 + (score // 10) * 0.1
    
    return 1.0  # Por ahora, dificultad constante


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