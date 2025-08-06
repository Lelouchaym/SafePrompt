import re
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def detect_with_regex(prompt):
    patterns = {
        "EMAIL": r"\b[\w\.-]+@[\w\.-]+\.\w+\b",
        "CIN": r"\b[A-Z]{1,2}\d{6}\b",
        "PHONE": r"\b(0[67]\d{8})\b",
    }
    found = []
    for label, pattern in patterns.items():
        if re.search(pattern, prompt):
            found.append(label)
    return found

def detect_with_llm(prompt):
    instruction = f"""Tu es un détecteur de données sensibles. 
Liste uniquement les types de données personnelles présentes dans ce texte : 
exemples : email, numéro de téléphone, CIN, nom complet, adresse, RIB...

Texte : {prompt}

Réponse (format : EMAIL, PHONE, NAME...) :
"""
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": instruction,
            "stream": False
        })
        raw = response.json()["response"].strip().upper()

        # ✅ On filtre les phrases négatives
        if "PAS DE DONNÉES" in raw or "AUCUNE" in raw:
            return []
        
        return [e.strip() for e in raw.split(",") if e.strip()]
    except Exception:
        return []

def detect_sensitive_data(prompt):
    found = set(detect_with_regex(prompt) + detect_with_llm(prompt))
    return list(found)

def get_alert_message(detected_list):
    if not detected_list:
        return None
    return "Des données sensibles ont été détectées : " + ", ".join(detected_list)

# === Test ===
if __name__ == "__main__":
    prompt = input("Entrez votre prompt : ")
    sensitive_data = detect_sensitive_data(prompt)
    message = get_alert_message(sensitive_data)

    if message:
        print(message)
    else:
        print("✅ Aucune donnée sensible détectée.")
