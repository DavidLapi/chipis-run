# Julia's Run 🏃‍♀️🔪

Un mini-juego arcade desarrollado en Python + Pygame para aprender Programación Orientada a Objetos.

## 🎮 Historia

Julia es una valiente aventurera que debe esquivar obstáculos que caen del cielo mientras recolecta power-ups especiales. Armada únicamente con cuchillos de lanzamiento y su agilidad, debe sobrevivir el mayor tiempo posible para conseguir la puntuación más alta.

## 🎯 Controles

- **Flechas direccionales**: Mover a Julia
- **Espacio**: Lanzar cuchillo (con cooldown)
- **Enter**: Reiniciar juego (en pantalla de Game Over)
- **P**: Pausar juego
- **ESC**: Salir del juego

## ⚡ Power-ups

- **🍺 Vodka Boost**: Aumenta la velocidad de movimiento temporalmente
- **🍵 Té Mágico**: Proporciona un escudo temporal contra colisiones

## 🚀 Instalación rápida

```bash
# Crear entorno virtual
make venv

# Instalar dependencias
make install

# Ejecutar el juego
make run
```

### Instalación manual (Windows)

```powershell
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el juego
python -m src.main
```

## 📚 Objetivos de aprendizaje

Este proyecto está diseñado para estudiantes que han completado fundamentos de Python y están comenzando con POO. Incluye:

- Clases y objetos simples
- Herencia básica
- Gestión de estados
- Manejo de colisiones
- Persistencia de datos (JSON)
- Estructura de proyecto organizada

## ✅ Checklist de TODOs para implementar

- [ ] **TODO 1**: Añadir sistema de pausa con tecla P
- [ ] **TODO 2**: Implementar barra visual del cooldown
- [ ] **TODO 3**: Mejorar algoritmo de spawn de power-ups
- [ ] **TODO 4**: Añadir sprites personalizados y efectos sonoros
- [ ] **TODO 5**: Implementar dificultad progresiva cada 10 puntos
- [ ] **TODO 6**: Guardar historial de puntuaciones (top 5)
- [ ] **TODO 7**: Añadir efectos de partículas al destruir obstáculos
- [ ] **TODO 8**: Implementar diferentes tipos de obstáculos
- [ ] **TODO 9**: Crear menú de opciones para ajustar volumen
- [ ] **TODO 10**: Añadir animaciones de sprites

## 🏆 Sistema de puntuación

- **+1 punto**: Por cada obstáculo esquivado
- **+5 puntos**: Por cada obstáculo destruido con cuchillo
- **+10 puntos**: Por cada power-up recolectado
- **Récord**: Se guarda automáticamente en `best_score.json`

## 🎯 Rúbrica de evaluación (10 puntos)

1. **Lógica de juego básica (2 pts)**: Movimiento, colisiones, vidas
2. **POO y clases (2 pts)**: Implementación correcta de clases y métodos
3. **Colisiones y power-ups (2 pts)**: Sistema de detección y efectos
4. **Persistencia y HUD (2 pts)**: Guardado de datos y interfaz
5. **Pulido y presentación (2 pts)**: Código limpio y funcionalidad completa

## 🛠️ Estructura del proyecto

```
julias_run/
├── README.md
├── requirements.txt
├── .gitignore
├── Makefile
├── src/
│   ├── main.py          # Punto de entrada del juego
│   ├── settings.py      # Configuración y constantes
│   ├── entities.py      # Clases de entidades del juego
│   ├── abilities.py     # Sistema de power-ups y cooldowns
│   ├── game_states.py   # Estados del juego (menú, juego, game over)
│   └── utils.py         # Funciones auxiliares
├── assets/
│   ├── sprites/         # Imágenes del juego
│   └── sounds/          # Efectos de sonido
└── tests/
    └── test_utils.py    # Tests unitarios
```

## 📖 Referencias útiles

- [Documentación de Pygame](https://www.pygame.org/docs/)
- [Tutorial de POO en Python](https://docs.python.org/3/tutorial/classes.html)
- [Manejo de colisiones en Pygame](https://www.pygame.org/docs/ref/rect.html)

## 🤝 Contribuir

Este es un proyecto educativo. Se anima a los estudiantes a:

1. Completar los TODOs enumerados
2. Experimentar con nuevas funcionalidades
3. Mejorar el código existente
4. Añadir tests para las nuevas funciones

¡Buena suerte y que disfrutes programando! 🎮✨