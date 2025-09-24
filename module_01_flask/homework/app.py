import os
import random
import re
from datetime import datetime, timedelta
from flask import Flask

app = Flask(__name__)

cars = ["Chevrolet", "Renault", "Ford", "Lada"]

cats = ["корниш-рекс", "русская голубая", "шотландская вислоухая",
        "мейн-кун", "манчкин"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, "war_and_peace.txt")

def load_words():
    with open(BOOK_FILE, encoding="utf-8") as book:
        text = book.read().lower()

        words = re.findall(r"[а-яА-Яa-zA-Z]+", text)
    return words

words_list = load_words()

counter_visits = 0

@app.route("/")
def hello_world():
    return "Привет, мир!"

@app.route("/cars")
def get_cars():
    return ", ".join(cars)

@app.route("/cats")
def get_cats():
    return random.choice(cats)

@app.route("/get_time/now")
def get_time_now():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Точное время: {current_time}"

@app.route("/get_time/future")
def get_time_future():
    current_time_after_hour = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    return f"Точное время через час будет {current_time_after_hour}"

@app.route("/get_random_word")
def get_random_word():
    word = random.choice(words_list)
    return word

@app.route("/counter")
def counter():
    global counter_visits
    counter_visits += 1
    return f"Страница открывалась {counter_visits} раз(а)."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)
