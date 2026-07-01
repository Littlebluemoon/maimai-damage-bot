from discord.ext import commands

from command.songdata import get_song_object
from constants import DIFFICULTY_MAPPING
from datasource.SongData import generate_chart_detail
from exceptions.SongQueryException import IncorrectChartTypeException, NoSongFoundException, DeletedSongFoundException, \
	LowConfidenceException, NoChartFoundException
from paginator import Paginator
from utils.edging import calculate_edging_conditions


@commands.command()
async def edging(ctx, chart_type: str, diff: str, *, query: str):
	try:
		diff = DIFFICULTY_MAPPING[diff.lower()]
		obj = get_song_object(query)[0]
		# song_id
		target_id = obj.id

		if chart_type.lower() not in ['dx', 'st', 'std']:
			raise IncorrectChartTypeException("The chart type code you entered is invalid. Available values: `st, dx, std`")

		if chart_type.lower() in ['st', 'std'] and obj.id > 10000:
			target_id = obj.id - 10000
		elif chart_type.lower() == 'dx' and obj.id < 10000:
			target_id = obj.id + 10000

		await Paginator.Multi().start(ctx, pages=calculate_edging_conditions(target_id, diff))
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
		await ctx.send("The difficulty code you entered is invalid. Available values: `bas, adv, exp, mas, rem, remas` (or their full forms)")