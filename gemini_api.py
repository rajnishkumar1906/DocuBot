import os
from dotenv import load_dotenv
from google import genai

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=API_KEY)

def ask_gemini(prompt: str, model: str = "gemini-2.5-flash") -> str:
    """
    Send a prompt to Gemini API and return the generated text.
    """
    try:
        response = client.generate_content(
            model=model,
            prompt=prompt
        )
        return response.text
    except Exception as e:
        return f"Error: {e}"
