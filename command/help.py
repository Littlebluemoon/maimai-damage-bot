from discord.ext import commands

from datasource.Help import get_help_embed
from exceptions.HelpCommandException import CommandNotFoundException

@commands.command()
async def help(ctx, command):
	try:
		await ctx.send(embed=get_help_embed(command))
	except CommandNotFoundException as e:
		await ctx.send(str(e))