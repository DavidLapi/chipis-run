# Developer Onboarding Guide 🚀

¡Bienvenido al equipo de desarrollo de Julia's Run! Esta guía te ayudará a ponerte al día rápidamente y empezar a contribuir de manera efectiva.

## 📋 Checklist del Primer Día

### Setup Inicial
- [ ] Clonar el repositorio
- [ ] Instalar Python 3.7+ y pygame
- [ ] Ejecutar el juego exitosamente
- [ ] Leer este documento completo
- [ ] Revisar el [BACKLOG.md](BACKLOG.md)
- [ ] Configurar entorno de desarrollo

### Exploración del Código
- [ ] Ejecutar el juego al menos 15 minutos
- [ ] Leer `settings.py` completo
- [ ] Seguir el flow del `main.py`
- [ ] Explorar clases en `entities.py`
- [ ] Entender estados en `game_states.py`

### Primera Contribución
- [ ] Elegir un task de nivel Beginner del backlog
- [ ] Crear rama para el task
- [ ] Implementar cambio pequeño
- [ ] Testear que no rompe nada
- [ ] Crear PR

## 🏗️ Arquitectura del Proyecto

### Flujo Principal del Juego
```
main.py
├── JuliasRunGame.__init__()     # Inicialización pygame
├── JuliasRunGame.run()          # Game loop principal
│   ├── handle_events()          # Input del usuario
│   ├── update()                 # Lógica del juego
│   └── draw()                   # Renderizado
└── cleanup()                    # Limpieza al salir
```

### Gestión de Estados
```
game_states.py
├── MenuState        # Pantalla principal
├── PlayingState     # Juego activo
├── PausedState      # Juego pausado
└── GameOverState    # Fin de partida
```

### Entidades del Juego
```
entities.py
├── Player          # Personaje principal (Julia)
├── Obstacle        # Cachopos que caen
├── Knife           # Proyectiles del jugador
├── PowerUp         # Items especiales
├── Enemy           # Enemigos inteligentes
├── Explosion       # Efectos de destrucción
└── ScreenEffect    # Efectos de pantalla
```

## 🔍 Code Deep Dive

### Game Loop Pattern
El juego sigue el patrón clásico de game loop:

```python
while running:
    # 1. Handle Input
    for event in pygame.event.get():
        # Process user input
    
    # 2. Update Game State
    player.update()
    for obstacle in obstacles:
        obstacle.update()
    
    # 3. Render Everything
    screen.fill(BLACK)
    player.draw(screen)
    for obstacle in obstacles:
        obstacle.draw(screen)
    pygame.display.flip()
    
    # 4. Control Timing
    clock.tick(60)  # 60 FPS
```

### Entity Lifecycle
Todas las entidades siguen un patrón similar:

```python
class GameEntity:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, width, height)
        self.load_sprite()  # Cargar imagen
    
    def update(self):
        # Update position, state, animations
        pass
    
    def draw(self, screen):
        # Render on screen
        screen.blit(self.sprite, self.rect)
    
    def is_alive(self):
        # Check if entity should be removed
        return True
```

### Sprite System
El sistema de sprites tiene fallbacks automáticos:

```python
def load_sprite_with_fallback(path, fallback_color, width, height):
    try:
        sprite = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(sprite, (width, height)), False
    except:
        # Create colored rectangle as fallback
        return create_fallback_sprite(fallback_color, width, height), True
```

## 🧪 Testing Strategy

### Manual Testing Checklist
Después de cualquier cambio, verifica:

```bash
# 1. El juego inicia sin errores
python src/main.py

# 2. Funcionalidad básica
# - ¿Se puede mover Julia?
# - ¿Aparecen obstáculos?
# - ¿Se pueden lanzar cuchillos?
# - ¿Funcionan las colisiones?

# 3. Estados del juego
# - ¿Funciona el menú?
# - ¿Se puede pausar con P?
# - ¿Aparece game over al morir?
# - ¿Se puede volver al menú?

# 4. Power-ups
# - ¿Aparecen power-ups?
# - ¿Funcionan sus efectos?
# - ¿Se ven los efectos visuales?

# 5. Persistencia
# - ¿Se guarda la mejor puntuación?
# - ¿Se mantienen las estadísticas?
```

### Performance Testing
```bash
# Verificar FPS bajo carga
# 1. Jugar 5+ minutos
# 2. Esperar que aparezcan muchos obstáculos
# 3. Verificar que FPS se mantiene estable
# 4. Monitorear uso de memoria
```

## 🐛 Debugging Tips

### Debugging Visual
Activa el modo debug en `settings.py`:
```python
DEBUG_MODE = True          # Muestra hitboxes
SHOW_FPS = True           # Muestra FPS counter
DEBUG_COLLISIONS = True   # Destaca colisiones
```

### Print Debugging
Estratégicamente coloca prints para entender el flow:
```python
# En update loops
print(f"Player pos: {self.rect.x}, {self.rect.y}")

# En colisiones
print(f"Collision detected: {player.rect} vs {obstacle.rect}")

# En spawning
print(f"Spawning obstacle at frame {frame_count}")
```

### Common Issues y Soluciones

**Issue**: "Game is laggy"  
**Debug**: Check FPS counter, profile object counts  
**Solution**: Limit max objects, optimize drawing  

**Issue**: "Sprites not loading"  
**Debug**: Check file paths, verify assets folder  
**Solution**: Verify asset files exist, check relative paths  

**Issue**: "Collisions feel wrong"  
**Debug**: Enable collision debug mode  
**Solution**: Adjust hitboxes, review collision logic  

## 📁 File Organization Guidelines

### Naming Conventions
```python
# Variables and functions
player_speed = 5
obstacle_count = 0

def calculate_score():
    pass

# Classes
class PowerUpEffect:
    pass

# Constants
SCREEN_WIDTH = 800
MAX_OBSTACLES = 20
```

### Code Comments
```python
# Single line for simple explanations
player.x += speed  # Move player right

# Multi-line for complex logic
"""
This function calculates the spawn rate of obstacles based on:
1. Current game time
2. Player score
3. Difficulty multiplier
"""

# TODO comments for future work
# TODO: Add sound effects for power-ups
# FIXME: Collision detection in corners is imprecise
# HACK: Temporary fix for memory leak - needs proper solution
```

### File Structure Rules
- **One class per file** (when possible)
- **Related functions together**
- **Constants at top of file**
- **Imports grouped and sorted**

## 🎯 Contribution Guidelines

### Branch Naming
```bash
feature/shield-powerup      # New features
bugfix/collision-corners    # Bug fixes
refactor/player-class       # Code improvements
hotfix/critical-crash       # Emergency fixes
```

### Commit Messages
Follow conventional commits:
```bash
feat: add shield power-up with 5-second duration
fix: correct collision detection in obstacle corners  
refactor: split Player class into smaller components
docs: update README with new power-up information
test: add unit tests for collision system
```

### Code Review Checklist
Antes de crear PR, verifica:

**Functionality**:
- [ ] Change works as intended
- [ ] No regressions introduced
- [ ] Edge cases considered

**Code Quality**:
- [ ] Functions are small and focused
- [ ] Variable names are descriptive
- [ ] No magic numbers
- [ ] Comments explain "why", not "what"

**Performance**:
- [ ] No unnecessary object creation in loops
- [ ] Sprites loaded once, not every frame
- [ ] No memory leaks introduced

## 🚀 Common Tasks

### Adding a New Power-Up
1. **Define sprite** in `assets/sprites/`
2. **Add type** to `PowerUp` class in `entities.py`
3. **Implement effect** in `abilities.py`
4. **Add spawn logic** in `utils.py`
5. **Update settings** in `settings.py`

### Adding a New Obstacle Type
1. **Extend Obstacle class** or create new class
2. **Add unique behavior** in `update()` method
3. **Add visual distinction** in `draw()` method
4. **Update spawn logic** to include new type

### Performance Optimization
1. **Profile first**: Identify actual bottlenecks
2. **Object pooling**: Reuse objects instead of creating new ones
3. **Efficient drawing**: Batch draws, use dirty rectangles
4. **Memory management**: Clean up unused objects

## 🎓 Learning Resources

### Pygame Específico
- [Pygame Documentation](https://www.pygame.org/docs/) - Reference oficial
- [Real Python Pygame Tutorial](https://realpython.com/pygame-a-primer/) - Tutorial comprensivo

### Game Development
- [Game Programming Patterns](https://gameprogrammingpatterns.com/) - Patrones esenciales
- [Gamasutra](https://www.gamasutra.com/) - Artículos de industria

### Python Best Practices
- [PEP 8](https://www.python.org/dev/peps/pep-0008/) - Style guide
- [Clean Code](https://blog.cleancoder.com/) - Principios de código limpio

## 💡 Pro Tips

### Development Workflow
```bash
# 1. Always start with fresh master
git checkout master
git pull origin master

# 2. Create feature branch
git checkout -b feature/my-awesome-feature

# 3. Make small, focused commits
git add specific_files
git commit -m "specific change description"

# 4. Test frequently
python src/main.py  # After each significant change

# 5. Push and create PR when ready
git push origin feature/my-awesome-feature
```

### Productivity Hacks
- **Use IDE debugging**: Set breakpoints instead of print statements
- **Hot reload**: Modify settings.py while game runs to see changes
- **Quick testing**: Create test scenarios in main.py for specific features
- **Git stash**: Save work in progress when switching tasks

### Avoid Common Pitfalls
- **Don't optimize prematurely**: Profile first, then optimize
- **Don't break existing features**: Always test backward compatibility
- **Don't hardcode values**: Use constants from settings.py
- **Don't ignore edge cases**: Test with extreme values

---

## 🤝 Getting Help

### Escalation Path
1. **Try debugging yourself** (15-30 minutes)
2. **Search online** for similar issues
3. **Check git history** for related changes
4. **Ask team member** with context of what you tried
5. **Escalate to senior dev** if blocking

### Asking Good Questions
```
❌ "My code doesn't work"

✅ "I'm trying to add a new power-up but the sprite isn't loading. 
   I added the file to assets/sprites/ and followed the same pattern 
   as vodka_pixelart.jpg, but get a FileNotFoundError. 
   Here's my code: [code snippet]"
```

---

¡Bienvenido al equipo! 🎉 Este es un proyecto legacy real donde aprenderás las skills que usarás en el trabajo día a día. No dudes en preguntar y experimentar.

**Recuerda**: El mejor código es el que el siguiente desarrollador puede entender fácilmente. ¡Haz que ese desarrollador sea tu futuro yo!

*Happy coding!* 🚀