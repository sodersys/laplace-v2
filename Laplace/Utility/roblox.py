from roblox import Client
import os, time, json, requests
from Laplace.Utility.db import DepartmentInfo, getQuotaStatuses
from Laplace.Utility.config import getConfigData

configData = getConfigData()
client: Client = None

def getUserName(userId: int) -> str | None:
     result = requests.get(f"https://users.roblox.com/v1/users/{userId}")
     if not result.ok:
          return None
     return result.json()['name']

def getGroupRoles(userId: int) -> dict[str, DepartmentInfo]:
     result = requests.get(f'https://groups.roblox.com/v1/users/{userId}/groups/roles?includeLocked=false')
     if not result.ok:
          raise Exception().add_note("Error getting group roles.")
     
     jsonResult = result.json()['data']
     groupRoles: dict[str, DepartmentInfo] = {}
     quotaStatuses = getQuotaStatuses(userId)

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
     