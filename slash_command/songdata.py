import discord
from discord import app_commands

from command.songdata import get_song_object
from datasource.SongData import generate_song_card
from exceptions.SongQueryException import NoSongFoundException, DeletedSongFoundException, LowConfidenceException
from paginator import Paginator
from constants import DIFFICULTY_MAPPING, DIFF_NAME_MAPPING, DIFF_EMOJI
from datasource.SongData import *
from exceptions.SongQueryException import NoSongFoundException, LowConfidenceException, DeletedSongFoundException, \
	IncorrectChartTypeException

@app_commands.command(name="lookup", description="Look up a song")
@app_commands.describe(query="Song name to search for")
async def lookup(interaction: discord.Interaction, query: str):
	try:
		obj = get_song_object(query)
		await interaction.response.send_message(
			embed=generate_song_card(obj)
		)
	except NoSongFoundException as e:
		await interaction.response.send_message(str(e))
	except DeletedSongFoundException as e:
		await interaction.response.send_message(str(e))
	except LowConfidenceException as e:
		await interaction.response.send_message(str(e))

@app_commands.command(name="detail", description="Look up a song")
@app_commands.describe(chart_type="Chart type (ST/DX)",
                       diff="Chart difficulty",
                       query="Song name")
async def detail(ctx, chart_type: str, diff: str, *, query: str):
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

		await Paginator.Multi().start(ctx, pages=generate_chart_detail(target_id, diff))
	except NoSongFoundException as e:
		await ctx.response.send_message(str(e))
	except DeletedSongFoundException as e:
		await ctx.response.send_message(str(e))
	except LowConfidenceException as e:
		await ctx.response.send_message(str(e))
	except NoChartFoundException as e:
		await ctx.response.send_message(str(e))
	except IncorrectChartTypeException as e:
		await ctx.response.send_message(str(e))
	except KeyError as e:
		await ctx.response.send_message("The difficulty code you entered is invalid. Available values: `bas, adv, exp, mas, rem, remas` (or their full forms)")

@app_commands.command(name="find", description="Find all charts with a given difficulty, or chart constant")
@app_commands.describe(cc="Chart level or chart constant")
async def find(ctx, cc: str):
	try:
		song_list = find_song_by_difficulty(cc)
		song_data_lines = []
		cnt = 1
		for i in [4, 3, 2, 1, 0]:
			for song in song_list[i]:
				difficulty_array = [song.bas, song.adv, song.exp, song.mas, song.rem]
				if '.' in cc:
					song_data_lines.append(f"{cnt}. {DIFF_EMOJI[i]} {STD_EMOJI if song.id < 10000 else DX_EMOJI} {song.title}")
				else:
					song_data_lines.append(
						f"{cnt}. **[{difficulty_array[i]}]** {DIFF_EMOJI[i]} {STD_EMOJI if song.id < 10000 else DX_EMOJI} {song.title}")
				cnt += 1
		pages = [song_data_lines[i:i+10] for i in range(0, len(song_data_lines), 10)]
		emb = [[Embed(title="",
					 description='\n'.join(x))] for x in pages]
		if cnt == 1:
			if '.' in cc:
				await ctx.response.send_message(f"No songs was found with chart constant **{cc}**.")
			else:
				await ctx.response.send_message(f"No songs was found with level **{cc}**.")
		else:
			if '.' in cc:
				await Paginator.Multi().start(ctx,
											  message=f"There are **{cnt - 1}** songs with chart constant **{cc}**:",
											  pages=emb)
			else:
				await Paginator.Multi().start(ctx,
											  message=f"There are **{cnt - 1}** songs with level **{cc}**:",
											  pages=emb)


	except InvalidChartConstantException as e:
		await ctx.response.send_message(str(e))
	except InvalidChartLevelException as e:
		await ctx.response.send_message(str(e))