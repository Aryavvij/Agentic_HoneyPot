# Simple in-memory session storage
# In production, you would use Redis or PostgreSQL
sessions = {}

def get_session(session_id: str):
    return sessions.get(session_id, {
        "history": [],
        "intelligence": {
            "bankAccounts": [],
            "upilds": [],
            "phishingLinks": [],
            "phoneNumbers": [],
            "suspiciousKeywords": []
        },
        "message_count": 0
    })

def update_session(session_id: str, data: dict):
    sessions[session_id] = data
