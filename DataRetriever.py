from langchain_community.tools import DuckDuckGoSearchRun  # 使用 DuckDuckGo 進行網路搜尋
from langchain_community.utilities import WikipediaAPIWrapper  # 使用 Wikipedia API 查詢資料
from BaseAgent import BaseAgent

class DataRetriever(BaseAgent):
    """從網路與 Wikipedia 檢索相關資訊"""

    def __init__(self):
        # 初始化網路搜尋工具與 Wikipedia 查詢工具
        self.search_tool = DuckDuckGoSearchRun()
        self.wiki_tool = WikipediaAPIWrapper()

    def invoke(self, input_data: dict) -> dict:
        """根據傳入的查詢關鍵字檢索外部資料"""
        query = input_data["query"]
        print(f"[DataRetriever] 檢索中: {query}")

        try:
            search_results = self.search_tool.run(query)
            wiki_results = self.wiki_tool.run(query)
            
            result_text = f"""
搜尋結果:
{search_results}

維基百科資料:
{wiki_results}
"""
            return {
                "query": query,
                "data": result_text,
                "status": "success"
            }
        except Exception as e:
            print(f"[DataRetriever] 錯誤: {str(e)}")
            return {
                "query": query,
                "data": "抱歉，檢索過程中發生錯誤。",
                "status": "error"
            }
