import math

from discord.ext import commands
from constants import RANK, ACHV
from utils.charts import generate_calculate_command_card, generate_rating_table
from paginator import Paginator

@commands.command()
async def rating(ctx, cc, rate):
	cc = float(cc)
	rate = float(rate)
	if cc < 1 or cc > 15:
		await ctx.send("Chart constant must be between **1.0** and **15.0**")
	elif rate > 101:
		await ctx.send("Achievement rate must be between **0.0000** and **101.0000**")
	else:
		rate = '{:.4f}'.format(rate)
		cc = '{:.1f}'.format(cc)
		achv_rate = int(str(rate).replace('.', ''))
		for i in range(len(ACHV)):
			if achv_rate < ACHV[i]:
				i -= 1
				break
			elif achv_rate == ACHV[i]:
				break
		msg = f'A chart with a difficulty of {cc} and a score of {rate}% would award you **{math.floor(min(1005000, achv_rate) * RANK[i] * float(cc) / 10000000)}** rating.'''
		if int(rate.replace('.', '')) >= 1005000:
			msg += f'\n- If you achieved an All Perfect, you will get **{math.floor(min(1005000, achv_rate) * RANK[i] * float(cc) / 10000000) + 1}** rating instead.'


@commands.command()
async def target(ctx, tgt_rating):
	if int(tgt_rating) <= 0:
		await ctx.send(f"Rating to target should be higher than 0")
	elif int(tgt_rating) > 338:
		await ctx.send(f"We will need a 15.1 for that")
	else:
		data = generate_rating_table(tgt_rating)
		await Paginator.Multi().start(ctx, pages=data['embeds'])

@commands.command()
async def calculate(ctx, cc):
	card = generate_calculate_command_card(cc)
	if not card:
		await ctx.send("You entered an invalid chart constant value. Must be between **1.0** and **15.0**")
	await Paginator.Multi().start(ctx, pages=card)
