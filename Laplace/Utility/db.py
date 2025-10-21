import firebase_admin
from firebase_admin import db, credentials

def init():
    cred = credentials.ApplicationDefault()  # Must call it!
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://iapetus-74c01-default-rtdb.firebaseio.com/'
    })

def get(path: str):
    ref = db.reference(f"data/{path}/discordId")
    return str(ref.get())
