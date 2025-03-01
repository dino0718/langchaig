#import chromadb
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma  # 更新導入路徑
from langchain_core.documents import Document
from datetime import datetime, timedelta
import re
import jieba  # 新增：用於中文分詞

class LongTermMemory:
    """使用 ChromaDB 來存儲 AI 過去的回應，提升記憶能力"""

    def __init__(self, persist_directory="./chroma_db"):
        self.persist_directory = persist_directory
        self.embedding = OpenAIEmbeddings()
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding,
            collection_name="memory"
        )
        self.company_keywords = {}  # 用於儲存公司關鍵字

    def store_memory(self, query: str, response: str, timestamp: str = None):
        """將用戶查詢與 AI 回應存入向量資料庫"""
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        memory_content = f"""
時間: {timestamp}
查詢: {query}
回應: {response}
"""
        doc = Document(page_content=memory_content)
        self.vector_store.add_documents([doc])
        print(f"[LongTermMemory] 已儲存查詢: {query}")

    def extract_company_name(self, query: str) -> str:
        """從查詢中提取公司名稱"""
        # 常見股票代號格式
        stock_pattern = r'([0-9]{4,6})|([a-zA-Z]+[0-9]+)'
        stock_match = re.search(stock_pattern, query)
        if stock_match:
            return stock_match.group()
            
        # 常見公司名稱
        company_pattern = r'([\u4e00-\u9fff]{2,})[股票|股價|公司]?'
        company_match = re.search(company_pattern, query)
        if company_match:
            return company_match.group(1)
            
        return ""

    def is_query_similar(self, memory_content: str, query: str) -> bool:
        """檢查查詢是否相似"""
        # 提取公司名稱
        memory_company = self.extract_company_name(memory_content)
        query_company = self.extract_company_name(query)
        
        # 如果都有公司名稱，必須相同才算相似
        if memory_company and query_company:
            return memory_company == query_company
            
        # 如果沒有公司名稱，進行一般相似度比較
        memory_words = set(jieba.cut(memory_content))
        query_words = set(jieba.cut(query))
        
        # 計算詞彙重疊度
        overlap = len(memory_words & query_words)
        return overlap >= 2  # 至少需要2個詞彙重疊

    def is_date_relevant(self, memory_content: str, query: str) -> bool:
        """檢查記憶中的日期是否與查詢相關"""
        # 從查詢中提取特定日期
        query_date_match = re.search(r'(\d{1,2}/\d{1,2})', query)
        if not query_date_match:
            # 如果查詢沒有指定日期（查詢最新資料），則檢查記憶時間是否在24小時內
            time_match = re.search(r'時間: ([\d-]+ [\d:]+)', memory_content)
            if time_match:
                memory_time = datetime.strptime(time_match.group(1), '%Y-%m-%d %H:%M:%S')
                return (datetime.now() - memory_time) < timedelta(hours=24)
            return False

        # 如果查詢指定了特定日期
        query_date = query_date_match.group(1)
        current_year = datetime.now().year
        try:
            # 將查詢日期轉換為完整日期格式
            target_date = datetime.strptime(f"{current_year}/{query_date}", '%Y/%m/%d')
            
            # 從記憶內容中尋找日期相關資訊
            memory_date_matches = re.finditer(r'(\d{1,2}/\d{1,2}|\d{4}-\d{2}-\d{2})', memory_content)
            
            for match in memory_date_matches:
                memory_date_str = match.group(1)
                try:
                    # 統一日期格式
                    if '/' in memory_date_str:
                        memory_date = datetime.strptime(f"{current_year}/{memory_date_str}", '%Y/%m/%d')
                    else:
                        memory_date = datetime.strptime(memory_date_str, '%Y-%m-%d')
                    
                    # 檢查日期是否相同
                    if memory_date.date() == target_date.date():
                        print(f"[LongTermMemory] 找到符合日期的記憶: {memory_date_str}")
                        return True
                except ValueError:
                    continue
            
            return False
            
        except ValueError as e:
            print(f"[LongTermMemory] 日期解析錯誤: {str(e)}")
            return False

    def retrieve_similar_queries(self, query: str, k: int = 3):
        """檢索相關記錄並進行時間和相似度篩選"""
        try:
            # 增加搜尋範圍以提高找到相關日期的機會
            results = self.vector_store.similarity_search(query, k=k+2)
            if not results:
                return []
                
            # 過濾出相關且時效性符合的記憶
            relevant_results = [
                result for result in results 
                if self.is_query_similar(result.page_content, query) and 
                   self.is_date_relevant(result.page_content, query)
            ]
            
            if relevant_results:
                print(f"[LongTermMemory] 找到 {len(relevant_results)} 筆相關且符合時效的記憶")
                return relevant_results[:k]  # 只返回前k筆結果
            else:
                print("[LongTermMemory] 沒有找到相關記憶，需要重新檢索")
                return []
                
        except Exception as e:
            print(f"[LongTermMemory] 檢索錯誤: {str(e)}")
            return []
