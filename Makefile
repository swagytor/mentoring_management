PROJECT_NAME=mentoring_management
SERVICE_NAME=backend

up:
	docker compose -f docker/docker-compose.yml -p $(PROJECT_NAME) up --remove-orphans
build:
	docker compose -f docker/docker-compose.yml -p $(PROJECT_NAME) build --no-cache
developup:
	docker compose -f docker/docker-compose.yml -p $(PROJECT_NAME) up --remove-orphans
developbuild:
	docker compose -f docker/docker-compose.yml -p $(PROJECT_NAME) build --no-cache
migrations:
	docker exec -it $(PROJECT_NAME)-${SERVICE_NAME} python manage.py makemigrations
migrate:
	docker exec -it $(PROJECT_NAME)-${SERVICE_NAME} python manage.py migrate
startapp:
	docker exec -it $(PROJECT_NAME)-${SERVICE_NAME} python manage.py startapp $(app_name)
test:
	docker exec -it $(PROJECT_NAME)-${SERVICE_NAME} pytest .
lint:
	docker exec -it $(PROJECT_NAME)-${SERVICE_NAME} flake8 .
typecheck:
	docker exec -it $(PROJECT_NAME)-${SERVICE_NAME} mypy .
format:
	docker exec -it $(PROJECT_NAME)-${SERVICE_NAME} black .
sortimports:
	docker exec -it $(PROJECT_NAME)-${SERVICE_NAME} isort . --profile black --filter-files