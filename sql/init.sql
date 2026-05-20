-- Создание таблиц для проекта КиноДневник
-- PostgreSQL
-- Сброс старых таблиц (если мы перезапускаем скрипт)
DROP TABLE IF EXISTS movies CASCADE;
DROP TABLE IF EXISTS genres CASCADE;
DROP TABLE IF EXISTS users CASCADE;
-- Пользователи
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
-- Жанры фильмов
CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);
-- Фильмы
CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    year INTEGER,
    genre_id INTEGER REFERENCES genres(id),
    user_id INTEGER REFERENCES users(id),
    rating INTEGER CHECK (rating BETWEEN 1 AND 10),
    review TEXT,
    watch_date DATE,
    created_at TIMESTAMP DEFAULT NOW()
);
-- Индексы для поиска
CREATE INDEX idx_movies_title ON movies(title);
CREATE INDEX idx_movies_user_id ON movies(user_id);
CREATE INDEX idx_movies_genre_id ON movies(genre_id);