from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

# Make sure your OpenAI API key is properly set in your .env file
# OPENAI_API_KEY=your_api_key_here

embeddings = OpenAIEmbeddings()

text_splitter = CharacterTextSplitter(
    separator='\n',
    chunk_size=200,
    chunk_overlap=0,
)

loader = TextLoader('facts.txt')
docs = loader.load_and_split(
    text_splitter=text_splitter
)

db = Chroma.from_documents(
    docs,
    embedding=embeddings,
    persist_directory='emb'
)

results = db.similarity_search_with_score("we usualy walk a lot ",k=1)

for result in results:
    print("\n")
    print(result[1])
    print(result[0].page_content)