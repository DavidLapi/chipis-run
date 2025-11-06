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
- [x] **TODO 4**: ✅ Añadir sprites personalizados y efectos sonoros
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
│   │   ├── julia_pixelart.jpg    # Sprite del personaje principal
│   │   ├── cachopo_pixelart.jpg  # Sprite de obstáculos
│   │   ├── knife__pixelart.jpg   # Sprite de cuchillos
│   │   └── vodka_pixelart.jpg    # Sprite de power-ups
│   └── sounds/          # Efectos de sonido
└── tests/
    └── test_utils.py    # Tests unitarios
```

## 🎨 Sistema de Sprites

El juego incluye un sistema completo de sprites que reemplaza los rectángulos de colores con gráficos pixelados:

### Características del Sistema de Sprites

**Carga Automática con Fallback:**
- Cada entidad intenta cargar su sprite correspondiente
- Si la imagen no existe, usa un rectángulo de color como fallback
- Mensajes informativos en consola sobre el estado de carga

**Sprites Disponibles:**
- `julia_pixelart.jpg` - Personaje principal (Julia)
- `cachopo_pixelart.jpg` - Obstáculos (Cachopos)
- `knife__pixelart.jpg` - Proyectiles (Cuchillos)
- `vodka_pixelart.jpg` - Power-ups (Vodka/Té)

**Efectos Visuales Mejorados:**
- Rotación de sprites (cuchillos girando, obstáculos cayendo)
- Escalado dinámico (power-ups con efecto de pulso)
- Volteo horizontal (Julia mirando izquierda/derecha)
- Tintes de color (escudo, diferentes tipos de power-ups)

**Optimización:**
- `convert_alpha()` para mejor rendimiento
- Escalado automático a dimensiones del juego
- Preservación del centro durante rotaciones

### Conceptos Educativos Cubiertos

**Gestión de Archivos:**
```python
# Carga de sprites con gestión de errores
sprite_path = os.path.join("assets", "sprites", "julia_pixelart.jpg")
image = pygame.image.load(sprite_path)
image = image.convert_alpha()  # Optimización
```

**Transformaciones de Imagen:**
```python
# Escalado
sprite = pygame.transform.scale(image, (width, height))
# Rotación
rotated = pygame.transform.rotate(sprite, angle)
# Volteo
flipped = pygame.transform.flip(sprite, True, False)
```

**Renderizado Avanzado:**
```python
# Dibujar sprite vs rectángulo
screen.blit(sprite, position)  # Sprite
pygame.draw.rect(screen, color, rect)  # Fallback
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

## 👥 Autoría y Licencia

### ✍️ Autoría
Creado y diseñado por: **Anaïs Rodríguez Villanueva**  
Contacto: [GitHub @Anais-RV](https://github.com/Anais-RV)

Este material educativo ha sido desarrollado de forma independiente y vocacional con el objetivo de proporcionar recursos de calidad para el aprendizaje de Python. Representa cientos de horas de trabajo en diseño pedagógico, creación de contenidos y desarrollo de ejercicios progresivos.

### 📄 Licencia y Uso
Este proyecto está licenciado bajo **MIT License** (ver `LICENSE`).

Esto significa que puedes:

✅ Usar este material para aprender o enseñar Python  
✅ Compartir el repositorio con estudiantes  
✅ Adaptar los ejercicios para tus necesidades  
✅ Hacer fork del proyecto  

Con la condición de:

⚠️ Mantener la atribución de autoría original en todos los materiales derivados  
⚠️ Incluir una referencia a este repositorio: [github.com/Anais-RV/python-fundamentos](https://github.com/Anais-RV/python-fundamentos)  
⚠️ Mencionar a Anaïs Rodríguez Villanueva como autora original  

**Uso comercial:**  
Si deseas usar este material en contextos comerciales (cursos de pago, bootcamps, formaciones empresariales), por favor:

- Mantén visiblemente la atribución de autoría  
- Considera contactar para una mención o colaboración  
- Respeta el espíritu educativo y vocacional del proyecto  

### 🤝 Contribuciones
Las contribuciones son bienvenidas y apreciadas. Al contribuir, aceptas que:

- Tu contribución se licenciará bajo los mismos términos (MIT)  
- La autoría original del proyecto se mantiene como Anaïs Rodríguez Villanueva  
- Las contribuciones significativas serán reconocidas en `CONTRIBUTING.md`  

Por favor, consulta `CONTRIBUTING.md` para más detalles sobre cómo participar en el proyecto.

### 💝 Reconocimientos
Este proyecto es un esfuerzo educativo independiente creado con dedicación para la comunidad de aprendizaje de Python. Si te ha sido útil, considera:

⭐ Dar una estrella al repositorio  
🔄 Compartir con otros estudiantes  
💬 Proporcionar feedback o mejoras  
📢 Mencionar el proyecto si lo usas en tus clases  

© 2025 Anaïs Rodríguez Villanueva. Material educativo de código abierto bajo licencia MIT.