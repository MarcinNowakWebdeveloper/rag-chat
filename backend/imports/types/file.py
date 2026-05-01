from langchain_community.document_loaders import TextLoader
from backend.core.vector_store import get_vector_db
from backend.core.config import config
from backend.imports.splitter import split_documents

import os

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
def import_file(path: str):
    print(f"📄 Loading: {path}")

    docs = load_file(path)
    chunks = split_documents(docs)

    print(f"✂️ Chunks created: {len(chunks)}")

    for chunk in chunks:
        chunk.metadata["source"] = os.path.basename(path)

    db.add_documents(chunks)

    print("✅ Added to vector DB")


# =========================
# BULK IMPORT
# =========================
def import_folder(folder_path: str):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            import_file(os.path.join(folder_path, filename))
