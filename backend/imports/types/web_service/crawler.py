from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
from backend.core.config import config
from langchain_core.documents import Document
import trafilatura
import requests


class WebCrawler:
    def __init__(self):
        self.max_depth = config.WEB_CRAWLER.max_depth
        self.max_pages = config.WEB_CRAWLER.max_pages
        self.allowed_domain = (
            config.WEB_CRAWLER.domain if config.WEB_CRAWLER.domain != "" else None
        )

        self.visited = set()
        self.queue = deque()

    def is_valid_url(self, url):
        parsed = urlparse(url)

        if self.allowed_domain and self.allowed_domain not in parsed.netloc:
            return False

        return parsed.scheme in ("http", "https")

    def extract_links(self, html, base_url):
        soup = BeautifulSoup(html, "html.parser")
        links = []

        for a in soup.find_all("a", href=True):
            full_url = urljoin(base_url, a["href"])
            if self.is_valid_url(full_url):
                links.append(full_url)

        return links

    def extract_text(self, html):
        # 🔥 best extraction method
        text = trafilatura.extract(html)
        return text or ""

    def crawl(self, seed_urls: list[str]):
        results = []

        for url in seed_urls:
            self.queue.append((url, 0))

        while self.queue and len(self.visited) < self.max_pages:
            url, depth = self.queue.popleft()

            if url in self.visited:
                continue

            if depth > self.max_depth:
                continue

            try:
                response = requests.get(url, timeout=10)
                html = response.text

                text = self.extract_text(html)

                if text.strip():
                    results.append(
                        Document(
                            page_content=text,
                            metadata={
                                "source": url,
                                "type": "web",
                                "length": len(text),
                            },
                        )
                    )

                self.visited.add(url)

                if depth < self.max_depth:
                    links = self.extract_links(html, url)

                    for link in links:
                        if link not in self.visited:
                            self.queue.append((link, depth + 1))

            except Exception as e:
                print(f"❌ Error {url}: {e}")

        return results
