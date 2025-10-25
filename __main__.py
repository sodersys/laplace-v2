from Laplace import port, bot
from Laplace.Utility import auth, db, config, embeds, quota, roblox
from threading import Thread
import asyncio

Thread(target = port.init).start()
config.updateConfig()
roblox.init()
bot.init()