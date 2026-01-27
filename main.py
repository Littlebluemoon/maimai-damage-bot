import os

import certifi
import discord
from discord.ext import commands
from dotenv import load_dotenv

from command.info import info

load_dotenv()
from command.songdata import lookup, detail, find
from command.rating import rating, target, calculate
from command.courses import dan, shindan, otomodachi
from command.collection import collection, titles, icons, plates, frames
from command.cheats import hold, mash
from command.damage import damage
from command.border import border
from command.help import help

intents = discord.Intents.default()
intents.message_content = True

os.environ["SSL_CERT_FILE"] = certifi.where()

bot = commands.Bot(command_prefix='m$', intents=intents)
bot.help_command = None

bot.add_command(info)
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

bot.run(os.getenv("BOT_TOKEN"))