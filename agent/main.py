from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate,MessagesPlaceholder
from langchain.agents import OpenAIFunctionsAgent,AgentExecutor
from dotenv import load_dotenv
from tools.sql import run_query_tool,list_tables,describe_table_tool
from langchain.schema import SystemMessage

import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") 

chat= ChatOpenAI()
tables=list_tables()  # Call the function
print("Available tables:", [table[0] for table in tables])  # Format the output nicely
prompt=ChatPromptTemplate(
    messages=[
        SystemMessage(content=(
            "You are an AI that has access to a SQLite database with available tables.\n"
            f"the database has of :{tables}"
            "Do not make any assumption on what tables exist or columns exist use 'describe table function"
                               
                               )),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

agent = OpenAIFunctionsAgent(
    llm=chat,
    prompt=prompt,
    tools=[run_query_tool,describe_table_tool]
)

agent_executor=AgentExecutor(
    agent=agent,
    verbose=True,
    tools=[run_query_tool,describe_table_tool]


)

agent_executor("what was  the total number of orders taken by users whose address is 877 Logan Views Apt. 413, East Chelseaview, MT 14625")