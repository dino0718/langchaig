from HiveController import HiveController
from datetime import datetime

if __name__ == "__main__":
    hive = HiveController()
    
    # 基本查詢
    query = "請分析台積電的市場趨勢"
    response = hive.process_request(query)
    
    # 模擬用戶反饋
    user_feedback = {
        "user_rating": 4,  # 1-5 分
        "feedback_type": "accuracy",
        "comment": "預測準確",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 處理同樣的查詢，但這次帶有反饋
    response_with_feedback = hive.process_request(query, user_feedback)

    query = "今天是幾月幾號"
    
    print("\n🔥 第一次查詢 🔥")
    response1 = hive.process_request(query)
    print(f"\n查詢: {response1.get('query')}")
    print(f"回應: {response1.get('response')}")
    if response1.get('evaluation'):
        print(f"\n品質評估: {response1.get('evaluation')}")
        print(f"評分: {response1.get('quality_score', '無')}")
    
    # 測試市場情緒分析
    sentiment_query = "請分析台積電最近的新聞情緒"
    
    print("\n🔥 市場情緒分析測試 🔥")
    response = hive.process_request(sentiment_query)
    print(f"\n查詢: {response.get('query')}")
    print(f"回應: {response.get('response')}")



