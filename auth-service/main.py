# Auth-сервис: Вспомогательный сервис (FastAPI)
# Порт: 8000
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
import jwt
import hashlib
import json
import bcrypt
from datetime import datetime, timedelta
from pathlib import Path

app = FastAPI(title="Auth Service - КиноДневник")

# Секретный ключ для JWT
SECRET_KEY = "student-secret-key-change-in-prod"
ALGORITHM = "HS256"

#МОДЕЛИ ДЛЯ ВАЛИДАЦИИ

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenRequest(BaseModel):
    token: str

#JWT ФУНКЦИИ
def create_token(user_id: int, username: str):
    """Генерируем JWT-токен (срок действия 24 часа)"""
    expire = datetime.utcnow() + timedelta(hours=24)
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token: str):
    """Проверяем JWT-токен"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Токен истёк
    except jwt.InvalidTokenError:
        return None  # Токен невалидный

#ОБЯЗАТЕЛЬНЫЕ ЭНДПОИНТЫ
@app.get('/api/hash/{text}')
async def hash_endpoint(text: str):
    """
    Эндпоинт из методички: принимает строку, возвращает hash
    """
    #Используем SHA256 для хэширования
    hash_result = hashlib.sha256(text.encode('utf-8')).hexdigest()

    return {
        "request": text,
        "result": hash_result
    }

@app.get('/api/about')
async def api_about():
    """
    эндпоинт как в методичке: возвращает JSON из about.json
    Fallback: если файл не найден, возвращаем данные напрямую
    """
    try:
        # Пытаемся прочитать файл about.json
        about_file = Path(__file__).parent / 'about.json'
        with open(about_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback-ответ
        return {
            "project": "КиноДневник",
            "author": "Седухин Кирилл",
            "group": "204б",
            "description": "Персональное веб-приложение для учета просмотренных фильмов",
            "fallback": True
        }

#АВТОРИЗАЦИЯ

@app.post('/api/login')
async def login(data: LoginRequest):
    """
    Вход пользователя — возвращает JWT-токен
    если это был бы ряльный проект то — проверка пароля через БД
    """
    # Упрощённая проверка (для тестов
    # В продакшене нужно делать запрос к базе данных
    if data.username == 'sedukhin' and data.password == 'test123':
        token = create_token(user_id=1, username=data.username)
        return {
            "token": token,
            "username": data.username,
            "expires_in": 86400  # 24 часа в секундах
        }

    # Если неверные данные
    raise HTTPException(status_code=401, detail="Неверный логин или пароль")


@app.post('/api/verify')
async def verify_token_endpoint(data: TokenRequest):
    """
    Проверка токена для других сервисов (Core-сервис обращается прям сюда)
    """
    payload = verify_token(data.token)

    if payload:
        return {
            "valid": True,
            "user_id": payload['user_id'],
            "username": payload['username']
        }

    return {"valid": False}


@app.get('/api/refresh/{username}')
async def refresh_token(username: str, authorization: str = Header(None)):
    """
    Обновление токена (защищённый роут)
    Требование из методички: кнопка обновления токена в профиле
    """
    #Проверяем что есть токен в заголовке
    if not authorization:
        raise HTTPException(status_code=401, detail="Token required")

    #Убираем префикс "Bearer " если есть
    token = authorization.replace("Bearer ", "")
    payload = verify_token(token)

    #Проверяем что токен валидный и username совпадает
    if not payload or payload.get('username') != username:
        raise HTTPException(status_code=403, detail="Invalid token")

    #Генерируем новый токен
    new_token = create_token(payload['user_id'], username)

    return {
        "token": new_token,
        "message": "Token refreshed successfully"
    }


#HEALTH CHECK
@app.get('/health')
async def health():
    """Проверка работоспособности сервиса"""
    return {
        "status": "ok",
        "service": "auth-service",
        "timestamp": datetime.utcnow().isoformat()
    }


#ЗАПУСК
# Запуск: uvicorn main:app --reload --port 8000
# В терминале: cd auth-service && uvicorn main:app --reload --port 8000
if __name__ == '__main__':
    import uvicorn

    print("Запускаю Auth-сервис на порту 8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)