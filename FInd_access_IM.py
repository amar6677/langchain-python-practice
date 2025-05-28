#importing the required packages
import pandas as pd
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
#Below fucntion to get the result from the open AI if the ticket is related to access or not
def getIMDetail(IMDesc):
    #connecting witht he open AI
    #  Step 1: Setup LangChain LLM
    os.environ["OPENAI_API_KEY"]=key
    openai.api_key=key
    Descripion=IMDesc
    # Send a prompt to the model
    response = openai.ChatCompletion.create(
    model="gpt-4",  # Or "gpt-3.5-turbo" if you don't have GPT-4 access
    messages=[
        {"role": "user", "content": f"Read the below description and let us know its come under which category like  1. New access 2. Unable to 3. Remove Access 4. Not Related to access \n Description: {Descripion} "}
    ],
    max_tokens=300,
    temperature=0.7
)
# Print the response
    print( response['choices'][0]['message']['content'].strip())

#End funcion

# Step 2: Fetch Tickets 
#reading the incident CSV file
# Read the incident CSV
df = pd.read_csv("C:\LangChainPractice\langchain-python-practice\sample_incidents.csv")
Des="""Request to grant read access to schema sales_db for user john.doe,SupportGroup-XYZ"""
getIMDetail(Des)
for i in df['ticket_id']:
    des=df[df['ticket_id']==1]
    des=des['description']
    print(f"Category for: {i}")
    getIMDetail(des)
    print("-------------------------------------------------------")
    
#print(df.head())