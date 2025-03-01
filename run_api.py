import uvicorn
from api_service import app
import string

if __name__ == "__main__":
    print("啟動 API 服務...")
    uvicorn.run(
        "api_service:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )