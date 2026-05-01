from langchain_ollama import OllamaLLM
from backend.core.config import config


def get_llm():
    return OllamaLLM(model=config.OLLAMA_MODEL)
