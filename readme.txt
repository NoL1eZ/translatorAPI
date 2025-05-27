0. В самом начале создайте БД postgreSQL и настройте файл .env в корне проекта

Примерное наполнение:

DB_USER=postgres
DB_PASSWORD=secret
DB_NAME=mydatabase
DB_HOST=localhost
DB_PORT=5432


1. Общее описание

    Назначение API: Система учета переводов манги/ранобэ с учетом ролей, подмен и глав.

    Основные функции:

        Управление людьми, ролями, тайтлами и главами

        Фиксация подмен участников

        Отслеживание прогресса перевода

    Технологии: FastAPI, SQLAlchemy, PostgreSQL/SQLite, Pydantic

2. Требования

    Python: 3.12+

    Зависимости: requirements.txt (FastAPI, SQLAlchemy и др.)

    База данных: PostgreSQL 14+ или SQLite 3

    Дополнительно: Docker (для запуска в контейнере)

3. Установка и запуск

# Клонирование репозитория
git clone https://github.com/NoL1eZ/translatorAPI.git
cd translatorAPI

# Установка зависимостей
pip install -r requirements.txt

# Настройка окружения (копируем и редактируем .env)
cp .env.example .env

# Запуск
uvicorn app.main:app --reload

# Запуск через докер

docker build -t translator-api .
docker run -d -p 8000:8000 translator-api


5 Эндпоинты

Все эндпоинты можно увидеть после запуска приложения командой uvicorn app.main:app --reload

Эндпоинты названы в соответствии с назначением и распределены по сущностям с которыми взаимодействуют. Неявными могут быть 2 команды:
Delete Person - не удаляет человека, а меняет параметр is_active на False
Rezero Person (не придумал нормальное название, каюсь) - меняет параметр is_active на True

ВНИМАНИЕ ФИЧА сейчас все методы для сущности Person сгруппированы по тегу translator, и соответственно путь к методам будет начинаться с /translator

6 Сущности

Описаны в app/models

