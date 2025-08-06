import re

def anonymize_text(prompt):
    prompt = re.sub(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", "<EMAIL>", prompt)
    prompt = re.sub(r"\b(0[67]\d{8})\b", "<PHONE>", prompt)
    prompt = re.sub(r"\b[A-Z]{1,2}\d{6}\b", "<CIN>", prompt)
    return prompt
