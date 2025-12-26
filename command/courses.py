from discord.ext import commands

from datasource.Course import get_course_card, get_otomodachi_course
from exceptions.CourseException import GradeNotFoundException, RankNotFoundException


@commands.command()
async def dan(ctx, course_id):
	try:
		if int(course_id) > 10:
			await ctx.send("Course ID invalid. Accepted values: 1~10.\n"
						   "If you are looking for 真段 courses, use shindan instead.")
		else:
			data = get_course_card(course_id)
			await ctx.send(data['flavor_text'], embeds=data['embeds'])
	except GradeNotFoundException as e:
		await ctx.send(str(e) + ' Accepted values: 1~10.')

@commands.command()
async def shindan(ctx, course_id):
	if int(course_id) not in range(1, 11) and course_id not in ['kai', 'ura']:
		await ctx.send("Course ID invalid. Accepted values: 1~10, kai or 11 (for 真皆伝), ura or 12 (for 裏皆伝).")
	else:
		if course_id.lower() == 'kai':
			data = get_course_card(21)
		elif course_id.lower() == 'ura':
			data = get_course_card(22)
		else:
			data = get_course_card(int(course_id)+10)
		await ctx.send(data['flavor_text'], embeds=data['embeds'])

@commands.command(aliases=['otomo', 'grade', 'legend'])
async def otomodachi(ctx, grade):
	try:
		await ctx.send(embeds=get_otomodachi_course(grade))
	except RankNotFoundException as e:
		await ctx.send(str(e))
