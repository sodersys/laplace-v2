import firebase_admin
from firebase_admin import db, credentials, initialize_app

pending = {}

app = initialize_app(credentials.ApplicationDefault(), {
        'databaseURL': 'https://iapetus-74c01-default-rtdb.firebaseio.com/'
    }, name="db_app")

class QuotaData():
     events: int
     time: int

class DepartmentInfo():
    groupRank: int
    groupRole: str
    quotaStatus: QuotaData

class UserProfile():
    discordId: str
    robloxId: int
    robloxName: str
    departments: dict[str, DepartmentInfo]

def link(robloxId: int, discordId: int):
    db.reference(f"data/{robloxId}/discordId", app=app).set(str(discordId))
    db.reference(f"reverseLookUp/{discordId}", app=app).set(robloxId)

def getDiscordId(robloxId: int) -> str: 
    return db.reference(f"data/{robloxId}/discordId", app=app).get() or "0"

def getRobloxId(discordId: str) -> int:
    return db.reference(f"reverseLookUp/{discordId}", app=app).get() or 0

def getQuotaStatus(userId: int, team: str) -> dict[str, QuotaData]:
    return db.reference(f"data/{userId}/quotas/{team}", app=app).get() or {}
    
def resetQuotaStatus(userId: int, team: str, ignoreQuota: bool):
    return db.reference(f"data/{userId}/quotas/{team}", app=app).set({'time': 0, 'events': 0, 'ignoreQuota': ignoreQuota})
    