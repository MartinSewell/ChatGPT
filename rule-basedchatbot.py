# Simple rule-based chatbot only, not ChatGPT
# View in browser: http://127.0.0.1:5000/
# uses flask

from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <title>ChatBot</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 40px; }
      .chatbox { max-width: 600px; margin: auto; }
      .message { margin: 10px 0; }
      .user { color: blue; }
      .bot { color: green; }
    </style>
  </head>
  <body>
    <div class="chatbox">
      <h1>ChatBuddy</h1>
      {% for user_msg, bot_msg in chat_history %}
        <div class="message user"><strong>You:</strong> {{ user_msg }}</div>
        <div class="message bot"><strong>ChatBuddy:</strong> {{ bot_msg }}</div>
      {% endfor %}
      <form method="POST">
        <input type="text" name="user_input" autofocus required style="width: 80%;">
        <button type="submit">Send</button>
      </form>
    </div>
  </body>
</html>
"""

chat_history = []

def chatbot_response(user_input):
    user_input = user_input.lower()

    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I help you today?"
    elif "how are you" in user_input:
        return "I'm a bot, but I'm functioning perfectly. How are you?"
    elif "help" in user_input:
        return "Sure, I'm here to help! What do you need assistance with?"
    elif "bye" in user_input or "goodbye" in user_input:
        return "Goodbye! Have a great day!"
    elif "your name" in user_input:
        return "I'm a simple rule-based chatbot. You can call me ChatBuddy!"
    else:
        return "I'm sorry, I didn't understand that. Could you please rephrase?"

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_input = request.form["user_input"]
        bot_response = chatbot_response(user_input)
        chat_history.append((user_input, bot_response))
    return render_template_string(HTML_TEMPLATE, chat_history=chat_history)

if __name__ == "__main__":
    app.run(debug=True)
