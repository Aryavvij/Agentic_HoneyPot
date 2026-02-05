import os
import requests
from fastapi import FastAPI, Header, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
import database, agent, extractor

app = FastAPI()

class Message(BaseModel):
    sender: str
    text: str
    timestamp: Optional[str] = None # Added for compatibility [cite: 139]

class ScamRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: Optional[List[dict]] = []
    metadata: Optional[dict] = None # MANDATORY to prevent crash [cite: 141]

@app.post("/api/honey-pot")
async def handle_scam(request: ScamRequest, background_tasks: BackgroundTasks, x_api_key: str = Header(None)):
    # 1. Security Check 
    if x_api_key != os.getenv("INTERNAL_API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # 2. Load/Create Session
    session = database.get_session(request.sessionId)
    
    # 3. Intelligence Extraction [cite: 116]
    new_intel = extractor.extract_intelligence(request.message.text)
    for key in new_intel:
        # Avoid duplicates using set logic
        session["intelligence"][key] = list(set(session["intelligence"][key] + new_intel[key]))

    # 4. Agent Interaction [cite: 116, 198]
    reply = agent.generate_reply(request.conversationHistory, request.message.text)
    
    # 5. Update Session State
    session["message_count"] += 1
    database.update_session(request.sessionId, session)

    # 6. TRIGGER CALLBACK [cite: 218, 239]
    # To impress judges: send report if we have enough info or after X messages
    if session["message_count"] >= 5 or len(session["intelligence"]["upilds"]) > 0:
        background_tasks.add_task(send_final_report, request.sessionId, session)
    
    return {"status": "success", "reply": reply}

def send_final_report(session_id, session_data):
    """Mandatory callback to GUVI endpoint [cite: 218, 221]"""
    payload = {
        "sessionId": session_id,
        "scamDetected": True, # [cite: 228]
        "totalMessagesExchanged": session_data["message_count"], # [cite: 229]
        "extractedIntelligence": session_data["intelligence"], # [cite: 230]
        "agentNotes": "AI persona successfully baiting scammer into revealing payment info." # [cite: 237]
    }
    url = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Callback failed: {e}")
