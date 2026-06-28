# Система управления общежитием

Дипломный проект на базе FastAPI и PostgreSQL.

## Используемые технологии

* Python 3.13
* FastAPI
* SQLAlchemy (Async)
* PostgreSQL 17
* asyncpg
* Docker
* Docker Compose

---

# Требования

Перед запуском необходимо установить:

* Docker Desktop
* Git

После установки Docker Desktop убедитесь, что он запущен.

---

# Клонирование проекта

Откройте терминал и выполните:

```bash
git clone https://github.com/zAukaRS/diplom.git
```

Перейдите в папку проекта:

```bash
cd REPOSITORY
```

---

# Первый запуск

Запустите проект одной командой:

```bash
docker compose up --build
```

При первом запуске Docker автоматически:

* скачает необходимые образы;
* соберет backend;
* создаст контейнер PostgreSQL;
* создаст базу данных;
* импортирует файл `data.sql`;
* запустит FastAPI.

Первый запуск может занять несколько минут.

---

# Доступ к приложению

FastAPI:

```
http://localhost:8000
```

Swagger UI:

```
http://localhost:8000/docs
```

ReDoc:

```
http://localhost:8000/redoc
```

---

# Повторный запуск

После первого запуска достаточно выполнить:

```bash
docker compose up
```

---

# Полная пересборка проекта

Если необходимо полностью удалить базу данных и создать её заново:

```bash
docker compose down -v
docker compose up --build
```

После удаления Docker Volume база данных будет автоматически восстановлена из файла `postgres/init/data.sql`.

---

# Остановка проекта

```bash
docker compose down
```

---

# Структура проекта

```
.
├── app
├── postgres
│   └── init
│       └── data.sql
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.docker
└── README.md
```
