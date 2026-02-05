import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# This system prompt defines the 'Intelligence Extractor' persona
SYSTEM_PROMPT = """
You are an Agentic Honey-Pot. Your goal is to autonomously engage scammers.
1. Maintain a believable human persona (e.g., tech-illiterate senior).
2. Do not reveal you know it's a scam[cite: 199].
3. Persuade the scammer to give you their UPI ID, bank details, or links[cite: 112].
4. Be persistent and keep the conversation going as long as possible[cite: 198].
"""

def generate_agent_response(history, new_message):
    # Convert conversationHistory into the format Gemini expects
    formatted_history = []
    for msg in history:
        role = "user" if msg['sender'] == "scammer" else "model"
        formatted_history.append({"role": role, "parts": [{"text": msg['text']}]})

    chat = client.chats.create(
        model="gemini-1.5-flash",
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
    )
    
    # Send the history + new message
    response = chat.send_message(new_message)
    return response.text
