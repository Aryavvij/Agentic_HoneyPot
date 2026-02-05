import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Ensure the API key is being pulled correctly
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_reply(history, new_message):
    system_instruction = """
    You are a professional AI Honey-Pot. 
    1. Act like a believable human victim.
    2. Respond in the SAME LANGUAGE as the scammer.
    3. Keep them engaged to extract UPI IDs and links.
    """

    # Format history for the new SDK
    contents = []
    for msg in history:
        # Map 'agent' to 'model' for Gemini
        role = "user" if msg['sender'] == "scammer" else "model"
        contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg['text'])]))
    
    # Add the current message
    contents.append(types.Content(role="user", parts=[types.Part.from_text(text=new_message)]))

    try:
        # Use the simple model name string
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            config=types.GenerateContentConfig(system_instruction=system_instruction),
            contents=contents
        )
        return response.text
    except Exception as e:
        print(f"AI Generation Error: {e}")
        return "I'm a bit confused, can you explain that again?"
