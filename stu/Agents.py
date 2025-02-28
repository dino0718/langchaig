import os
from dotenv import load_dotenv
load_dotenv()
openai_key =os.getenv("OPENAI_API_KEY")
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain_openai import OpenAI
# 初始化 LLM
llm = OpenAI(temperature=0)
# 載入內建的工具：llm-math (數學計算工具)
tools = load_tools(["llm-math"], llm=llm)

# 建立一個零次提示（Zero-shot）Reactive Agent，允許使用計算工具
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# 使用 Agent 來回答問題
query = "請問美國第40任總統出生年份的平方是多少？"
result = agent.invoke(query)
print("Agent 最終答案：", result)
