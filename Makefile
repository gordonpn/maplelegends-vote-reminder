.DEFAULT_GOAL := help
.PHONY: up help db ci
SHELL := /bin/bash

up: ## Bring up dev stack with docker compose
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

db: ## Start an interactive mongo shell for the dev db
	source .env && docker exec -it maplelegends-vote-reminder-mongodb-dev mongosh "mongodb://127.0.0.1:27017/$$MONGO_INITDB_DATABASE" --username $$MONGO_NON_ROOT_USERNAME --password $$MONGO_NON_ROOT_PASSWORD

help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-20s\033[0m %s\n", $$1, $$2}'

ci: ## Generate the ci cd file
	drone jsonnet --format
