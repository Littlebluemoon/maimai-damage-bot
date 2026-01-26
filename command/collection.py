import discord
from discord.ext import commands
from datasource.Collection import get_title_for_song, get_icon_for_song
from paginator import Paginator

@commands.command()
async def collection(ctx, *, query):
	await ctx.send("**collection** has moved to **titles** and **icons**! "
				   "Use these commands to find your desired type of collection.")

@commands.command()
async def titles(ctx, *, query):
	data = get_title_for_song(query)
	titles = data['pages']
	song_title = data['title']
	if len(titles) == 0:
		await ctx.send(f"No titles related to **{song_title}** was found.")
	pages = [titles[i:i+4] for i in range(0, len(titles), 4)]
	await Paginator.Multi().start(ctx, message=f"Total of **{len(titles)}** titles related to **{song_title}**:",
								  pages=pages)

@commands.command()
async def icons(ctx, *, query):
	icons, files = get_icon_for_song(query)
	if len(icons) == 0:
		await ctx.send(f"No icons related to **{icons['title']}**.")
	pages = [icons[i:i+4] for i in range(0, len(icons['pages']), 4)]
	await Paginator.Multi().start(ctx, pages=pages, files=files)