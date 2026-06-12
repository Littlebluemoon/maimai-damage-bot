import discord
from discord import app_commands

from datasource.Help import get_help_embed
from exceptions.HelpCommandException import CommandNotFoundException


@app_commands.command(name="help", description="Get help about usage of this bot, or a command")
@app_commands.describe(command="Command that you need help with (optional). If unspecified, returns a generic help message")
async def help(ctx, command: str = 'help'):
	try:
		await ctx.response.send_message(embed=get_help_embed(command))
	except CommandNotFoundException as e:
		await ctx.response.send_message(str(e))