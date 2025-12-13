import requests
import time
import logging
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.DEBUG)

class APIClient:
    def __init__(self, base_url, use_session=False):
        self.base_url = base_url
        self.session = requests.Session() if use_session else requests

    def get_book(self, book_id):
        return self.session.get(f"{self.base_url}/api/books/{book_id}")

    def create_author(self, data):
        return self.session.post(f"{self.base_url}/api/authors/", json=data)

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
    client = APIClient(base_url, use_session=True)

    # тест: 10 запросов без потоков
    t1 = benchmark(client, 10, use_threads=False)
    print("10 запросов без потоков:", t1, "секунд")

    # тест: 10 запросов с потоками
    t2 = benchmark(client, 10, use_threads=True)
    print("10 запросов с потоками:", t2, "секунд")

    # можно добавить 100 и 1000 запросов
    for n in [10, 100, 1000]:
        t_no_threads = benchmark(client, n, use_threads=False)
        t_threads = benchmark(client, n, use_threads=True)
        print(f"{n} запросов: без потоков={t_no_threads:.2f}s, с потоками={t_threads:.2f}s")