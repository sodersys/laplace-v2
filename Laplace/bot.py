import os
import hikari

def init():
     bot = hikari.GatewayBot(token = os.getenv("DiscordAPIKey"))
     