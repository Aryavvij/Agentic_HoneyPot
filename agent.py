import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Initialize Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_reply(history, new_message):
    system_instruction = """
    You are an undercover fraud investigator acting as a tech-illiterate victim.
    Goal: Keep the scammer talking to get their bank/UPI details.
    Rule: Never reveal you are an AI. Reply in the same language as the scammer.
    """

    # Properly format history for Gemini
    formatted_contents = []
    for msg in history:
        role = "user" if msg['sender'] == "scammer" else "model"
        formatted_contents.append(
            types.Content(role=role, parts=[types.Part.from_text(text=msg['text'])])
        )
    
    # Add the current scammer message
    formatted_contents.append(
        types.Content(role="user", parts=[types.Part.from_text(text=new_message)])
    )

    try:
        # THE FIX: We are switching the model string to the fully qualified name
        # Some SDK versions require the 'models/' prefix, others don't. 
        # 'gemini-1.5-flash' is the safest bet for the new 1.0.0+ SDK.
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7
            ),
            contents=formatted_contents
        )
        return response.text
    except Exception as e:
        # Check if the error is still a 404
        print(f"DEBUG_ERROR: {str(e)}")
        # If the AI fails, we stay in character
        return "Oh dear, my phone is acting up. What did you say about the bank?"
