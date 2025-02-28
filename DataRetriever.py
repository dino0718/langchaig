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

        # 使用 DuckDuckGo 進行網路搜尋，獲取網路上的相關資料
        search_results = self.search_tool.run(query)

        # 若查詢主題適用，使用 Wikipedia API 進行資料查詢
        wiki_results = self.wiki_tool.run(query)

        return {
            "query": query,                   # 返回原查詢關鍵字
            "search_results": search_results, # 返回網路搜尋結果
            "wiki_results": wiki_results      # 返回 Wikipedia 查詢結果
        }
