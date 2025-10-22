import os
import hikari
from Laplace.Commands import Verification


def init():
     bot = hikari.GatewayBot(token = os.getenv("botToken"))
     Verification.init(bot)