from dotenv import load_dotenv  # 新增：引入 dotenv
load_dotenv()  # 新增：載入 .env 之環境變數
from langchain_openai import OpenAI  # 修改：由 langchain_openai 匯入 OpenAI
from langchain.prompts import PromptTemplate
from os import environ

# 建立提示模板，{question} 將被使用者問題內容替換
template = "問：{question}\n答："
prompt = PromptTemplate(template=template, input_variables=["question"])

# 初始化 OpenAI LLM (temperature=0 使回覆更穩定，需先設定 OPENAI_API_KEY 環境變數)
llm = OpenAI(temperature=0)

# 可選：示範如何取得環境變數
api_key = environ.get("OPENAI_API_KEY")
# print("使用的 OPENAI_API_KEY:", api_key)

# 使用新版管道風格，連接提示模板與 LLM，不再使用 LLMChain
chain = prompt | llm

# 提供一個問題給鏈，獲取模型的回答
user_question = "請用一句話形容共產黨"
# 修改：改用 chain.invoke 呼叫連接的鏈
answer = chain.invoke({"question": user_question})
print(answer)
