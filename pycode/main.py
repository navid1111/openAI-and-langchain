import os
from langchain.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from getpass import getpass
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
from dotenv import load_dotenv
import argparse

# Load environment variables
load_dotenv()

# Set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--task", default="Sum two numbers 55 and 99")
parser.add_argument("--language", default="c++")
args = parser.parse_args()

# Get OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") or getpass(
    "Enter OpenAI API Key: "
)


# Initialize the OpenAI model
openai_model = "gpt-4o-mini"
llm = ChatOpenAI(temperature=0.7, model=openai_model)
creative_llm = ChatOpenAI(temperature=0.7, model=openai_model)

# Create system prompt
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are a AI chat assistant"
)

# Set up file history and conversation memory
file_history = FileChatMessageHistory("messages.json")
memory = ConversationBufferMemory(
    chat_memory=file_history,
    memory_key="messages", 
    return_messages=True
)

# Create message placeholders
memory_prompt = MessagesPlaceholder(variable_name="messages")

# Create user prompt
user_prompt = HumanMessagePromptTemplate.from_template(
    "{content}",
    input_variables=["content"]
)

# Create chat prompt template
prompt = ChatPromptTemplate.from_messages([
    system_prompt,
    memory_prompt,
    user_prompt
])

# Create chain
chain = prompt | llm

# Main chat loop
while True:
    try:
        content = input(">> ")
        if content.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
            
        # Get messages from memory
        memory_messages = memory.load_memory_variables({})["messages"]
        
        # Invoke the chain
        result = chain.invoke({
            "content": content,
            "messages": memory_messages
        })
        
        # Save the conversation to memory
        memory.save_context({"input": content}, {"output": result.content})
        
        # Print the result
        print(result.content)
    except KeyboardInterrupt:
        print("\nGoodbye!")
        break
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Continuing conversation...")