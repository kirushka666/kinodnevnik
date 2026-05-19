# Core-сервис: Основная бизнес-логика (Flask)
from flask import Flask, render_template, request, jsonify, redirect, session, flash
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'movie_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASS', 'postgres'),
    'port': os.getenv('DB_PORT', '5432')
}

@app.route('/')
def index():
    return "<h1>КиноДневник работает!</h1><p>Core-сервис запущен</p>"

@app.route('/test')
def test():
    return jsonify({"status": "ok", "service": "core"})
@app.route('/dashboard')
def dashboard():
    try:
            conn = psycopg2.connect(host='localhost', database='movie_db', user='postgres', password='postgres', port='5432')
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*), AVG(rating), COUNT(DISTINCT genre_id) FROM movies")
            stats = cur.fetchone()
            cur.execute("SELECT name, COUNT(*) FROM genres g LEFT JOIN movies m ON g.id = m.genre_id GROUP BY name")
            genres = cur.fetchall()
            cur.close()
            conn.close()
            return render_template('dashboard.html', stats={'total_movies': stats[0] or 0, 'avg_rating': stats[1] or 0, 'genres_count': stats[2] or 0}, genre_labels=[g[0] for g in genres], genre_data=[g[1] for g in genres])
    except Exception as e:
            return f"Error: {str(e)}", 500
if __name__ == '__main__':
    print("Запускаю Core-сервис на порту 5000...")
    app.run(debug=True, port=5000)