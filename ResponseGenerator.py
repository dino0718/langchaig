from langchain_openai import ChatOpenAI  # 從新版模組導入 ChatOpenAI
from langchain.prompts import PromptTemplate
from BaseAgent import BaseAgent

class ResponseGenerator(BaseAgent):
    """根據檢索到的資料生成自然語言回應"""

    def __init__(self):
        # 初始化 ChatOpenAI 模型與預設提示模板
        self.llm = ChatOpenAI(model_name="gpt-4o")  # 使用 gpt-4o 模型生成回應
        self.template = PromptTemplate.from_template(
            "請根據以下資訊生成簡明易懂的回應：\n\n{data}"
        )

    def invoke(self, input_data: dict) -> dict:  # 將 run 改名為 invoke
        """生成最終回應：格式化提示 -> 呼叫 LLM 生成回應 -> 回傳查詢與回應內容"""
        # 取得由 DataRetriever 提供的檢索資料
        retrieved_data = input_data["data"]
        # 將檢索結果填入提示模板中
        prompt = self.template.format(data=retrieved_data)
        
        print("[ResponseGenerator] 正在生成回應...")
        # 使用新版的 invoke 方法呼叫 LLM 生成回應
        response = self.llm.invoke(prompt)

        return {
            "query": retrieved_data["query"],  # 返回原查詢內容
            "response": response               # 返回 LLM 生成的回應結果
        }
