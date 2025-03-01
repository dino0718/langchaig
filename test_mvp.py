from HiveController import HiveController
# ...existing code...

if __name__ == "__main__":
    hive = HiveController()
    query = "請問南港2/1的股價是多少"
    
    print("\n🔥 第一次查詢 🔥")
    response1 = hive.process_request(query)
    print(f"\n查詢: {response1.get('query')}")
    print(f"回應: {response1.get('response')}")
    if response1.get('evaluation'):
        print(f"\n品質評估: {response1.get('evaluation')}")
        print(f"評分: {response1.get('quality_score', '無')}")
    
    print("\n🔥 第二次查詢 🔥")
    response2 = hive.process_request(query)
    print(f"\n查詢: {response2.get('query')}")
    print(f"回應: {response2.get('response')}")
    if response2.get('from_memory'):
        print("(從記憶中獲取)")
