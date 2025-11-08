import re
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.ollama import OllamaEmbeddings
from modules.config import EMBED_MODEL, BASE_URL

def clean_text(text: str) -> str:
    """清理文件文字內容"""
    text = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9\s,.?!:：；、()\[\]「」『』。，！？\n]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def build_vector_db_from_pdfs(uploaded_files, pdf_dir: str, vector_dir: str):
    """共用上傳 + 向量庫建立流程"""
    import os
    from streamlit import info, success

    if not uploaded_files:
        return None

    os.makedirs(pdf_dir, exist_ok=True)
    os.makedirs(vector_dir, exist_ok=True)

    all_docs = []
    for uploaded_file in uploaded_files:
        file_path = os.path.join(pdf_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        loader = PyPDFLoader(file_path)
        docs = loader.load()
        for doc in docs:
            doc.page_content = clean_text(doc.page_content)
        all_docs.extend(docs)

    info(f"已讀取 {len(all_docs)} 頁文件，開始建立向量資料庫...")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    split_docs = splitter.split_documents(all_docs)
    embedder = OllamaEmbeddings(
        model=EMBED_MODEL,
        base_url=BASE_URL   # ✅ 指向 Docker 裡的 ollama 容器
    )
    vectordb = Chroma.from_documents(split_docs, embedding=embedder, persist_directory=vector_dir)
    vectordb.persist()

    success(f"✅ 向量資料庫已建立完成！\n\n儲存路徑：{vector_dir}")
    return vectordb
