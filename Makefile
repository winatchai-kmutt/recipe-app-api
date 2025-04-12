# Define variables for convenience
DOCKER_COMPOSE = docker compose run --rm app sh -c
PYTHON_CMD = python manage.py

# Target to run tests
test:
	$(DOCKER_COMPOSE) "$(PYTHON_CMD) test"

# Target to start the server
run:
	$(DOCKER_COMPOSE) "$(PYTHON_CMD) runserver"

# Target to run flake8
lint:
	$(DOCKER_COMPOSE) "flake8"
