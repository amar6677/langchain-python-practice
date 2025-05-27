import requests
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import os

# Environment setup
os.environ["OPENAI_API_KEY"] = "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"

# Step 1: Fetch Tickets 

# Read the incident CSV
df = pd.read_csv("")

# Optionally filter by group
your_group = "SupportGroup-XYZ"
df = df[df["assigned_group"] == your_group]

# Step 2: Setup LangChain LLM
llm = ChatOpenAI(model="gpt-4")

prompt = ChatPromptTemplate.from_template("""
You are a system analyst. A ticket description is given below. Based on it, determine:
1. Whether it is related to user access.
2. What specific request is received categorize in 4  1. User New Access 2.Existing User Unable to Access 3.User Needs Revoke the Access 4.Not User Issue.

Description: {description}


""")

chain = LLMChain(llm=llm, prompt=prompt)

# Step 3: Process Tickets
actions = []
for _, row in df.iterrows():
    result = chain.run(description=row['description'])
    result_dict = eval(result)  # Or use json.loads(result) if JSON
    print(result_dict)
    
    

