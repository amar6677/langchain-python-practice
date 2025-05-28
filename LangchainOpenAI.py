#importing the required packages
import pandas as pd
#from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
import openai
from dotenv import load_dotenv
from warnings import filterwarnings
filterwarnings('ignore')


import os
# Environment setup
load_dotenv()
key=os.getenv("OpenAIKey")
print(f"printing the open AI key \n {key}")


#connecting witht he open AI

# Step 1: Setup LangChain LLM
os.environ["OPENAI_API_KEY"]=key
openai.api_key=key
# Send a prompt to the model
response = openai.ChatCompletion.create(
    model="gpt-4",  # Or "gpt-3.5-turbo" if you don't have GPT-4 access
    messages=[
        {"role": "user", "content": "Tell 5 things about India"}
    ],
    max_tokens=300,
    temperature=0.7
)
# Print the response
print(response)

# Step 2: Fetch Tickets 
#reading the incident CSV file
# Read the incident CSV
df = pd.read_csv("C:\LangChainPractice\langchain-python-practice\sample_incidents.csv")
#print(df.head())