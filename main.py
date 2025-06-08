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

#字串清理函數
def clean_text(text):
    # 移除奇怪符號與非語意字元
    text = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9\s,.?!:：；、()\[\]「」『』。，！？\n]", "", text)
    # 移除多餘空白（連續空白、斷行、前後空白）
    text = re.sub(r"\s+", " ", text).strip()
    return text

# --- 初始化 ---
st.title("Local Chatbot System")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'qa_chain' not in st.session_state:
    st.session_state.qa_chain = None

# --- 上傳 PDF ---
uploaded_files = st.file_uploader("請上傳多份 PDF 文件", type="pdf", accept_multiple_files=True)

if uploaded_files:
    all_docs = []
    os.makedirs("pdfFiles", exist_ok=True)

    for uploaded_file in uploaded_files:
        # 儲存檔案
        file_path = os.path.join("pdfFiles", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        # 載入文字
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        # 清理每段文字內容
        for doc in docs:
            doc.page_content = clean_text(doc.page_content)
            
        all_docs.extend(docs)

    # 分段
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200) #chunk_size是一段最多幾字，chunk_overlap是前一段的結尾幾字會重複出現在下一段開頭
    split_docs = splitter.split_documents(all_docs)

    # 嵌入與儲存
    embedder = OllamaEmbeddings(model="nomic-embed-text") #nomic-embed-text是針對中文的嵌入模型
    vectordb = Chroma.from_documents(split_docs, embedding=embedder)
    retriever = vectordb.as_retriever()

    # Prompt 語氣設定
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

    # 記憶功能
    memory = ConversationBufferWindowMemory(
        memory_key="history",
        return_messages=True,
        input_key="question",
        k=3 #只記憶前三輪對話，避免影響效能
    )

    # 模型與 QA chain
    llm = Ollama(model="gemma3:4b", base_url="http://localhost:11434") #gemma3是Google的開源大語言模型，11434是ollama的預設port
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt, "memory": memory},
        verbose=False
    )

    st.session_state.qa_chain = qa_chain
    st.success("✅ 向量資料庫建置完成")

# --- 聊天介面 ---
question = st.chat_input("請輸入問題")
if question:
    if st.session_state.qa_chain:
        with st.spinner("AI 思考中..."):
            response = st.session_state.qa_chain.run(question)
    else:
        response = "請先上傳文件。"

    # 加入歷史紀錄
    st.session_state.chat_history.append({"role": "user", "message": question})
    st.session_state.chat_history.append({"role": "assistant", "message": response})

# --- 顯示對話歷史---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["message"])



