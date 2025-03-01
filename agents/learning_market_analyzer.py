from agents.base_learning_agent import BaseLearningAgent
from typing import Dict
import pandas as pd
from datetime import datetime

class LearningMarketAnalyzer(BaseLearningAgent):
    def __init__(self):
        super().__init__("market_analyzer")
        self.confidence_threshold = 0.7

    def invoke(self, input_data: dict) -> dict:
        """實作 BaseAgent 要求的 invoke 方法"""
        context = input_data.get("context", {})
        strategy = self.adjust_strategy(context)
        
        return {
            "strategy": strategy,
            "confidence_threshold": self.confidence_threshold,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
    def learn_from_feedback(self, feedback: Dict):
        """從市場回饋中學習"""
        prediction = feedback.get("prediction")
        actual_result = feedback.get("actual_result")
        
        if prediction and actual_result:
            if prediction["direction"] == actual_result["direction"]:
                self.experience["successful_cases"].append(feedback)
                self.confidence_threshold *= 1.1  # 提高信心閾值
            else:
                self.experience["failed_cases"].append(feedback)
                self.confidence_threshold *= 0.9  # 降低信心閾值
                
            self.save_experience()
            
    def adjust_strategy(self, context: Dict):
        """根據過往經驗調整分析策略"""
        similar_cases = self._find_similar_cases(context)
        if similar_cases:
            success_rate = len([c for c in similar_cases if c["success"]]) / len(similar_cases)
            return {
                "strategy_adjustment": {
                    "confidence_threshold": self.confidence_threshold,
                    "success_rate": success_rate,
                    "recommended_indicators": self._get_best_indicators(similar_cases)
                }
            }
        return {"strategy_adjustment": None}

    def _find_similar_cases(self, context: Dict) -> list:
        """尋找類似的歷史案例"""
        # 實作尋找相似案例的邏輯
        return [case for case in self.experience["successful_cases"] 
                if self._calculate_similarity(case, context) > 0.7]

    def _get_best_indicators(self, cases: list) -> list:
        """分析最有效的技術指標"""
        # 實作分析最佳指標的邏輯
        return ["RSI", "MA", "MACD"]  # 示例返回值

    def _calculate_similarity(self, case: Dict, context: Dict) -> float:
        """計算案例相似度"""
        # 實作相似度計算邏輯
        return 0.8  # 示例返回值
