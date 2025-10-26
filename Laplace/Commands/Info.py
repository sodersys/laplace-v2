import hikari, lightbulb
from Laplace.Utility import db, roblox, embeds

loader = lightbulb.Loader()

@loader.command
class whois(
     lightbulb.SlashCommand,
     name = "whois",
     description = "Get info about a discord user."
     ):
     
     robloxName = lightbulb.string("roblox", "The roblox name you want info on.", default=None)
     discordUser = lightbulb.user("user", "The discord user you want info on.", default=None)
     @lightbulb.invoke
     async def invoke(self, ctx: lightbulb.Context):
          user = self.discordUser
          if user is None:
               if self.robloxName is None:
                    user = ctx.user
               else:
                    robloxId = await roblox.getIdByUsername(self.robloxName)
                    if robloxId == 0:
                         await ctx.respond("No user is bound to that roblox name.")
                         return
                    discordUser = int(db.getDiscordId(robloxId))
                    if discordUser == 0:
                         await ctx.respond(f"No discord user is bound to [{self.robloxName}](<https://www.roblox.com/users/{robloxId}/profile>)")
                         return
          
          await ctx.respond(embeds.makeEmbed("Success", f"Account Bindings For <@{discordUser}>", f"[{self.robloxName}](<https://www.roblox.com/users/{robloxId}/profile>)"))

