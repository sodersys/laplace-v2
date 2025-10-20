import os
from flask import Flask

app = Flask(__name__)
port = int(os.getenv("PORT", 8080))  # Default to 8080 if not set

@app.route("/")
def home():
    return "Bot is running!"

def init():
    app.run(host="0.0.0.0", port=port)
