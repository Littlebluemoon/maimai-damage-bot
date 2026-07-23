import discord
from discord.ext import commands

from constants import DIFFICULTY_MAPPING, DIFF_NAME_MAPPING, STD_EMOJI, DX_EMOJI, DIFF_COLOR
from datasource.SongData import query_chart_stats_by_id
from exceptions.SongQueryException import IncorrectChartTypeException, NoSongFoundException, DeletedSongFoundException, \
	LowConfidenceException, NoChartFoundException
from command.songdata import get_song_object
from utils.heatmap import generate_song_heatmap

@commands.command()
async def heatmap(ctx, chart_type: str, diff: str, *, query: str):
	try:
		diff = DIFFICULTY_MAPPING[diff.lower()]
		obj = get_song_object(query)[0]
		# song_id
		target_id = obj.id
		diff_array = [obj.bas, obj.adv, obj.exp, obj.mas, obj.rem]
		if chart_type.lower() not in ['dx', 'st', 'std']:
			raise IncorrectChartTypeException("The chart type code you entered is invalid. Available values: `st, dx, std`")

		if chart_type.lower() in ['st', 'std'] and obj.id > 10000:
			target_id = obj.id - 10000
		elif chart_type.lower() == 'dx' and obj.id < 10000:
			target_id = obj.id + 10000
		chart = query_chart_stats_by_id(target_id, diff)
		heatmap_file = f"{target_id:06}_0{diff}.json"
		heatmap_data = generate_song_heatmap(heatmap_file)
		file = heatmap_data['image']
		embed_title = f"{obj.title}    " + (STD_EMOJI if target_id < 10000 else DX_EMOJI)
		embed_color = DIFF_COLOR[diff]
		embed = discord.Embed(title=embed_title, color=embed_color,
		description=f"""- Note count: {heatmap_data['note_count']}
- Average density: {format(heatmap_data['note_count'] / chart.duration, '.2f')} notes per second
- Maximum measure density: {heatmap_data['max_measure_density']} notes

**Legend**: Pink = Non-Slides, Blue = Slides, Orange = Breaks
""")
		embed.set_image(url='attachment://heatmap.jpeg')
		await ctx.send(embed=embed, file=file)
	except NoSongFoundException as e:
		await ctx.send(str(e))
	except DeletedSongFoundException as e:
		await ctx.send(str(e))
	except LowConfidenceException as e:
		await ctx.send(str(e))
	except NoChartFoundException as e:
		await ctx.send(str(e))
	except IncorrectChartTypeException as e:
		await ctx.send(str(e))
	except KeyError as e:
		await ctx.send(
			"The difficulty code you entered is invalid. Available values: `bas, adv, exp, mas, rem, remas` (or their full forms)")