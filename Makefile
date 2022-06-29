.DEFAULT_GOAL := help
.PHONY: up help db ci config
SHELL := /bin/bash

up: ## Bring up dev stack with docker compose
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

config: ## Print docker compose dev stack
	docker compose -f docker-compose.yml -f docker-compose.dev.yml config

config-prod: ## Print docker compose prod stack
	docker compose -f docker-compose.yml -f docker-compose.prod.yml config

db: ## Start an interactive mongo shell for the dev db
	source .env && docker exec -it maplelegends-vote-reminder-mongodb-dev mongosh "mongodb://127.0.0.1:27017/$$MONGO_INITDB_DATABASE" --username $$MONGO_NON_ROOT_USERNAME --password $$MONGO_NON_ROOT_PASSWORD

help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-20s\033[0m %s\n", $$1, $$2}'

ci: ## Generate the ci cd file
	drone jsonnet --stream --format
