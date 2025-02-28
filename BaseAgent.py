from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """Agent 的抽象基礎類別"""
    
    @abstractmethod
    def invoke(self, input_data: dict) -> dict:
        """執行 Agent 的主要功能"""
        pass
