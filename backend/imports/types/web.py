from backend.core.vector_store import get_vector_db
from backend.imports.splitter import split_documents
from backend.imports.types.web_service.crawler import WebCrawler

db = get_vector_db()


def import_web_list(seed_urls: list[str]):
    print("🌐 Starting web imports...")

    crawler = WebCrawler()

    docs = crawler.crawl(seed_urls)

    print(f"📄 Pages fetched: {len(docs)}")

    chunks = split_documents(docs)

    print(f"✂️ Chunks created: {len(chunks)}")

    if not chunks:
        return

    db.add_documents(chunks)

    print("✅ Web RAG complete")
