# ChatGPT with (built into ChatGPT) options for tone (formal, casual, friendly), audience (general public, professionals, students) and special considerations (keep it brief, use examples, be humorous).
# View in browser: indexst.html
# Uses openai and flask
# Store your OPENAI_API_KEY in .env

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)  # Allow requests from browser (frontend)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    topic = data.get("topic")
    tone = data.get("tone")
    audience = data.get("audience")
    extras = data.get("extras")  # list of extras from checkboxes

    # Build a structured prompt
    prompt = f"""
You are a helpful assistant.
Topic: {topic}
Tone: {tone}
Audience: {audience}
Special Considerations: {', '.join(extras) if extras else 'None'}

Please generate a clear and appropriate response.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
