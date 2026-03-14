# streamlit_app.py

import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"

st.set_page_config(page_title="AI Chatbot")

st.title("Gemini Chatbot")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
# for history
if st.sidebar.button("Load History"):

    history = requests.get("http://localhost:8000/history").json()

    for role, text, time in history["chat_history"]:
        st.session_state.messages.append({
            "role": role,
            "content": text
        })
# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input box
prompt = st.chat_input("Ask something...")

if prompt:

    # show user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # send request to FastAPI
    response = requests.post(
        API_URL,
        params={"prompt": prompt}
    )

    bot_reply = response.json()["bot_message"]["text"]

    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )