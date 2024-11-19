DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
APP_FILE = docker_compose/app.yaml
POSTGRES_FILE = docker_compose/postgresql.yaml
APP_CONTAINER = movies-app
ENV = --env-file .env

.PHONY: app
app:
	${DC} ${ENV} -f ${APP_FILE} up --build -d

.PHONY: postgres
postgres:
	${DC} ${ENV} -f ${POSTGRES_FILE} up --build -d

.PHONY: all
all:
	${DC} ${ENV} -f ${POSTGRES_FILE} -f ${APP_FILE} up --build -d

.PHONY: all-down
all-down:
	${DC} ${ENV} -f ${POSTGRES_FILE} -f ${APP_FILE} down

.PHONY: app-down
app-down:
	${DC} ${ENV} -f ${APP_FILE} down

.PHONY: postgres-down
postgres-down:
	${DC} ${ENV} -f ${POSTGRES_FILE} down

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: test
test:
	${EXEC} ${APP_CONTAINER} pytest