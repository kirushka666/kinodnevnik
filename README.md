# 🎬 КиноДневник

Учебный проект по курсу "Базы данных"  
МТИ, группа 204б, Седухин Кирилл  
Преподаватель: А. Красильников

## Описание

Приложение для учета просмотренных фильмов. Можно добавлять фильмы, 
ставить оценки и оставлять отзывы.

## Технологии

- Backend: Flask + FastAPI
- Database: PostgreSQL 18
- Frontend: HTML + Bootstrap 5
- Auth: JWT

## Как запустить

```bash
# Установка зависимостей
pip install -r core-service/requirements.txt
pip install -r auth-service/requirements.txt

# Запуск Core-сервиса
python core-service/app.py

# Запуск Auth-сервиса
uvicorn auth-service/main:app --reload --port 8000