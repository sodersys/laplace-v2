import firebase_admin
from firebase_admin import db, credentials

def init():
     firebase_admin.initialize_app(credential=credentials.ApplicationDefault(), options={
          'databaseURL': 'https://iapetus-74c01-default-rtdb.firebaseio.com/'
     })

def get(path: str):
     ref = db.reference("data/"+path+"/discordId")
     return str(ref.get())
