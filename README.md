# LangChain 智能代理人系統

## 專案概述
基於 LangChain 開發的多代理人協作系統，具備自主學習能力、長期記憶和市場分析功能。本系統包含多個專業代理人，能夠處理股票分析、新聞解讀等任務。

## 系統架構

### 核心組件

1. **HiveController**
   - 中央控制與調度中心
   - 代理人協作管理
   - 學習機制觸發
   - 回應品質控制

2. **記憶系統**
   - 短期記憶 (ChatMessageHistory)
   - 長期記憶 (ChromaDB)
   - 時效性驗證機制

### 專業代理人

1. **DataRetriever**
   - 支援股票代碼與公司名稱識別
   - 即時股價查詢
   - 財務報表分析
   - 網路資訊檢索
   - 維基百科資料整合

2. **MarketSentimentAnalyzer**
   - 市場情緒分析
   - 新聞情緒評估
   - 技術指標計算
   - 趨勢預測

3. **SelfEvaluator**
   - 回應品質評估
   - 資訊時效性檢查
   - 準確度驗證

4. **LearningMarketAnalyzer**
   - 經驗學習與累積
   - 策略自動調整
   - 預測準確度追蹤

### API 服務

- `/analyze`: 市場分析端點
- `/feedback`: 使用者反饋端點
- `/user/{user_id}/preferences`: 使用者偏好設定

## 安裝需求

```bash
pip install -r requirements.txt
```

需要安裝的主要套件：
- langchain-openai
- langchain-community
- langchain-chroma
- chromadb
- pandas
- yfinance
- textblob
- jieba
- fastapi
- uvicorn

## 環境設定

1. 設定 OpenAI API 金鑰：
```bash
export OPENAI_API_KEY="your-api-key"
```

2. 創建必要目錄：
```bash
mkdir -p ./chroma_db
mkdir -p ./agent_memory
```

## 使用方式

1. 啟動 API 服務：
```bash
uvicorn api_service:app --reload --host 0.0.0.0 --port 8000
```

2. 基本查詢：
```python
from HiveController import HiveController

hive = HiveController()
response = hive.process_request("請分析台積電的最新股價")
```

3. 使用者反饋：
```python
feedback = {
    "user_rating": 4,
    "feedback_type": "accuracy",
    "comment": "分析準確"
}
response = hive.process_request("分析台積電走勢", feedback=feedback)
```

## 功能特點

1. **智能查詢處理**
   - 自動識別股票代碼和公司名稱
   - 即時市場數據獲取
   - 財報資訊分析

2. **自主學習系統**
   - 基於用戶反饋的學習
   - 預測準確度追蹤
   - 策略自動調整

3. **記憶管理**
   - 智能快取機制
   - 時效性驗證
   - 相似度檢索

4. **代理人協作**
   - 多代理人協調
   - 衝突解決機制
   - 資訊共享

## 開發指南

### 添加新代理人

1. 繼承基礎類別：
```python
from BaseAgent import BaseAgent

class NewAgent(BaseAgent):
    def invoke(self, input_data: dict) -> dict:
        # 實作代理人邏輯
        pass
```

2. 加入學習能力：
```python
from agents.base_learning_agent import BaseLearningAgent

class LearningAgent(BaseLearningAgent):
    def learn_from_feedback(self, feedback: Dict):
        # 實作學習邏輯
        pass
```

## 注意事項

1. **資料安全**
   - 定期備份記憶數據
   - 監控 API 使用量
   - 注意資料時效性

2. **系統維護**
   - 定期清理過期記憶
   - 監控學習效果
   - 更新公司資訊數據庫

## 授權
MIT License
