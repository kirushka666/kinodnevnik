from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import hashlib

app = Flask(__name__)
app.secret_key = 'student_secret_key_123'  # нужно для работы сессий

#настройки БД
DB_CONFIG = {
    'host': 'localhost',
    'database': 'movie_db',
    'user': 'postgres',
    'password': 'postgres',
    'port': '5432'
}
#главная страница
@app.route('/')
def index():
    return render_template('index.html')

#регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']

        #проверяем совпадение паролей
        if password != password2:
            return render_template('register.html', error='Пароли не совпадают!')

        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()

            #смотрим нет ли уже такого юзера
            cur.execute("SELECT id FROM users WHERE user_name = %s", (username,))
            if cur.fetchone():
                return render_template('register.html', error='Такой пользователь уже есть')

            #хэшируем пароль и сохраняем
            hashed = hashlib.sha256(password.encode()).hexdigest()
            cur.execute("INSERT INTO users (user_name, password_hash) VALUES (%s, %s)", (username, hashed))
            conn.commit()
            cur.close()
            conn.close()

            #после регистрации кидаем на вход
            return redirect(url_for('login'))
        except Exception as e:
            return render_template('register.html', error='Ошибка: ' + str(e))

    return render_template('register.html')

#вход в аккаунт
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed = hashlib.sha256(password.encode()).hexdigest()

        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            cur.execute("SELECT id, user_name FROM users WHERE user_name = %s AND password_hash = %s", (username, hashed))
            user = cur.fetchone()
            cur.close()
            conn.close()

            if user:
                # записываем в сессию чтобы помнить кто вошёл
                session['user_id'] = user[0]
                session['username'] = user[1]
                return redirect(url_for('account'))
            else:
                return render_template('login.html', error='Неверный логин или пароль')
        except Exception as e:
            return render_template('login.html', error='Ошибка БД: ' + str(e))

    return render_template('login.html')

#личный кабинет
@app.route('/account')
def account():
    # если не залогинен - не пускаем
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        # считаем сколько фильмов добавил этот юзер
        cur.execute("SELECT COUNT(*) FROM movies WHERE user_id = %s", (session['user_id'],))
        movies_count = cur.fetchone()[0]
        cur.close()
        conn.close()

        return render_template('account.html', username=session['username'], movies_count=movies_count)
    except Exception as e:
        return "Ошибка загрузки профиля"

#выход из аккаунта
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*), AVG(rating), COUNT(DISTINCT genre_id) FROM movies")
        stats = cur.fetchone()
        cur.execute("SELECT name, COUNT(*) FROM genres g LEFT JOIN movies m ON g.id = m.genre_id GROUP BY name")
        genres = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('dashboard.html',
            stats={'total_movies': stats[0] or 0, 'avg_rating': stats[1] or 0, 'genres_count': stats[2] or 0},
            genre_labels=[g[0] for g in genres],
            genre_data=[g[1] for g in genres]
        )
    except Exception as e:
        return f"Ошибка: {str(e)}", 500

@app.route('/test')
def test():
    return {"status": "ok", "service": "core"}

# страница добавления фильма
@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    # если не залогинен - не пускаем
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # загружаем жанры для выпадающего списка
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM genres ORDER BY name")
    genres = cur.fetchall()
    cur.close()
    conn.close()

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        genre_id = request.form['genre_id']
        rating = request.form['rating']
        review = request.form['review']
        watch_date = request.form['watch_date']

        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            # вставляем фильм и привязываем к текущему юзеру
            cur.execute("""
                INSERT INTO movies (title, year, genre_id, user_id, rating, review, watch_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (title, year, genre_id, session['user_id'], rating, review, watch_date))
            conn.commit()
            cur.close()
            conn.close()
            # после сохранения кидаем обратно в кабинет
            return redirect(url_for('account'))
        except Exception as e:
            return render_template('add_movie.html', genres=genres, error='Ошибка при сохранении: ' + str(e))

    return render_template('add_movie.html', genres=genres)

if __name__ == '__main__':
    print("Запускаю Core-сервис на порту 5000...")
    app.run(debug=True, port=5000)