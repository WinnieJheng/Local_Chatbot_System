import streamlit as st
import os
import re
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

# ---------- 字串清理函數 ----------
def clean_text(text):
    text = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9\s,.?!:：；、()\[\]「」『』。，！？\n]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ---------- 分類選單 ----------
category_map = {
    "人事財務": "hr_finance",
    "資訊": "it"
}
category = st.sidebar.selectbox("📁 請選擇分類", list(category_map.keys()))
category_key = category_map[category]
pdf_dir = os.path.join("pdfFiles", category_key)
vector_dir = os.path.join("vectorDB", category_key)
os.makedirs(pdf_dir, exist_ok=True)
os.makedirs(vector_dir, exist_ok=True)

# ---------- 初始化狀態 ----------
st.title("📚 Local Chatbot System (Traditonal Chinese)")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'qa_chain' not in st.session_state:
    st.session_state.qa_chain = None
if 'loaded_category' not in st.session_state:
    st.session_state.loaded_category = None

# ---------- Prompt 與記憶 ----------
chat_template = """你是一個親切且知識豐富的 AI 助理，只能根據下方 context 回答問題：
請用台灣繁體中文回答，語氣自然、完整、給非技術員工看得懂。

Context: {context}
History: {history}
User: {question}
AI:"""

prompt = PromptTemplate(
    input_variables=["history", "context", "question"],
    template=chat_template
)

memory = ConversationBufferWindowMemory(
    memory_key="history",
    return_messages=True,
    input_key="question",
    k=3
)

# ---------- 載入既有分類向量資料庫 ----------
if st.session_state.qa_chain is None or st.session_state.loaded_category != category_key:
    if os.path.exists(vector_dir):
        embedder = OllamaEmbeddings(model="nomic-embed-text")
        vectordb = Chroma(
            embedding_function=embedder,
            persist_directory=vector_dir
        )
        retriever = vectordb.as_retriever()
        llm = Ollama(model="gemma3:4b", base_url="http://localhost:11434")
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": prompt, "memory": memory},
            verbose=False
        )
        st.session_state.qa_chain = qa_chain
        st.session_state.loaded_category = category_key
        st.success(f"✅ 已載入「{category}」分類的向量資料庫")

# ---------- 上傳 PDF 並建立分類向量庫 ----------
uploaded_files = st.file_uploader("📄 上傳 PDF 文件", type="pdf", accept_multiple_files=True)

if uploaded_files:
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

    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    split_docs = splitter.split_documents(all_docs)

    embedder = OllamaEmbeddings(model="nomic-embed-text")
    vectordb = Chroma.from_documents(
        split_docs,
        embedding=embedder,
        persist_directory=vector_dir
    )
    vectordb.persist()
    retriever = vectordb.as_retriever()

    llm = Ollama(model="gemma3:4b", base_url="http://localhost:11434")
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt, "memory": memory},
        verbose=False
    )
    st.session_state.qa_chain = qa_chain
    st.session_state.loaded_category = category_key
    st.success(f"✅「{category}」分類的向量資料庫已更新")

# ---------- 聊天輸入 ----------
question = st.chat_input("💬 請輸入問題")
if question:
    if st.session_state.qa_chain:
        with st.spinner("AI 思考中..."):
            response = st.session_state.qa_chain.run(question)
    else:
        response = "⚠️ 請先上傳文件或選擇已有分類"

    st.session_state.chat_history.append({"role": "user", "message": question})
    st.session_state.chat_history.append({"role": "assistant", "message": response})

# ---------- 顯示對話紀錄 ----------
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["message"])
