import os
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from modules.config import llm, EMBED_MODEL, BASE_URL

# === 定義 LangGraph 狀態 ===
class ChatState(TypedDict):
    question: str
    department: str
    answer: str
    history: list

# === Prompt 模板 ===
qa_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "你是一個公司內部的智慧助理，根據 context 與對話歷史回答問題。\n"
        "請用台灣繁體中文、自然語氣回答。\n\n"
        "【過去對話】\n{context}\n\n【目前問題】\n{question}\n\n請給出完整回答："
    ),
)

# === Node 1: 部門分類 ===
def classify_node(state: ChatState) -> ChatState:
    question = state["question"].lower()
    if any(k in question for k in ["請假", "報帳", "薪資", "特休", "加班", "婚假", "保險", "費用"]):
        dept = "hr_finance"
    elif any(k in question for k in ["vpn", "電腦", "teams", "登入", "伺服器", "網路", "印表機"]):
        dept = "it"
    else:
        prompt = (
            "你是公司助理，請判斷下列問題屬於哪個部門："
            "『人事財務』或『資訊』，只回答 hr_finance 或 it。\n\n問題：" + state["question"]
        )
        dept = llm.invoke(prompt).strip().lower()
        dept = "hr_finance" if "hr" in dept else "it"
    return {**state, "department": dept}

# === Node 2: 問答 ===
def qa_node(state: ChatState) -> ChatState:
    department = state["department"]
    db_path = f"vectorDB/{department}"
    if not os.path.exists(db_path):
        return {**state, "answer": f"⚠️ 尚未建立 {department} 向量庫"}

    embedder = OllamaEmbeddings(
    model=EMBED_MODEL,
    base_url=BASE_URL
)
    vectordb = Chroma(embedding_function=embedder, persist_directory=db_path)
    retriever = vectordb.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": qa_prompt},
    )

    past_context = "\n".join([f"User: {x['user']}\nAI: {x['assistant']}" for x in state["history"]])
    merged_query = f"【過去對話】\n{past_context}\n\n【目前問題】\n{state['question']}"
    result = qa_chain.run({"query": merged_query})

    updated_history = state["history"] + [{"user": state["question"], "assistant": result}]
    return {**state, "answer": result, "history": updated_history}

# === 建立 Graph ===
def build_chat_graph():
    graph = StateGraph(ChatState)
    graph.add_node("classify", classify_node)
    graph.add_node("qa", qa_node)
    graph.set_entry_point("classify")
    graph.add_conditional_edges("classify", lambda s: s["department"], {"hr_finance": "qa", "it": "qa"})
    graph.add_edge("qa", END)
    return graph.compile()
