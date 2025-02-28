from typing import Dict
from DataRetriever import DataRetriever
from ResponseGenerator import ResponseGenerator
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory  # 修正導入路徑

class HiveController:
    """負責管理並調度不同的 Agent"""

    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-4o")
        self.retriever = DataRetriever()
        self.generator = ResponseGenerator()
        self.memory = ChatMessageHistory()  # 初始化聊天記憶

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
        """接收用戶請求，查詢記憶，決定是否要重新檢索"""
        print(f"[HiveController] 收到請求: {user_input}")

        # 檢查記憶
        messages = self.memory.messages
        for i in range(0, len(messages), 2):  # 每次檢查一組對話
            if i + 1 < len(messages):  # 確保有配對的回應
                user_msg = messages[i]
                ai_msg = messages[i + 1]
                if user_input.strip() == user_msg.content.strip():
                    print("[HiveController] 發現相似的查詢，直接返回記憶結果。")
                    return {
                        "query": user_input,
                        "response": ai_msg.content,
                        "from_memory": True
                    }

        # 如果是新問題，執行資料檢索
        retrieved_data = self.retriever.invoke({"query": user_input})
        
        # 使用 ResponseGenerator 處理結果
        if retrieved_data["status"] == "success":
            response = self.generator.invoke({"data": retrieved_data})
            if response and response.get("response"):
                # 儲存到記憶
                self.memory.add_user_message(user_input)
                self.memory.add_ai_message(response["response"])
                return {
                    "query": user_input,
                    "response": response["response"]
                }

        return {
            "query": user_input,
            "response": "抱歉，無法獲取相關資訊。"
        }