from backend.constants.vector_collection import VectorCollection
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from backend.core.config import config
from typing import Type, Dict


class VectorDbCollection:
    collection: Dict[str, Dict[bool, Chroma]] = {}

    def get_vector_db_by_collection(
        self, collection_name: str, with_embeddings: bool = True
    ):
        if collection_name in self.collection:
            if with_embeddings in self.collection[collection_name]:
                return self.collection[collection_name][with_embeddings]

        if collection_name not in self.collection:
            self.collection[collection_name] = {}

        self.collection[collection_name][with_embeddings] = get_vector_db(
            collection_name, with_embeddings
        )
        return self.collection[collection_name][with_embeddings]


# =========================
# EMBEDDINGS FACTORY
# =========================
def get_embeddings():
    return OllamaEmbeddings(model=config.EMBEDDING_MODEL)


# =========================
# VECTOR DB FACTORY
# =========================
def get_vector_db(collection_name: str, with_embeddings: bool = True):
    """
    Factory for vector store abstraction.
    """

    embeddings = get_embeddings() if with_embeddings else None

    if config.VECTOR_DB == "chroma":
        return Chroma(
            persist_directory=config.VECTOR_DB_PATH,
            embedding_function=embeddings,
            collection_name=collection_name,
        )

    raise ValueError(f"Unsupported VECTOR_DB: {config.VECTOR_DB}")


def delete_collection():
    if config.VECTOR_DB == "chroma":

        collections = list(VectorCollection)
        for collection in collections:
            db = get_vector_db(collection)
            data = db.get()
            ids = data["ids"]

            if ids:
                db._collection.delete(ids=ids)
