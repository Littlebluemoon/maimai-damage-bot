import discord
from discord.ext import commands
from datasource.Collection import get_title_for_song, get_icon_for_song, get_plate_for_song, get_frame_for_song
from paginator import Paginator

@commands.command()
async def collection(ctx, *, query):
	await ctx.send("**collection** has moved to **titles**, **icons**, **plates** and **frames**!\n"
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
	files = [files[i:i+4] for i in range(0, len(icons['pages']), 4)]
	pages = [icons['pages'][i:i+4] for i in range(0, len(icons['pages']), 4)]
	await Paginator.Multi().start(ctx, pages=pages, files=files)

@commands.command(aliases=['nameplates'])
async def plates(ctx, *, query):
	plates, files = get_plate_for_song(query)
	if len(plates) == 0:
		await ctx.send(f"No nameplates related to **{icons['title']}**.")
	files = [[i] for i in files]
	pages = [[i] for i in plates['pages']]
	await Paginator.Multi().start(ctx, pages=pages, files=files)

@commands.command()
async def frames(ctx, *, query):
	plates, files = get_frame_for_song(query)
	if len(plates) == 0:
		await ctx.send(f"No frames related to **{icons['title']}**.")
	files = [[i] for i in files]
	pages = [[i] for i in plates['pages']]
	await Paginator.Multi().start(ctx, pages=pages, files=files)