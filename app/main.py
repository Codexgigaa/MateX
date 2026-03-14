# app/main.py

from fastapi import FastAPI
from routes.chat import router as chat_router

app = FastAPI(
    title="AI Chatbot API",
    description="Backend API for Gemini chatbot",
    version="1.0"
)

# attach router
app.include_router(chat_router)

@app.get("/")
def root():
    return {"message": "API is running"}