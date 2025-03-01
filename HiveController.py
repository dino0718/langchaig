from typing import Dict
from DataRetriever import DataRetriever
from ResponseGenerator import ResponseGenerator
from SelfEvaluator import SelfEvaluator
from long_term_memory import LongTermMemory  # 新增導入
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory  # 修正導入路徑
from market_sentiment_analyzer import MarketSentimentAnalyzer
import re  # 新增導入
from agents.agent_coordinator import AgentCoordinator  # 新增導入
from agents.learning_market_analyzer import LearningMarketAnalyzer

class HiveController:
    """負責管理並調度不同的 Agent"""
    
    QUALITY_THRESHOLD = 70  # 新增：品質評分閾值
    MAX_RETRIES = 2        # 新增：最大重試次數

    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-4o")
        self.retriever = DataRetriever()
        self.generator = ResponseGenerator()
        self.evaluator = SelfEvaluator()  # 新增 evaluator
        self.memory = ChatMessageHistory()  # 初始化聊天記憶
        self.long_term_memory = LongTermMemory()  # 初始化長期記憶系統
        self.sentiment_analyzer = MarketSentimentAnalyzer()  # 初始化市場情緒分析器
        self.coordinator = AgentCoordinator()  # 新增協調器
        self.learning_market_analyzer = LearningMarketAnalyzer()
        self.learning_threshold = 0.8  # 學習觸發閾值

    def analyze_request(self, user_input: str) -> list:
        """用 GPT-4o 決定需要哪些 Agent"""
        prompt = f"""
        你是一個 AI 任務調度器，負責決定該派遣哪些 AI Agent 來處理使用者的請求：
        "{user_input}"

        你的選擇：
        - 如果需要從外部數據源檢索資訊，請選擇 "DataRetriever"
        - 如果需要進行數據分析或趨勢預測，請選擇 "ResponseGenerator"
        - 如果需要評估資料可信度，請選擇 "SelfEvaluator"
        - 如果需要分析市場情緒，請選擇 "MarketSentimentAnalyzer"

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

    def trigger_learning(self, response: Dict, feedback: Dict = None) -> None:
        """觸發學習機制的條件"""
        # 1. 評分過低時觸發學習
        if response.get("quality_score", 0) < self.QUALITY_THRESHOLD:
            print("[HiveController] 檢測到低品質回應，觸發學習機制")
            self.learning_market_analyzer.learn_from_feedback({
                "type": "quality_issue",
                "response": response,
                "feedback": "評分過低"
            })

        # 2. 市場預測結果驗證
        if "market_prediction" in response:
            actual_price = self._verify_market_prediction(response["market_prediction"])
            prediction_accuracy = self._calculate_prediction_accuracy(
                response["market_prediction"], 
                actual_price
            )
            
            if prediction_accuracy < self.learning_threshold:
                print("[HiveController] 預測準確度不足，觸發學習機制")
                self.learning_market_analyzer.learn_from_feedback({
                    "type": "prediction_error",
                    "prediction": response["market_prediction"],
                    "actual": actual_price
                })

        # 3. 用戶提供明確反饋
        if feedback and feedback.get("user_rating"):
            print("[HiveController] 收到用戶反饋，觸發學習機制")
            self.learning_market_analyzer.learn_from_feedback(feedback)

    def _verify_market_prediction(self, prediction: Dict) -> Dict:
        """驗證市場預測結果"""
        try:
            symbol = prediction.get("symbol")
            predicted_price = prediction.get("price")
            predicted_direction = prediction.get("direction")
            
            # 獲取實際市場數據
            stock = yf.Ticker(symbol)
            current_price = stock.history(period="1d")['Close'][-1]
            
            return {
                "symbol": symbol,
                "actual_price": current_price,
                "prediction_diff": current_price - predicted_price,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            print(f"[HiveController] 預測驗證錯誤: {str(e)}")
            return {}

    def process_request(self, user_input: str, feedback: Dict = None) -> Dict:
        print(f"[HiveController] 收到請求: {user_input}")

        # 檢查是否是情緒分析相關查詢
        if "情緒" in user_input or "新聞" in user_input:
            # 提取股票代碼（如果有的話）
            stock_pattern = r'([0-9]{4,6}\.TW|[0-9]{4,6})'
            stock_match = re.search(stock_pattern, user_input)
            stock_symbol = stock_match.group() if stock_match else "2330.TW"
            
            # 執行市場情緒分析
            sentiment_result = self.sentiment_analyzer.invoke({
                "query": user_input,
                "symbol": f"{stock_symbol}.TW" if not stock_symbol.endswith('.TW') else stock_symbol
            })
            
            if sentiment_result["status"] == "success":
                response = f"""
查詢時間: {sentiment_result['timestamp']}

市場情緒分析結果：
{sentiment_result['analysis']}

相關新聞摘要：
{chr(10).join(sentiment_result['news_sentiment'][:5])}  # 只顯示前5條新聞

技術指標數據：
- 最新價格：{sentiment_result['technical_data'].get('latest_price', 'N/A')}
- RSI：{sentiment_result['technical_data'].get('rsi', 'N/A')}
- 趨勢：{sentiment_result['technical_data'].get('trend', 'N/A')}
"""
                return {
                    "query": user_input,
                    "response": response,
                    "timestamp": sentiment_result['timestamp']
                }

        # 先檢查長期記憶
        similar_memories = self.long_term_memory.retrieve_similar_queries(user_input)
        if similar_memories:
            memory = similar_memories[0].page_content
            print("[HiveController] 從長期記憶中找到相關且時效性符合的查詢")
            return {
                "query": user_input,
                "response": memory,
                "from_memory": True,
                "memory_type": "long_term"
            }

        # 檢查短期記憶
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
        
        final_response = {"query": user_input, "response": None}
        
        if retrieved_data["status"] == "success":
            # 嘗試生成高品質回應
            for attempt in range(self.MAX_RETRIES):
                # 生成回應
                response = self.generator.invoke({
                    "data": retrieved_data,
                    "retry_count": attempt  # 傳入重試次數
                })
                
                if response and response.get("response"):
                    # 評估回應品質
                    evaluation = self.evaluator.invoke({
                        "query": user_input,
                        "response": response["response"]
                    })
                    
                    # 解析評分：尋找 "分數：" 後面的數字
                    try:
                        eval_text = evaluation["evaluation"]
                        score_idx = eval_text.find("分數：")
                        if score_idx != -1:
                            score_text = eval_text[score_idx:].split('\n')[0]
                            score = int(''.join(filter(str.isdigit, score_text)))
                        else:
                            score = 0
                    except Exception as e:
                        print(f"[HiveController] 評分解析錯誤: {str(e)}")
                        score = 0
                    
                    print(f"[HiveController] 回應品質評分: {score}")
                    
                    # 如果評分達標或已是最後一次嘗試
                    if score >= self.QUALITY_THRESHOLD or attempt == self.MAX_RETRIES - 1:
                        final_response["response"] = response["response"]
                        final_response["evaluation"] = evaluation["evaluation"]
                        final_response["quality_score"] = score
                        final_response["timestamp"] = response.get("timestamp")
                        
                        # 同時儲存到短期和長期記憶
                        memory_text = f"[查詢時間: {response.get('timestamp')}]\n{response['response']}"
                        self.memory.add_user_message(user_input)
                        self.memory.add_ai_message(memory_text)
                        
                        # 儲存到長期記憶
                        self.long_term_memory.store_memory(
                            user_input, 
                            response["response"],
                            response.get("timestamp")
                        )
                        break
        
        if final_response["response"] is None:
            final_response["response"] = "抱歉，無法獲取相關資訊。"

        # 觸發學習機制
        self.trigger_learning(final_response, feedback)
        
        return final_response

    def resolve_conflicts(self, agent_responses: Dict) -> Dict:
        """解決代理人之間的意見分歧"""
        # 例如：當 DataRetriever 和 MarketSentimentAnalyzer 對市場趨勢有不同判斷
        if ("DataRetriever" in agent_responses and 
            "MarketSentimentAnalyzer" in agent_responses):
            
            resolution = self.coordinator.negotiate(
                "DataRetriever",
                agent_responses["DataRetriever"],
                "MarketSentimentAnalyzer",
                agent_responses["MarketSentimentAnalyzer"]
            )
            
            # 將協調結果廣播給相關代理人
            self.coordinator.broadcast(
                resolution,
                ["DataRetriever", "MarketSentimentAnalyzer"]
            )
            
            return resolution
            
        return agent_responses