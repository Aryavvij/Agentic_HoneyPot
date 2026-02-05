sessions = {}

def get_session(session_id: str):
    if session_id not in sessions:
        sessions[session_id] = {
            "intelligence": {"bankAccounts":[], "upilds":[], "phishingLinks":[], "phoneNumbers":[], "suspiciousKeywords":[]},
            "message_count": 0,
            "final_report_sent": False
        }
    return sessions[session_id]

def update_session(session_id: str, data: dict):
    sessions[session_id] = data
