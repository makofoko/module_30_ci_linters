import requests
import sqlite3
import time
from typing import Dict, List
from multiprocessing import Pool, cpu_count
from concurrent.futures import ThreadPoolExecutor

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
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "name": data.get("name"),
                "height": data.get("height"),
                "gender": data.get("gender")
            }
    except Exception as e:
        print(f"Error fetching {i}: {e}")
    return {}

def pool_requests():
    start = time.time()
    with Pool(processes=cpu_count()) as pool:
        results: List[Dict[str, str]] = pool.map(fetch_character, range(1, 21))
    for character in results:
        if character:
            save_character(character)
    end = time.time()
    print("Multiprocessing Pool time:", round(end - start, 2), "секунд")

def threadpool_requests():
    start = time.time()
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(fetch_character, range(1, 21)))
    for character in results:
        if character:
            save_character(character)
    end = time.time()
    print("ThreadPool time:", round(end - start, 2), "секунд")

if __name__ == "__main__":
    init_db()
    pool_requests()
    threadpool_requests()