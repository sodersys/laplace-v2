import hikari, lightbulb
from Laplace.Utility import db, config, embeds, roblox

loader = lightbulb.Loader()

def failedUpdate(content: str):
     return embeds.makeEmbed("Failure", "Update failed.", content)

async def update(ctx: lightbulb.Context, otherUser: int | None = None) -> hikari.Embed:
     if otherUser is None:
          robloxId = db.getRobloxId(ctx.user.id)
     else:
          robloxId = db.getRobloxId(otherUser)
     if robloxId == 0:
          if otherUser:
               return failedUpdate(f"<@{otherUser}> don't have a bound roblox account.")
          return failedUpdate("You don't have a bound roblox account.")

     guildId = str(ctx.guild_id)

     configData = config.getConfig()

     if not guildId in configData['discords']:
          return failedUpdate("Server is not set up to grant roles.")

     guildData: dict[int, dict[int, list[str]]] = configData['discords'][guildId]['binds']
     robloxGroups = roblox.getGroupRoles(robloxId)

     rolesToAdd = []
     for groupId, boundRoles in guildData.items():
          groupName = configData['map'][str(groupId)]
          if not groupName in robloxGroups:
               continue

          groupRank = robloxGroups[groupName]['groupRank']

          if not groupRank in boundRoles:
               continue
          
          rolesToAdd.extend(boundRoles[groupRank])

     member = await ctx.client.app.rest.fetch_member(ctx.guild_id, ctx.user.id)
     roleIds = member.role_ids

     rolesToRemove = []

     for role in configData['discords'][guildId]['ranks']:
          if role in roleIds and not role in rolesToAdd:
               rolesToRemove.append(role)

     rolesToAdd = set(rolesToAdd)
     rolesToRemove = set(rolesToRemove)

     addString = ""
     removeString = ""

     for role in rolesToAdd:
          addString += f"<@&{role}>\n"
          member.add_role(role)
          
     for role in rolesToRemove:
          removeString += f"<@&{role}>\n"
          member.remove_role(role)

     fields: list[embeds.field] = []

     if addString != "":
          fields.append({
               "name": "Roles Added",
               "value": addString,
               "inline": False
          })

     if removeString != "":
          fields.append({
               "name": "Roles Removed",
               "value": removeString,
               "inline": False
          })

     if addString == "" and removeString == "":
          return embeds.makeEmbed("Success", "Update Successful.", "No roles were added or removed.")
     
     if otherUser:
          return embeds.makeEmbed("Success", "Update Successful", f"<@{otherUser}>'s roles were changed.", fields = fields)
     return embeds.makeEmbed("Success", "Update Successful", f"Your roles were changed.", fields = fields)

async def canUserUpdateOthers(ctx: lightbulb.Context):
     member = await ctx.client.app.rest.fetch_member(ctx.guild_id, ctx.user.id)
     roles = member.get_roles()

     for role in roles:
          role.name == "Laplace Updater"
          return True

     return False


@loader.command
class Verify(
     lightbulb.SlashCommand,
     name = "verify",
     description = "Verify to get your roles."
):
     robloxId = lightbulb.integer("robloxid", "Your Roblox User ID", default=0)
     @lightbulb.invoke
     async def invoke(self, ctx: lightbulb.Context) -> None:
          await ctx.defer()
          if ctx.channel_id == (await ctx.user.fetch_dm_channel()).id:
               return await ctx.respond("You can only use commands inside of Fourier Discord servers.")

          if self.robloxId == 0:
               await ctx.respond(await update(ctx.user, ctx.guild_id))
               return

          boundAccount = db.getDiscordId(self.robloxId)
          if boundAccount != "0":
               if boundAccount == ctx.user.id:
                    await ctx.respond(await update(ctx.user, ctx.guild_id))
               else:
                    robloxUserName = roblox.getUserName(self.robloxId)
                    await ctx.respond(embeds.makeEmbed("Failure", "Failed to authenticate.", f"[{robloxUserName}](https://www.roblox.com/users/{self.robloxId}/profile) is already bound to user: <@{boundAccount}>"))
               return
          
          boundRobloxAccount = db.getRobloxId(ctx.user.id)
          if boundRobloxAccount != "0":
               if boundRobloxAccount == self.robloxId:
                    await ctx.respond(update(ctx.user, ctx.guild_id))
               else: 
                    robloxUserName = roblox.getUserName(boundRobloxAccount)
                    await ctx.respond(embeds.makeEmbed("Failure", "Failed to authenticate.", f"Your account is already bound to [{robloxUserName}](https://www.roblox.com/users/{boundRobloxAccount}/profile). If you want to get this account removed, create a ticket in the AD server."))
               return
                    
@loader.command
class Update(
     lightbulb.SlashCommand,
     name = "update",
     description = "Update to get your roles."
):
     otherUser = lightbulb.user("otheruser", "The user you want to update", default=None)
     @lightbulb.invoke
     async def invoke(self, ctx: lightbulb.Context):
          await ctx.defer()
          if self.otherUser is None or self.otherUser == ctx.user:
               await ctx.respond(await update(ctx))
          elif await canUserUpdateOthers(ctx):
               await ctx.respond(await update(ctx, self.otherUser))
          else:
               await ctx.respond(embeds.makeEmbed("Failure", "Failed to update.", "You do not have permissions to update other users."))


