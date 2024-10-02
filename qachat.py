from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("Google_API_Key"))

modal = genai.GenerativeModel("gemini-pro")
chat = modal.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question,stream=True)
    return response
st.set_page_config(page_title="Q&A Demo")
st.header("geminni LLM Application")
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
    
input = st.text_input("Input:",key="input")
submit= st.button("Ask The Question")
if submit and input:
    response = get_gemini_response(input)
    
    ##add user query and response to session chat
st.session_state['chat_history'].append(("You",input))
st.subheader("The Response is")
for chunk in response:
    st.write(chunk.text)
    st.session_state['chat_history'].append(("Bot",input))

st.subheader("The chat history is")

for role,text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")