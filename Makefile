.EXPORT_ALL_VARIABLES:
COMPOSE_FILE ?= ./build/docker-compose/docker-compose.yml
FINANCE_CALCULATOR_SERVICE ?= finance_calculator_backend

DOTENV_BASE_FILE ?= .env
-include $(DOTENV_BASE_FILE)


.PHONY: start-server
start-server: docker-build docker-frontend-build docker-up

.PHONY: docker-up
docker-up:
	docker compose -f $(COMPOSE_FILE) up -d
	docker compose ps

.PHONY: docker-down
docker-down:
	docker compose down

.PHONY: docker-logs
docker-logs:
	docker compose logs --follow

.PHONY: docker-connect
docker-connect:
	docker compose exec -it $(FINANCE_CALCULATOR_SERVICE) /bin/bash

.PHONY: makemigrations
makemigrations:
	docker compose exec $(FINANCE_CALCULATOR_SERVICE) python ./finance_calculator/manage.py makemigrations

.PHONY: migrate
migrate:
	docker compose exec $(FINANCE_CALCULATOR_SERVICE) python ./finance_calculator/manage.py migrate

.PHONY: test
test:
	docker compose -f $(COMPOSE_FILE) exec $(FINANCE_CALCULATOR_SERVICE) pytest ./finance_calculator

.PHONY: lint
lint:
	docker compose -f $(COMPOSE_FILE) exec $(FINANCE_CALCULATOR_SERVICE) black ./finance_calculator

.PHONY: docker-build
docker-build:
	docker build \
		--tag=finance-calculator \
		--file=build/docker/finance-calculator/Dockerfile-finance-calculator \
		finance_calculator/

.PHONY: docker-frontend-build
docker-frontend-build:
	docker build \
		--tag=finance-calculator-frontend \
		--file=build/docker/frontend/Dockerfile-frontend \
		--target=prod-stage \
		./frontend/
