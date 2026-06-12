from discord import app_commands

from datasource.Collection import get_title_for_song, get_icon_for_song, get_plate_for_song, get_frame_for_song
from paginator import Paginator


# @app_commands.command(name='')
# async def collection(ctx, *, query):
# 	await ctx.send("**collection** has moved to **titles**, **icons**, **plates** and **frames**!\n"
# 				   "Use these commands to find your desired type of collection.")

@app_commands.command(name='titles', description='Retrieve a list of titles from a song')
@app_commands.describe(query='Song name to look up')
async def titles(ctx, *, query: str):
	data = get_title_for_song(query)
	titles = data['pages']
	song_title = data['title']
	if len(titles) == 0:
		await ctx.response.send_message(f"No titles related to **{song_title}** was found.")
	pages = [titles[i:i+4] for i in range(0, len(titles), 4)]
	await Paginator.Multi().start(ctx, message=f"Total of **{len(titles)}** titles related to **{song_title}**:",
								  pages=pages)

@app_commands.command(name='icons', description='Retrieve a list of icons from a song')
@app_commands.describe(query='Song name to look up')
async def icons(ctx, *, query: str):
	icons, files = get_icon_for_song(query)
	if len(icons['pages']) == 0:
		await ctx.response.send_message(f"No icons related to **{icons['title']}**.")
	files = [files[i:i+4] for i in range(0, len(icons['pages']), 4)]
	pages = [icons['pages'][i:i+4] for i in range(0, len(icons['pages']), 4)]
	await Paginator.Multi().start(ctx, pages=pages, files=files)

@app_commands.command(name='plates', description='Retrieve a list of nameplates from a song')
@app_commands.describe(query='Song name to look up')
async def plates(ctx, *, query: str):
	plates, files = get_plate_for_song(query)
	if len(plates['pages']) == 0:
		await ctx.response.send_message(f"No nameplates related to **{plates['title']}**.")
	files = [[i] for i in files]
	pages = [[i] for i in plates['pages']]
	await Paginator.Multi().start(ctx, pages=pages, files=files)

@app_commands.command(name='frames', description='Retrieve a list of frames from a song')
@app_commands.describe(query='Song name to look up')
async def frames(ctx, *, query: str):
	frames, files = get_frame_for_song(query)
	if len(frames['pages']) == 0:
		await ctx.response.send_message(f"No frames related to **{frames['title']}**.")
	print(files)
	files = [[i] for i in files]
	pages = [[i] for i in frames['pages']]
	await Paginator.Multi().start(ctx, pages=pages, files=files)