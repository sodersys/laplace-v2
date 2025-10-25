from Laplace import port, bot
from Laplace.Utility import db, config, embeds, quota, roblox
from threading import Thread

Thread(target = port.init).start()
config.updateConfig()
roblox.init()
bot.init()