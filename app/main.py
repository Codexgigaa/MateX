from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routes.chat import router as chat_router
import time
import logging

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s -%(name)s- %(levelname)s- %(message)s "
)
logger = logging.getLogger("MateX-Core")

app = FastAPI(
    title="MateX API",
    description="Empathetic AI Academic Assistant for Students (DAVIET Project)",
    version="1.1.0"
)

# help to UI for request
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # प्रोडक्शन में इसे अपने स्पेसिफिक डोमेन पर सेट करें
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Global Exception Handler
# यह सुनिश्चित करता है कि अगर कभी फिर से 429 एरर आए, तो ऐप क्रैश न हो
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error occurred: {str(exc)}")
    
    status_code = 500
    message = "MateX is experiencing a temporary hiccup."
    
    if "429" in str(exc):
        status_code = 429
        message = "MateX needs a short break (Quota Limit). Please retry in 10 seconds."
    
    return JSONResponse(
        status_code=status_code,
        content={"success": False, "message": message, "detail": str(exc)}
    )

# 4. Request Timing Middleware (Optional: Performance ट्रैक करने के लिए)
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# 5. Routes Inclusion
# हमने 'prefix' जोड़ा है ताकि endpoints professional लगें (e.g., /api/v1/chat)
app.include_router(chat_router, prefix="/api/v1", tags=["Conversation"])

# 6. Health Check Endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "project": "MateX",
        "status": "Online",
        "message": "Sensing emotions and ready to help students!"
    }

if __name__ == "__main__":
    import uvicorn
    # आप इसे 'python app/main.py' से सीधे रन कर सकते हैं
    uvicorn.run(app, host="0.0.0.0", port=8000)