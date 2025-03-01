from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from HiveController import HiveController
app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    user_id: str
    preferences: Dict = None

@app.post("/analyze")
async def analyze_market(request: QueryRequest):
    try:
        hive = HiveController()
        response = hive.process_request(
            request.query,
            user_preferences=request.preferences
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback")
async def submit_feedback(feedback: Dict):
    # 處理用戶反饋
    pass

@app.get("/user/{user_id}/preferences")
async def get_user_preferences(user_id: str):
    # 獲取用戶設定
    pass
