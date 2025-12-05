import threading
import time
import requests
from queue import Queue
from datetime import datetime

LOG_FILE = "logs.txt"
URL = "http://127.0.0.1:8080/timestamp/{}"

log_queue = Queue()

def worker(thread_id: int):
    """Поток: каждые 1 секунд получает timestamp и дату, кладёт в очередь"""
    start_time = time.time()
    while time.time() - start_time < 20:
        ts = int(time.time())
        try:
            response = requests.get(URL.format(ts))
            if response.status_code == 200:
                log_queue.put((ts, response.text.strip()))
        except Exception as e:
            print(f"Thread {thread_id} error: {e}")
        time.sleep(1)

def logger():
    """Отдельный поток: пишет логи в файл в порядке timestamp"""
    logs = []
    while True:
        try:
            ts, date = log_queue.get(timeout=22)
            logs.append((ts, date))
        except:
            break

    logs.sort(key=lambda x: x[0])
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        for ts, date in logs:
            f.write(f"{ts} {date}\n")

if __name__ == "__main__":
    threads = []

    for i in range(10):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()
        time.sleep(1)

    for t in threads:
        t.join()

    logger()

    print("Логи записаны в", LOG_FILE)