# LangChain 智能代理系統

這是一個基於 LangChain 開發的智能代理系統，能夠自動化處理資訊檢索和回應生成任務。

## 系統架構

### 核心組件

1. **HiveController**: 系統的核心控制器
   - 負責任務調度和代理協調
   - 整合記憶系統，避免重複查詢
   - 使用 GPT-4 進行任務分析

2. **BaseAgent**: 代理基礎類別
   - 定義標準介面
   - 確保所有代理遵循相同的協議

3. **專業代理**
   - **DataRetriever**: 資料檢索代理
     - 使用 DuckDuckGo 搜尋引擎
     - 整合 Wikipedia API
   - **ResponseGenerator**: 回應生成代理
     - 使用 GPT-4 處理和總結資訊
     - 生成結構化且易讀的回應

### 記憶系統

- 使用 ChatMessageHistory 儲存對話歷史
- 配對儲存用戶查詢和系統回應
- 提供快速檢索功能，避免重複處理

## 安裝需求

```bash
pip install langchain langchain-openai langchain-community
```

## 使用方式

```python
from HiveController import HiveController

# 初始化控制器
hive = HiveController()

# 發送查詢請求
query = "請問南港最新的財報是什麼時候出來的"
response = hive.process_request(query)

# 輸出結果
print(response.get("response"))
```

## 功能特點

1. **智能任務分配**
   - 自動分析查詢需求
   - 動態選擇適合的代理

2. **資訊整合**
   - 多來源資料檢索
   - 智能摘要和分析

3. **記憶系統**
   - 避免重複查詢
   - 確保回應一致性

4. **錯誤處理**
   - 完整的異常處理機制
   - 優雅的降級策略

## 開發者指南

### 添加新代理

1. 繼承 BaseAgent 類別
2. 實作 invoke 方法
3. 在 HiveController 中註冊新代理

```python
class NewAgent(BaseAgent):
    def invoke(self, input_data: dict) -> dict:
        # 實作代理邏輯
        pass
```

### 自訂提示模板

可以在 ResponseGenerator 中自訂提示模板來改進回應格式。

## 注意事項

- 需要設定適當的 API 金鑰
- 注意 API 呼叫限制
- 建議在生產環境中實作快取機制

## 授權

MIT License
