import requests, time
import Laplace.Utility.config as Config
import Laplace.Utility.db as db
import Laplace.Utility.embeds as embeds
import Laplace.bot as bot

def quotaCheck(playerData: db.QuotaData, quotaData: db.QuotaData):
     if "firstQuota" in playerData or "ignoreQuota" in playerData:
          return True
     for key, value in quotaData.items():
          if not key in playerData:
               return False
          if playerData[key] < value:
               return False
          
     return True

def getGroupMembers(divisionId: str, cursor: str | None) -> any:
     if not cursor is None:
          requesturi = f"https://groups.roblox.com/v1/groups/{divisionId}/users?limit=100&sortOrder=Asc"
     else:
          requesturi = f"https://groups.roblox.com/v1/groups/{divisionId}/users?limit=100&cursor={cursor}&sortOrder=Asc"
     try:
          result = requests.get(requesturi)
          if not result.ok:
               if result.status_code == 429:
                    time.sleep(80)
                    # rate limit, wait 80 seconds and retry.
                    return getGroupMembers(divisionId, cursor)
               elif result.status_code == 400:
                    return None
               else:
                    # log to discord
                    return None
               
          return result.json()
     except:
          time.sleep(80)
          return getGroupMembers(divisionId, cursor)
     
def checkDivisionQuotas(divisionQuota: db.QuotaData, divisionId: int, divisionName: str, cache: dict[int, dict[int, bool]], time: dict[int, int]):
     data = getGroupMembers(divisionId)
     while data != None:
          for playerData in data['data']:
               rank = playerData['rank']
               userId = playerData['user']['userId']

               discordId = db.getDiscordId(userId)

               if rank >= 100:
                    print("member of hc, skipped")
                    # member of HC, skip.
                    continue

               if discordId == "0":
                    # not bound to a discordId
                    # kick from group
                    print(f"not bound, kicking {userId}")
                    continue
               
               quota = db.getQuotaStatus(userId, divisionName)
               db.resetQuotaStatus(userId, divisionName, "ignoreQuota" in quota)

               cache[divisionName] = quotaCheck(quota, divisionQuota)
          data = getGroupMembers(divisionId, data['nextPageCursor'])

async def announceQuotaCheck(division: str, results: dict[int, bool], best: list[tuple[int, int]]):
     channelId = Config.currentConfig['groupData'][division]['channelId']
     
     success = []
     fail = []

     for userId, passed in results.items():
          if passed:
               success.append(userId)
          else:
               fail.append(userId)

     t = 0
     field = ""
     for userId in success:
          field += f"<@{userId}>\n"
          t += 1
          if t > 150 :
               t = 0
               await bot.bot.rest.create_message(channelId, embeds.makeEmbed("Success", "Passed Quota", field))
               field = ""

     if t != 0:
          await bot.bot.rest.create_message(channelId, embeds.makeEmbed("Success", "Passed Quota", field))
     
     t = 0
     field = ""
     for userId in fail:
          field += f"<@{userId}>\n"
          t += 1
          if t > 150 :
               t = 0
               await bot.bot.rest.create_message(channelId, embeds.makeEmbed("Failure", "Failed Quota", field))
               field = ""

     if t != 0:
          await bot.bot.rest.create_message(channelId, embeds.makeEmbed("Failure", "Failed Quota", field))
             
     await bot.bot.rest.create_message(channelId, )

async def checkAllQuotas():
     for division, divisionId in Config.currentConfig['map'].items():
          divisionData: dict[int, bool] = {}
          if not type(divisionId) is int:
               continue
          if division == "main":
               continue
          if division != "MTF":
               # testing
               continue
          times: dict[int, int] = {}
          divisionQuota = Config.currentConfig['quotas']['division'][division]
          checkDivisionQuotas(divisionQuota, divisionId, division, divisionData, times)
          bestTimes = sorted(times.items(), key=lambda item: item[1], reverse=True)[:10]
          announceQuotaCheck(division, divisionData, bestTimes)
     
