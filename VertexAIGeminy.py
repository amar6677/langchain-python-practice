import vertexai
from vertexai.preview.generative_models import GenerativeModel
import pandas as pd
import re

# Step 1: Init Vertex AI
vertexai.init(project="gen-lang-client-0601660044", location="us-central1")
model = GenerativeModel("gemini-pro")

# Step 2: Load CSV
df = pd.read_csv("incidents.csv")

# Step 3: Process each record
results = []

for _, row in df.iterrows():
    ticket = row["ticket_number"]
    desc = row["description"]

    prompt = f"""
You are an expert support analyst. Given the below incident description:
"{desc}"

Answer:
1. Is this an access issue related to the application 'DisputeApp'? (Yes/No)
2. If yes, extract the user's email ID from the text. Else reply NA.
Reply in format: Access Issue: [Yes/No], Email: [email/NA]
    """

    response = model.generate_content(prompt)
    reply = response.text.strip()

    # Extract structured result using regex
    access_match = re.search(r"Access Issue:\s*(Yes|No)", reply, re.IGNORECASE)
    email_match = re.search(r"Email:\s*([^\s]+)", reply, re.IGNORECASE)

    access_status = access_match.group(1) if access_match else "Unknown"
    email = email_match.group(1) if email_match and access_status.lower() == "yes" else "NA"

    results.append({
        "ticket_number": ticket,
        "access_issue": "Access Issue" if access_status.lower() == "yes" else "Non Access Issue",
        "email_id": email
    })

# Step 4: Save output to review CSV
review_df = pd.DataFrame(results)
review_df.to_csv("incident_review.csv", index=False)

print("Review file generated: incident_review.csv")
