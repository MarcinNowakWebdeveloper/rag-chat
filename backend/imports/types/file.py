from backend.core.config import config
from backend.core.vector_store import get_vector_db
from backend.imports.splitter import split_documents
from langchain_community.document_loaders import TextLoader

import os
import asyncio

# =========================
# INIT
# =========================
db = get_vector_db()


# =========================
# LOAD FILE
# =========================
def load_file(path: str):
    loader = TextLoader(path, encoding="utf-8")
    return loader.load()


# =========================
# IMPORT
# =========================
async def import_file(path: str):
    print(f"📄 Loading: {path}")

    docs = await asyncio.to_thread(load_file, path)
    chunks = await asyncio.to_thread(split_documents, docs)

    for chunk in chunks:
        chunk.metadata["source"] = os.path.basename(path)

    for i in range(0, len(chunks), config.RAG.batch_size):
        batch = chunks[i : i + config.RAG.batch_size]

        await asyncio.to_thread(
            db.add_documents,
            batch,
        )

    return len(chunks)


# =========================
# BULK IMPORT
# =========================
async def import_folder(folder_path: str):
    files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.endswith(".txt")
    ]

    tasks = [import_file(f) for f in files]

    results = await asyncio.gather(*tasks)

    total_chunks = sum(results)
    print(f"🚀 TOTAL chunks imported from files: {total_chunks}")
