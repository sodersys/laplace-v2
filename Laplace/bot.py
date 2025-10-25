import os
import hikari, lightbulb
from Laplace.Commands import Verification

bot: hikari.GatewayBot

def init():
     global bot
     bot = hikari.GatewayBot(token = os.getenv("botToken"))
     client = lightbulb.client_from_app(bot)
     Verification.registerCommands(client)