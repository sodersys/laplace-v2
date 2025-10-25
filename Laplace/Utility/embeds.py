import hikari, datetime
from typing import Literal
from hikari import embeds

embedTypes = {
     "Failure": hikari.Color(0xcc0000), # red
     "Success": hikari.Color(0x006b3c), # green
}


embedTypeKeys = Literal["Failure", "Success"]

class field():
     name: str
     value: str
     inline: bool

def makeEmbed(type: embedTypeKeys, title: str, description: str, to: hikari.User | None, fields: list[field] | None) -> hikari.Embed:
     embed = embeds.Embed(title, description, color=embedTypes[type], timestamp=datetime.datetime.now())
     if not to is None:
          embed.set_author(name=to.global_name, icon=to.make_avatar_url())

     if fields is None:
          return embed

     for field in fields:
          embed.add_field(field.name, field.value, inline=field.inline)
     
     return embed

