from langchain_openai import ChatOpenAI  # 修正導入路徑
from langchain.prompts import PromptTemplate
from BaseAgent import BaseAgent  # 修正導入路徑

class SelfEvaluator(BaseAgent):
    """使用 LLM 來評估 AI 回應的準確性與完整性"""

    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-4o")
        self.template = PromptTemplate.from_template(
            """請根據以下準則評估 AI 的回應品質：

1. **準確性**（是否符合查詢主題？）
2. **完整性**（是否足夠詳盡？）
3. **可讀性**（是否語句通順、結構良好？）
4. **相關性**（是否與原始查詢相關？）

原始查詢：{query}
AI 產生的回應：{response}

請按照以下格式回應：
分數：[0-100]
評語：
[詳細評語]
"""
        )

    def invoke(self, input_data: dict) -> dict:  # 改為 invoke
        """對 AI 產生的回應進行評估"""
        query = input_data.get("query", "")
        response = input_data.get("response", "")

        # 建立評估 Prompt
        prompt = self.template.format(query=query, response=response)

        print("[SelfEvaluator] 正在評估 AI 回應...")
        evaluation = self.llm.invoke(prompt)  # 使用 invoke 而不是 predict

        return {
            "query": query,
            "response": response,
            "evaluation": evaluation.content  # 取得回應內容
        }
