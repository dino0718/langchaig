import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from textblob import TextBlob
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from BaseAgent import BaseAgent

class MarketSentimentAnalyzer(BaseAgent):
    """分析股票市場情緒並提供即時分析"""

    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-4o")
        self.template = PromptTemplate.from_template(
            """請根據以下資訊分析 {symbol} 的市場情緒：

新聞分析：
{news_summary}

技術指標：
{technical_indicators}

請提供以下分析：
1. 市場情緒評估（正面/負面/中性）
2. 主要影響因素
3. 短期趨勢預測（1-2週）
4. 風險提示

請以結構化方式呈現分析結果。
"""
        )

    def set_indicators(self, indicators: list):
        """設置技術指標"""
        self.technical_indicators = indicators

    def set_timeframes(self, timeframes: list):
        """設置時間週期"""
        self.timeframes = timeframes

    def fetch_stock_data(self, symbol: str):
        """獲取股票數據"""
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="1mo")
            news = stock.news[:10]
            return hist, news
        except Exception as e:
            print(f"[MarketSentimentAnalyzer] 股票數據獲取錯誤: {str(e)}")
            return None, []

    def analyze_technical_indicators(self, hist: pd.DataFrame) -> dict:
        """計算技術指標"""
        if (hist.empty):
            return {}
            
        try:
            # 計算基本技術指標
            latest_price = hist['Close'][-1]
            ma5 = hist['Close'].rolling(window=5).mean()[-1]
            ma20 = hist['Close'].rolling(window=20).mean()[-1]
            rsi = self.calculate_rsi(hist['Close'])
            
            return {
                "latest_price": round(latest_price, 2),
                "ma5": round(ma5, 2),
                "ma20": round(ma20, 2),
                "rsi": round(rsi, 2),
                "trend": "上升" if ma5 > ma20 else "下降"
            }
        except Exception as e:
            print(f"[MarketSentimentAnalyzer] 技術分析錯誤: {str(e)}")
            return {}

    def calculate_rsi(self, prices: pd.Series, periods: int = 14) -> float:
        """計算 RSI 指標"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs.iloc[-1]))

    def analyze_news_sentiment(self, news: list) -> list:
        """分析新聞情緒"""
        news_analysis = []
        for article in news:
            title = article.get('title', '')
            sentiment = TextBlob(title).sentiment.polarity
            label = "📈 正面" if sentiment > 0.1 else "📉 負面" if sentiment < -0.1 else "➖ 中性"
            news_analysis.append(f"{label} | {title}")
        return news_analysis

    def invoke(self, input_data: dict) -> dict:
        """執行市場情緒分析"""
        query = input_data.get("query", "")
        symbol = input_data.get("symbol", "2330.TW")  # 預設台積電
        
        print(f"[MarketSentimentAnalyzer] 分析 {symbol} 的市場情緒")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 獲取數據
        hist, news = self.fetch_stock_data(symbol)
        if hist is None:
            return {
                "status": "error",
                "message": "無法獲取股票數據",
                "timestamp": current_time
            }

        # 分析技術指標
        indicators = self.analyze_technical_indicators(hist)
        
        # 分析新聞情緒
        news_summary = self.analyze_news_sentiment(news)

        # 生成綜合分析
        prompt = self.template.format(
            symbol=symbol,
            news_summary="\n".join(news_summary),
            technical_indicators=indicators
        )
        
        analysis = self.llm.invoke(prompt)

        return {
            "query": query,
            "symbol": symbol,
            "timestamp": current_time,
            "technical_data": indicators,
            "news_sentiment": news_summary,
            "analysis": analysis.content,
            "status": "success"
        }
