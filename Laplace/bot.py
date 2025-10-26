import os
import hikari, lightbulb

bot: hikari.GatewayBot

def init():
     global bot
     bot = hikari.GatewayBot(token = os.getenv("botToken"))
     client = lightbulb.client_from_app(bot)
     
     @bot.listen(hikari.StartingEvent)
     async def on_starting(_: hikari.StartingEvent) -> None:
          await client.load_extensions("Laplace.Commands.Verification", "Laplace.Commands.UpdateDB")
          await client.start()
          await client.sync_application_commands()


     bot.run()