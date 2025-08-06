# SafePrompt

🛡️ SafePrompt est un outil local de cybersécurité conçu pour détecter et anonymiser les données sensibles (CIN, email, téléphone, etc.) dans les prompts adressés à des IA publiques (ex : ChatGPT).

## 🔍 Fonctionnalités

- Extension Chrome qui intercepte les prompts avant envoi.
- Détection via regex et LLM local (Ollama).
- Alerte utilisateur avec choix : Anonymiser ou Annuler.
- Conformité avec les lois marocaines 09-08 et 05-20.

## ⚙️ Stack

- Flask · HTML/CSS/JS · Regex · Ollama · Chrome Extension

## 🚀 Lancer le projet

```bash
pip install -r requirements.txt
python app.py
