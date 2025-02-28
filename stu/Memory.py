from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
openai_key =os.getenv("OPENAI_API_KEY")

# 初始化一個 OpenAI LLM
llm = OpenAI(temperature=0)
# 準備對話記憶體（會將對話記錄緩存起來）
memory = ConversationBufferMemory()

# 建立帶記憶的對話鏈
conversation = ConversationChain(llm=llm, memory=memory)

# 模擬兩輪對話
response1 = conversation.invoke(input="嗨，LangChain 是什麼？")
print("助理：", response1)

response2 = conversation.invoke(input="它有哪些核心組件？")
print("助理：", response2)
