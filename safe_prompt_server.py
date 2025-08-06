from flask import Flask, request, render_template, jsonify
from analyzer import detect_sensitive_data
from anonymizer import anonymize_text
import requests
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def ask_llm(prompt):
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    prompt = request.json.get("prompt", "")
    detected = detect_sensitive_data(prompt)
    return jsonify({"sensitive": len(detected) > 0, "entities": detected})

@app.route("/process", methods=["POST"])
def process():
    prompt = request.json.get("prompt", "")
    anonymized = anonymize_text(prompt)
    response = ask_llm(anonymized)
    return jsonify({
        "original": prompt,
        "anonymized": anonymized,
        "response": response
    })

if __name__ == "__main__":
    app.run(port=5000)
