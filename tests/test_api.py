import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from api_service import app
import pytest

client = TestClient(app)

def test_analyze_endpoint():
    """測試市場分析端點"""
    request_data = {
        "query": "請分析台積電最新股價",
        "user_id": "test_user_001",
        "preferences": {
            "technical_indicators": ["RSI", "MA"],
            "time_frames": ["daily"]
        }
    }
    
    response = client.post("/analyze", json=request_data)
    
    assert response.status_code == 200
    assert "response" in response.json()
    assert "timestamp" in response.json()

def test_user_preferences():
    """測試用戶偏好設定端點"""
    user_id = "test_user_001"
    response = client.get(f"/user/{user_id}/preferences")
    
    assert response.status_code == 200
    assert "favorite_stocks" in response.json()

def test_feedback_submission():
    """測試反饋提交端點"""
    feedback_data = {
        "user_id": "test_user_001",
        "query": "請分析台積電最新股價",
        "rating": 5,
        "comment": "分析非常準確"
    }
    
    response = client.post("/feedback", json=feedback_data)
    assert response.status_code == 200
