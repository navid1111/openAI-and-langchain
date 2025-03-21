import os
from dotenv import load_dotenv
from langchain.vectorstores import Chroma # Updated import
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from redundant_filter_retrieval import RedundantFilterRetrievar

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

openai_model = "gpt-4o-mini"
llm = ChatOpenAI(temperature=0.7, model=openai_model)
embeddings = OpenAIEmbeddings()
db = Chroma(
    persist_directory='emb',
    embedding_function=embeddings
)
retriever = RedundantFilterRetrievar(
    embedding=embeddings,
    chroma=db
)

chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type='stuff'
)

# Using invoke() instead of run()
query = "what is an interesting fact about the Eiffel Tower?"
result = chain.invoke({"query": query})

print(result["result"])