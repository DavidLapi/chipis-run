# Makefile para Julia's Run
# Comandos básicos para gestionar el proyecto

.PHONY: venv install run test clean help

# Crear entorno virtual
venv:
	python -m venv .venv
	@echo "Entorno virtual creado. Actívalo con: .venv\Scripts\activate (Windows) o source .venv/bin/activate (Linux/Mac)"

# Instalar dependencias
install:
	.venv\Scripts\activate && pip install -r requirements.txt

# Ejecutar el juego
run:
	.venv\Scripts\activate && python -m src.main

# Ejecutar tests
test:
	.venv\Scripts\activate && python -m unittest discover tests

# Limpiar archivos temporales
clean:
	rmdir /s /q __pycache__ 2>nul || echo "No hay cache para limpiar"
	rmdir /s /q .pytest_cache 2>nul || echo "No hay pytest cache para limpiar"
	del /q *.pyc 2>nul || echo "No hay archivos .pyc para limpiar"

# Mostrar ayuda
help:
	@echo "Comandos disponibles:"
	@echo "  make venv     - Crear entorno virtual"
	@echo "  make install  - Instalar dependencias"
	@echo "  make run      - Ejecutar el juego"
	@echo "  make test     - Ejecutar tests"
	@echo "  make clean    - Limpiar archivos temporales"
	@echo "  make help     - Mostrar esta ayuda"