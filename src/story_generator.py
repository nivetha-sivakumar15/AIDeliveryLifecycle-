import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-flash-latest")


def generate_user_stories(input_data):
    prompt = f"""
You are a product manager.

Input:
Transcript: {input_data['transcript']}
Process Flow: {input_data['process']}

IMPORTANT:
- Return ONLY valid JSON
- Do NOT include any explanation, text, or headings
- Do NOT wrap in markdown
- Ensure the JSON is properly formatted

Output format:
[
  {{
    "epic": "string",
    "user_story": "As a ..., I want ..., so that ...",
    "acceptance_criteria": [
      "Given ..., When ..., Then ..."
    ]
  }}
]
"""

    response = model.generate_content(prompt)

    return response.text 