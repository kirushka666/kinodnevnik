from flask import Flask, jsonify, render_template
import psycopg2

app = Flask(__name__)
# Настройки подключения к PostgreSQL
DB_CONFIG = {
    'host': 'localhost',
    'database': 'movie_db',
    'user': 'postgres',
    'password': 'postgres',
    'port': '5432'
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
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        #Общая статистика
        cur.execute("SELECT COUNT(*), AVG(rating), COUNT(DISTINCT genre_id) FROM movies")
        stats = cur.fetchone()

        #Данные для графика по жанрам
        cur.execute("SELECT name, COUNT(*) FROM genres g LEFT JOIN movies m ON g.id = m.genre_id GROUP BY name")
        genres = cur.fetchall()

        cur.close()
        conn.close()

        return render_template('dashboard.html',
                               stats={
                                   'total_movies': stats[0] or 0,
                                   'avg_rating': stats[1] or 0,
                                   'genres_count': stats[2] or 0
                               },
                               genre_labels=[g[0] for g in genres],
                               genre_data=[g[1] for g in genres]
                               )
    except Exception as e:
        return f"Ошибка: {str(e)}", 500

if __name__ == '__main__':
    print("Запускаю Core-сервис на порту 5000...")
    app.run(debug=True, port=5000)