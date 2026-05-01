from enum import Enum


class AnswerStyle(str, Enum):
    DEFAULT = "default"
    FORMAL = "formal"
    CHILD = "child"
    PESSIMISTIC = "pessimistic"
    OPTIMISTIC = "optimistic"


STYLE_PROMPTS = {
    AnswerStyle.DEFAULT: "",
    AnswerStyle.FORMAL: "Respond in a formal, bureaucratic tone.",
    AnswerStyle.CHILD: "Explain like a fairy tale for a child.",
    AnswerStyle.PESSIMISTIC: "Respond in a pessimistic tone.",
    AnswerStyle.OPTIMISTIC: "Respond in a very optimistic tone.",
}

STYLE_LABELS = {
    "pl": {
        AnswerStyle.DEFAULT: "Domyślny",
        AnswerStyle.FORMAL: "Formalny (urzędowy)",
        AnswerStyle.CHILD: "Dla dziecka (bajka)",
        AnswerStyle.PESSIMISTIC: "Pesymistyczny",
        AnswerStyle.OPTIMISTIC: "Optymistyczny",
    },
    "en": {
        AnswerStyle.DEFAULT: "Default",
        AnswerStyle.FORMAL: "Formal",
        AnswerStyle.CHILD: "Child-friendly",
        AnswerStyle.PESSIMISTIC: "Pessimistic",
        AnswerStyle.OPTIMISTIC: "Optimistic",
    },
}


def get_style_label(style: AnswerStyle, lang: str = "en") -> str:
    return STYLE_LABELS.get(lang, STYLE_LABELS["en"]).get(style, style.value)


def get_language_instruction(lang: str) -> str:
    if lang == "pl":
        return "Answer in Polish."
    if lang == "en":
        return "Answer in English."
    return ""
