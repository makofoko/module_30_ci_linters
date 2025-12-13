import requests
import time
import logging
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO)

class APIClient:
    def __init__(self, base_url, use_session=False):
        self.base_url = base_url
        self.session = requests.Session() if use_session else requests

    def get_book(self, book_id):
        return self.session.get(f"{self.base_url}/api/books/{book_id}")

def benchmark(client, n_requests, use_threads=False):
    def task():
        client.get_book(1)

    start = time.time()
    if use_threads:
        with ThreadPoolExecutor() as pool:
            pool.map(lambda _: task(), range(n_requests))
    else:
        for _ in range(n_requests):
            task()
    return time.time() - start

if __name__ == "__main__":
    base_url = "http://127.0.0.1:5000"

    # все комбинации: -S/+S и -T/+T
    results = {}
    for use_session in [False, True]:
        for use_threads in [False, True]:
            combo = f"S={'+' if use_session else '-'} T={'+' if use_threads else '-'}"
            results[combo] = {}
            client = APIClient(base_url, use_session=use_session)
            for n in [10, 100, 1000]:
                t = benchmark(client, n, use_threads=use_threads)
                results[combo][n] = round(t, 2)

    # выводим таблицу для REPORT.md
    print("\nREPORT.md таблица:\n")
    print("+----------------+----------------+----------------+----------------+----------------+")
    print("| Число запросов | -S -T          | -S +T          | +S -T          | +S +T          |")
    print("+----------------+----------------+----------------+----------------+----------------+")
    for n in [10, 100, 1000]:
        row = f"| {n:<14} | {results['S=- T=-'][n]:<14} | {results['S=- T=+'][n]:<14} | {results['S=+ T=-'][n]:<14} | {results['S=+ T=+'][n]:<14} |"
        print(row)
    print("+----------------+----------------+----------------+----------------+----------------+")