from roblox import Client
import os, time, json, requests
from Laplace.Utility.db import DepartmentInfo
from Laplace.Utility.config import getConfigData

configData = getConfigData()

def getGroupRoles(userId: int) -> dict[str, DepartmentInfo]:
     result = requests.get(f'https://groups.roblox.com/v1/users/{userId}/groups/roles?includeLocked=false')
     if not result.ok:
          raise Exception().add_note("Error getting group roles.")
     
     jsonResult = result.json()['data']
     groupRoles: dict[str, DepartmentInfo] = {}

     for group in jsonResult:
          groupId = group['group']['id']
          groupRank = group['group']['rank']

          if not groupId in 
     