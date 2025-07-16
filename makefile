default: help

export DOCKER_ENV_PATH = docker/.env
export DOCKER_COMPOSE_PATH = docker/docker-compose.yaml
export DOCKER_COMPOSE_DEV_PATH = docker/docker-compose.dev.yaml

HELP_FORMAT = "	\033[36m%-25s\033[0m %s\n"
help: ## Display information about commands
	@echo "Available commands:"
	@grep -E '^[^ ]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS = ":.*?## "}; \
			{printf $(HELP_FORMAT), $$1, $$2}'
	@echo

--check-env-location:
	@if [ ! -e "$(DOCKER_ENV_PATH)" ]; then\
		echo "File $(DOCKER_ENV_PATH) not found";\
		exit 1;\
	fi

--cleanup-docker-containers:
	@docker ps -q | xargs docker stop > /dev/null 2> /dev/null || true
	@docker ps -aq | xargs docker rm > /dev/null 2> /dev/null || true

up: --check-env-location --cleanup-docker-containers ## Create and start project containers
	@docker compose -f "$(DOCKER_COMPOSE_DEV_PATH)" \
		--env-file "$(DOCKER_ENV_PATH)" \
		up --wait

down: ## Stop and remove project containers
	@docker compose -f "$(DOCKER_COMPOSE_DEV_PATH)" \
		--env-file "$(DOCKER_ENV_PATH)" \
		down

run_api: ## Локально запустить сервер фастапи
	export ENVIRONMENT="local" && python ./src/core/api_entrypoint.py