# LangChain 智能代理人系統

一個基於 LangChain 開發的多代理人協作系統，具備自學習能力、長期記憶和市場分析功能。

## 系統架構

### 1. 核心組件

- **HiveController**: 中央控制器
  - 任務分派與協調
  - 代理人間溝通管理
  - 學習機制觸發
  - 品質控制

- **記憶系統**
  - 短期記憶 (ChatMessageHistory)
  - 長期記憶 (ChromaDB 向量資料庫)
  - 智能時效性判斷

### 2. 專業代理人

1. **DataRetriever**
   - 網路資訊檢索
   - Wikipedia 查詢
   - 自動時間戳記

2. **ResponseGenerator**
   - 智能回應生成
   - 多重嘗試機制
   - 上下文感知

3. **MarketSentimentAnalyzer**
   - 市場情緒分析
   - 技術指標計算
   - 新聞情緒評估

4. **SelfEvaluator**
   - 回應品質評估
   - 準確性檢查
   - 相關性評分

### 3. 學習系統

- **BaseLearningAgent**
  - 經驗累積
  - 策略調整
  - 案例學習

- **學習觸發條件**
  1. 低品質回應
  2. 預測誤差
  3. 用戶反饋
  4. 市場波動

## 安裝需求

```bash
pip install langchain langchain-openai langchain-community langchain-chroma
pip install chromadb pandas yfinance textblob jieba
```

## 環境變數

```bash
export OPENAI_API_KEY="your-api-key"
```

## 使用方式

```python
from HiveController import HiveController

# 初始化系統
hive = HiveController()

# 基本查詢
response = hive.process_request("請分析台積電的市場趨勢")

# 帶有反饋的查詢
feedback = {
    "user_rating": 4,
    "feedback_type": "accuracy",
    "comment": "預測準確"
}
response = hive.process_request("分析台積電走勢", feedback)
```

## 特色功能

1. **智能記憶**
   - 向量化儲存
   - 相似度檢索
   - 時效性驗證

2. **自主學習**
   - 經驗累積
   - 策略優化
   - 持續改進

3. **市場分析**
   - 技術指標
   - 新聞情緒
   - 趨勢預測

4. **代理人協作**
   - 意見協調
   - 衝突解決
   - 資訊共享

## 開發指南

### 添加新代理人

1. 繼承基礎類別
```python
from BaseAgent import BaseAgent

class NewAgent(BaseAgent):
    def invoke(self, input_data: dict) -> dict:
        # 實作代理人邏輯
        pass
```

### 加入學習能力

```python
from agents.base_learning_agent import BaseLearningAgent

class LearningAgent(BaseLearningAgent):
    def learn_from_feedback(self, feedback: Dict):
        # 實作學習邏輯
        pass
```

## 注意事項

- 確保 API 金鑰設置正確
- 注意記憶系統的儲存空間
- 定期清理過期的記憶
- 監控學習系統的效能

## 授權

MIT License
