import pandas as pd
import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from dotenv import load_dotenv
load_dotenv()  # Loads variables from .env file
from warnings import filterwarnings
filterwarnings('ignore')

import os
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# === CONFIGURATION ===
INPUT_FILE = "C:\LangChainPractice\langchain-python-practice\sample.csv"
REVIEW_FILE = "review_output.csv"
FEEDBACK_FILE = "few_shot_feedback_gemini.json"
COLUMN_TO_CHECK = "description"
KEYWORDS = [
    "login is not working", "cant access", "not able to access",
    "Getting error while logging into the", "The account abc@outlook.com cant access",
    "User def@gmail.com cant access system in IMC",
    "The Merchant could not access SIMS email - xyz@gmail.com",
    "The Merchant could not login to SIMS, email - xyz@gmail.com"
]

# Set your Gemini API key
#GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # or hardcode: "your-api-key"



# === BASE FEW-SHOT EXAMPLES ===
base_examples = [
    {
        "text": "The merchant was trying to access SIMS but getting unable to fetch authorization error.",
        "keywords": "authorization error, access, unable to login",
        "label": "matching"
    },
    {
        "text": "The merch is getting system error while accessing system",
        "keywords": "authorization error, access, unable to login",
        "label": "matching"
    }
]

# === FUNCTIONS ===
def load_feedback_examples():
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as f:
            return json.load(f)
    return []

def save_feedback_examples(examples):
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(examples, f, indent=2)

def prepare_prompt(examples):
    example_prompt = PromptTemplate(
        input_variables=["text", "keywords", "label"],
        template="Text: {text}\nKeywords: {keywords}\nCategory: {label}"
    )
    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix="You are a text classifier. Categorize the text as 'matching' or 'not_matching' based on relevance to keywords.\nExamples:\n",
        suffix="Text: {input}\nKeywords: {keywords}\nCategory:",
        input_variables=["input", "keywords"]
    )
    return few_shot_prompt

def run_classification(df, llm_chain):
    def classify(text):
        result = llm_chain.run({"input": text, "keywords": ", ".join(KEYWORDS)})
        result = result.strip().lower()
        return result if result in ["matching", "not_matching"] else "not_matching"

    df["category"] = df[COLUMN_TO_CHECK].apply(classify)
    df["feedback"] = ""  # Empty feedback column for reviewers
    df.to_csv(REVIEW_FILE, index=False)
    print(f"Classification complete. Review file saved as '{REVIEW_FILE}'")

def apply_feedback():
    if not os.path.exists(REVIEW_FILE):
        print("No review file found.")
        return

    df = pd.read_csv(REVIEW_FILE)
    corrected = df[df["feedback"].isin(["matching", "not_matching"])]
    if corrected.empty:
        print("No feedback provided.")
        return

    new_examples = [
        {
            "text": row[COLUMN_TO_CHECK],
            "keywords": ", ".join(KEYWORDS),
            "label": row["feedback"]
        }
        for _, row in corrected.iterrows()
    ]
    old = load_feedback_examples()
    updated = old + new_examples
    save_feedback_examples(updated)
    print(f"{len(new_examples)} feedback examples added. Total now: {len(updated)}.")

# === MAIN FLOW ===
def main():
    df = pd.read_csv(INPUT_FILE)
    print(df.head)

    # Load few-shot examples
    feedback_examples = load_feedback_examples()
    all_examples = base_examples + feedback_examples

    # Gemini LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest",
        temperature=0,
        google_api_key=GOOGLE_API_KEY,
        convert_system_message_to_human=True  # Required for proper prompt formatting
    )

    prompt = prepare_prompt(all_examples)
    chain = LLMChain(llm=llm, prompt=prompt)

    # Classify
    run_classification(df, chain)

    print("\n✅ Please review 'review_output.csv', add corrections under the 'feedback' column, then rerun the script with '--update' flag to train with feedback.")

if __name__ == "__main__":
    import sys
    if "--update" in sys.argv:
        apply_feedback()
    else:
        main()