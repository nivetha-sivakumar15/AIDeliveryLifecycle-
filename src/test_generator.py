import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-flash-latest")


def generate_unit_tests(input_data):
    prompt = f"""
You are a senior QA engineer.

--- INPUT START ---

Transcript:
{input_data['transcript']}

Process Flow:
{input_data['process']}

--- INPUT END ---

Generate UNIT TEST scenarios with the goal of achieving >90% test coverage.

Include:
- Positive test cases
- Negative test cases
- Edge cases
- Boundary conditions

Format:
- Module/Component Name
- Test Case Description
- Input
- Expected Output
"""

    response = model.generate_content(prompt)

    return response.text 