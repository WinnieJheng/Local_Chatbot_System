
# 📚 Local Chatbot System｜本地端企業知識問答系統

本專案是一套基於本地部署的大語言模型（LLM）與語意檢索架構的企業內部問答原型系統，支援 PDF 文件上傳、嵌入向量庫建置、自然語言提問與多輪對話記憶。使用者可透過簡易 UI 與內部文件互動，有效降低重複性問答與行政負擔。

This project is a prototype of a local enterprise knowledge chatbot system powered by an on-premise LLM and semantic retrieval. It allows users to upload internal PDF documents, build a vector store, and ask questions in natural language with multi-turn memory, aiming to reduce repetitive queries and streamline internal communication.

---

## 🌟 功能 Features

- 📄 支援多份 PDF 文件上傳與向量嵌入  
  Support multiple PDF uploads with vector embedding
- 🧹 自動進行文字清理與語意切片（Chunking）  
  Automatic text cleaning and semantic chunking
- 🧠 本地端 LLM（Ollama + Gemma3 模型）  
  On-device LLM (Ollama + Gemma3)
- 🔎 結合 LangChain Retriever 進行語意檢索  
  Integrated LangChain Retriever for semantic search
- 💬 多輪對話記憶（記憶最近三輪對話）  
  Multi-turn memory (last 3 turns)
- 🖥️ Streamlit UI 提供簡易問答介面  
  Streamlit-based user interface for chatbot interaction
- 🧾 支援繁體中文自然語言問答  
  Traditional Chinese natural language Q&A
- 📂 測試文件與回答示意圖附於專案中  
  Demo documents and screenshot included

---

## 📁 專案結構 Project Structure

```
Local_Chatbot_System/
├── main.py                   # 主程式 Main script
├── answer_example.jpg        # 回答畫面示意圖 Screenshot
├── requirements.txt          # 套件需求 Required packages
└── test_doc/                 # 測試用 PDF 資料夾 Test documents
    ├── HR_QA.pdf
    └── Finance_QA.pdf
```

---

## 🛠 使用技術 Tech Stack

- **LLM**：Ollama（Gemma3）  
  Ollama (Gemma3 local model)
- **語意嵌入模型**：nomic-embed-text  
  nomic-embed-text (embedding for Chinese)
- **向量資料庫**：Chroma（記憶體中）  
  Chroma (in-memory vector store)
- **框架整合**：LangChain  
  LangChain for agent orchestration
- **UI介面**：Streamlit  
  Streamlit interface
- **記憶模組**：ConversationBufferWindowMemory  
  Memory module: window memory (3 rounds)

---

## 🚀 執行方式 How to Run

### 1️⃣ 安裝必要 Python 套件 Install required packages

```bash
pip install -r requirements.txt
```

### 2️⃣ 安裝 Ollama 並下載模型 Install Ollama & Models

請至 Ollama 官方網站安裝：  
Visit https://ollama.com/ to install Ollama

下載所需模型：  
Download the required models:

```bash
ollama pull nomic-embed-text
ollama pull gemma3:4b
```

### 3️⃣ 啟動系統 Launch the app

```bash
streamlit run main.py
```

---

## 🔮 未來規劃 Roadmap

- [ ] 加入 SQLite 儲存向量庫，支援跨次啟動  
      Add SQLite backend to persist vector store
- [ ] 支援多機器人分類（HR/財務/IT）  
      Multiple bot modes for HR/Finance/IT
- [ ] 整合 Docker + Ubuntu GPU 部署架構  
      Docker + GPU deployment for enterprise use
- [ ] 加入原文段落引用與回答來源標示  
      Display cited sources from PDF text
- [ ] 實作知識上傳與權限管理介面  
      Upload interface with access control

---

## 🙋‍♀️ 作者 Author

**鄭宛瑜（Winnie Jheng）**  

