from langchain_openai import ChatOpenAI  # 從新版模組導入 ChatOpenAI
from langchain.prompts import PromptTemplate
from BaseAgent import BaseAgent
from datetime import datetime

class ResponseGenerator(BaseAgent):
    """根據檢索到的資料生成自然語言回應"""

    def __init__(self):
        # 初始化 ChatOpenAI 模型與預設提示模板
        self.llm = ChatOpenAI(model_name="gpt-4o")  # 使用 gpt-4o 模型生成回應
        self.template = PromptTemplate.from_template(
            """請{retry_hint}根據查詢類型和資訊生成合適的回應。

查詢類型判斷：
1. 如果是詢問身份（例如：你是誰），請進行自我介紹
2. 如果是查詢股票或財報，請提供相關數據分析
3. 如果是一般資訊查詢，請提供相關資訊摘要

原始查詢：{query}
查詢時間：{timestamp}

資訊來源：
{data}

如果是身份相關查詢，請使用以下格式回應：
我是一個基於 AI 技術開發的智能助理，專長包括：
- 股票市場分析和財報解讀
- 即時新聞和資訊檢索
- 市場情緒分析
- 數據分析和趨勢預測

其他查詢則使用原有結構化格式回應。
"""
        )

    def invoke(self, input_data: dict) -> dict:  # 將 run 改名為 invoke
        """生成最終回應：格式化提示 -> 呼叫 LLM 生成回應 -> 回傳查詢與回應內容"""
        # 取得由 DataRetriever 提供的檢索資料
        retrieved_data = input_data["data"]
        retry_count = input_data.get("retry_count", 0)
        query = retrieved_data.get("query", "")
        timestamp = retrieved_data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # 根據重試次數調整提示
        retry_hint = "更仔細地" if retry_count > 0 else ""
        
        # 將檢索結果填入提示模板中
        prompt = self.template.format(
            query=query,
            data=retrieved_data.get("data", ""),
            retry_hint=retry_hint,
            timestamp=timestamp
        )
        
        print(f"[ResponseGenerator] {'重新' if retry_count > 0 else ''}生成回應...")
        # 使用新版的 invoke 方法呼叫 LLM 生成回應
        response = self.llm.invoke(prompt)

        return {
            "query": query,  # 返回原查詢內容
            "response": response.content,       # 只回傳實際內容，不包含元數據
            "timestamp": timestamp
        }
