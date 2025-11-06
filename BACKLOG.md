# Julia's Run - Product Backlog 📋

Este es el backlog oficial del proyecto Julia's Run. Representa las tareas, bugs y mejoras que el equipo de desarrollo debe abordar.

## 🚨 Critical Issues (P0)

### Bug #001 - Performance Degradation with Multiple Obstacles
**Priority**: Critical  
**Status**: Open  
**Reporter**: QA Team  
**Assigned to**: -  

**Description**: El juego experimenta drops significativos de FPS cuando hay más de 15 obstáculos en pantalla simultáneamente.

**Steps to Reproduce**:
1. Jugar durante 2-3 minutos hasta que aparezcan muchos obstáculos
2. Observar el FPS counter (si está activado)
3. Notar stuttering y lag

**Expected**: 60 FPS constantes  
**Actual**: FPS baja a 15-20 con muchos objetos  

**Technical Notes**: Posible problema en el rendering loop o gestión de memoria de sprites.

---

### Bug #002 - Memory Leak in Particle System
**Priority**: Critical  
**Status**: Open  
**Reporter**: DevOps  
**Assigned to**: -  

**Description**: Las partículas de efectos visuales no se eliminan correctamente de memoria, causando memory leaks durante sesiones largas.

**Steps to Reproduce**:
1. Jugar durante 10+ minutos
2. Lanzar muchos cuchillos (genera partículas)
3. Monitorear uso de memoria RAM

**Expected**: Memoria estable  
**Actual**: Memoria crece continuamente hasta crash  

**Technical Notes**: Revisar clase `ParticleEffect` y su lifecycle.

---

### Bug #003 - Collision Detection Corner Case
**Priority**: High  
**Status**: Open  
**Reporter**: Player Feedback  
**Assigned to**: -  

**Description**: Las colisiones en las esquinas de los obstáculos son imprecisas. Jugadores reportan hits cuando visualmente no hay contacto.

**Steps to Reproduce**:
1. Posicionarse en esquina inferior de un obstáculo cayendo
2. El obstáculo "toca" al jugador sin contacto visual claro

**Expected**: Colisión solo cuando hay contacto visual real  
**Actual**: Colisiones prematuras en esquinas  

**Technical Notes**: Posible problema con `pygame.Rect.colliderect()` siendo demasiado permisivo.

---

## ⚠️ High Priority Features (P1)

### Feature #004 - Shield Power-Up
**Priority**: High  
**Status**: Planned  
**Requested by**: Game Design  
**Assigned to**: -  

**Description**: Implementar un nuevo power-up que otorgue un escudo temporal de 5 segundos.

**Acceptance Criteria**:
- [ ] Sprite visual del escudo
- [ ] Duración de 5 segundos
- [ ] Indicador visual cuando está activo
- [ ] Absorbe 1 hit y luego se desactiva
- [ ] Sonido/efecto al activarse y desactivarse

**Technical Requirements**: Extender sistema de power-ups existente.

---

### Feature #005 - Level Progression System
**Priority**: High  
**Status**: In Design  
**Requested by**: Product Owner  
**Assigned to**: -  

**Description**: Sistema de niveles que aumente la dificultad progresivamente.

**Acceptance Criteria**:
- [ ] Cada nivel dura 60 segundos
- [ ] Velocidad de obstáculos aumenta 10% por nivel
- [ ] Spawn rate aumenta 15% por nivel
- [ ] UI muestra nivel actual
- [ ] Bonus de puntos por completar nivel

---

### Bug #006 - Player Class Too Large (Code Smell)
**Priority**: High  
**Status**: Open  
**Reporter**: Code Review  
**Assigned to**: -  

**Description**: La clase `Player` tiene más de 200 líneas y viola el principio de responsabilidad única.

**Technical Debt**: Refactorizar en componentes:
- `PlayerMovement`: Manejo de input y física
- `PlayerGraphics`: Renderizado y animaciones  
- `PlayerState`: Vidas, escudo, power-ups
- `PlayerStats`: Puntuación y estadísticas

---

## 💡 Medium Priority Improvements (P2)

### Feature #007 - Audio System
**Priority**: Medium  
**Status**: Planned  
**Requested by**: UX Team  
**Assigned to**: -  

**Description**: Añadir efectos de sonido y música de fondo.

**Scope**:
- [ ] Música de fondo en loop
- [ ] SFX para saltos, lanzamientos, colisiones
- [ ] SFX para power-ups
- [ ] Control de volumen en settings

---

### Feature #008 - Improved Visual Effects
**Priority**: Medium  
**Status**: Planned  
**Requested by**: Art Team  
**Assigned to**: -  

**Description**: Mejorar efectos visuales para mayor juice y feedback.

**Ideas**:
- [ ] Screen shake en colisiones
- [ ] Partículas mejoradas
- [ ] Trails para objetos en movimiento
- [ ] Transiciones suaves entre estados

---

### Bug #009 - Magic Numbers Everywhere
**Priority**: Medium  
**Status**: Open  
**Reporter**: Code Review  
**Assigned to**: -  

**Description**: Muchos valores hardcodeados sin constantes definidas.

**Examples**:
```python
# En lugar de:
if self.timer > 60:  # ¿Qué significa 60?

# Debería ser:
if self.timer > POWER_UP_DURATION:
```

**Task**: Identificar y convertir a constantes en `settings.py`.

---

## 🔧 Low Priority Tasks (P3)

### Feature #010 - Unit Testing Framework
**Priority**: Low  
**Status**: Future  
**Requested by**: QA Team  
**Assigned to**: -  

**Description**: Implementar tests unitarios para funciones críticas.

**Scope**:
- [ ] Tests para detección de colisiones
- [ ] Tests para lógica de power-ups  
- [ ] Tests para cálculos de puntuación
- [ ] Setup de CI/CD básico

---

### Feature #011 - Configuration Persistence
**Priority**: Low  
**Status**: Future  
**Requested by**: UX Team  
**Assigned to**: -  

**Description**: Guardar configuraciones de usuario (controles, volumen, etc.)

**Technical**: Extender sistema de persistencia actual.

---

### Feature #012 - Mobile Controls
**Priority**: Low  
**Status**: Future  
**Requested by**: Mobile Team  
**Assigned to**: -  

**Description**: Adaptar controles para dispositivos táctiles.

**Scope**: Virtual joystick y botones touch.

---

## 🏆 Epic Features (Future)

### Epic #013 - Multiplayer Support
**Priority**: Future  
**Status**: Concept  
**Requested by**: Community  

**Description**: Modo multijugador local (split-screen).

**Complexity**: Epic - Requiere refactoring significativo.

---

### Epic #014 - Level Editor
**Priority**: Future  
**Status**: Concept  
**Requested by**: Community  

**Description**: Editor visual para crear niveles personalizados.

**Complexity**: Epic - Nuevo sistema completo.

---

## 📊 Sprint Planning

### Current Sprint (Sprint 23)
**Duration**: 2 weeks  
**Sprint Goal**: Fix critical performance issues

**Selected Items**:
- [ ] Bug #001 - Performance Degradation
- [ ] Bug #002 - Memory Leak
- [ ] Bug #009 - Magic Numbers (partial)

### Next Sprint (Sprint 24)
**Proposed Focus**: New features and UX improvements

**Candidates**:
- Feature #004 - Shield Power-Up
- Bug #003 - Collision Detection
- Feature #007 - Audio System (planning)

---

## 📈 Definition of Done

For any task to be considered complete:

**Code Quality**:
- [ ] Code passes all existing tests
- [ ] New code has appropriate comments
- [ ] No new critical code smells introduced
- [ ] Performance impact measured and acceptable

**Testing**:
- [ ] Manual testing completed
- [ ] Edge cases tested
- [ ] No regressions introduced
- [ ] Game remains playable on target devices

**Documentation**:
- [ ] Code changes documented
- [ ] User-facing changes added to README
- [ ] Breaking changes communicated to team

---

## 🎯 How to Contribute

1. **Pick a task** from this backlog
2. **Create a branch**: `git checkout -b feature/issue-XXX`
3. **Work on the task** following DoD criteria
4. **Test thoroughly** - don't break the game!
5. **Create PR** with clear description
6. **Move task** to "In Review" status

---

*Este backlog se actualiza semanalmente en las reuniones de sprint planning. Para sugerir nuevas features o reportar bugs, crea un issue en el repositorio.*