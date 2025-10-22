import hikari, lightbulb
from Laplace.Utility import db, config

class Verify(
     lightbulb.SlashCommand,
     name = "verify",
     description = "Verify to get your roles."
):
     robloxId = lightbulb.integer("")