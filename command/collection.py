import discord
from discord.ext import commands
from datasource.Collection import get_title_for_song, get_icon_for_song
from paginator import Paginator

@commands.command()
async def collection(ctx, *, query):
	await ctx.send("*collection* has moved to *titles* and *icons*! "
				   "Use these commands to find your desired type of collection.")

@commands.command()
async def titles(ctx, *, query):
	titles = get_title_for_song(query)
	pages = [titles[i:i+4] for i in range(0, len(titles), 4)]
	await Paginator.Multi().start(ctx, pages=pages)

@commands.command()
async def icons(ctx, *, query):
	icons, files = get_icon_for_song(query)
	pages = [icons[i:i+4] for i in range(0, len(icons), 4)]
	await Paginator.Multi().start(ctx, pages=pages, files=files)