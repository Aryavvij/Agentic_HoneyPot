import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Client setup
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_reply(history, new_message):
    system_instruction = """
    You are an undercover fraud investigator acting as a tech-illiterate victim.
    Goal: Keep the scammer talking to get their bank/UPI details.
    Rule: Never reveal you are an AI. Reply in the same language as the scammer.
    """

    # Formatting history correctly for the SDK
    formatted_contents = []
    for msg in history:
        role = "user" if msg['sender'] == "scammer" else "model"
        formatted_contents.append(
            types.Content(role=role, parts=[types.Part.from_text(text=msg['text'])])
        )
    
    # Add the latest scammer message
    formatted_contents.append(
        types.Content(role="user", parts=[types.Part.from_text(text=new_message)])
    )

    try:
        # CHANGED: Use 'gemini-1.5-flash' directly without prefixes
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7 # Adds a bit of 'human' randomness
            ),
            contents=formatted_contents
        )
        return response.text
    except Exception as e:
        # If it fails, print the error to Render logs so you can see why
        print(f"DEBUG AI ERROR: {str(e)}")
        return "Oh dear, my phone is acting up. What did you say about the bank?"
