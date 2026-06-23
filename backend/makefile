.PHONY: install lint typecheck run


help:
	@echo "Comandos disponibles: "
	@echo "make install: Instala dependencias del proyecto"
	@echo "make lint: Llama a ruff para revisar el codigo"
	@echo "make typecheck: Llama a mypy para revisar el tipado"
	@echo "make run: Ejecuta el servidor de desarrollo de fastapi"

install:
	uv sync

lint:
	@uv run ruff check .

typecheck:
	@uv run mypy .

run:
	@uv run fastapi dev

dev: lint typecheck run
