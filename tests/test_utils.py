"""
test_utils.py - Tests unitarios para el módulo utils

Este archivo contiene tests para verificar que las funciones del módulo utils
funcionan correctamente. Los tests son una parte importante del desarrollo
de software porque nos ayudan a:

1. Verificar que el código funciona como esperamos
2. Detectar errores cuando modificamos código existente
3. Documentar cómo se supone que funcionen las funciones

Conceptos de testing cubiertos:
- Tests unitarios con unittest
- Casos de prueba (test cases)
- Assertions (verificaciones)
- Setup y teardown de tests
- Mocking de archivos

Para ejecutar los tests:
    python -m unittest discover tests
    
O específicamente este archivo:
    python -m unittest tests.test_utils

Referencias útiles:
- unittest: https://docs.python.org/3/library/unittest.html

IMPORTANTE:
Añadir un punto (.) detrás de cada módulo para hacer funcionar los testeos de los objetos.
De esta forma, Python sabe cuál es el 'paquete padre' al que debe referirse.
EJEMPLO: 
from settings import *
Saltaría este error --> ModuleNotFoundError: No module named 'settings'
Para solucionarlo, se modifica lo siguiente:
from .settings import *

Otra cosa importante:
Si se requiere de ejecutar el juego (comando: 'make run' o 'py .\src\main.py'),
se tienen que eliminar dichos puntos explicados en el ejemplo anterior.
El programa en sí ya sabe qué módulos se debe ejecutar

"""

import unittest
import os
import json
import tempfile
from unittest.mock import patch, mock_open

# Importar las funciones que queremos testear
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import (
    clamp, distance, format_score, get_random_powerup_type,
    should_spawn_obstacle, should_spawn_powerup, is_point_in_rect,
    lerp, create_random_color, load_best_score, save_best_score
)
from src.settings import OBSTACLE_SPAWN_RATE, POWERUP_SPAWN_RATE


class TestUtilityFunctions(unittest.TestCase):
    """
    Clase de tests para las funciones de utilidad.
    
    Cada método que empieza con 'test_' es un caso de prueba individual.
    unittest ejecutará automáticamente todos estos métodos.
    """
    
    def test_clamp_basic_cases(self):
        """Test de la función clamp con casos básicos."""
        
        # Caso 1: Valor dentro del rango
        result = clamp(50, 0, 100)
        self.assertEqual(result, 50, "Valor dentro del rango debe mantenerse igual")
        
        # Caso 2: Valor por debajo del mínimo
        result = clamp(-10, 0, 100)
        self.assertEqual(result, 0, "Valor por debajo del mínimo debe ajustarse al mínimo")
        
        # Caso 3: Valor por encima del máximo
        result = clamp(150, 0, 100)
        self.assertEqual(result, 100, "Valor por encima del máximo debe ajustarse al máximo")
        
        # Caso 4: Valor igual al mínimo
        result = clamp(0, 0, 100)
        self.assertEqual(result, 0, "Valor igual al mínimo debe mantenerse")
        
        # Caso 5: Valor igual al máximo
        result = clamp(100, 0, 100)
        self.assertEqual(result, 100, "Valor igual al máximo debe mantenerse")
    
    def test_distance_calculation(self):
        """Test de la función distance."""
        
        # Caso 1: Distancia entre puntos en línea horizontal
        result = distance((0, 0), (3, 0))
        self.assertEqual(result, 3.0, "Distancia horizontal debe ser correcta")
        
        # Caso 2: Distancia entre puntos en línea vertical
        result = distance((0, 0), (0, 4))
        self.assertEqual(result, 4.0, "Distancia vertical debe ser correcta")
        
        # Caso 3: Distancia pitagórica (3-4-5)
        result = distance((0, 0), (3, 4))
        self.assertEqual(result, 5.0, "Distancia pitagórica debe ser correcta")
        
        # Caso 4: Distancia con números negativos
        result = distance((-1, -1), (2, 3))
        expected = ((2 - (-1))**2 + (3 - (-1))**2)**0.5  # sqrt(9 + 16) = 5
        self.assertEqual(result, expected, "Distancia con negativos debe ser correcta")
    
    def test_format_score(self):
        """Test de la función format_score."""
        
        # Caso 1: Número pequeño
        result = format_score(123)
        self.assertEqual(result, "123", "Número pequeño no debe tener comas")
        
        # Caso 2: Número con miles
        result = format_score(1234)
        self.assertEqual(result, "1,234", "Número con miles debe tener coma")
        
        # Caso 3: Número grande
        result = format_score(1234567)
        self.assertEqual(result, "1,234,567", "Número grande debe tener múltiples comas")
        
        # Caso 4: Cero
        result = format_score(0)
        self.assertEqual(result, "0", "Cero debe formatearse correctamente")
    
    def test_should_spawn_obstacle(self):
        """Test de la función should_spawn_obstacle."""
        
        # Caso 1: Frame que debería generar obstáculo
        result = should_spawn_obstacle(OBSTACLE_SPAWN_RATE)
        self.assertTrue(result, f"Frame {OBSTACLE_SPAWN_RATE} debería generar obstáculo")
        
        # Caso 2: Frame que NO debería generar obstáculo
        result = should_spawn_obstacle(OBSTACLE_SPAWN_RATE + 1)
        self.assertFalse(result, f"Frame {OBSTACLE_SPAWN_RATE + 1} NO debería generar obstáculo")
        
        # Caso 3: Frame 0 debería generar (0 % cualquier_número = 0)
        result = should_spawn_obstacle(0)
        self.assertTrue(result, "Frame 0 debería generar obstáculo")
    
    def test_should_spawn_powerup(self):
        """Test de la función should_spawn_powerup."""
        
        # Similar a should_spawn_obstacle pero con POWERUP_SPAWN_RATE
        result = should_spawn_powerup(POWERUP_SPAWN_RATE)
        self.assertTrue(result, f"Frame {POWERUP_SPAWN_RATE} debería generar power-up")
        
        result = should_spawn_powerup(POWERUP_SPAWN_RATE + 1)
        self.assertFalse(result, f"Frame {POWERUP_SPAWN_RATE + 1} NO debería generar power-up")
    
    def test_get_random_powerup_type(self):
        """Test de la función get_random_powerup_type."""
        
        # Ejecutar la función varias veces para verificar que solo devuelve tipos válidos
        valid_types = {'vodka', 'tea'}
        
        for _ in range(20):  # Probar 20 veces para tener buena cobertura
            result = get_random_powerup_type()
            self.assertIn(result, valid_types, 
                         f"get_random_powerup_type() devolvió '{result}', debe ser 'vodka' o 'tea'")
    
    def test_lerp_interpolation(self):
        """Test de la función lerp (interpolación lineal)."""
        
        # Caso 1: t = 0 (debería devolver start)
        result = lerp(0, 100, 0.0)
        self.assertEqual(result, 0, "lerp con t=0 debe devolver el valor inicial")
        
        # Caso 2: t = 1 (debería devolver end)
        result = lerp(0, 100, 1.0)
        self.assertEqual(result, 100, "lerp con t=1 debe devolver el valor final")
        
        # Caso 3: t = 0.5 (debería devolver el punto medio)
        result = lerp(0, 100, 0.5)
        self.assertEqual(result, 50, "lerp con t=0.5 debe devolver el punto medio")
        
        # Caso 4: Interpolación con decimales
        result = lerp(10, 20, 0.25)
        self.assertEqual(result, 12.5, "lerp debe calcular correctamente valores decimales")
    
    def test_create_random_color(self):
        """Test de la función create_random_color."""
        
        for _ in range(10):  # Probar varias veces
            color = create_random_color()
            
            # Verificar que devuelve una tupla de 3 elementos
            self.assertIsInstance(color, tuple, "create_random_color debe devolver una tupla")
            self.assertEqual(len(color), 3, "Color debe tener exactamente 3 componentes (R, G, B)")
            
            # Verificar que todos los valores están en el rango 0-255
            for component in color:
                self.assertIsInstance(component, int, "Componentes de color deben ser enteros")
                self.assertGreaterEqual(component, 0, "Componentes de color deben ser >= 0")
                self.assertLessEqual(component, 255, "Componentes de color deben ser <= 255")
    
    # TODO: Tests para funciones de archivos JSON
    # Estos tests son más complejos porque requieren mocking de archivos
    
    @patch('builtins.open', new_callable=mock_open, read_data='{"best_score": 1000}')
    @patch('os.path.exists', return_value=True)
    def test_load_best_score_success(self, mock_exists, mock_file):
        """Test de load_best_score cuando el archivo existe y es válido."""
        
        result = load_best_score()
        self.assertEqual(result, 1000, "load_best_score debe leer correctamente el archivo JSON")
    
    @patch('os.path.exists', return_value=False)
    def test_load_best_score_no_file(self, mock_exists):
        """Test de load_best_score cuando el archivo no existe."""
        
        result = load_best_score()
        self.assertEqual(result, 0, "load_best_score debe devolver 0 si no existe el archivo")
    
    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    @patch('os.path.exists', return_value=True)
    def test_load_best_score_invalid_json(self, mock_exists, mock_file):
        """Test de load_best_score cuando el archivo contiene JSON inválido."""
        
        result = load_best_score()
        self.assertEqual(result, 0, "load_best_score debe devolver 0 si el JSON es inválido")
    
    # TODO: Más tests para save_best_score
    # TODO: Tests para is_point_in_rect cuando se implemente pygame.Rect mocking


class TestGameLogic(unittest.TestCase):
    """
    Tests para lógica específica del juego.
    
    Estos tests verifican que las reglas del juego funcionan correctamente.
    """
    
    def test_spawn_rates_are_reasonable(self):
        """Verifica que las tasas de spawn sean razonables."""
        
        # Los obstáculos deberían aparecer más frecuentemente que los power-ups
        self.assertLess(OBSTACLE_SPAWN_RATE, POWERUP_SPAWN_RATE, 
                       "Los obstáculos deben aparecer más frecuentemente que los power-ups")
        
        # Las tasas no deberían ser demasiado altas (causaría lag)
        self.assertGreater(OBSTACLE_SPAWN_RATE, 10, 
                          "Tasa de spawn de obstáculos no debe ser demasiado alta")
        self.assertGreater(POWERUP_SPAWN_RATE, 10, 
                          "Tasa de spawn de power-ups no debe ser demasiado alta")


def run_tests():
    """
    Función auxiliar para ejecutar todos los tests.
    
    Esta función puede ser llamada desde otros módulos para ejecutar
    todos los tests programáticamente.
    """
    
    # Crear un test suite con todos los tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Añadir todas las clases de test
    suite.addTests(loader.loadTestsFromTestCase(TestUtilityFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestGameLogic))
    
    # Ejecutar los tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Devolver True si todos los tests pasaron
    return result.wasSuccessful()


if __name__ == '__main__':
    """
    Si este archivo se ejecuta directamente, correr todos los tests.
    
    Uso: python -m tests.test_utils
    """
    
    print("=== EJECUTANDO TESTS DE JULIA'S RUN ===")
    print("Verificando funciones de utilidad...")
    print()
    
    # Ejecutar tests con verbosidad alta para ver detalles
    unittest.main(verbosity=2)

# === NOTAS EDUCATIVAS SOBRE TESTING ===
"""
Conceptos importantes sobre testing:

1. TESTS UNITARIOS:
   Prueban funciones individuales de forma aislada.
   Cada test debería probar una sola cosa específica.

2. ASSERTIONS:
   Verificaciones que deben ser ciertas. Si fallan, el test falla.
   - assertEqual(a, b): a debe ser igual a b
   - assertTrue(x): x debe ser True
   - assertIn(item, container): item debe estar en container

3. TEST CASES:
   Cada método test_ es un caso de prueba independiente.
   Los tests deben ser independientes entre sí.

4. MOCKING:
   Simular componentes externos (archivos, red, etc.) para
   aislar la función que estamos probando.

5. EDGE CASES:
   Probar casos extremos: valores límite, inputs inválidos, etc.
   Estos casos a menudo revelan bugs.

6. COVERAGE:
   Medir qué porcentaje del código está cubierto por tests.
   Más coverage = más confianza en el código.

Ejercicios para estudiantes:
- Añadir más tests para funciones no cubiertas
- Crear tests para las clases de entities.py
- Implementar tests de integración que prueben múltiples componentes
- Usar coverage.py para medir cobertura de tests

Comandos útiles:
- python -m unittest discover tests  # Ejecutar todos los tests
- python -m unittest tests.test_utils -v  # Ejecutar solo este archivo
- python -m coverage run -m unittest discover  # Ejecutar con coverage
- python -m coverage report  # Ver reporte de coverage
"""