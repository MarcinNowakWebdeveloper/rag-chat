from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.core.config import config


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNKS.size, chunk_overlap=config.CHUNKS.overlap
    )
    return splitter.split_documents(documents)
