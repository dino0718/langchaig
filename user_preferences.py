from typing import Dict
import json
import os

class UserPreferences:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.preferences_path = f"./user_data/{user_id}/preferences.json"
        self.default_preferences = {
            "favorite_stocks": [],      # 關注的股票
            "news_sources": [],         # 偏好的新聞來源
            "risk_tolerance": "medium", # 風險承受度
            "notification_settings": {   # 通知設定
                "price_alert": True,
                "news_alert": True,
                "report_alert": True
            },
            "analysis_preferences": {    # 分析偏好
                "technical_indicators": ["RSI", "MA", "MACD"],
                "time_frames": ["daily", "weekly"]
            }
        }
        self.load_preferences()

    def load_preferences(self):
        if os.path.exists(self.preferences_path):
            with open(self.preferences_path, 'r') as f:
                self.preferences = json.load(f)
        else:
            self.preferences = self.default_preferences
            self.save_preferences()

    def save_preferences(self):
        os.makedirs(os.path.dirname(self.preferences_path), exist_ok=True)
        with open(self.preferences_path, 'w') as f:
            json.dump(self.preferences, f, indent=2)
