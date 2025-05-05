# The user enters data in some fields, then ChatGPT puts a probability on a statement, and provides advice accordingly.
# View in browser: http://127.0.0.1:5000/
# Also uses /templates/index.html
# Uses openai and flask
# Store your OPENAI_API_KEY in .env


import os
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, request, render_template

load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)


app = Flask(__name__)

# Evaluate prompt using GPT-4
def evaluate_node(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert decision assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    reply = response.choices[0].message.content

    # Extract confidence
    try:
        confidence_line = [line for line in reply.split('\n') if "Confidence" in line][0]
        confidence = float(confidence_line.split(":")[1].strip().replace("%", "")) / 100
    except:
        confidence = 0.5

    return reply.strip(), confidence

@app.route("/", methods=["GET", "POST"])
def index():
    result1 = result2 = ""
    if request.method == "POST":
        age = request.form.get("age")
        exp = request.form.get("experience")
        field = request.form.get("field")

        # Node 1
        prompt1 = f"""
The user is {age} years old with {exp} years of experience in {field}.
How likely are they to be considered mid-career?
Provide a confidence score between 0% and 100%.
"""
        result1, confidence = evaluate_node(prompt1)

        if confidence > 0.6:
            # Node 2a
            prompt2 = f"""
Given that the user is likely mid-career and works in {field}, would a leadership or specialist track suit them better?
Confidence in leadership potential: ___%
Confidence in specialist potential: ___%
"""
        else:
            # Node 2b
            prompt2 = f"""
The user may be early-career. What are the best next steps for someone with {exp} years in {field}?
Also, give a confidence score that this person is early-career.
"""
        result2, _ = evaluate_node(prompt2)

    return render_template("index.html", result1=result1, result2=result2)

if __name__ == "__main__":
    app.run(debug=True)
