# SQL-запросы для работы с базой данных
# Здесь храню все запросы чтобы не писать их в коде каждый раз
#РАБОТА С ПОЛЬЗОВАТЕЛЯМИ
# Найти пользователя по имени (это для логина)
GET_USER_BY_NAME = """
    SELECT id, user_name, password_hash, created_at
    FROM users
    WHERE user_name = %s
"""
# Создать нового пользователя при регистрации
CREATE_USER = """
    INSERT INTO users (user_name, password_hash)
    VALUES (%s, %s)
    RETURNING id, user_name, created_at
"""
#ЖАНРЫ ФИЛЬМОВ
#Получить все жанры для выпадающего списка
GET_ALL_GENRES = """
    SELECT id, name 
    FROM genres 
    ORDER BY name
"""
#ФИЛЬМЫ
#Все фильмы с названиями жанров
GET_ALL_MOVIES = """
    SELECT 
        m.id, 
        m.title, 
        m.year,
        g.name as genre_name,
        m.rating, 
        m.review, 
        m.watch_date, 
        m.created_at
    FROM movies m
    LEFT JOIN genres g ON m.genre_id = g.id
    ORDER BY m.created_at DESC
"""
#Фильмы конкретного пользователя
GET_MOVIES_BY_USER = """
    SELECT 
        m.id, 
        m.title, 
        m.year,
        g.name as genre_name,
        m.rating, 
        m.review, 
        m.watch_date, 
        m.created_at
    FROM movies m
    LEFT JOIN genres g ON m.genre_id = g.id
    WHERE m.user_id = %s
    ORDER BY m.created_at DESC
"""
#Один фильм по ID
GET_MOVIE_BY_ID = """
    SELECT 
        m.id, 
        m.title, 
        m.year,
        g.name as genre_name,
        m.rating, 
        m.review, 
        m.watch_date
    FROM movies m
    LEFT JOIN genres g ON m.genre_id = g.id
    WHERE m.id = %s
"""
#Добавить новый фильм
CREATE_MOVIE = """
    INSERT INTO movies (title, year, genre_id, user_id, rating, review, watch_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    RETURNING id, created_at
"""
#Обновить информацию о фильме
UPDATE_MOVIE = """
    UPDATE movies
    SET title = %s, 
        year = %s, 
        genre_id = %s,
        rating = %s, 
        review = %s, 
        watch_date = %s
    WHERE id = %s AND user_id = %s
    RETURNING id
"""

#Удалить фильм
DELETE_MOVIE = """
    DELETE FROM movies
    WHERE id = %s AND user_id = %s
    RETURNING id
"""
#СТАТИСТИКА ДЛЯ DASHBOARD
# Общая статистика
GET_MOVIES_STATS = """
    SELECT 
        COUNT(*) as total_movies,
        AVG(rating) as avg_rating,
        COUNT(DISTINCT genre_id) as genres_count
    FROM movies
"""
# Сколько фильмов в каждом жанре
GET_MOVIES_BY_GENRE = """
    SELECT 
        g.name, 
        COUNT(m.id) as movie_count
    FROM genres g
    LEFT JOIN movies m ON g.id = m.genre_id
    GROUP BY g.name
    ORDER BY movie_count DESC
"""
# Фильмы по годам (для графика)
GET_MOVIES_BY_YEAR = """
    SELECT 
        year, 
        COUNT(*) as count
    FROM movies
    WHERE year IS NOT NULL
    GROUP BY year
    ORDER BY year DESC
    LIMIT 10
"""