import hikari, lightbulb
from Laplace.Utility import db, config, embeds, roblox

def update(user: hikari.User, guildId: int) -> hikari.Embed:
     return 10


class Verify(
     lightbulb.SlashCommand,
     name = "verify",
     description = "Verify to get your roles."
):
     robloxId = lightbulb.integer("robloxid", "Your Roblox User ID")
     @lightbulb.invoke
     async def invoke(self, ctx: lightbulb.Context) -> None:
          boundAccount = db.getDiscordId(self.robloxId)
          if boundAccount != "0":
               if boundAccount == ctx.user.id:
                    await ctx.respond(update(ctx.user, ctx.guild_id))
               else:
                    robloxUserName = roblox.getUserName(self.robloxId)
                    await ctx.respond(embeds.makeEmbed("Failure", "Failed to authenticate.", f"[{robloxUserName}](https://www.roblox.com/users/{self.robloxId}/profile) is already bound to user: <@{boundAccount}>"))
               return
          
          boundRobloxAccount = db.getRobloxId(ctx.user.id)
          if boundRobloxAccount != "0":
               if boundRobloxAccount == self.robloxId:
                    await ctx.respond(update(ctx.user, ctx.guild_id))
               else: 
                    await ctx.respond(embeds.makeEmbed("Failure", "Failed to authenticate.", f"You {10}"))
               return
                    






def registerCommands(client: lightbulb.Client):
     client.register(Verify)