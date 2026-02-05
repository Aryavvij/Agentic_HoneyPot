import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_reply(history, new_message):
    # System Instruction to ensure the AI behaves like a human victim
    system_instruction = """
    You are a professional AI Honey-Pot. Your goal:
    1. Adopt a persona (e.g., an elderly person or a busy student).
    2. Keep the scammer engaged as long as possible.
    3. Respond in the SAME LANGUAGE as the scammer (Hindi, Tamil, English, etc.).
    4. Act slightly confused about technology to encourage them to give clear payment IDs or links.
    5. NEVER admit you are an AI.
    """

    # Format history for Gemini
    contents = []
    for msg in history:
        role = "user" if msg['sender'] == "scammer" else "model"
        contents.append({"role": role, "parts": [{"text": msg['text']}]})
    
    # Add the current message
    contents.append({"role": "user", "parts": [{"text": new_message}]})

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        config=types.GenerateContentConfig(system_instruction=system_instruction),
        contents=contents
    )
    return response.text
