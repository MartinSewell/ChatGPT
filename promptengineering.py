# ChatGPT with prompt engineering used to change the style of the answer (general, technical or casual).
# View in browser: http://127.0.0.1:5000/
# uses flask, langchain and langchain_openai
# Store your OPENAI_API_KEY in .env

import os
from langchain.schema.runnable import RunnableSequence
from langchain.prompts import PromptTemplate
from flask import Flask, render_template_string, request
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

from dotenv import load_dotenv
load_dotenv()

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__)

# Initialize ChatGPT model
chat_model = ChatOpenAI(model_name="gpt-4", temperature=0.7)

# Define base prompt
base_prompt = PromptTemplate(
    input_variables=["user_query"],
    template="""
You are an expert assistant.
Here is the user's question:
{user_query}

Please answer helpfully and clearly.
"""
)

# Function to dynamically adjust prompts based on context
def dynamic_prompt(user_query, context_type="general"):
    if context_type == "technical":
        new_prompt = PromptTemplate(
            input_variables=["user_query"],
            template="""
You are a highly technical expert.
Answer the user's question precisely, using technical language where appropriate.

Question:
{user_query}
"""
        )
    elif context_type == "casual":
        new_prompt = PromptTemplate(
            input_variables=["user_query"],
            template="""
You're a friendly helper.
Answer casually and warmly.

User asks:
{user_query}
"""
        )
    else:
        new_prompt = base_prompt

    dynamic_chain = LLMChain(llm=chat_model, prompt=new_prompt)
    response = dynamic_chain.run(user_query)
    return response

# HTML template
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <title>Dynamic ChatGPT</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 40px; }
    .chatbox { max-width: 700px; margin: auto; }
    .message { margin: 10px 0; }
    .user, .bot { margin: 10px 0; padding: 10px; border-radius: 5px; }
    .user { background-color: #e6f7ff; }
    .bot { background-color: #f9f9f9; }
  </style>
</head>
<body>
  <div class="chatbox">
    <h1>Dynamic ChatGPT</h1>
    {% if user_query and bot_response %}
      <div class="user"><strong>You:</strong> {{ user_query }}</div>
      <div class="bot"><strong>ChatGPT:</strong> {{ bot_response }}</div>
    {% endif %}
    <form method="POST">
      <input type="text" name="user_query" placeholder="Enter your question" style="width: 70%;" required>
      <select name="context">
        <option value="general">General</option>
        <option value="technical">Technical</option>
        <option value="casual">Casual</option>
      </select>
      <button type="submit">Send</button>
    </form>
  </div>
</body>
</html>
"""

# Flask route
@app.route("/", methods=["GET", "POST"])
def chat():
    user_query = None
    bot_response = None
    if request.method == "POST":
        user_query = request.form["user_query"]
        context = request.form["context"]
        bot_response = dynamic_prompt(user_query, context)
    return render_template_string(HTML_TEMPLATE, user_query=user_query, bot_response=bot_response)

if __name__ == "__main__":
    app.run(debug=True)
