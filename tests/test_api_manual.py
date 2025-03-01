import requests
import json
import sys
from time import sleep

def test_market_analysis():
    """手動測試市場分析 API"""
    url = "http://localhost:8000/analyze"
    
    payload = {
        "query": "請查查南港輪胎的最新財報",
        "user_id": "test_user_001",
        "preferences": {
            "technical_indicators": ["RSI", "MA"],
            "time_frames": ["daily"]
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # 嘗試連接 API
    max_retries = 3
    timeout = 30  # 增加超時時間至 30 秒
    
    for i in range(max_retries):
        try:
            print(f"嘗試連接 API (第 {i+1} 次)...")
            
            # 先確認服務是否在運行
            try:
                requests.get(f"http://localhost:8000/docs", timeout=2)
            except requests.exceptions.ConnectionError:
                print("API 服務未啟動，請先執行 'uvicorn api_service:app --reload'")
                sys.exit(1)
            
            # 發送實際請求
            print("發送查詢請求...")
            response = requests.post(url, json=payload, headers=headers, timeout=timeout)
            
            print("\n🔥 API 測試結果 🔥")
            print(f"狀態碼: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("\n回應內容:")
                print(f"查詢: {result.get('query')}")
                print(f"回應: {result.get('response')}")
                if result.get('quality_score'):
                    print(f"品質評分: {result.get('quality_score')}")
                print(f"\n時間戳記: {result.get('timestamp', '無')}")
            else:
                print(f"錯誤響應: {response.text}")
            break
            
        except requests.exceptions.ReadTimeout:
            print(f"請求超時 (超過 {timeout} 秒)")
            if i < max_retries - 1:
                print("正在重試...")
                sleep(3)
            else:
                print("已達到最大重試次數，請檢查 API 服務狀態")
                sys.exit(1)
                
        except Exception as e:
            print(f"發生錯誤: {str(e)}")
            if i < max_retries - 1:
                print("正在重試...")
                sleep(3)
            else:
                print("已達到最大重試次數")
                sys.exit(1)

if __name__ == "__main__":
    test_market_analysis()
