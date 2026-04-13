import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-flash-latest")


def generate_tdd(input_data):
    prompt = f"""
You are a senior software architect.

You MUST use the following input to generate the document.

--- INPUT START ---

Transcript:
{input_data['transcript']}

Process Flow:
{input_data['process']}

--- INPUT END ---

IMPORTANT:
- Do NOT ask for more input
- Do NOT generate sample or generic examples
- Use ONLY the provided input
- Be specific to the given context

Generate a Technical Design Document (TDD) with:

1. System Overview
2. Architecture Design
3. Component Breakdown
4. Data Flow
5. API Design (if applicable)
6. Database Design (if applicable)
7. Error Handling & Edge Cases
8. Assumptions

Output must be detailed and directly based on the input.
"""

    response = model.generate_content(prompt)

    return response.text 