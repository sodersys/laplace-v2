import hikari, lightbulb
from Laplace.Utility import db, config, embeds, roblox, quota
loader = lightbulb.Loader()

def makeEmojiProgressBar(amount: int, required: int) -> str:
     scaled = int(((min(max(amount, 0), required) / required) * 10) // 1)
     return "🟩" * scaled + "🟥" * int(10-scaled)


@loader.command
class QuotaCheck(
     lightbulb.SlashCommand,
     name = "quota",
     description = "Check your quota or another quota."
):
     user = lightbulb.user("user", "The user you want to check.", default = None)

     @lightbulb.invoke
     async def invoke(self, ctx: lightbulb.Context) -> None:
          await ctx.defer()
          configData = config.getConfig()

          targetUser = self.user or ctx.user
          targetUserProfile = roblox.getRobloxId(targetUser.id)

          if targetUserProfile == 0:
               await ctx.respond(embeds.makeEmbed("Failure", "User is not verified.", "No quota data can be provided."))
               return

          if not str(ctx.guild_id) in configData['discords']:
               await ctx.respond(embeds.makeEmbed("Failure", "This discord has no quotas linked.", "Try using the command in a department server to check someone's quota."))
               return

          division = configData['discords'][str(ctx.guild_id)]['group']

          if division == "main":
               await ctx.respond(embeds.makeEmbed("Failure", "This discord has no quotas linked.", "Try using the command in a department server to check someone's quota."))
               return
          
          quotaData = db.getQuotaStatus(targetUserProfile, division)
          quotaRequirements = configData['quotas']['divisions'][division]

          passed = quota.quotaCheck(quotaData, quotaRequirements)

          if passed:
               embed = embeds.makeEmbed("Success", "Quota Passed", f'Time: {quotaData['time']} / {quotaRequirements['time']}\n{makeEmojiProgressBar(quotaData['time'], quotaRequirements['time'])}\nEvents: {quotaData['events']} / {quotaRequirements['events']}\n{makeEmojiProgressBar(quotaData['events'], quotaRequirements['events'])}', targetUser)
          else:
               embed = embeds.makeEmbed("Failed", "Quota Failed", f'Time: {quotaData['time']} / {quotaRequirements['time']}\n{makeEmojiProgressBar(quotaData['time'], quotaRequirements['time'])}\nEvents: {quotaData['events']} / {quotaRequirements['events']}\n{makeEmojiProgressBar(quotaData['events'], quotaRequirements['events'])}', targetUser)
               
          await ctx.respond(embed)
          
          




          



