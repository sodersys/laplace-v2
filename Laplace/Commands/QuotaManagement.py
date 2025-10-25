import hikari, lightbulb
from Laplace.Utility import db, config, embeds, roblox
loader = lightbulb.Loader()

def makeEmojiProgressBar(amount: int, required: int) -> str:
     amount = min(max(amount, 0), required)
     scaled = ((amount / required) * 10) // 1
     return "🟩" * scaled + "🟥" * (10-scaled)


@loader.command
class quota(
     lightbulb.SlashCommand,
     mame = "quota",
     description = "Check your quota or someone else's"
):
     user = lightbulb.user("user", "The user you want to check.", default = None)

     @lightbulb.invoke
     async def invoke(self, ctx: lightbulb.Context) -> None:
          await ctx.defer()
          configData = config.getConfig()

          targetUser = self.user or ctx.user
          division = configData[str(ctx.guild_id)]['group']

          if division == "main":
               await ctx.respond(embeds.makeEmbed("Failure", "This discord has no quotas linked.", "Try using the command in a department server to check someone's quota."))
               return
          
          



