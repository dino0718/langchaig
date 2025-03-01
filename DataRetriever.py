import yfinance as yf
from langchain_community.tools import DuckDuckGoSearchRun  # 使用 DuckDuckGo 進行網路搜尋
from langchain_community.utilities import WikipediaAPIWrapper  # 使用 Wikipedia API 查詢資料
from BaseAgent import BaseAgent
from datetime import datetime
import re

class DataRetriever(BaseAgent):
    """從網路與 Wikipedia 檢索相關資訊"""

    def __init__(self):
        # 初始化網路搜尋工具與 Wikipedia 查詢工具
        self.search_tool = DuckDuckGoSearchRun()
        self.wiki_tool = WikipediaAPIWrapper()
        self.price_cache = {}
        self.price_cache_time = {}
        self.company_codes = {
            "南港": "2101",
            "台積電": "2330",
            "聯發科": "2454",
            # 可以繼續添加其他公司
        }

    def extract_stock_code(self, query: str) -> str:
        """從查詢中提取股票代碼"""
        # 直接檢查股票代碼
        stock_pattern = r'([0-9]{4,6})'
        stock_match = re.search(stock_pattern, query)
        if stock_match:
            return stock_match.group(1)
            
        # 檢查公司名稱
        for company, code in self.company_codes.items():
            if company in query:
                return code
                
        return None

    def get_live_stock_price(self, symbol: str) -> dict:
        """獲取即時股價並進行驗證"""
        try:
            stock = yf.Ticker(symbol)
            live_data = stock.history(period='1d')
            
            if live_data.empty:
                print(f"[DataRetriever] 警告: {symbol} 無法獲取即時數據")
                return None
                
            current_price = live_data['Close'].iloc[-1]
            
            # 驗證價格是否在合理範圍內
            if current_price <= 0 or current_price > 1000000:
                print(f"[DataRetriever] 警告: {symbol} 價格異常 ({current_price})")
                return None
                
            price_info = {
                "symbol": symbol,
                "current_price": current_price,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "change": live_data['Close'].iloc[-1] - live_data['Open'].iloc[0],
                "volume": live_data['Volume'].iloc[-1],
                "verified": True
            }
            
            # 更新快取
            self.price_cache[symbol] = price_info
            self.price_cache_time[symbol] = datetime.now()
            
            return price_info
        except Exception as e:
            print(f"[DataRetriever] 股價獲取錯誤 ({symbol}): {str(e)}")
            return None

    def get_financial_data(self, symbol: str) -> dict:
        """獲取公司財務資訊"""
        try:
            stock = yf.Ticker(symbol)
            
            # 獲取基本財務資訊
            info = stock.info
            financials = stock.financials
            
            if financials.empty:
                return None
                
            latest_quarter = financials.columns[0]
            
            financial_data = {
                "symbol": symbol,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "revenue": financials.loc['Total Revenue', latest_quarter] if 'Total Revenue' in financials.index else None,
                "net_income": financials.loc['Net Income', latest_quarter] if 'Net Income' in financials.index else None,
                "eps": info.get('trailingEPS'),
                "pe_ratio": info.get('trailingPE'),
                "market_cap": info.get('marketCap'),
                "report_date": latest_quarter.strftime("%Y-%m-%d") if isinstance(latest_quarter, datetime) else str(latest_quarter)
            }
            
            return financial_data
            
        except Exception as e:
            print(f"[DataRetriever] 財務資料獲取錯誤 ({symbol}): {str(e)}")
            return None

    def invoke(self, input_data: dict) -> dict:
        """根據傳入的查詢關鍵字檢索外部資料"""
        query = input_data["query"]
        print(f"[DataRetriever] 檢索中: {query}")
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            # 提取股票代碼
            stock_code = self.extract_stock_code(query)
            stock_info = {}
            financial_data = {}
            
            if stock_code:
                symbol = f"{stock_code}.TW"
                
                # 獲取股價資訊
                if "股價" in query:
                    stock_info = self.get_live_stock_price(symbol)
                    
                # 獲取財報資訊
                if "財報" in query:
                    financial_data = self.get_financial_data(symbol)

            # 整理回應資訊
            result_text = f"\n檢索時間: {current_time}\n"
            
            if stock_info:
                result_text += f"\n股價資訊：\n"
                result_text += f"現價: NT${stock_info['current_price']:.2f}\n"
                result_text += f"漲跌: {stock_info['change']:+.2f}\n"
                result_text += f"成交量: {stock_info['volume']:,}\n"
                
            if financial_data:
                result_text += f"\n最新財報資訊 (日期: {financial_data['report_date']})：\n"
                result_text += f"營收: {financial_data['revenue']:,.0f}\n" if financial_data['revenue'] else ""
                result_text += f"淨利: {financial_data['net_income']:,.0f}\n" if financial_data['net_income'] else ""
                result_text += f"EPS: {financial_data['eps']:.2f}\n" if financial_data['eps'] else ""
                result_text += f"本益比: {financial_data['pe_ratio']:.2f}\n" if financial_data['pe_ratio'] else ""

            # 添加一般搜索結果
            search_results = self.search_tool.run(query)
            wiki_results = self.wiki_tool.run(query)
            
            result_text += f"\n搜尋結果:\n{search_results}\n"
            result_text += f"\n維基百科資料:\n{wiki_results}"

            return {
                "query": query,
                "data": result_text,
                "stock_info": stock_info,
                "financial_data": financial_data,
                "timestamp": current_time,
                "status": "success"
            }
            
        except Exception as e:
            print(f"[DataRetriever] 錯誤: {str(e)}")
            return {
                "query": query,
                "data": "抱歉，檢索過程中發生錯誤。",
                "status": "error"
            }
