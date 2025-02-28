import os
from dotenv import load_dotenv
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
product_faq = """
產平名稱：水管
功能：運送水
保固：兩年
支援服務：無
"""
faq_prompt_template = PromptTemplate(
    input_variables=["history", "input"],
    template=f"以下是產品常見的問答資料：{product_faq}\n你是一個客服機器人，根據上述資料回答用戶問題。\n{{history}}\n用戶：{{input}}\n助理："
)
llm = OpenAI(temperature=0)
memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(llm=llm, memory=memory, prompt=faq_prompt_template)

# 開始對話
user_q1 = "這個神奇小工具有哪些主要功能？"
answer1 = conversation.predict(input=user_q1)
print("助理：", answer1)

user_q2 = "保固多久？"
answer2 = conversation.predict(input=user_q2)
print("助理：", answer2)

user_q3 = "很好，那清潔呢？"
answer3 = conversation.predict(input=user_q3)
print("助理：", answer3)