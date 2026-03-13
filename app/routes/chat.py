from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.gemini_service import ask_Gemini  # पक्का करें कि नाम मैच कर रहा है

router = APIRouter()

# 1. Input Schema (यह Swagger UI में इनपुट बॉक्स बना देगा)
class ChatRequest(BaseModel):
    prompt: str

# 2. Response Schema (Professional output structure)
class ChatResponse(BaseModel):
    matex_response: str
    status: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    MateX Interaction Endpoint:
    Takes user input, senses emotion via Gemini, and returns a response.
    """
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    # Calling your service function
    response = ask_Gemini(request.prompt)

    # अगर सर्विस से कोई एरर स्ट्रिंग आती है (जैसे '429' या 'Connection Error')
    if "error" in response.lower() or "quota" in response.lower():
        raise HTTPException(status_code=429, detail=response)

    return {
        "matex_response": response,
        "status": "success"
    }