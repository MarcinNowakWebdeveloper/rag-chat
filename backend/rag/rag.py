from backend.core.config import config
from backend.core.vector_store import get_vector_db

db = get_vector_db()


def retrieve(question: str):
    """
    Returns:
        list of (doc, score)
    """
    results = db.similarity_search_with_score(question, k=config.RAG.k)
    return results


def build_context(results):
    """
    Filters weak matches and builds structured context
    """

    context = ""
    sources = []

    for i, (doc, score) in enumerate(results):

        # filter weak chunks
        if score < config.RAG.similarity_threshold:
            continue

        chunk = doc.page_content

        context += f"\n[CHUNK {i+1} | score={score:.2f}]\n{chunk}\n"
        sources.append({"id": i + 1, "score": score, "text": chunk[:200]})

    return context, sources


def build_prompt(context: str, question: str, style_prompt: str):
    return f"""
{style_prompt}

You are a strict technical assistant.

Rules:
- Answer ONLY using the provided context
- If the context is relevant but incomplete, try to answer as best as possible using available information.
- You may generalize if context is partially relevant.
- Do NOT invent anything
- Cite sources like [CHUNK 1]

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""
