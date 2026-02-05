import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Client setup
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_reply(history, new_message):
    # This persona is key for 'Engagement Depth' scoring [cite: 208, 263]
    system_instruction = """
    You are an undercover fraud investigator acting as a tech-illiterate victim.
    Goal: Keep the scammer talking to get their bank/UPI details.
    Rule: Never reveal you are an AI. Reply in the same language as the scammer.
    """

    formatted_contents = []
    for msg in history:
        # Map roles correctly: 'user' for scammer, 'model' for your agent [cite: 180]
        role = "user" if msg['sender'] == "scammer" else "model"
        formatted_contents.append(
            types.Content(role=role, parts=[types.Part.from_text(text=msg['text'])])
        )
    
    formatted_contents.append(
        types.Content(role="user", parts=[types.Part.from_text(text=new_message)])
    )

    try:
        # THE FIX: Use ONLY the string 'gemini-1.5-flash'
        # The new SDK adds the 'models/' prefix automatically. 
        # Adding it manually often causes the 404 you see.
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
        print(f"GEMINI_ERROR: {str(e)}")
        return "Oh dear, my phone is acting up. What did you say about the bank?"
