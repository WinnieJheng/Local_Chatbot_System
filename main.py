import streamlit as st
from modules.langgraph_chat import build_chat_graph

st.set_page_config(page_title="企業內部問答系統", page_icon="🤖")
st.title("💬 企業內部問答系統")

app_graph = build_chat_graph()

# 初始化對話記錄
if "history" not in st.session_state:
    st.session_state.history = []

# 顯示歷史對話
for msg in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(msg["user"])
    with st.chat_message("assistant"):
        st.markdown(msg["assistant"])

# 使用者輸入
question = st.chat_input("💬 請輸入問題")

if question:
    with st.spinner("AI 思考中..."):
        result = app_graph.invoke({
            "question": question,
            "department": "",
            "answer": "",
            "history": st.session_state.history
        })

        dept = "人事財務" if result["department"] == "hr_finance" else "資訊"
        st.chat_message("user").markdown(question)
        st.chat_message("assistant").markdown(
            f"**📁 部門判斷：{dept}**\n\n{result['answer']}"
        )
        st.session_state.history = result["history"]
