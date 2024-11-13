DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
APP_FILE = docker_compose/app.yaml
POSTGRES_FILE = docker_compose/postgresql.yaml
APP_CONTAINER = kinopoisk-app

.PHONY: app
app:
	${DC} -f ${APP_FILE} up --build -d

.PHONY: postgres
postgres:
	${DC} -f ${POSTGRES_FILE} up --build -d

.PHONY: all
all:
	${DC} -f ${POSTGRES_FILE} -f ${APP_FILE} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down

.PHONY: postgres-down
postgres-down:
	${DC} -f ${POSTGRES_FILE} down

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: test
test:
	${EXEC} ${APP_CONTAINER} pytest