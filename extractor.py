import re

def extract_intelligence(text: str):
    return {
        "upilds": re.findall(r'[\w.-]+@[\w.-]+', text),
        "bankAccounts": re.findall(r'\b\d{9,18}\b', text),
        "phoneNumbers": re.findall(r'\+?\d{10,12}', text),
        "phishingLinks": re.findall(r'https?://\S+', text)
    }
