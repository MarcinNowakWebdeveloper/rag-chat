from backend.core.config import config
from backend.core.vector_store import VectorDbCollection
from backend.imports.splitter import split_documents
from backend.constants.vector_collection import VectorCollection
from langchain_community.document_loaders import TextLoader
from typing import Dict

import os
import asyncio


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
    collections: Dict[str, list] = {}
    for chunk in chunks:
        chunk.metadata["source"] = os.path.basename(path)
        collection_name = chunk.metadata.get(
            "collection", VectorCollection.DEFAULT.value
        )

        collections.setdefault(collection_name, []).append(chunk)

    VectorDbCollectionService = VectorDbCollection()
    for collection_name, collection in collections.items():

        db = VectorDbCollectionService.get_vector_db_by_collection(collection_name)
        for i in range(0, len(collection), config.RAG.batch_size):
            batch = collection[i : i + config.RAG.batch_size]

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
