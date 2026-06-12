import discord
from discord import app_commands

from command.damage import get_play_data_table, process_damage, generate_damage_table, generate_damage_table_text
from exceptions.DamageCommandException import NotReplyToPlayRecordException, ImpossiblePlayRecordException

# Slash commands could not be used to reply to any messages.
# That's so sad.

# There's a workaround, by letting this command blindly target the last message fired by mimi xd bot,
# but like, why

# Just use the prefix command instead

# @app_commands.command(name="damage", description="Show how much score you lost")
# async def damage(ctx):
# 	try:
# 		msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
# 		if msg is None:
# 			raise NotReplyToPlayRecordException("This command was not used to reply to any message.\n"
# 						"Try again while replying to a message.")
# 		msg_text = get_play_data_table(msg)
# 		damage_table = process_damage(msg_text)
# 		if damage_table is None:
# 			raise ImpossiblePlayRecordException("This play result is impossible in normal play.\n"
# 							"If you got the score legitimately and think that it's a bug, please contact the author.")
# 		damage_table = generate_damage_table(damage_table)
# 		table_text = generate_damage_table_text(damage_table)
# 		emb = discord.Embed(title=msg_text['title'], description="```ansi\n" + table_text + "\n```")
# 		emb.set_author(name="Lost Score Information")
# 		emb.set_thumbnail(url=msg_text['thumb'])
# 		await ctx.send(embed=emb)
# 	except ImpossiblePlayRecordException as e:
# 		await ctx.send(str(e))
# 	except NotReplyToPlayRecordException as e:
# 		await ctx.send(str(e))

