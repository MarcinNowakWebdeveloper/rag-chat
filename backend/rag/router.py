from backend.core.llm import get_llm
from backend.rag.classifier import classifier
from backend.rag.rag import retrieve, build_context, build_prompt
from backend.constants.answer_style import (
    STYLE_PROMPTS,
    AnswerStyle,
    get_language_instruction,
)

llm = get_llm()

# =========================
# MAIN PIPELINE
# =========================


def answer_question(question: str, style: AnswerStyle, lang: str = "en"):
    style_prompt = STYLE_PROMPTS[style]
    lang_prompt = get_language_instruction(lang)
    final_style_prompt = f"{lang_prompt}\n{style_prompt}"

    # =========================
    # 1. RAG GATE
    # =========================
    classify = classifier.classify(question)

    if not classify:
        return {
            "answer": "❌ Question is outside knowledge base.",
            "confidence": 0.0,
            "sources": [],
        }

    # =========================
    # 2. RETRIEVE
    # =========================
    results = retrieve(question)

    # =========================
    # 3. BUILD CONTEXT
    # =========================
    context, sources = build_context(results)
    confidence = max(s["score"] for s in sources) if sources else 0.0

    if not context.strip():
        return {
            "answer": "❌ No strong matches found in knowledge base.",
            "confidence": confidence,
            "sources": [],
        }

    # =========================
    # 4. GENERATE
    # =========================
    prompt = build_prompt(context, question, final_style_prompt)

    answer = llm.invoke(prompt)

    return {"answer": answer, "confidence": confidence, "sources": sources}
