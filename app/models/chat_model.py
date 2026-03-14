from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
class ChatRequest(BaseModel):
    prompt: str = Field(..., example="I'm feeling a bit stressed about my exams.", min_length=1)
    user_id: Optional[str] = Field(None, example="user_123")

class ChatResponse(BaseModel):
    matex_response: str
    emotion_sensed: Optional[str] = Field(None, description="The emotion detected by MateX")
    timestamp: datetime = Field(default_factory=datetime.now)
    status: str = "success"
class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: int