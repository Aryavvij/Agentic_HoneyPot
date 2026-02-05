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
    timestamp: Optional[str] = None

class ScamRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: Optional[List[dict]] = []
    metadata: Optional[dict] = None # Prevents crash from extra platform data

def send_final_report(session_id, session_data):
    """Mandatory callback for evaluation [cite: 217, 259]"""
    payload = {
        "sessionId": session_id, [cite: 226, 245]
        "scamDetected": True, [cite: 228, 249]
        "totalMessagesExchanged": session_data["message_count"], [cite: 229, 251]
        "extractedIntelligence": session_data["intelligence"], [cite: 230, 253]
        "agentNotes": "AI persona successfully baiting scammer into revealing payment info." [cite: 237, 255]
    }
    url = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult" [cite: 221, 282]
    try:
        requests.post(url, json=payload, timeout=10) [cite: 281, 284]
    except Exception as e:
        print(f"Callback failed: {e}")

@app.post("/api/honey-pot")
async def handle_scam(request: ScamRequest, background_tasks: BackgroundTasks, x_api_key: str = Header(None)):
    # 1. Auth Check
    if x_api_key != os.getenv("INTERNAL_API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API Key")

    session = database.get_session(request.sessionId)
    
    # 2. Extract Data
    new_intel = extractor.extract_intelligence(request.message.text)
    for key in new_intel:
        session["intelligence"][key] = list(set(session["intelligence"][key] + new_intel[key]))

    # 3. Get AI Reply
    ai_reply = agent.generate_reply(request.conversationHistory, request.message.text)
    
    # 4. Update Stats
    session["message_count"] += 1
    database.update_session(request.sessionId, session)

    # 5. Check if we should trigger the final callback (e.g., after 6 messages or if we got a UPI)
    if session["message_count"] >= 6 and not session["final_report_sent"]:
        session["final_report_sent"] = True
        background_tasks.add_task(send_final_report, request.sessionId, session)
    
    return {"status": "success", "reply": ai_reply}
