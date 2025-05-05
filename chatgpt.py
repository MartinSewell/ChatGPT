# Vanilla ChatGPT in a browser window.
# View in browser: http://127.0.0.1:5000/
# Uses openai and flask
# Store your OPENAI_API_KEY in .env

import os
from openai import OpenAI
from flask import Flask, request, render_template_string
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

app = Flask(__name__)

# HTML Template
HTML_PAGE = """
<!doctype html>
<title>ChatGPT</title>
<h2>ChatGPT</h2>
<form method=post>
  <textarea name=prompt rows=6 cols=60 placeholder="Ask something...">{{prompt}}</textarea><br>
  <input type=submit value="Send">
</form>
{% if response %}
  <h4>Response:</h4>
  <div style="white-space: pre-wrap;">{{response}}</div>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def chat():
    response = ""
    prompt = ""
    if request.method == "POST":
        prompt = request.form["prompt"]
        if prompt:
            try:
                completion = client.chat.completions.create(
					model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ]
                )
                response = completion.choices[0].message.content
            except Exception as e:
                response = f"Error: {e}"

    return render_template_string(HTML_PAGE, prompt=prompt, response=response)

if __name__ == "__main__":
    app.run(debug=True)
