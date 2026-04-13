import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-flash-latest")


def generate_e2e_tests(input_data):
    prompt = f"""
You are a QA lead.

--- INPUT START ---

Transcript:
{input_data['transcript']}

Process Flow:
{input_data['process']}

--- INPUT END ---

Generate END-TO-END test scenarios covering >70% business flow.

Include:
- Full user journey scenarios
- Happy path
- Failure scenarios
- Edge scenarios

Format:
- Scenario Name
- Steps
- Expected Outcome
"""

    response = model.generate_content(prompt)

    return response.text