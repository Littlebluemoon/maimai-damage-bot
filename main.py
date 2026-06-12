import os

import certifi
import discord
from discord.ext import commands
from dotenv import load_dotenv

from command.chiho import chiho
from command.info import about

load_dotenv()
from command.songdata import lookup, detail, find
from command.rating import rating, target, calculate
from command.courses import dan, shindan, otomodachi
from command.collection import collection, titles, icons, plates, frames
from command.cheats import hold, mash
from command.damage import damage
from command.border import border
from command.help import help

import slash_command.songdata
import slash_command.rating
import slash_command.info
import slash_command.help
import slash_command.courses
import slash_command.collection
import slash_command.cheats
import slash_command.border

intents = discord.Intents.default()
intents.message_content = True

os.environ["SSL_CERT_FILE"] = certifi.where()

bot = commands.Bot(command_prefix='m$', intents=intents)
bot.help_command = None

bot.add_command(about)
bot.add_command(lookup)
bot.add_command(find)
bot.add_command(rating)
bot.add_command(target)
bot.add_command(calculate)
bot.add_command(dan)
bot.add_command(shindan)
bot.add_command(detail)
bot.add_command(collection)
bot.add_command(titles)
bot.add_command(icons)
bot.add_command(otomodachi)
bot.add_command(hold)
bot.add_command(mash)
bot.add_command(damage)
bot.add_command(border)
bot.add_command(help)
bot.add_command(plates)
bot.add_command(frames)
bot.add_command(chiho)

bot.tree.add_command(slash_command.songdata.lookup)
bot.tree.add_command(slash_command.songdata.detail)
bot.tree.add_command(slash_command.songdata.find)

bot.tree.add_command(slash_command.rating.rating)
bot.tree.add_command(slash_command.rating.calculate)
bot.tree.add_command(slash_command.rating.target)

bot.tree.add_command(slash_command.info.about)

bot.tree.add_command(slash_command.help.help)

bot.tree.add_command(slash_command.courses.dan)
bot.tree.add_command(slash_command.courses.shindan)
bot.tree.add_command(slash_command.courses.otomodachi)

bot.tree.add_command(slash_command.collection.titles)
bot.tree.add_command(slash_command.collection.icons)
bot.tree.add_command(slash_command.collection.plates)
bot.tree.add_command(slash_command.collection.frames)

bot.tree.add_command(slash_command.cheats.mash)
bot.tree.add_command(slash_command.cheats.hold)

bot.tree.add_command(slash_command.border.border)

@bot.event
async def on_ready():
	synced = await bot.tree.sync()
	# print(synced)

# print(bot.tree.get_commands())
bot.run(os.getenv("BOT_TOKEN"))

