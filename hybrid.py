# Hybrid rule-based (if defined) and ChatGPT (fallback)
# View in browser: indexh.html
# Uses openai and flask
# Store your OPENAI_API_KEY in .env

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

# (a) Rule-Based Responses
rule_based_responses = {
    "hello": "Hi there! How can I help you today?",
    "hi": "Hello! What can I do for you?",
    "hours": "Our working hours are 9 AM to 6 PM, Monday to Friday.",
    "pricing": "Our pricing details are available on our website.",
    "contact": "You can contact us at support@example.com.",
    "bye": "Goodbye! Have a great day."
}

def rule_based_reply(user_message):
    """Check if user_message matches a rule-based response."""
    user_message = user_message.lower()
    for keyword, response in rule_based_responses.items():
        if keyword in user_message:
            return response
    return None

# (b) ChatGPT Fallback
def chatgpt_reply(user_message):
    prompt = f"You are a helpful customer support assistant. Answer the following query:\n\n{user_message}"
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    # (c) Integration Logic
    reply = rule_based_reply(user_message)
    if reply is None:
        reply = chatgpt_reply(user_message)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
