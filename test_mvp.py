from HiveController import HiveController  # 導入 HiveController，負責呼叫各 Agent

if __name__ == "__main__":
    # 建立 HiveController 實例，負責協調資料檢索與回應產生
    hive = HiveController()
    
    # 測試查詢，定義要查詢的關鍵字
    query = "請問南港最新的財報是什麼時候出來的"
    
    # 第一次查詢
    print("\n🔥 第一次查詢 🔥")
    response1 = hive.process_request(query)
    print(f"\n查詢: {response1.get('query')}")
    print(f"回應: {response1.get('response')}")
    
    # 第二次查詢（應該從記憶中獲取）
    print("\n🔥 第二次查詢 🔥")
    response2 = hive.process_request(query)
    print(f"\n查詢: {response2.get('query')}")
    print(f"回應: {response2.get('response')}")
    if response2.get('from_memory'):
        print("(從記憶中獲取)")


