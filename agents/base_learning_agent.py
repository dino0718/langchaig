from abc import abstractmethod
from BaseAgent import BaseAgent
from typing import Dict, List
import json
import os

class BaseLearningAgent(BaseAgent):
    """具有自學習能力的基礎代理人類別"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.experience_path = f"./agent_memory/{agent_id}_experience.json"
        self.load_experience()

    def load_experience(self):
        """載入過往經驗"""
        if os.path.exists(self.experience_path):
            with open(self.experience_path, 'r', encoding='utf-8') as f:
                self.experience = json.load(f)
        else:
            self.experience = {
                "successful_cases": [],
                "failed_cases": [],
                "learning_points": {}
            }

    def save_experience(self):
        """儲存學習經驗"""
        os.makedirs(os.path.dirname(self.experience_path), exist_ok=True)
        with open(self.experience_path, 'w', encoding='utf-8') as f:
            json.dump(self.experience, f, ensure_ascii=False, indent=2)

    @abstractmethod
    def learn_from_feedback(self, feedback: Dict):
        """從回饋中學習"""
        pass

    @abstractmethod
    def adjust_strategy(self, context: Dict):
        """根據經驗調整策略"""
        pass
