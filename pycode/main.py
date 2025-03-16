import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from getpass import getpass
from langchain_core.output_parsers import JsonOutputParser
import argparse
parser=argparse.ArgumentParser()
parser.add_argument("--task",default="Sum two numbers 55 and 99")
parser.add_argument("--language",default="c++")
args=parser.parse_args()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") or getpass(
    "Enter OpenAI API Key: "
)

openai_model = "gpt-4o-mini"
llm=ChatOpenAI(temperature=0,model=openai_model)
creative_llm=ChatOpenAI(temperature=0.9,model=openai_model)
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are a AI chat assistant that helps generate article titles",
    
)
user_prompt=HumanMessagePromptTemplate.from_template(
        """ Write a very short {language} function that will {task}""",
    input_variables=["language","task"]

)

user_prompt_test=HumanMessagePromptTemplate.from_template(
        """ Write a test for the following language {language} code:\n{code}""",
    input_variables=["language","code"]

)
prompt=ChatPromptTemplate.from_messages(
[ system_prompt,
 user_prompt]
)
prompt_test=ChatPromptTemplate.from_messages(
[ system_prompt,
 user_prompt_test]
)
chain= prompt | llm
test_chain= prompt_test |llm
result=chain.invoke({"language":args.language,"task":args.task}).content
test=test_chain.invoke({"language":args.language,"code":result})

print(test.content)
