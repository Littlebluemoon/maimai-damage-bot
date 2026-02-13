from fractions import Fraction

from discord import Embed
from discord.ext import commands

from command.songdata import get_song_object
from constants import DIFFICULTY_MAPPING, STD_EMOJI, DX_EMOJI
from datasource.SongData import query_chart_stats_by_id
from exceptions.BorderException import TooManyBreaksException
from exceptions.SongQueryException import IncorrectChartTypeException, NoSongFoundException, DeletedSongFoundException, \
	LowConfidenceException, NoChartFoundException
from utils.border import calculate_chart_border
from utils.charts import convert_cc_to_difficulty


@commands.command()
async def border(ctx, chart_type, diff, query, brk=None):
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
		warning_text = ""
		chart_obj = query_chart_stats_by_id(target_id, diff)
		weight = (chart_obj.num_tap + 2 * chart_obj.num_hld + 3 * chart_obj.num_sld
				  + chart_obj.num_ttp + chart_obj.num_brk * 5)
		if brk is None:
			brk = chart_obj.num_brk // 10
			warning_text = ("No High Perfect Break count specified, "
				"using 10% of the break count rounded down: **") + str(brk) + "**."
		else:
			brk = int(brk)
			if chart_obj.num_brk * 2 < brk:
				raise TooManyBreaksException("Break count specified exceed double the chart's note count.")
		init_score = str(int(1010000 - Fraction(2500, chart_obj.num_brk) * brk))
		lost_score = int(Fraction(2500, chart_obj.num_brk) * brk)
		init_score = init_score[:-4] + '.' + init_score[-4:] + '%'
		# Always lower than 1
		lost_score = '-0.' + str(lost_score).zfill(4) + '%'
		embed_title = obj.title + '   ' + STD_EMOJI if target_id < 10000 else DX_EMOJI
		embed_desc = obj.artist
		emb = Embed(title=embed_title, description=embed_desc)
		emb.add_field(name="Difficulty", value=f"{convert_cc_to_difficulty(diff_array[diff])} ({diff_array[diff]})", inline=True)
		emb.add_field(name="Weight", value=weight, inline=True)
		emb.add_field(name="Remaining score", value=f"{init_score} ({lost_score})", inline=True)
		emb.add_field(name="Estimated borders", value=calculate_chart_border(chart_obj, brk))
		emb.set_footer(text="Great/Good/Miss are calculated based on tap notes.\n"
								  "The results showed is for reference only, you might be able to get "
								  "one more great taps or two, and still be able to reach targeted ranks.")
		emb.set_thumbnail(url=f'https://dp4p6x0xfi5o9.cloudfront.net/maimai/img/cover/{obj.jacket}')
		await ctx.send(warning_text, embed=emb)

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
	except TooManyBreaksException as e:
		await ctx.send(str(e))
	except ValueError as e:
		await ctx.send(str(e) +'\nThis error must have been thrown because your song title has more than one word. If that is the case, wrap the song title around quotes.')
	except KeyError as e:
		await ctx.send("The difficulty code you entered is invalid. Available values: `bas, adv, exp, mas, rem, remas` (or their full forms)")