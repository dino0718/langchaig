from langchain_openai import ChatOpenAI  # 從新版模組導入 ChatOpenAI
from langchain.prompts import PromptTemplate
from BaseAgent import BaseAgent

class ResponseGenerator(BaseAgent):
    """根據檢索到的資料生成自然語言回應"""

    def __init__(self):
        # 初始化 ChatOpenAI 模型與預設提示模板
        self.llm = ChatOpenAI(model_name="gpt-4o")  # 使用 gpt-4o 模型生成回應
        self.template = PromptTemplate.from_template(
            """請{retry_hint}根據以下資訊生成簡明易懂的回應。
            
要求：
1. 必須在回應開頭標註資料的檢索時間
2. 提取最新的財報日期和重要數據
3. 用簡潔的語言總結重要資訊
4. 僅保留相關且重要的資訊
5. 使用結構化的方式呈現
6. 特別標注資料的時效性（例如：股價資訊）

資訊來源：
{data}

請生成回應："""
        )

    def invoke(self, input_data: dict) -> dict:  # 將 run 改名為 invoke
        """生成最終回應：格式化提示 -> 呼叫 LLM 生成回應 -> 回傳查詢與回應內容"""
        # 取得由 DataRetriever 提供的檢索資料
        retrieved_data = input_data["data"]
        retry_count = input_data.get("retry_count", 0)
        
        # 根據重試次數調整提示
        retry_hint = "更仔細地" if retry_count > 0 else ""
        
        # 將檢索結果填入提示模板中
        prompt = self.template.format(
            data=retrieved_data,
            retry_hint=retry_hint
        )
        
        print(f"[ResponseGenerator] {'重新' if retry_count > 0 else ''}生成回應...")
        # 使用新版的 invoke 方法呼叫 LLM 生成回應
        response = self.llm.invoke(prompt)

        return {
            "query": retrieved_data.get("query"),  # 返回原查詢內容
            "response": response.content,       # 只回傳實際內容，不包含元數據
            "timestamp": retrieved_data.get("timestamp")
        }
