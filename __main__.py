from Laplace import port, bot
from Laplace.Utility import db, config, embeds, quota, roblox
from threading import Thread
import asyncio

Thread(target = port.init).start()
config.updateConfig()
roblox.init()
bot.init()