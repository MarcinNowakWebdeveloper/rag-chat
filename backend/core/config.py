from dotenv import load_dotenv
from dataclasses import dataclass
import os
import json

load_dotenv()


@dataclass
class RAGConfig:
    k: int
    similarity_threshold: float
    batch_size: int


@dataclass
class ChunksConfig:
    size: int
    overlap: int


@dataclass
class WebCrawlerConfig:
    max_depth: int
    max_pages: int
    domain: str
    source: list[str]
    workers_count: int


@dataclass
class Config:
    # LLM
    OLLAMA_MODEL: str

    # Embeddings
    EMBEDDING_MODEL: str

    # DB
    VECTOR_DB: str
    VECTOR_DB_PATH: str

    # RAG
    RAG: RAGConfig

    # Classifier
    MIN_ALLOWED_TOPIC_SCORE: float

    # Chunks
    CHUNKS: ChunksConfig

    # Import
    DATA_PATH: str
    WEB_CRAWLER: WebCrawlerConfig


def load_config() -> Config:
    return Config(
        OLLAMA_MODEL=os.getenv("OLLAMA_MODEL", "llama3:8b"),
        EMBEDDING_MODEL=os.getenv("EMBEDDING_MODEL", "nomic-embed-text"),
        VECTOR_DB=os.getenv("VECTOR_DB", "chroma"),
        VECTOR_DB_PATH=os.getenv("VECTOR_DB_PATH", "./chroma_db"),
        RAG=RAGConfig(
            k=int(os.getenv("RAG_K", 3)),
            similarity_threshold=float(os.getenv("RAG_SIMILARITY_THRESHOLD", 0.4)),
            batch_size=int(os.getenv("RAG_BATCH_SIZE", 150)),
        ),
        CHUNKS=ChunksConfig(
            size=int(os.getenv("CHUNK_SIZE", 800)),
            overlap=int(os.getenv("CHUNK_OVERLAP", 150)),
        ),
        MIN_ALLOWED_TOPIC_SCORE=float(os.getenv("MIN_ALLOWED_TOPIC_SCORE", 0.6)),
        DATA_PATH=os.getenv("DATA_PATH", "./data"),
        WEB_CRAWLER=WebCrawlerConfig(
            max_depth=int(os.getenv("WEB_CRAWLER_MAX_DEPTH", 3)),
            max_pages=int(os.getenv("WEB_CRAWLER_MAX_PAGES", 60)),
            domain=os.getenv("WEB_CRAWLER_DOMAIN", ""),
            source=json.loads(os.getenv("WEB_CRAWLER_SOURCE", "[]")),
            workers_count=int(os.getenv("WEB_CRAWLER_WORKERS_COUNT", 10)),
        ),
    )


config = load_config()
