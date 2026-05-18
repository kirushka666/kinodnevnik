DROP TABLE IF EXISTS movies CASCADE;
DROP TABLE IF EXISTS genres CASCADE;
DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
id SERIAL PRIMARY KEY,
user_name VARCHAR(100) UNIQUE NOT NULL,
password_hash VARCHAR(255) NOT NULL,
created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE genres (
id SERIAL PRIMARY KEY,
name VARCHAR(50) UNIQUE NOT NULL
);
CREATE TABLE movies (
id SERIAL PRIMARY KEY,
title VARCHAR(150) NOT NULL,
year INTEGER,
genre_id INTEGER,
user_id INTEGER,
rating INTEGER,
review TEXT,
watch_date DATE,
created_at TIMESTAMP DEFAULT NOW(),
FOREIGN KEY (genre_id) REFERENCES genres(id),
FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE INDEX idx_movies_title ON movies(title);
CREATE INDEX idx_movies_user_id ON movies(user_id);
CREATE INDEX idx_movies_genre_id ON movies(genre_id);