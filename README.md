# Plant Pal

### Разработка

Создать и активировать виртуальное окружение
```shell
$ python3.12 -m venv .venv
$ source .venv/bin/activate
```

Установить [poetry](https://github.com/python-poetry/poetry)
```shell
$ pip install poetry
```

Установить зависимости
```shell
$ poetry install --no-root
```

Создаем файл настроек .env на основе примера и заполняем
```shell
$ cp ./docker/.env.example ./docker/.env
```

**Важно!** Чтобы между запусками контейнеров данные сохранялись в бд, нужно в директории *docker* 
создать следующую структуру директорий:
```
docker/
└── data/
    └── postgresql/
        ├── data/
        └── log/
```

Поднять сервис и его инфраструктурные зависимости локально можно разными способами:
```shell
# Выполнив команду вручную
$ docker compose -f docker/docker-compose.dev.yaml up --wait

# Выполнив команду из Makefile
$ make up
```

Доступный перечень команд make можно посмотреть выполнив
```shell
$ make help
```

Запустить только сервер фастапи локально можно выполнив следующую команду из корня проекта:
```shell
$ make run_api
```