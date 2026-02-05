import re

def extract_intelligence(text: str):
    # Regex patterns for high-quality extraction
    intel = {
        "upilds": re.findall(r'[\w.-]+@[\w.-]+', text),
        "bankAccounts": re.findall(r'\b\d{9,18}\b', text),
        "phoneNumbers": re.findall(r'(?:\+91|0)?[6789]\d{9}', text),
        "phishingLinks": re.findall(r'https?://\S+', text),
        "suspiciousKeywords": []
    }
    
    # Detect Tactics for Agent Notes
    keywords = ["urgent", "kyc", "blocked", "lottery", "winner", "otp", "police"]
    intel["suspiciousKeywords"] = [w for w in keywords if w in text.lower()]
    
    return intel
