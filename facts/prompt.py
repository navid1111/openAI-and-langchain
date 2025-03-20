from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
load_dotenv()
embeddings=OpenAIEmbeddings()
db=Chroma(
    persist_directory='emb',
    embedding_function=embeddings

)
