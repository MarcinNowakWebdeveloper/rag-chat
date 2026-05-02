from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
from backend.core.config import config
from langchain_core.documents import Document
from urllib.parse import urlparse, urlunparse
import trafilatura
import aiohttp
import asyncio


class WebCrawler:

    def __init__(self, pages_queue):
        self.max_depth = config.WEB_CRAWLER.max_depth
        self.max_pages = config.WEB_CRAWLER.max_pages
        self.workers_count = config.WEB_CRAWLER.workers_count
        self.allowed_domain = (
            config.WEB_CRAWLER.domain if config.WEB_CRAWLER.domain != "" else None
        )

        self.task_queue: asyncio.Queue[tuple[str, int] | None] = asyncio.Queue()
        self.results_queue: asyncio.Queue = asyncio.Queue()
        self.pages_queue = pages_queue

        self.seen = set()
        self.visited = set()

        self.lock = asyncio.Lock()

    # -------------------------
    # URL helpers
    # -------------------------
    def normalize_url(self, url: str) -> str:
        parsed = urlparse(url)
        netloc = parsed.netloc.lower()
        path = parsed.path.rstrip("/") or "/"
        return urlunparse((parsed.scheme, netloc, path, "", "", ""))

    def is_valid_url(self, url: str) -> bool:
        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            return False

        if self.allowed_domain and self.allowed_domain not in parsed.netloc:
            return False

        return True

    def extract_links(self, html, base_url):
        soup = BeautifulSoup(html, "html.parser")
        links = []

        for a in soup.find_all("a", href=True):
            full_url = self.normalize_url(urljoin(base_url, a["href"]))
            if self.is_valid_url(full_url):
                links.append(full_url)

        return links

    # -------------------------
    # Fetch
    # -------------------------
    async def fetch(self, session, url):
        try:
            async with session.get(url, timeout=10) as resp:
                return await resp.text()
        except:
            return None

    # -------------------------
    # Worker
    # -------------------------
    async def worker(self, session):
        while True:
            item = await self.task_queue.get()

            if item is None:
                self.task_queue.task_done()
                break

            url, depth = item

            try:
                async with self.lock:
                    if url in self.visited or len(self.visited) >= self.max_pages:
                        continue
                    self.visited.add(url)

                html = await self.fetch(session, url)
                if not html:
                    continue

                text = await asyncio.to_thread(trafilatura.extract, html)

                if text and text.strip():
                    await self.pages_queue.put(
                        Document(
                            page_content=text,
                            metadata={
                                "source": url,
                                "depth": depth,
                                "length": len(text),
                            },
                        )
                    )

                links = await asyncio.to_thread(self.extract_links, html, url)

                async with self.lock:
                    if int(depth) < self.max_depth:
                        for link in links:
                            if (
                                link not in self.seen
                                and len(self.seen) < self.max_pages * 10
                            ):
                                self.seen.add(link)
                                await self.task_queue.put((link, depth + 1))

            finally:
                self.task_queue.task_done()

    # -------------------------
    # Crawl
    # -------------------------
    async def crawl(self, seed_urls):
        async with aiohttp.ClientSession() as session:

            for url in seed_urls:
                url = self.normalize_url(url)
                self.seen.add(url)
                await self.task_queue.put((url, 0))

            workers = [
                asyncio.create_task(self.worker(session))
                for _ in range(self.workers_count)
            ]

            await self.task_queue.join()

            for _ in workers:
                await self.task_queue.put(None)

            await asyncio.gather(*workers)

        results = []
        while not self.results_queue.empty():
            results.append(self.results_queue.get_nowait())

        return results
