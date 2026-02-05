from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import database, agent, extractor

app = FastAPI()

class Message(BaseModel):
    sender: str
    text: str

class ScamRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: Optional[List[dict]] = []

@app.post("/api/honey-pot")
async def handle_scam(request: ScamRequest, x_api_key: str = Header(None)):
    if x_api_key != "AIzaSyDLTVQK9_ntDfP6usOhuJZEHp6FKKv_dJ8": 
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # 1. Load Session
    session = database.get_session(request.sessionId)
    
    # 2. Extract Intelligence
    new_intel = extractor.extract_intelligence(request.message.text)
    for key in new_intel:
        session["intelligence"][key].extend(new_intel[key])

    # 3. Generate AI Response
    reply = agent.generate_reply(request.conversationHistory, request.message.text)
    
    # 4. Save & Return
    session["message_count"] += 1
    database.update_session(request.sessionId, session)
    
    return {"status": "success", "reply": reply}
