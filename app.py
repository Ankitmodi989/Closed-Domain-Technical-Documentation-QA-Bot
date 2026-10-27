import glob
import os
import re

import fitz
import streamlit as st
from transformers import pipeline


MANUAL_DIRS = [os.path.join("data", "manuals"), os.path.join("output", "pdf")]
MODEL_NAME = "deepset/roberta-base-squad2"


@st.cache_data
def load_passages():
    passages = []
    pdf_paths = sorted({path for folder in MANUAL_DIRS for path in glob.glob(os.path.join(folder, "*.pdf"))})
    for path in pdf_paths:
        doc = fitz.open(path)
        for page_num, page in enumerate(doc, start=1):
            text = re.sub(r"\s+", " ", page.get_text()).strip()
            if not text:
                continue
            # Overlapping windows keep short answers together while retaining page citations.
            words = text.split()
            for start in range(0, len(words), 180):
                chunk = " ".join(words[start : start + 240])
                if chunk:
                    passages.append({"text": chunk, "source": os.path.basename(path), "page": page_num})
    return passages


@st.cache_resource
def get_qa_model():
    return pipeline("question-answering", model=MODEL_NAME, tokenizer=MODEL_NAME)


def retrieve(question, passages, limit=5):
    terms = set(re.findall(r"\w+", question.lower()))
    scored = []
    for passage in passages:
        body = passage["text"].lower()
        score = sum(body.count(term) for term in terms if len(term) > 2)
        if score:
            scored.append((score, passage))
    return [item[1] for item in sorted(scored, key=lambda item: item[0], reverse=True)[:limit]]


st.set_page_config(page_title="University Manual QA Bot", page_icon="📘")
st.title("📘 University Technical Manual QA Bot")
st.write("Answers are extracted only from the PDF manuals in `data/manuals` and `output/pdf`. Check the cited page in the original manual.")

passages = load_passages()
if not passages:
    st.warning("No readable PDF found. Add a text-based PDF inside `data/manuals/` or `output/pdf/` and refresh this page.")
    st.stop()

question = st.text_input("Ask a question about the manual")
if question:
    candidates = retrieve(question, passages)
    if not candidates:
        st.info("I couldn't find that in the provided manual.")
    else:
        with st.spinner("Searching the manual… (the model may download on first use)"):
            try:
                qa = get_qa_model()
            except Exception as error:
                st.error("Could not load the QA model. Restart with the project's `.venv` Python and check internet access for the first model download.")
                st.caption(f"Error type: {type(error).__name__}")
                st.stop()
            answers = [qa(question=question, context=p["text"]) for p in candidates]
        best_index = max(range(len(answers)), key=lambda i: answers[i]["score"])
        best, source = answers[best_index], candidates[best_index]
        # This threshold is a demo setting; validate it on your own examples.
        if best["score"] < 0.15 or not best["answer"].strip():
            st.info("I couldn't find that in the provided manual.")
        else:
            st.subheader("Answer")
            st.write(best["answer"])
            st.caption(f"Source: {source['source']}, page {source['page']} · model score {best['score']:.2f}")
            with st.expander("Show supporting passage"):
                st.write(source["text"])
