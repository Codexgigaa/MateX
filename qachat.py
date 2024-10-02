from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("Google_API_Key"))

# Initialize the Gemini model
modal = genai.GenerativeModel("gemini-pro")
chat = modal.start_chat(history=[])

# Function to get the Gemini response
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Streamlit page setup
st.set_page_config(page_title="Q&A Demo")

# Sidebar navigation
page = st.sidebar.selectbox("Select Page", ["Q&A", "History"])

# Initialize chat history in session state if not already initialized
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Q&A Page
if page == "Q&A":
    st.header("Gemini LLM Application")
    
    # Get user input
    user_input = st.text_input("Input:", key="input")
    submit = st.button("Ask The Question")
    
    # Handle question submission
    if submit and user_input:
        response = get_gemini_response(user_input)
    
        # Add user query to chat history
        st.session_state['chat_history'].append(("You", user_input))
        
        # Display the response and add it to chat history
        bot_response = ""
        st.subheader("The Response is")
        for chunk in response:
            st.write(chunk.text)
            bot_response += chunk.text
        
        # Add bot response to chat history
        st.session_state['chat_history'].append(("Bot", bot_response))

# History Page
elif page == "History":
    st.header("Chat History")

    # Display the chat history
    if st.session_state['chat_history']:
        for role, text in st.session_state['chat_history']:
            st.write(f"**{role}:** {text}")
    else:
        st.write("No chat history yet.")

