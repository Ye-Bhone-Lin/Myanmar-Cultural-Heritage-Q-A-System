import streamlit as st
import requests

API_URL = "http://localhost:8000/ask" 

st.set_page_config(page_title="Myanmar Cultural Heritage Q&A", page_icon="🌏", layout="centered")

st.title("🌏 Myanmar Cultural Heritage Q&A System")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])

if prompt := st.chat_input("Ask me about Myanmar culture..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    try:
        response = requests.post(API_URL, json={"query": prompt})
        response.raise_for_status()
        answer = response.json().get("answer", "No response from backend.")
    except Exception as e:
        answer = f"⚠️ Error: {e}"

    st.session_state["messages"].append({"role": "assistant", "content": answer})
    st.chat_message("assistant").markdown(answer)
