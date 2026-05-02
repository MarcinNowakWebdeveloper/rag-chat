from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from backend.core.config import config

# =========================
# EMBEDDINGS FACTORY
# =========================


def get_embeddings():
    return OllamaEmbeddings(model=config.EMBEDDING_MODEL)


# =========================
# VECTOR DB FACTORY
# =========================


def get_vector_db(with_embeddings: bool = True):
    """
    Factory for vector store abstraction.
    """

    embeddings = get_embeddings() if with_embeddings else None

    if config.VECTOR_DB == "chroma":
        return Chroma(
            persist_directory=config.VECTOR_DB_PATH, embedding_function=embeddings
        )

    raise ValueError(f"Unsupported VECTOR_DB: {config.VECTOR_DB}")


def delete_collection():
    db = get_vector_db()
    if config.VECTOR_DB == "chroma":
        data = db.get()
        ids = data["ids"]

        if ids:
            db._collection.delete(ids=ids)
