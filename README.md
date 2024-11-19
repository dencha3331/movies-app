# Movies App

## Описание

Movies App - это веб-приложение, позволяющее пользователям просматривать и управлять списком своих любимых фильмов.
Приложение хранит информацию о фильмах и позволяет пользователям добавлять, удалять и редактировать записи.

## Требования

- Python 3.12+
- [Kinopoisk API Unofficial API-ключ](https://kinopoiskapiunofficial.tech/)


- Docker (необязательно)
- Docker Compose (необязательно)
- Poetry (необязательно)

## API

- `POST` `/register`: Регистрация нового пользователя с указанием имени пользователя и пароля.
- `POST` `/login`: Аутентификация пользователя и получение JWT токена.
- `GET` `/profile`: Получение информации о текущем аутентифицированном пользователе.
- `GET` `/movies/search?query=НазваниеФильма`: Ищет фильмы по названию. Возвращает результаты поиска с основной информацией о фильмах.
- `GET` `/movies/{kinopoisk_id}`: Получает подробную информацию о фильме по его Kinopoisk ID.
- `POST` `/movies/favorites`: Добавляет фильм в список избранных пользователя по Kinopoisk ID.
- `DELETE` `/movies/favorites/{kinopoisk_id}`: Удаляет фильм из списка избранных пользователя.
- `GET` `/movies/favorites`: Возвращает список избранных фильмов пользователя с подробной информацией.
    

## Установка

---

Клонировать репозиторий: 
``` bash
git clone https://github.com/username/movies-app.git`
cd movies-app
```

### Конфигурация

Создать файл `.env` и добавить [Kinopoisk API Unofficial API-ключ](https://kinopoiskapiunofficial.tech/)
```jsunicoderegexp
APP_CONFIG__KINOPOISK__API_KEY=Your API key
```

Все остальные необходимые переменные окружения для запуска уже есть в .env.example, но вы можете их переопределить.


---

+ ### Poetry or Pip:

 ### Установить зависимостей: 

#### 1. Создать виртуальное окружение:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 2. Установить зависимости:


``` bash
poetry install
```

#### Или

``` bash
pip install -r requirements.txt
```
Установка таблиц базы данных:

```bash
alembic upgrade head
```

#### 3. Запуск приложения: 

```bash
cd app/
python3 main.py
```
#### или

```bash
PYTHONPATH=app python3 app/main.py
```
___

+ ### Docker Compose + Docker:



#### 1. C makefile:


Запустить контейнеры с приложением и базой данных:

```bash
make all
```

Запустить только приложение:

```bash
make app
```

Запустить только базу данных:

```bash
make postgres
```

#### Закрытие контейнеров:

```bash
make all-down  # закрытие приложения и базы данных
make app-down  # закрытие приложения
make postgres-down  # закрытие базы данных
```

#### 2. Docker Compose:

```bash
# запустить контейнер с приложением
docker compose --env-file .env -f docker_compose/app.yaml up --build -d

# запустить контейнер с базой данных
docker compose --env-file .env -f docker_compose/postgresql.yaml up --build -d
```



# Лицензия

- MIT License

