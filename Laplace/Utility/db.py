import firebase_admin
from firebase_admin import db, credentials, initialize_app
from Laplace.Utility.roblox import getGroupRoles, getUserName

app = initialize_app(credentials.ApplicationDefault(), {
        'databaseURL': 'https://iapetus-74c01-default-rtdb.firebaseio.com/'
    })

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

def getDiscordId(robloxId: int) -> str:
     return db.reference(f"data/{robloxId}/discordId", app).get() or "0"

def getRobloxId(discordId: str) -> int:
     return db.reference(f"reverseLookUp/{discordId}", app).get() or 0

def getUserProfile(discordId: str) -> UserProfile:
     robloxId = getRobloxId(discordId)

     userProfile: UserProfile = {
         'discordId': discordId,
         'robloxId': robloxId,
         'robloxName': getUserName(robloxId),
         'departments': getGroupRoles(robloxId)
     }

     if robloxId == 0:
          return userProfile


def getQuotaStatus(userId: int, team: str) -> dict[str, QuotaData]:
    return db.reference(f"data/{userId}/quotas/{team}").get() or {}
    
def resetQuotaStatus(userId: int, team: str, ignoreQuota: bool):
    return db.reference(f"data/{userId}/quotas/{team}").set({'time': 0, 'events': 0, 'ignoreQuota': ignoreQuota})
    