import os
from langchain_openai import ChatOpenAI
from getpass import getpass

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") or getpass(
    "Enter OpenAI API Key: "
)

openai_model = "gpt-4o-mini"
llm=ChatOpenAI(temperature=0,model=openai_model)
creative_llm=ChatOpenAI(temperature=0.9,model=openai_model)


result=creative_llm.invoke("write a very short poem").content

print(result)
