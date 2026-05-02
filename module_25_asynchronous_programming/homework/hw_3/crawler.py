# crawler.py
import aiohttp
import asyncio
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

class AsyncCrawler:
    def __init__(self, start_urls, max_depth=3, output_file="links.txt"):
        self.start_urls = start_urls
        self.max_depth = max_depth
        self.output_file = output_file
        self.visited = set()
        self.found_links = set()

    async def fetch(self, session, url):
        try:
            async with session.get(url, timeout=10) as resp:
                if resp.status == 200 and "text/html" in resp.headers.get("Content-Type", ""):
                    return await resp.text()
        except Exception as e:
            print(f"❌ Ошибка при загрузке {url}: {e}")
        return None

    def extract_links(self, html, base_url):
        soup = BeautifulSoup(html, "html.parser")
        links = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            full_url = urljoin(base_url, href)
            # фильтруем только внешние ссылки
            if urlparse(full_url).netloc != urlparse(base_url).netloc:
                links.add(full_url)
        return links

    async def crawl(self, url, depth, session):
        if depth > self.max_depth or url in self.visited:
            return
        self.visited.add(url)
        html = await self.fetch(session, url)
        if html:
            links = self.extract_links(html, url)
            self.found_links.update(links)
            tasks = [self.crawl(link, depth + 1, session) for link in links]
            await asyncio.gather(*tasks)

    async def run(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.crawl(url, 1, session) for url in self.start_urls]
            await asyncio.gather(*tasks)
        # сохраняем все найденные ссылки в файл
        with open(self.output_file, "w", encoding="utf-8") as f:
            for link in sorted(self.found_links):
                f.write(link + "\n")
        print(f"✅ Найдено {len(self.found_links)} внешних ссылок. Сохранено в {self.output_file}.")

if __name__ == "__main__":
    start = ["https://example.com"]  # можно указать несколько стартовых ссылок
    crawler = AsyncCrawler(start_urls=start, max_depth=3)
    asyncio.run(crawler.run())
