from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from backend.core.config import config
from backend.core.llm import get_classifier
from backend.imports.splitters.base_splitter import BaseSplitter

classifier = get_classifier()


def split_documents(documents):
    chunks: list[Document] = []
    for document in documents:
        service = get_service(document)
        if service:
            chunks.extend(service.split_documents(document))
            continue

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNKS.size, chunk_overlap=config.CHUNKS.overlap
        )
        chunks.extend(splitter.split_documents([document]))

    return chunks


def get_service(document: Document, repeat=0) -> BaseSplitter:
    prompt = build_routing_prompt(document.page_content)

    service_name = classifier.invoke(prompt).strip().lower()
    service_cls = BaseSplitter.registry.get(service_name)

    if not service_cls:
        if repeat == 5:
            raise Exception(f"Unknown service: {service_name}")
        return get_service(document, repeat + 1)

    return service_cls()


def build_routing_prompt(text: str) -> str:
    prompts = []

    for service in BaseSplitter.registry.values():
        prompts.append(f"{service.get_name()}: {service.get_support_prompt()}")

    return f"""
You have the text:
"{text}"

Just say the name of the service that best suits you.

Available services (name: qualifying question):
{chr(10).join(prompts)}

Return format:
<service_name>

Rules:
- exactly one word
- must be one of: cv
- no punctuation
- no explanation
"""
