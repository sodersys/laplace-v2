from roblox import Client
import os, time, json, requests
from Laplace.Utility.db import UserProfile, DepartmentInfo, getQuotaStatus, getRobloxId, getDiscordId
import Laplace.Utility.config as config
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
         'departments': getGroupRolesWithQuota(robloxId)
     }

     if robloxId == 0:
          return userProfile
     
async def getIdByUsername(username: str) -> int:
     user = await client.get_user_by_username(username)
     if user is None:
          return 0
     return user.id

def getGroupRoles(userId: int) -> dict[str, DepartmentInfo]: 
     result = requests.get(f'https://groups.roblox.com/v1/users/{userId}/groups/roles?includeLocked=false')
     if not result.ok:
          raise Exception().add_note("Error getting group roles.")
     
     jsonResult = result.json()['data']
     groupRoles: dict[str, DepartmentInfo] = {}

     configData = config.getConfig()

     for group in jsonResult:
          groupId = group['group']['id']
          
          if not str(groupId) in configData['map']:
               continue
          
          groupName = configData['map'][str(groupId)]
          groupRank = group['role']['rank']
          groupRole = group['role']['name']

          groupRoles[groupName] = {
               "groupRank": groupRank,
               "groupRole": groupRole
          }

     return groupRoles

def getGroupRolesWithQuota(userId: int) -> dict[str, DepartmentInfo]: 

     result = requests.get(f'https://groups.roblox.com/v1/users/{userId}/groups/roles?includeLocked=false')
     if not result.ok:
          raise Exception().add_note("Error getting group roles.")
     
     jsonResult = result.json()['data']
     groupRoles: dict[str, DepartmentInfo] = {}

     configData = config.getConfig()

     for group in jsonResult:
          groupId = group['group']['id']
          
          if not groupId in configData['map']:
               continue
          
          groupName = configData['map'][groupId]
          groupRank = group['group']['rank']
          groupRole = groupRole['group']['role']

          groupRoles[groupName] = {
               "groupRank": groupRank,
               "groupRole": groupRole,
               "quotaStatus": getQuotaStatus(userId, groupName)
          }

     return groupRoles

def init():
     global client
     client = Client(os.getenv("robloxCookie"))
     