import os
from flask import Flask, request
import Laplace.Utility.db as db

app = Flask(__name__)
port = int(os.getenv("PORT", 8080))

def validateRequest(key: str):
    return key == os.getenv("Authentication")

@app.route("/")
def home():
    return "omg"

@app.route("/validateuserranks/<user_id>",)
def validateUserRanks(user_id):
    return db.get(user_id)

def init():
    app.run(host="0.0.0.0", port=port)
