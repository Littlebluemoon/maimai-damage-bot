from discord import app_commands

from datasource.Course import get_course_card, get_otomodachi_course
from exceptions.CourseException import GradeNotFoundException, RankNotFoundException


@app_commands.command(name='dan', description='Retrieve a dan course\'s track list')
@app_commands.describe(course_id="Dan course level")
async def dan(ctx, course_id: str):
	try:
		if int(course_id) > 10:
			await ctx.response.send_message("Course ID invalid. Accepted values: 1~10.\n"
						   "If you are looking for 真段 courses, use shindan instead.")
		else:
			data = get_course_card(course_id)
			await ctx.response.send_message(data['flavor_text'], embeds=data['embeds'])
	except GradeNotFoundException as e:
		await ctx.response.send_message(str(e) + ' Accepted values: 1~10.')

@app_commands.command(name='shindan', description='Retrieve a shindan course\'s track list')
@app_commands.describe(course_id="Shindan course level; use kai for 真皆伝, ura for 裏皆伝")
async def shindan(ctx, course_id: str):
	if course_id.lower() == 'kai':
		data = get_course_card(21)
	elif course_id.lower() == 'ura':
		data = get_course_card(22)
	else:
		if int(course_id) not in range(1, 13):
			await ctx.response.send_message("Course ID invalid. Accepted values: 1~10, kai or 11 (for 真皆伝), ura or 12 (for 裏皆伝).")
		else:
			data = get_course_card(int(course_id)+10)
	await ctx.response.send_message(data['flavor_text'], embeds=data['embeds'])

@app_commands.command(name='otomodachi', description='Retrieve the boss track list in Otomodachi Battle')
@app_commands.describe(grade="Rank range, from A to SSS")
async def otomodachi(ctx, grade: str):
	try:
		await ctx.response.send_message(embeds=get_otomodachi_course(grade))
	except RankNotFoundException as e:
		await ctx.response.send_message(str(e))
