# cats_benchmark.py
import aiohttp
import asyncio
import requests
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

URLS = [f"https://placekitten.com/{200+i}/{300+i}" for i in range(100)]

# ---------------- Асинхронная реализация ----------------
async def save_file_async(filename: str, content: bytes):
    await asyncio.to_thread(lambda: open(filename, "wb").write(content))

async def download_cat_async(url: str, filename: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = await resp.read()
            await save_file_async(filename, content)

async def run_async(n: int):
    tasks = [download_cat_async(URLS[i], f"async_cat_{i}.jpg") for i in range(n)]
    await asyncio.gather(*tasks)

# ---------------- Реализация на тредах ----------------
def download_cat_thread(url: str, filename: str):
    resp = requests.get(url)
    with open(filename, "wb") as f:
        f.write(resp.content)

def run_threads(n: int):
    with ThreadPoolExecutor() as executor:
        executor.map(lambda i: download_cat_thread(URLS[i], f"thread_cat_{i}.jpg"), range(n))

# ---------------- Реализация на процессах ----------------
def download_cat_process(i: int):
    resp = requests.get(URLS[i])
    with open(f"process_cat_{i}.jpg", "wb") as f:
        f.write(resp.content)

def run_processes(n: int):
    with ProcessPoolExecutor() as executor:
        executor.map(download_cat_process, range(n))

# ---------------- Бенчмарк ----------------
def benchmark():
    results = []
    for n in [10, 50, 100]:
        # Асинхронность
        start = time.time()
        asyncio.run(run_async(n))
        async_time = time.time() - start

        # Треды
        start = time.time()
        run_threads(n)
        thread_time = time.time() - start

        # Процессы
        start = time.time()
        run_processes(n)
        process_time = time.time() - start

        results.append((n, async_time, thread_time, process_time))

    print("\n## Результаты бенчмарка\n")
    print("| Кол-во картинок | Асинхронность | Треды | Процессы |")
    print("|-----------------|---------------|-------|----------|")
    for n, a, t, p in results:
        print(f"| {n} | {a:.2f} сек | {t:.2f} сек | {p:.2f} сек |")

if __name__ == "__main__":
    benchmark()
