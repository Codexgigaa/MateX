import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_root_endpoint():
    """चेक करें कि क्या रूट (/) सही काम कर रहा है"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json()["project"] == "MateX"

@pytest.mark.asyncio
async def test_chat_endpoint_valid_input():
    """चेक करें कि क्या /chat सही प्रॉम्प्ट पर जवाब दे रहा है"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"prompt": "Hello MateX, how are you?"}
        response = await ac.post("/api/v1/chat", json=payload)
    
    assert response.status_code == 200
    assert "matex_response" in response.json()
    assert response.json()["status"] == "success"

@pytest.mark.asyncio
async def test_chat_endpoint_empty_input():
    """चेक करें कि क्या खाली प्रॉम्प्ट भेजने पर एरर आता है"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"prompt": ""}
        response = await ac.post("/api/v1/chat", json=payload)
    
    assert response.status_code == 400
    assert "detail" in response.json()