from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.gemini_service import ask_Gemini 

router = APIRouter()
class ChatRequest(BaseModel):
    prompt: str


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


    response = ask_Gemini(request.prompt)

    if "error" in response.lower() or "quota" in response.lower():
        raise HTTPException(status_code=429, detail=response)

    return {
        "matex_response": response,
        "status": "success"
    }