# Uses private data plus ChatGPT's normal response.
# Put private data in /data/
# View in browser: http://127.0.0.1:5000/
# Uses openai, flask and llama_index
# Store your OPENAI_API_KEY in .env

from openai import OpenAI
from flask import Flask, request, render_template_string
import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader


from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Load documents using LlamaIndex
DATA_FOLDER = "data"
documents = SimpleDirectoryReader(DATA_FOLDER).load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

# HTML Template
HTML_PAGE = """
<!doctype html>
<title>Private Data Query</title>
<h2>Ask a question about your private data</h2>
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
                response = query_engine.query(prompt)
            except Exception as e:
                response = f"Error: {e}"

    return render_template_string(HTML_PAGE, prompt=prompt, response=response)

if __name__ == "__main__":
    app.run(debug=True)

