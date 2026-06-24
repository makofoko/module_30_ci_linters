# cats_downloader.py
import aiohttp
import asyncio

async def save_file(filename: str, content: bytes):
    """Асинхронная запись файла через стандартный open."""
    await asyncio.to_thread(
        lambda: open(filename, "wb").write(content)
    )

async def download_cat(url: str, filename: str):
    """Скачивание картинки кота и сохранение в файл."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                content = await resp.read()
                await save_file(filename, content)
                print(f"✅ Скачан {filename}")
            else:
                print(f"❌ Ошибка {resp.status} при загрузке {url}")

async def main():
    urls = [
        ("https://placekitten.com/200/300", "cat1.jpg"),
        ("https://placekitten.com/400/500", "cat2.jpg"),
        ("https://placekitten.com/600/400", "cat3.jpg"),
    ]
    tasks = [download_cat(url, fname) for url, fname in urls]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
