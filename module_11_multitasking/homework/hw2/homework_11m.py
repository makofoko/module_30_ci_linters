import requests
import sqlite3
import threading
import time
from typing import List, Dict

DB_NAME = "starwars.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                height TEXT,
                gender TEXT
            )
        """)
        conn.commit()

def save_character(character: Dict[str, str]):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO characters (name, height, gender)
            VALUES (?, ?, ?)
        """, (character["name"], character["height"], character["gender"]))
        conn.commit()

def fetch_character(i: int) -> Dict[str, str]:
    url = f"https://swapi.dev/api/people/{i}/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "name": data.get("name"),
            "height": data.get("height"),
            "gender": data.get("gender")
        }
    return {}

def sequential_requests():
    start = time.time()
    for i in range(1, 21):
        character = fetch_character(i)
        if character:
            save_character(character)
    end = time.time()
    print("Sequential time:", round(end - start, 2), "секунд")

def threaded_requests():
    start = time.time()
    threads: List[threading.Thread] = []

    def worker(i: int):
        character = fetch_character(i)
        if character:
            save_character(character)

    for i in range(1, 21):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end = time.time()
    print("Threaded time:", round(end - start, 2), "секунд")

if __name__ == "__main__":
    init_db()
    sequential_requests()
    threaded_requests()