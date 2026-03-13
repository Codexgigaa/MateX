import streamlit as st
import requests
import time

# 1. Page Configuration (Browser Tab Setting)
st.set_page_config(page_title="MateX | AI Assistant", page_icon="🤖", layout="centered")

# 2. Custom Styling (CSS for a cleaner look)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stTextInput>div>div>input { border-radius: 20px; }
    .stButton>button { border-radius: 20px; width: 100%; background-color: #4CAF50; color: white; }
    .matex-response { background-color: #ffffff; padding: 20px; border-radius: 15px; border-left: 5px solid #4CAF50; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar for MateX Info
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=100)
    st.title("MateX AI")
    st.info("I sense your emotions and help with your studies. Your empathetic academic buddy.")
    if st.button("Clear Chat"):
        st.session_state.messages = []

# 4. Header
st.title("🤖 MateX")
st.caption("How are you feeling today? Let's discuss your studies.")

# 5. Chat History Management
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. User Input
if prompt := st.chat_input("I'm feeling a bit stressed about exams..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 7. Call FastAPI Backend
    with st.chat_message("assistant"):
        with st.spinner("MateX is thinking..."):
            try:
                # Update URL to match your FastAPI prefix
                payload = {"prompt": prompt}
                response = requests.post("http://localhost:8000/api/v1/chat", json=payload)
                
                if response.status_code == 200:
                    result = response.json()["matex_response"]
                    st.markdown(result)
                    st.session_state.messages.append({"role": "assistant", "content": result})
                elif response.status_code == 429:
                    st.warning("Quota reached! Please wait 10 seconds.")
                else:
                    st.error("MateX is sleeping. Check your FastAPI backend.")
            except Exception as e:
                st.error(f"Connection Error: {e}")