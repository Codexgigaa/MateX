from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from transformers import pipeline
import torch

# Load environment variables
load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("Google_API_Key"))

# Initialize the Gemini model
modal = genai.GenerativeModel("gemini-pro")
chat = modal.start_chat(history=[])

# Initialize the sentiment analysis model using Hugging Face's transformers pipeline
# Explicit model name and device to avoid meta tensor error
emotion_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    device=0 if torch.cuda.is_available() else -1
)

# Function to get the Gemini response
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Function to analyze emotion
def analyze_emotion(user_input):
    emotion = emotion_analyzer(user_input)[0]
    return emotion['label'], emotion['score']

# Function to generate custom emotional support response
def generate_supportive_response(emotion_label):
    if emotion_label == "NEGATIVE":
        return "It sounds like you're feeling down. Remember, it's okay to have tough days. How can I assist you further?"
    elif emotion_label == "POSITIVE":
        return "I'm glad you're feeling positive! Keep up the good work!"
    elif emotion_label == "NEUTRAL":
        return "It seems like you're feeling neutral. Let me know if you need assistance with anything!"
    else:
        return "I'm here for you, no matter how you're feeling."

# Streamlit page setup
st.set_page_config(page_title="Q&A with Emotional Support")
st.header("Gemini LLM with Emotional Support")

# Sidebar navigation
page = st.sidebar.selectbox("Select Page", ["Q&A", "History"])

# Initialize chat history in session state if not already initialized
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Q&A Page
if page == "Q&A":
    st.subheader("Ask a Question")
    
    # Get user input
    user_input = st.text_input("Input:", key="input")
    submit = st.button("Ask The Question")
    
    # Handle question submission
    if submit and user_input:
        # Analyze user's emotion
        emotion_label, emotion_score = analyze_emotion(user_input)
        
        # Generate an emotionally supportive response
        emotional_support_response = generate_supportive_response(emotion_label)
        
        # Get response from Gemini AI
        response = get_gemini_response(user_input)
    
        # Add user query to chat history
        st.session_state['chat_history'].append(("You", user_input))
        st.session_state['chat_history'].append(("Emotion Analysis", f"{emotion_label} ({emotion_score:.2f})"))
        st.session_state['chat_history'].append(("Bot (Emotional Support)", emotional_support_response))
        
        # Display Gemini AI response and add it to chat history
        bot_response = ""
        st.subheader("Gemini AI Response")
        for chunk in response:
            st.write(chunk.text)
            bot_response += chunk.text
        
        # Add Gemini AI response to chat history
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
