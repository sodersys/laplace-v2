import os
from flask import Flask

app = Flask(__name__)
port = int(os.getenv("PORT", 8080))

@app.route("/")
def home():
    return "omg"

def init():
    app.run(host="0.0.0.0", port=port)
