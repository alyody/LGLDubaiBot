import streamlit as st
import pandas as pd
import docx
import fitz  # PyMuPDF
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tempfile

st.set_page_config(page_title="LGLDubaiBot", layout="wide")
st.title("🚢 LGLDubaiBot")
st.markdown("Upload your documents and ask questions. LGLDubaiBot will find the most relevant answers from your files.")

uploaded_files = st.file_uploader("Upload Excel, PDF, DOCX, or TXT files", type=["xlsx", "xls", "pdf", "docx", "txt"], accept_multiple_files=True)

documents = []

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(file):
    return file.read().decode("utf-8")

def extract_text_from_excel(file):
    text = ""
    try:
        xls = pd.ExcelFile(file, engine="openpyxl")
    except:
        xls = pd.ExcelFile(file, engine="xlrd")
    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name)
        text += f"\nSheet: {sheet_name}\n"
        text += df.to_string(index=False)
    return text

if uploaded_files:
    for file in uploaded_files:
        if file.type == "application/pdf":
            content = extract_text_from_pdf(file)
        elif file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            content = extract_text_from_docx(file)
        elif file.type in ["text/plain"]:
            content = extract_text_from_txt(file)
        elif file.type in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
            content = extract_text_from_excel(file)
        else:
            content = ""
        documents.append(content)

    st.success(f"{len(documents)} document(s) processed successfully.")

    query = st.text_input("Ask a question about your documents:")

    if query and documents:
        corpus = documents + [query]
        vectorizer = TfidfVectorizer().fit_transform(corpus)
        vectors = vectorizer.toarray()
        cosine_sim = cosine_similarity([vectors[-1]], vectors[:-1])
        best_match_idx = cosine_sim[0].argmax()
        best_score = cosine_sim[0][best_match_idx]

        st.subheader("📄 Most Relevant Answer")
        st.write(documents[best_match_idx])
        st.caption(f"Similarity Score: {best_score:.2f}")

