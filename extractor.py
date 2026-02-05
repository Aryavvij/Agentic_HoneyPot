import re

def extract_scam_intel(text: str):
    """
    This function uses Regular Expressions (Regex) to mine 
    the scammer's data from their messages.
    """
    return {
        # Finds UPI IDs like scammer@okicici
        "upilds": re.findall(r'[\w.-]+@[\w.-]+', text),
        
        # Finds 9-18 digit bank account numbers
        "bankAccounts": re.findall(r'\b\d{9,18}\b', text),
        
        # Finds Phone Numbers (Indian format)
        "phoneNumbers": re.findall(r'(?:\+91|0)?[6789]\d{9}', text),
        
        # Finds Phishing Links
        "phishingLinks": re.findall(r'https?://\S+', text),
        
        # Common scam triggers for the 'agentNotes'
        "suspiciousKeywords": [word for word in ["urgent", "blocked", "verify", "kyc", "winner"] if word in text.lower()]
    }
