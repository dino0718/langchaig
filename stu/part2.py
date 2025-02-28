from os import getenv
from dotenv import load_dotenv
load_dotenv()
openai_key = getenv("OPENAI_API_KEY")

# 準備一份文件內容（這裡我們用一小段文字模擬）
document_content = """
LangChain 是一個用於構建大型語言模型應用的框架。它提供了 Chains、Agents、Memory 等組件，
方便開發者串聯 LLM 與外部工具或資料。LangChain 支援與多種向量資料庫整合，如 FAISS、Chroma、Pinecone 等。
"""
# 將內容封裝為 LangChain 的 Document 對象
from langchain.docstore.document import Document
docs = [Document(page_content=document_content, metadata={"source": "intro"})]

# 將文件切分為較小的 chunk（段落），以利向量化與檢索
from langchain.text_splitter import CharacterTextSplitter
text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
split_docs = text_splitter.split_documents(docs)

# 建立文本向量嵌入（使用 OpenAI Embeddings，需要 OpenAI API 金鑰）
from langchain_community.embeddings import OpenAIEmbeddings
embedding_model = OpenAIEmbeddings()

# 建立向量存儲（使用 FAISS 向量數據庫，在記憶體中構建索引）
from langchain_community.vectorstores import FAISS
vector_store = FAISS.from_documents(split_docs, embedding_model)

# 構建檢索問答鏈（RetrievalQA），把向量庫包裝為檢索器提供給鏈
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(temperature=0),
                                      chain_type="stuff",
                                      retriever=vector_store.as_retriever())

# 提出問題並取得答案
query = "LangChain 提供了哪些核心組件？"
result = qa_chain.run(query)
print("問題：", query)
print("回答：", result)
