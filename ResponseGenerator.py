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
2. 如果是查詢股票或財報，請優先使用即時股價資訊，並標註資料時間
3. 如果是一般資訊查詢，請提供相關資訊摘要

注意事項：
1. 股價資訊必須使用即時數據
2. 所有資訊都要標註時間
3. 如果發現資訊可能過時，要明確說明

原始查詢：{query}
查詢時間：{timestamp}

資訊來源：
{data}

請生成結構化的回應："""
        )

    def invoke(self, input_data: dict) -> dict:  # 將 run 改名為 invoke
        """生成最終回應：格式化提示 -> 呼叫 LLM 生成回應 -> 回傳查詢與回應內容"""
        # 取得由 DataRetriever 提供的檢索資料
        retrieved_data = input_data["data"]
        retry_count = input_data.get("retry_count", 0)
        query = retrieved_data.get("query", "")
        timestamp = retrieved_data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # 檢查是否有驗證過的股票資訊
        stock_info = retrieved_data.get("stock_info", {})
        if stock_info and stock_info.get("verified"):
            stock_data = (
                f"即時股價資訊 (更新時間: {stock_info['timestamp']}):\n"
                f"股票代碼: {stock_info['symbol']}\n"
                f"現價: NT${stock_info['current_price']:.2f}\n"
                f"漲跌: {stock_info['change']:.2f}\n"
                f"成交量: {stock_info['volume']:,.0f}"
            )
        else:
            stock_data = "無法獲取可靠的即時股價資訊。請稍後再試或直接查詢交易所網站。"

        retry_hint = "更仔細地" if retry_count > 0 else ""
        
        # 將檢索結果填入提示模板中
        prompt = self.template.format(
            query=query,
            data=stock_data,
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
