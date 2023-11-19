[![pwe-build](https://github.com/vartmih/PWE/actions/workflows/fastapi-app.yml/badge.svg?branch=develop)](https://github.com/vartmih/PWE/actions/workflows/fastapi-app.yml)
<h1 align="center">PWE - plan, write, execute.</h1>

API для работы с индивидуальными задачами, с помощью авторизации (личного кабинета).

### Быстрый старт:

Переименовать файл `.env.example` в `.env` и по желанию изменить переменные.

```
mv .env.example .env
```

- ***Docker***:

```
docker compose up
```

- ***Локально***:  
  Для локального запуска приложения необходимо в файле .env заменить переменную `DB_HOST` на хост
  вашей базы данных PostgreSQL.

1. устанавливаем зависимости и виртуальное окружение

```
poetry install
```

2. накатываем миграции в базу данных

```
alembic upgrade head
```

3. запускаем приложение

```
python3 main.py
```
Тесты можно запустить с помощью команды
```
pytest
```  
или через `poetry`
```
poetry run pytest
```
### Дополнительная информация:

В проекте используется линтер `flake8`. Вот список плагинов, с помощью которых выполнялось форматирование кода:

- `flake8-bugbear`
- `pep8-naming`
- `flake8-async`
- `flake8-docstrings-complete`
- `flake8-fastapi`

`flake8`, а также `pytest` и дополнительные плагины указаны внутри `pyproject.toml` в качестве dev зависимостей.

***Документация к API сформирована автоматически FastAPI, ознакомиться с ней можно по маршруту:***  
`0.0.0.0:8000/docs` *- Swagger*  
`0.0.0.0:8000/redoc` *- ReDoc*
