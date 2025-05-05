# Uses a decision tree before using ChatGPT at the end.
# View in browser: http://127.0.0.1:5000/
# Uses openai and flask
# Store your OPENAI_API_KEY in .env

from flask import Flask, request, redirect, url_for, render_template_string, session
from openai import OpenAI
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# Decision tree for financial advice
decision_tree = {
    "start": {
        "question": "What type of business problem do you have?",
        "options": {
            "Operational": "operational",
            "Financial": "financial",
            "Marketing": "marketing"
        }
    },
    "operational": {
        "question": "What type of operational problems?",
        "options": {
            "Supply chain": "supply_chain",
            "Process": "process"
        }
    },
    "financial": {
        "question": "What type of financial problems?",
        "options": {
            "Cash flow": "cash_flow",
            "Profitability": "profitability"
        }
    },
    "marketing": {
        "question": "What type of marketing problems?",
        "options": {
            "Poor Customer Engagement & Brand Awareness": "brand",
            "Ineffective Targeting & Positioning": "targeting"
        }
    },
	"supply_chain": "I am the CEO of a small company in Cambridge, UK.  Find me some consultants who can help solve my supply chain problems.",
    "process": "I am the CEO of a small company in Cambridge, UK.  Find me some consultants who can help solve my process problems.",
	"cash_flow": "I am the CEO of a small company in Cambridge, UK.  Find me some consultants who can help solve my cash flow problems.",
    "profitability": "I am the CEO of a small company in Cambridge, UK.  Find me some consultants who can help solve my profitability problems.",
	"brand": "I am the CEO of a small company in Cambridge, UK.  Find me some consultants who can help solve my customer engagement and brand awareness problems.",
    "target": "I am the CEO of a small company in Cambridge, UK.  Find me some consultants who can help solve my ineffective targeting and positioning problems."
}

# ChatGPT response function
def chatgpt_response(user_input, context):
    prompt = f"""
    You are an expert financial advisor. Provide a concise and friendly explanation for:
    User query: \"{user_input}\"
    Context: \"{context}\"
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message.content

# HTML Template
HTML_TEMPLATE = """
<!doctype html>
<title>AI Financial Advisor</title>
<h2>{{ question }}</h2>
<form method="post">
    {% for option in options %}
        <button type="submit" name="choice" value="{{ option }}">{{ option }}</button><br>
    {% endfor %}
</form>
{% if response %}
    <h3>AI Advice:</h3>
    <p>{{ response }}</p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if "current" not in session:
        session["current"] = "start"

    node_key = session["current"]
    node = decision_tree[node_key]

    if isinstance(node, str):  # Final advice
        response = chatgpt_response(node, "Financial Investment Advice")
        session.clear()
        return render_template_string(HTML_TEMPLATE, question="Here’s what I recommend:", options=[], response=response)

    question = node["question"]
    options = list(node["options"].keys())

    if request.method == "POST":
        choice = request.form.get("choice")
        if choice in node["options"]:
            session["current"] = node["options"][choice]
            return redirect(url_for("index"))

    return render_template_string(HTML_TEMPLATE, question=question, options=options, response=None)

if __name__ == "__main__":
    app.run(debug=True)
