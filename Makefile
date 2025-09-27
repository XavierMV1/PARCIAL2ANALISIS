# Makefile para el Sistema de Gestión de Productos de Panadería
# Autor: Christian Xwer Reyes Valenzuela
# Carné: 0907-22-6610

.PHONY: help install run test clean setup-db migrate upgrade downgrade docs format lint

# Variables
PYTHON = python
PIP = pip
UVICORN = uvicorn
ALEMBIC = alembic
PYTEST = pytest

# Colores para output
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m # No Color

help: ## Mostrar esta ayuda
	@echo "$(GREEN)Sistema de Gestión de Productos de Panadería$(NC)"
	@echo "$(YELLOW)Comandos disponibles:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Instalar dependencias
	@echo "$(YELLOW)Instalando dependencias...$(NC)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✓ Dependencias instaladas$(NC)"

setup-db: ## Configurar base de datos (crear migración inicial)
	@echo "$(YELLOW)Configurando base de datos...$(NC)"
	$(ALEMBIC) revision --autogenerate -m "Initial migration"
	@echo "$(GREEN)✓ Migración inicial creada$(NC)"

migrate: ## Aplicar migraciones
	@echo "$(YELLOW)Aplicando migraciones...$(NC)"
	$(ALEMBIC) upgrade head
	@echo "$(GREEN)✓ Migraciones aplicadas$(NC)"

upgrade: migrate ## Alias para migrate

downgrade: ## Revertir última migración
	@echo "$(YELLOW)Revirtiendo migración...$(NC)"
	$(ALEMBIC) downgrade -1
	@echo "$(GREEN)✓ Migración revertida$(NC)"

run: ## Ejecutar la aplicación
	@echo "$(YELLOW)Ejecutando aplicación...$(NC)"
	$(PYTHON) main.py

run-dev: ## Ejecutar la aplicación en modo desarrollo
	@echo "$(YELLOW)Ejecutando aplicación en modo desarrollo...$(NC)"
	$(UVICORN) main:app --reload --host 0.0.0.0 --port 8000

test: ## Ejecutar tests
	@echo "$(YELLOW)Ejecutando tests...$(NC)"
	$(PYTEST) tests/ -v
	@echo "$(GREEN)✓ Tests completados$(NC)"

test-coverage: ## Ejecutar tests con cobertura
	@echo "$(YELLOW)Ejecutando tests con cobertura...$(NC)"
	$(PYTEST) tests/ --cov=. --cov-report=html --cov-report=term
	@echo "$(GREEN)✓ Tests con cobertura completados$(NC)"

docs: ## Abrir documentación de la API
	@echo "$(YELLOW)Documentación disponible en:$(NC)"
	@echo "  $(GREEN)Swagger UI:$(NC) http://localhost:8000/docs"
	@echo "  $(GREEN)ReDoc:$(NC) http://localhost:8000/redoc"

format: ## Formatear código con black
	@echo "$(YELLOW)Formateando código...$(NC)"
	black *.py routers/ tests/ --line-length 88
	@echo "$(GREEN)✓ Código formateado$(NC)"

lint: ## Verificar código con flake8
	@echo "$(YELLOW)Verificando código...$(NC)"
	flake8 *.py routers/ tests/ --max-line-length 88 --ignore E203,W503
	@echo "$(GREEN)✓ Verificación completada$(NC)"

clean: ## Limpiar archivos temporales
	@echo "$(YELLOW)Limpiando archivos temporales...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -f .coverage
	@echo "$(GREEN)✓ Limpieza completada$(NC)"

init: install setup-db migrate ## Inicializar proyecto completo
	@echo "$(GREEN)✓ Proyecto inicializado correctamente$(NC)"

status: ## Mostrar estado del proyecto
	@echo "$(GREEN)Estado del proyecto:$(NC)"
	@echo "  $(YELLOW)Archivos principales:$(NC)"
	@ls -la *.py *.ini Makefile requirements.txt 2>/dev/null || echo "  No encontrados"
	@echo "  $(YELLOW)Estructura de directorios:$(NC)"
	@tree -I '__pycache__|*.pyc|.git' -a || find . -type d | head -10

# Comandos específicos para desarrollo
dev-setup: install setup-db migrate test ## Configuración completa para desarrollo
	@echo "$(GREEN)✓ Entorno de desarrollo configurado$(NC)"

# Comandos para producción
prod-check: test lint ## Verificaciones antes de producción
	@echo "$(GREEN)✓ Verificaciones de producción completadas$(NC)"

# Información del proyecto
info: ## Mostrar información del proyecto
	@echo "$(GREEN)Sistema de Gestión de Productos de Panadería$(NC)"
	@echo "$(YELLOW)Autor:$(NC) Christian Xwer Reyes Valenzuela"
	@echo "$(YELLOW)Carné:$(NC) 0907-22-6610"
	@echo "$(YELLOW)Curso:$(NC) Análisis de Sistemas II"
	@echo "$(YELLOW)Profesor:$(NC) Ing. Bayron Carranza"
	@echo "$(YELLOW)Versión:$(NC) 1.0.0"
