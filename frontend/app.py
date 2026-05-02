import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.rag.router import answer_question
from backend.constants.answer_style import AnswerStyle, get_style_label
from backend.core.llm import get_llm
from frontend.i18n.i18n import I18n

# =========================
# INIT
# =========================
available_langs = I18n.get_available_languages()
LANG = st.selectbox("🌍", available_langs)
i18n = I18n(LANG)
st.set_page_config(page_title="RAG Chat", layout="wide")
st.title(i18n.t("title"))

llm = get_llm()

# =========================
# STYLE SELECTOR
# =========================

styles = list(AnswerStyle)

style_option = st.selectbox(
    i18n.t("style"), styles, format_func=lambda s: get_style_label(s, LANG)
)

# =========================
# INPUT
# =========================

question = st.text_input(i18n.t("question"))

if question:

    col1, col2 = st.columns(2)

    # =========================
    # LEFT → PURE LLM
    # =========================
    with col1:
        st.subheader(i18n.t("llm"))
        with st.spinner(i18n.t("thinking")):
            llm_answer = llm.invoke(question)

        st.write(llm_answer)

    # =========================
    # RIGHT → RAG
    # =========================
    with col2:
        st.subheader(i18n.t("rag"))

        with st.spinner(i18n.t("searching")):
            result = answer_question(question, style_option, LANG)

        st.write(result["answer"])

        st.markdown("---")

        st.write(f"{i18n.t('confidence')}: {result['confidence']:.2f}")

        # =========================
        # SOURCES
        # =========================
        if result["sources"]:
            st.subheader(i18n.t("sources"))

            for src in result["sources"]:
                with st.expander(f"Source {src['id']} (score={src['score']:.2f})"):
                    st.write(src["text"])
