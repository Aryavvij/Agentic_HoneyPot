import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Initialize Client - ensure no extra spaces in your Render API Key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_reply(history, new_message):
    system_instruction = """
    You are an undercover fraud investigator acting as a tech-illiterate victim.
    Goal: Keep the scammer talking to get their bank/UPI details.
    Rule: Never reveal you are an AI. Reply in the same language as the scammer.
    """

    # Properly format history for Gemini 1.5
    formatted_contents = []
    for msg in history:
        # Map 'agent' to 'model' for Gemini
        role = "user" if msg['sender'] == "scammer" else "model"
        formatted_contents.append(
            types.Content(role=role, parts=[types.Part.from_text(text=msg['text'])])
        )
    
    # Add the current scammer message
    formatted_contents.append(
        types.Content(role="user", parts=[types.Part.from_text(text=new_message)])
    )

    try:
        # THE FIX: Use 'gemini-1.5-flash' - the SDK handles the rest.
        # If this fails, the issue is almost certainly the API Key itself.
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
        # This will show up in your Render Logs
        print(f"GEMINI_ERROR: {str(e)}")
        return "Oh dear, my phone is acting up. What did you say about the bank?"
