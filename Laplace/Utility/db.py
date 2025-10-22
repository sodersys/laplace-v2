import firebase_admin
from firebase_admin import db, credentials, initialize_app

app = initialize_app(credentials.ApplicationDefault(), {
        'databaseURL': 'https://iapetus-74c01-default-rtdb.firebaseio.com/'
    })

class DepartmentInfo():
    groupRank: int
    groupRole: str
    quotaCompletion: int

class UserProfile():
    discordId: str
    robloxId: int
    departments: dict[str, DepartmentInfo]


def getDiscordId(robloxId: int) -> str:
     return db.reference(f"data/{robloxId}/discordId", app).get() or "0"

def getRobloxId(discordId: str) -> int:
     return db.reference(f"reverseLookUp/{discordId}", app).get() or 0

def getUserProfile(discordId: str) -> UserProfile:
     robloxId = getRobloxId(discordId)

     userProfile: UserProfile = {
         'discordId': discordId,
         'robloxId': robloxId,
         'departments': {} 
     }

     if robloxId == 0:
          return userProfile