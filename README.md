# Julia's Run - Legacy Codebase Challenge 🏃‍♀️

¡Bienvenido al equipo de desarrollo! Has sido asignado para trabajar en **Julia's Run**, un juego existente que necesita mantenimiento y mejoras.

## 🎯 Tu Misión

Este no es un proyecto desde cero. **Julia's Run** es un juego **funcional pero legacy** que ya está en producción. Tu trabajo es:

1. **🔍 Analizar** el código existente y entender cómo funciona
2. **🐛 Encontrar** problemas y áreas de mejora
3. **🚀 Implementar** nuevas características sin romper lo existente
4. **♻️ Refactorizar** código problemático manteniendo la funcionalidad

## 🎮 ¿Qué es Julia's Run?

Un juego de supervivencia donde Julia debe esquivar cachopos que caen del cielo mientras lanza cuchillos para defenderse. El juego incluye power-ups, sistema de combos, efectos visuales y persistencia de puntuaciones.

### Características Actuales
- ✅ Movimiento fluido del personaje
- ✅ Sistema de colisiones
- ✅ Power-ups (Vodka Boost y Té Mágico)
- ✅ Sistema de combos y puntuaciones
- ✅ Efectos visuales y de partículas
- ✅ Sprites pixelart integrados
- ✅ Persistencia de estadísticas
- ✅ Estados de juego (menú, jugando, pausa, game over)

## 🏗️ Arquitectura del Proyecto

```
julias_run/
├── src/
│   ├── main.py          # 🎮 Punto de entrada y game loop principal
│   ├── entities.py      # 👾 Clases de entidades (Player, Obstacle, etc.)
│   ├── abilities.py     # ⚡ Sistema de habilidades y efectos
│   ├── game_states.py   # 🎯 Gestión de estados del juego
│   ├── settings.py      # ⚙️ Configuración y constantes
│   └── utils.py         # 🛠️ Funciones auxiliares
├── assets/
│   └── sprites/         # 🎨 Imágenes del juego
└── game_stats.json      # 📊 Estadísticas persistentes
```

## 🚀 Setup Rápido

```bash
# 1. Instalar dependencias
pip install pygame

# 2. Ejecutar el juego
python src/main.py

# 3. Controles
# ⬅️➡️⬆️⬇️ - Mover a Julia
# ESPACIO - Lanzar cuchillo
# P - Pausar
# ESC - Salir
```

## 🔍 Análisis del Código - Tu Primer Día

### Paso 1: Ejecuta y Juega
Antes de tocar código, **ejecuta el juego** y juega al menos 5 minutos. Observa:
- ¿Qué funciona bien?
- ¿Qué se siente extraño o lento?
- ¿Hay bugs evidentes?
- ¿Qué mejorarías como jugador?

### Paso 2: Mapeo de Arquitectura
Explora estos archivos en orden:

1. **`settings.py`** - Entiende las constantes del juego
2. **`main.py`** - Sigue el game loop principal
3. **`entities.py`** - Analiza las clases principales
4. **`game_states.py`** - Comprende la máquina de estados

### Paso 3: Preguntas Clave
Mientras lees el código, pregúntate:

- ❓ **¿Cómo se crean los obstáculos?** (Pista: busca `should_spawn_obstacle`)
- ❓ **¿Dónde se detectan las colisiones?** (Pista: método `colliderect`)
- ❓ **¿Cómo funciona el sistema de combos?** (Pista: clase `ComboSystem`)
- ❓ **¿Qué hace el sistema de sprites?** (Pista: función `load_sprite_with_fallback`)

## 🐛 Problemas Conocidos (Issues)

El juego funciona, pero tiene algunos problemas que necesitan atención:

### 🔥 Críticos
- **Performance**: El juego se ralentiza con muchos obstáculos en pantalla
- **Memory leak**: Las partículas no se limpian correctamente
- **Collision bugs**: Colisiones imprecisas en esquinas

### ⚠️ Importantes  
- **Code smell**: La clase `Player` es demasiado grande (>200 líneas)
- **Magic numbers**: Muchos números hardcodeados sin constantes
- **No tests**: Cero cobertura de testing

### 💡 Mejoras Deseadas
- **Nuevos power-ups**: Escudo temporal, slow-motion
- **Niveles**: Sistema de progresión por niveles
- **Audio**: Efectos de sonido y música
- **Leaderboard**: Top 10 mejores puntuaciones
- **Mobile**: Controles táctiles

## 🎯 Retos Sugeridos (Por Dificultad)

### 🟢 Beginner
1. **Encuentra y documenta** 3 magic numbers y conviértelos en constantes
2. **Añade un nuevo color** de obstáculo con comportamiento diferente  
3. **Mejora los mensajes de debug** para ser más informativos
4. **Crea un power-up nuevo** basado en los existentes

### 🟡 Intermediate
5. **Refactoriza** la clase `Player` dividiéndola en componentes más pequeños
6. **Implementa un sistema básico de testing** para colisiones
7. **Optimiza el renderizado** para mejorar FPS con muchos objetos
8. **Añade persistencia** para configuraciones de usuario

### 🔴 Advanced
9. **Implementa un sistema de niveles** con dificultad progresiva
10. **Crea un editor de niveles** visual para diseñar pantallas
11. **Añade networking** para multijugador local
12. **Implementa shaders** para efectos visuales avanzados

## 🧪 Testing Your Changes

```bash
# Ejecutar el juego después de cambios
python src/main.py

# Verificar que no rompiste nada:
# 1. ¿El juego inicia correctamente?
# 2. ¿Las colisiones funcionan?
# 3. ¿Los power-ups aparecen?
# 4. ¿Se puede pausar y reanudar?
# 5. ¿Las puntuaciones se guardan?
```

## 📚 Recursos de Aprendizaje

### Python Game Development
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Real Python - Game Development](https://realpython.com/pygame-a-primer/)

### Clean Code & Refactoring
- [Refactoring Guru](https://refactoring.guru/)
- [Clean Code principles](https://blog.cleancoder.com/)

### Game Development Patterns
- [Game Programming Patterns](https://gameprogrammingpatterns.com/)
- [Entity-Component-System](https://www.gamedev.net/tutorials/programming/general-and-gameplay-programming/understanding-component-entity-systems-r3013/)

## 🤝 Contributing Guidelines

### Before Making Changes
1. **Create a new branch**: `git checkout -b feature/your-feature-name`
2. **Run the game** to ensure it works before your changes
3. **Document your changes** in comments

### Code Style
- Use **descriptive variable names** (`player_speed` not `ps`)
- **Comment complex logic** - future you will thank you
- **Keep functions small** - one responsibility per function
- **Use constants** instead of magic numbers

### Commit Messages
```bash
git commit -m "fix: correct collision detection in corners"
git commit -m "feat: add shield power-up with 5-second duration"
git commit -m "refactor: split Player class into smaller components"
```

## 🎖️ Achievement System

Tracks your progress in understanding and improving the codebase:

- 🔍 **Code Detective** - Find and fix 3 bugs
- 🧹 **Refactor Master** - Successfully refactor a large class
- ⚡ **Performance Guru** - Improve FPS by 20%
- 🎨 **Feature Creator** - Add a new game mechanic
- 🧪 **Test Champion** - Achieve 50% test coverage
- 📚 **Documentation Hero** - Document all major functions

## ❓ Getting Help

### Stuck? Try This Order:
1. **Read the code** - Often the answer is there
2. **Debug print statements** - See what's happening
3. **Draw on paper** - Visualize the game flow
4. **Google the error** - Someone else had this problem
5. **Ask for help** - But explain what you tried first

### Common Questions

**Q: ¿Dónde empiezo si quiero añadir una nueva característica?**
A: Busca características similares existentes y úsalas como template.

**Q: ¿Cómo debuggeo problemas de colisión?**
A: Activa el modo debug en `settings.py` para ver las hitboxes.

**Q: ¿Puedo cambiar la arquitectura completamente?**
A: Mejor refactoriza gradualmente. Los cambios grandes rompen cosas.

---

## 🎮 ¡Que comience la aventura!

Recuerda: **Este es código real** que funciona. Tu objetivo no es reescribirlo desde cero, sino **mejorarlo incrementalmente** como harías en cualquier trabajo de desarrollo.

**¡Diviértete explorando y mejorando Julia's Run!** 🚀

---

*💡 Tip: El mejor código es el que otros desarrolladores pueden entender y mantener fácilmente.*