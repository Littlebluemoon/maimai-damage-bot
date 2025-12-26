import discord
from discord.ext import commands

from paginator import Paginator


async def info(ctx):
    intro = discord.Embed(title="maimai damage bot",
                          description='**maimai damage bot** is a bot initially designed as a plugin to mimi xd bot,'
									  'now double as an information bot with many interesting functions, designed'
                                      ' by Littlebluemoon.\n')
    intro.set_thumbnail(url=
                        "https://cdn.discordapp.com/attachments/764341849921159191/1214866768015925248"
                        "/daijoubu.png?ex=65faabd"
                        "8&is=65e836d8&hm=d64caaa2361bcab18ab125ccf936b7eefd7c1bec49e485ed9e80e28864019900&")
    intro.add_field(name="Usage", value="Type $help for a list of commands.")
    embeds = [intro]
    await Paginator.Simple().start(ctx, pages=embeds)