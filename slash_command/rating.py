import math

from discord import app_commands
from constants import RANK, ACHV
from utils.charts import generate_calculate_command_card, generate_rating_table
from paginator import Paginator

@app_commands.command(name="rating", description="Calculate rating based on chart constant and achievement rate")
@app_commands.describe(cc="Chart constant", rate="Achievement rate as a decimal")
async def rating(ctx, cc: str, rate: str):
	cc = float(cc)
	rate = float(rate)
	if cc < 1 or cc > 15:
		await ctx.response.send_message("Chart constant must be between **1.0** and **15.0**")
	elif rate > 101:
		await ctx.response.send_message("Achievement rate must be between **0.0000** and **101.0000**")
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
		await ctx.response.send_message(msg)


@app_commands.command(name="target", description="What rating do you want to get?")
@app_commands.describe(tgt_rating="Targeted rating value")
async def target(ctx, tgt_rating: str):
	if int(tgt_rating) <= 0:
		await ctx.response.send_message(f"Rating to target should be higher than 0")
	elif int(tgt_rating) == 338:
		await ctx.response.send_message(f"The only way to reach **338** rating is by scoring an AP on a Lv. 15 chart!")
	elif int(tgt_rating) > 338:
		await ctx.response.send_message(f"We will need a 15.1 for that")
	else:
		data = generate_rating_table(tgt_rating)
		await Paginator.Multi().start(ctx, pages=data['embeds'])

@app_commands.command(name="calculate", description="Calculate all possible rating values possible for a chart constant")
@app_commands.describe(cc="Chart constant")
async def calculate(ctx, cc: str):
	card = generate_calculate_command_card(cc)
	if not card:
		await ctx.response.send_message("You entered an invalid chart constant value. Must be between **1.0** and **15.0**")
	await Paginator.Multi().start(ctx, pages=card)
