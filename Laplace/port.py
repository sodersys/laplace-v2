import os
from flask import Flask, request

app = Flask(__name__)
port = int(os.getenv("PORT", 8080))

def validateRequest(key: str):
    return key == os.getenv("Authentication")

@app.route("/")
def home():
    return os.getenv("DiscordAPIKey")

@app.route("/ValidateUserRanks", methods=["POST"])
def validateUserRanks():
    headers = request.headers


def init():
    app.run(host="0.0.0.0", port=port)
