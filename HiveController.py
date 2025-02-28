from typing import Dict
from DataRetriever import DataRetriever
from ResponseGenerator import ResponseGenerator
from langchain_openai import ChatOpenAI  # 從新版模組導入 ChatOpenAI


class HiveController:
    """負責管理並調度不同的 Agent"""

    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-4o")  # 讓 LLM 負責決策
        self.retriever = DataRetriever()
        self.generator = ResponseGenerator()

    def analyze_request(self, user_input: str) -> list:
        """用 GPT-4o 決定需要哪些 Agent"""
        prompt = f"""
        你是一個 AI 任務調度器，負責決定該派遣哪些 AI Agent 來處理使用者的請求：
        "{user_input}"

        你的選擇：
        - 如果需要從外部數據源檢索資訊，請選擇 "DataRetriever"
        - 如果需要進行數據分析或趨勢預測，請選擇 "ResponseGenerator"
        - 如果需要評估資料可信度，請選擇 "SelfEvaluator"

        請**只回傳一個 Python List**，例如：["DataRetriever", "ResponseGenerator"]
        """
        # 使用 invoke 方法呼叫 LLM 生成決策字串
        response = self.llm.invoke(prompt)
        # 移除可能含有的 code fence 標記
        response_lines = response.content.strip().splitlines()  # 修改：改用 response.content
        cleaned = [line for line in response_lines if not line.strip().startswith("```")]
        cleaned_response = "\n".join(cleaned)
        # 將清理後的字串轉換為 Python List
        return eval(cleaned_response)

    def process_request(self, user_input: str) -> Dict:
        """接收用戶請求，決定調用哪些 Agent"""
        print(f"[HiveController] 收到請求: {user_input}")

        agents_to_use = self.analyze_request(user_input)
        print(f"[HiveController] AI 決定派遣的 Agent: {agents_to_use}")

        results = {}

        if "DataRetriever" in agents_to_use:
            results["retrieved_data"] = self.retriever.invoke({"query": user_input})

        if "ResponseGenerator" in agents_to_use:
            results["response"] = self.generator.invoke({"data": results.get("retrieved_data", {})})

        if "SelfEvaluator" in agents_to_use:
            results["evaluation"] = self.evaluator.run({"response": results.get("response", {})})

        return results
