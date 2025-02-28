from HiveController import HiveController  # 導入 HiveController，負責呼叫各 Agent

if __name__ == "__main__":
    # 建立 HiveController 實例，負責協調資料檢索與回應產生
    hive = HiveController()
    
    # 測試查詢，定義要查詢的關鍵字
    query = "「請幫我找 中鋼  最新的財報，並分析該季度的營收趨勢」"
    # 呼叫 process_request 方法開始處理請求
    response = hive.process_request(query)
    
    # 列印最終生成的回應結果
    print("\n🔥 最終結果 🔥")
    print(response)
