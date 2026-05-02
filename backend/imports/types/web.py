from backend.core.vector_store import get_vector_db, get_embeddings
from backend.core.config import config
from backend.imports.splitter import split_documents
from backend.imports.types.web_service.crawler import WebCrawler
from asyncio import Queue
from langchain_core.documents import Document

import asyncio
import time

db = get_vector_db(with_embeddings=False)


async def import_web_list(seed_urls: list[str]):
    print("🌐 Starting web imports...")

    pages_queue: Queue[tuple[str, int]] = asyncio.Queue()
    chunks_queue: Queue[Document | None] = asyncio.Queue()

    monitor_task = asyncio.create_task(monitor(pages_queue, chunks_queue))

    crawler = WebCrawler(pages_queue)
    crawler_task = asyncio.create_task(crawler.crawl(seed_urls))

    chunk_task = asyncio.create_task(chunk_worker(pages_queue, chunks_queue))

    db_workers = [asyncio.create_task(db_worker(chunks_queue)) for _ in range(1)]

    await crawler_task
    await pages_queue.join()

    for _ in range(1):
        await chunks_queue.put(None)

    await chunks_queue.join()

    chunk_task.cancel()
    monitor_task.cancel()

    print(f"\r✅ Web RAG complete")


async def chunk_worker(pages_queue, chunks_queue):
    while True:
        doc = await pages_queue.get()

        chunks = split_documents([doc])

        for c in chunks:
            await chunks_queue.put(c)

        pages_queue.task_done()


async def db_worker(chunks_queue):
    batch = []

    while True:
        chunk = await chunks_queue.get()

        try:
            if chunk is None:
                break

            batch.append(chunk)

            if len(batch) >= config.RAG.batch_size:
                await add_embeddings(batch)
                batch = []

        finally:
            chunks_queue.task_done()

    if batch:
        await add_embeddings(batch)


async def add_embeddings(batch):
    texts = [c.page_content for c in batch]
    metadatas = [c.metadata for c in batch]
    ids = [c.metadata["source"] + str(i) for i, c in enumerate(batch)]

    embeddings = await asyncio.to_thread(get_embeddings().embed_documents, texts)

    await asyncio.to_thread(
        db._collection.add,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas,
        ids=ids,
    )


async def monitor(pages_queue, chunks_queue):
    while True:
        print(
            f"\r📊 pages_queue={pages_queue.qsize()} chunks_queue={chunks_queue.qsize()}    ",
            end="",
            flush=True,
        )
        await asyncio.sleep(2)
