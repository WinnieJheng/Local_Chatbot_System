# 📚 Local Chatbot System｜本地端企業知識問答系統

本專案是一套基於 **LangChain RAG Framework**、**LangGraph Agent** 與 **Ollama 本地 LLM**
的企業內部問答系統。\
使用者可上傳 PDF 文件建立向量資料庫，並以自然語言進行多輪提問。\
系統會自動判斷問題屬於「人事財務」或「資訊」分類，從對應資料庫中取得答案。

This project is a **local enterprise knowledge chatbot** powered by
**LangChain RAG Framework**, **LangGraph Agent** and **Ollama LLM**.\
It supports multi-turn Q&A in Traditional Chinese, automatically
classifies questions (HR/Finance or IT), and retrieves context from
local vector databases.

------------------------------------------------------------------------

## 🌟 功能 Features

-   🧭 **自動分類問答（LangGraph Agent）**\
    Automatically routes queries to HR/Finance or IT database
-   📄 **支援多份 PDF 文件上傳與向量嵌入**\
    Upload multiple PDFs to build persistent vector stores
-   🧠 **本地端 LLM：Ollama + Gemma3:4b**\
    On-device inference without external API
-   🔎 **語意檢索（Chroma + nomic-embed-text）**\
    Semantic retrieval using local embeddings
-   💬 **多輪記憶（Multi-turn Memory）**\
    Maintains conversation context for coherent answers
-   🧩 **模組化程式架構（config / utils / langgraph_chat）**\
    Modular code for easier maintenance and scaling
-   🐳 **Docker Compose 一鍵啟動**\
    Unified startup for chatbot and Ollama containers
-   💾 **Volume 永續化**\
    Uploaded files and vector DBs persist on the host system
-   🧾 **繁體中文自然語言互動**\
    Designed for non-technical enterprise users in Taiwan

---------------------------------------------------------------------------

## 🖼️ 範例畫面 Screenshots

**📄 文件上傳區 / Upload Interface**
![Upload Example](20251108%20upload_example.jpg)

**💬 問答互動區 / Q&A Interface**
![Answer Example](20251108%20answer_example.jpg)

---------------------------------------------------------------------------

## 📁 專案結構 Project Structure

    Local_Chatbot_System/
    ├── main.py                # Streamlit 問答主程式 / Main Streamlit Q&A app
    ├── modules/               # 模組化程式區 / Modular components
    │   ├── config.py          # 模型與目錄設定 / Model and directory configuration
    │   ├── langgraph_chat.py  # LangGraph Agent 定義 / Agent graph and state logic
    │   └── utils.py           # PDF 向量化與清理工具 / PDF vectorization and text cleaning
    ├── Dockerfile             # 主系統容器建置檔 / Streamlit app container build file
    ├── docker-compose.yml     # 一鍵啟動主系統 + Ollama / Launches app + Ollama containers
    ├── requirements.txt       # 套件需求 / Required Python packages
    ├── pdfFiles/              # 使用者上傳文件 / Uploaded PDF directory
    └── vectorDB/              # 向量資料庫（持久化）/ Persistent vector database

------------------------------------------------------------------------

## 🚀 執行方式 How to Run

### 🐍 Local Run

``` bash
pip install -r requirements.txt
ollama pull gemma3:4b
ollama pull nomic-embed-text
streamlit run main.py
```

### 🐳 Docker Compose

``` bash
docker compose up --build
```

-   Streamlit UI: <http://localhost:8501>
-   Ollama Service: http://ollama:11434

Uploaded PDFs and vector DBs will be saved locally under:

    ./pdfFiles/
    ./vectorDB/

------------------------------------------------------------------------

## 🆕 更新紀錄 Update Highlights (2025.11.08)

-   🧭 新增 **LangGraph Agent**：自動分類問題（人事財務 / 資訊）\
-   🧩 改為模組化架構（config / utils / agent）\
-   🐳 支援 **Docker Compose 一鍵部署**\
-   💾 Volume 掛載：資料與模型向量持久化

------------------------------------------------------------------------

## 🙋‍♀️ 作者 Author

**鄭宛瑜（Winnie Jheng）**\
Generative AI Engineer · Taiwan · 2025
