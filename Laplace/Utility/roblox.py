from roblox import Client
import os, time, json, requests
from Laplace.Utility.db import UserProfile, DepartmentInfo, getQuotaStatus, getRobloxId, getDiscordId
from Laplace.Utility.config import getConfig

configData = getConfig()
client: Client = None

def getUserName(userId: int) -> str | None:
     result = requests.get(f"https://users.roblox.com/v1/users/{userId}")
     if not result.ok:
          return None
     return result.json()['name']

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

def getGroupRoles(userId: int) -> dict[str, DepartmentInfo]: 

     result = requests.get(f'https://groups.roblox.com/v1/users/{userId}/groups/roles?includeLocked=false')
     if not result.ok:
          raise Exception().add_note("Error getting group roles.")
     
     jsonResult = result.json()['data']
     groupRoles: dict[str, DepartmentInfo] = {}
     quotaStatuses = getQuotaStatus(userId)

     for group in jsonResult:
          groupId = group['group']['id']
          
          if not groupId in configData['map']:
               continue
          
          groupName = configData['map'][groupId]
          groupRank = group['group']['rank']
          groupRole = groupRole['group']['role']

          if groupName in quotaStatuses:
               quotaStatus = quotaStatuses[groupName]
          else:
               quotaStatus = {"events": 0, "time": 0}

          groupRoles[groupName] = {
               "groupRank": groupRank,
               "groupRole": groupRole,
               "quotaStatus": quotaStatus
          }

     return groupRoles

def init():
     global client
     client = Client(os.getenv("robloxCookie"))
     