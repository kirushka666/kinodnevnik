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

if __name__ == '__main__':
    print("Запускаю Core-сервис на порту 5000...")
    app.run(debug=True, port=5000)