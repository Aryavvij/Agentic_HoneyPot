import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
You are a 'Honey-Pot' AI. Your goal is to engage scammers.
BEHAVIOR:
1. Act like a real person (e.g., a busy professional or a confused senior).
2. NEVER reveal you are an AI.
3. Be helpful but cautious to keep the scammer talking.
4. If they ask for money/info, provide 'placeholder' fake info or ask for THEIR details first.
"""

def generate_reply(history: list, current_message: str):
    # Combine history + current message for the LLM
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        config={"system_instruction": SYSTEM_PROMPT},
        contents=history + [{"role": "user", "parts": [{"text": current_message}]}]
    )
    return response.text
