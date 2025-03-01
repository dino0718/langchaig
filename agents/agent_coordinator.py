from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

class AgentCoordinator:
    """負責協調不同代理人之間的溝通與協商"""

    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-4o")
        self.negotiation_template = PromptTemplate.from_template(
            """請協調以下代理人的意見分歧：

代理人 A ({agent_a_id}) 的觀點：
{agent_a_opinion}

代理人 B ({agent_b_id}) 的觀點：
{agent_b_opinion}

請考慮：
1. 各方論點的可信度
2. 支持證據的強度
3. 時效性和相關性

給出協調建議："""
        )

    def negotiate(self, agent_a: str, opinion_a: Dict, agent_b: str, opinion_b: Dict) -> Dict:
        """協調兩個代理人之間的意見分歧"""
        prompt = self.negotiation_template.format(
            agent_a_id=agent_a,
            agent_a_opinion=opinion_a,
            agent_b_id=agent_b,
            agent_b_opinion=opinion_b
        )
        
        resolution = self.llm.invoke(prompt)
        
        return {
            "resolution": resolution.content,
            "agents_involved": [agent_a, agent_b],
            "status": "resolved"
        }

    def broadcast(self, message: Dict, recipients: List[str]):
        """向多個代理人廣播訊息"""
        return {
            "message": message,
            "recipients": recipients,
            "status": "broadcasted"
        }
