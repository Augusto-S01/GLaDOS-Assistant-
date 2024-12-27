DOCKER_COMPOSE=docker compose
DOCKER_COMPOSE_FLAGS=-f docker-compose.yml
CHECK_NETWORK_SCRIPT=./_scripts/check_network.sh

.PHONY: up down build check_network

up: check_network build
	$(DOCKER_COMPOSE) $(DOCKER_COMPOSE_FLAGS) up -d

down:
	$(DOCKER_COMPOSE) $(DOCKER_COMPOSE_FLAGS) down

build:
	$(DOCKER_COMPOSE) $(DOCKER_COMPOSE_FLAGS) build

check_network:
	$(CHECK_NETWORK_SCRIPT)