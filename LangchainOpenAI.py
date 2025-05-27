#importing the required packages
import pandas as pd
#from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


import os
# Environment setup
load_dotenv()
key=os.getenv("OpenAIKey")
print(f"printing the open AI key \n {key}")
# Step 1: Fetch Tickets 
#reading the incident CSV file
# Read the incident CSV
df = pd.read_csv("C:\LangChainPractice\langchain-python-practice\sample_incidents.csv")
print(df.head())

#connecting witht he open AI

# Step 2: Setup LangChain LLM
os.environ["OPENAI_API_KEY"]=key
llm = ChatOpenAI(model="gpt-4")
prompt = ChatPromptTemplate.from_template(""" Provide me latest news on Narendra Modi

""")

chain = LLMChain(llm=llm, prompt=prompt)
print("printing the promt result \n")
print(chain)
