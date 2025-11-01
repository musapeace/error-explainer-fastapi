# app/analyzer.py
import os
from dotenv import load_dotenv
from google import genai 

load_dotenv()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY")) 

SYSTEM_PROMPT = """... (Your prompt remains the same) ..."""

async def get_error_explanation(error_message: str) -> str:
    """Sends the error to the LLM and returns the structured explanation."""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=[
                {"role": "user", "parts": [
                    {"text": SYSTEM_PROMPT},
                    {"text": error_message}
                ]}
            ]
        )
        return response.text
    except Exception as e:
        return f"Error: Could not process request. Details: {e}"