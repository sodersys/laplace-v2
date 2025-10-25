import hikari, lightbulb
from Laplace.Utility import config

loader = lightbulb.Loader()

@loader.command
class updateDB(
     lightbulb.SlashCommand,
     name = "pushconfig",
     description = "push latest config"
     ):
     @lightbulb.invoke
     async def invoke(self, ctx: lightbulb.Context) -> None:
          if ctx.user.id != 1334305439025991730:
               return await ctx.respond("You do not have permission to run this command.")
          config.updateConfig()
          return await ctx.respond("New config pushed.")          

     