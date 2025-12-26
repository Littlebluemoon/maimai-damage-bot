from discord.ext import commands
from datasource.Collection import get_title_for_song
from paginator import Paginator

@commands.command()
async def collection(ctx, *, query):
	titles = get_title_for_song(query)
	pages = [titles[i:i+4] for i in range(0, len(titles), 4)]
	await Paginator.Multi().start(ctx, message=f"Total of **{len(titles)}** related title(s):", pages=pages)