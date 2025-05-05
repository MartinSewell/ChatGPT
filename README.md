# ChatGPT
Eight simple Python programs that use ChatGPT.

chatgpt.py
Vanilla ChatGPT in a browser window.
View in browser: http://127.0.0.1:5000/
Uses openai and flask
Store your OPENAI_API_KEY in .env

decisiontree.py
Uses a decision tree before using ChatGPT at the end.
View in browser: http://127.0.0.1:5000/
Uses openai and flask
Store your OPENAI_API_KEY in .env

hybrid.py
Hybrid rule-based (if defined) and ChatGPT (fallback)
View in browser: indexh.html
Uses openai and flask
Store your OPENAI_API_KEY in .env

nodeevaluator.py
The user enters data in some fields, then ChatGPT puts a probability on a statement, and provides advice accordingly.
View in browser: http://127.0.0.1:5000/
Also uses /templates/index.html
Uses openai and flask
Store your OPENAI_API_KEY in .env

privatedata.py
Uses private data plus ChatGPT's normal response.
Put private data in /data/
View in browser: http://127.0.0.1:5000/
Uses openai, flask and llama_index
Store your OPENAI_API_KEY in .env

promptengineering.py
ChatGPT with prompt engineering used to change the style of the answer (general, technical or casual).
View in browser: http://127.0.0.1:5000/
uses flask, langchain and langchain_openai
Store your OPENAI_API_KEY in .env

rule-basedchatbot.py
Simple rule-based chatbot only, not ChatGPT
View in browser: http://127.0.0.1:5000/
uses flask

structuredtemplates.py
ChatGPT with (built into ChatGPT) options for tone (formal, casual, friendly), audience (general public, professionals, students) and special considerations (keep it brief, use examples, be humorous).
View in browser: indexst.html
Uses openai and flask
Store your OPENAI_API_KEY in .env
