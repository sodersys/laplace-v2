from firebase_admin import credentials, db, initialize_app

app = initialize_app(credentials.ApplicationDefault(), {
        'databaseURL': 'https://endless-matter-474321-f8-default-rtdb.firebaseio.com/'
}, name="config_app")

currentConfig: any = None

def updateConfig():
     global currentConfig
     currentConfig = db.reference(path="/", app=app)

def getConfig():
     return currentConfig
