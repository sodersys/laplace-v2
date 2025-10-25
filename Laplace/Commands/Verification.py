import hikari, lightbulb, secrets, os
from hikari import messages
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

     guildData: dict[str, dict[int, dict[int, list[str]]] | str] = configData['discords'][guildId]['binds']
     robloxGroups = roblox.getGroupRoles(robloxId)

     rolesToAdd = []
     nameFormat = "{username}"
     currentPriority = 0
     for groupId, boundRoles in guildData.items():
          if "in" in boundRoles:
               for role in boundRoles["in"]['roles']:
                    role = int(role)
                    rolesToAdd.append(role)
               if 'nameFormat' in boundRoles["in"]:
                    if boundRoles["in"]['formatPriority'] > currentPriority:
                         nameFormat = boundRoles["in"]['nameFormat']
                         currentPriority = boundRoles["in"]['formatPriority']
               

          groupName = configData['map'][str(groupId)]
          if not groupName in robloxGroups:
               continue
          groupRank = str(robloxGroups[groupName]['groupRank'])
          if not groupRank in boundRoles:
               continue

          if 'nameFormat' in boundRoles[groupRank]:
               if boundRoles[groupRank]['formatPriority'] > currentPriority:
                    nameFormat = boundRoles[groupRank]['nameFormat']
                    currentPriority = boundRoles[groupRank]['formatPriority']
          for role in boundRoles[groupRank]['roles']:
               role = int(role)
               rolesToAdd.append(role)

     rolesToRemove = []
     member = await ctx.client.app.rest.fetch_member(ctx.guild_id, ctx.user.id)
     roleIds = member.role_ids

     for role in configData['discords'][guildId]['ranks']:
          role = int(role)
          if role in roleIds:
               if role in rolesToAdd:
                    rolesToAdd.remove(role)
                    continue

               rolesToRemove.append(role)

     rolesToAdd = set(rolesToAdd)
     rolesToRemove = set(rolesToRemove)

     addString = ""
     removeString = ""

     for role in rolesToAdd:
          addString += f"<@&{role}>\n"
          await member.add_role(role)
          
     for role in rolesToRemove:
          removeString += f"<@&{role}>\n"
          await member.remove_role(role)

     fields: list[embeds.field] = []

     if addString != "":
          fields.append({
               "name": "Roles Added",
               "value": addString,
               "inline": True
          })

     if removeString != "":
          fields.append({
               "name": "Roles Removed",
               "value": removeString,
               "inline": True
          })

     formattedName = nameFormat.format(username = roblox.getUserName(robloxId) or "brokenUserName")
     oldName = member.nickname or member.username
     if formattedName != member.nickname:
          try:
               await member.edit(nickname=formattedName)
               fields.append({
                    'name': "Nickname Set",
                    'value': f"{oldName} -> {formattedName}",
                    "inline": False,
               })
          except:
               fields.append({
                    'name': "Failed to set nickname.",
                    'value': f"Desired Nickname: {formattedName}",
                    "inline": False,
               })

     if removeString == "" and addString == "":
          return embeds.makeEmbed("Success", "Update Successful.", "No roles were added or removed.", fields = fields)
     
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

clientId = os.getenv("clientId")
redirectUri = "https://laplaceomg-190212166685.us-central1.run.app/redirect"
scope = "openid"

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
               await ctx.respond(await update(ctx))
               return

          boundAccount = db.getDiscordId(self.robloxId)
          if boundAccount != "0":
               if boundAccount == ctx.user.id:
                    await ctx.respond(await update(ctx))
               else:
                    robloxUserName = roblox.getUserName(self.robloxId)
                    await ctx.respond(embeds.makeEmbed("Failure", "Failed to authenticate.", f"[{robloxUserName}](https://www.roblox.com/users/{self.robloxId}/profile) is already bound to user: <@{boundAccount}>"))
               return
          
          boundRobloxAccount = db.getRobloxId(ctx.user.id)
          if boundRobloxAccount != 0:
               if boundRobloxAccount == self.robloxId:
                    await ctx.respond(update(ctx))
               else: 
                    robloxUserName = roblox.getUserName(boundRobloxAccount)
                    await ctx.respond(embeds.makeEmbed("Failure", "Failed to authenticate.", f"Your account is already bound to [{robloxUserName}](https://www.roblox.com/users/{boundRobloxAccount}/profile). If you want to get this account removed, create a ticket in the AD server."))
               return
         
          accountName = roblox.getUserName(self.robloxId)
          if accountName is None:
               await ctx.respond(await ctx.respond(embeds.makeEmbed("Failure", "Account does not exist.", f"There is no account linked to the id: {self.robloxId}")))
          await ctx.respond(embeds.makeEmbed("Success", "Ready to Verify.", "You don't have a linked account, click the link sent to you in DMs to authenticate your account."))
          stateToken = secrets.token_urlsafe(16)
          db.pending[stateToken] = {
               "discord": ctx.user.id,
               "roblox": self.robloxId
          }

          authUrl = (
               f"https://apis.roblox.com/oauth/v1/authorize"
               f"?client_id={clientId}"
               f"&response_type=code"
               f"&scope={scope}"
               f"&redirect_uri={redirectUri}"
               f"&state={stateToken}"
          )

          userChannel = await ctx.user.fetch_dm_channel()

          components = [
               hikari.impl.ContainerComponentBuilder(
                    components=[
                         hikari.impl.TextDisplayComponentBuilder(content=f"You have a pending verification request between [{robloxUserName}](https://www.roblox.com/users/{self.robloxId}/profile) and your discord account. Click the button below and authorize Laplace Authentication to complete verification."),
                    ]
               ),
               hikari.impl.MessageActionRowBuilder(
                    components=[
                         hikari.impl.LinkButtonBuilder(
                              url=authUrl,
                              label="Verify Your Account",
                         ),
                    ]
               ),
          ]

          await ctx.client.app.rest.create_message(userChannel.id, flags=messages.MessageFlag.IS_COMPONENTS_V2, components=components)
          
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