from fastapi import APIRouter
from models.chat_model import Message
from services.gemini_service import ask_Gemini
from datetime import datetime
from database.db import save_messages,get_history
router = APIRouter()

@router.post("\chat") #chat to insert from user
def chat(prompt : str):
    user = Message(
        role = 'User',
        text = prompt,
        timestamp = datetime.now()
    )
    save_messages(
        user.role,user.text,user.timestamp
    )
    respond = ask_Gemini(prompt)
    
    bot = Message(
        role = 'Bot',
        text = respond,
        timestamp = datetime.now()
    )
    save_messages(
        bot.role,bot.text,bot.timestamp
    )
    return {
        "User_message" : user,
        "Bot_message"  : bot
    }

@router.get("/history")
def history():

    data = get_history()

    return {"chat_history": data}