import streamlit as st
import os
from modules.config import PDF_DIR, VECTOR_DIR
from modules.utils import build_vector_db_from_pdfs

st.title("📤 檔案上傳區_資訊")

category_key = "it"
pdf_dir = os.path.join(PDF_DIR, category_key)
vector_dir = os.path.join(VECTOR_DIR, category_key)

uploaded_files = st.file_uploader("📎 上傳 IT 相關 PDF 文件", type="pdf", accept_multiple_files=True)

if uploaded_files:
    build_vector_db_from_pdfs(uploaded_files, pdf_dir, vector_dir)
