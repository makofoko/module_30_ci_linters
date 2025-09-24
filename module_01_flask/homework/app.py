from datetime import datetime, timedelta
from flask import Flask
import random
import os
import re

app = Flask(__name__)

CARS = ["Chevrolet", "Renault", "Ford", "Lada"]

CATS = [
    "корниш-рекс",
    "русская голубая",
    "шотландская вислоухая",
    "мейн-кун",
    "манчкин"
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')

def load_words():
    with open(BOOK_FILE, encoding='utf-8') as book:
        text = book.read()
        words = re.findall(r'\b[А-Яа-яЁёA-Za-z-]+\b', text)
        return words

WORDS = load_words()

@app.route('/hello_world')
def hello_world():
    return "<h1>Привет, мир!</h1>"

@app.route("/cars")
def cars():
    return ", ".join(CARS)

@app.route("/cats")
def cats():
    breed = random.choice(CATS)
    return f"<h1>{breed}</h1>"

@app.route("/time")
def current_time_page():
    current_time = datetime.now().strftime("%H:%M:%S")
    return f"<h1>Точное время: {current_time}</h1>"

@app.route("/time_future_hour")
def time_future_hour():
    now = datetime.now()
    time_after_hour = now + timedelta(hours=1)
    current_time_after_hour = time_after_hour.strftime("%H:%M:%S")
    return f"<h1>Точное время через час будет {current_time_after_hour}</h1>"

@app.route("/get_random_word")
def get_random_word():
    word = random.choice(WORDS)
    return f"<h1>{word}</h1>"

@app.route("/counter")
def counter():
    counter.visits += 1
    return f"<h1>Страница открывалась {counter.visits} раз(а)</h1>"

counter.visits = 0


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5555)
