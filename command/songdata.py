from discord.ext import commands

from paginator import Paginator
from constants import DIFFICULTY_MAPPING, DIFF_NAME_MAPPING, DIFF_EMOJI
from datasource.SongData import *
from exceptions.SongQueryException import NoSongFoundException, LowConfidenceException, DeletedSongFoundException, \
	IncorrectChartTypeException


def get_song_object(query: str):
	target_db = find_song_title_from_db(query)
	target_alias = find_song_title_from_aliases(query)
	if target_db[1] >= target_alias[1]:
		target = target_db
	else:
		target = target_alias
	if target[0] is None:
		raise NoSongFoundException("No such song was found.")

	if target:
		if not target[2]:
			raise LowConfidenceException(f"I am not so sure about your query... "
					f"Are you looking for **{target[0]}** ({round(target[1], 2)} % match)?)")
		else:
			try:
				## FUCK THESE SONGS
				if query.lower() in ['link maimai', 'link (maimai)']:
					obj = [query_single_by_id(131)]
				elif query.lower() in ['link nico', 'link2', 'link circle of friends', 'link (circle of friends)']:
					obj = [query_single_by_id(383)]
				else:
					obj = query_single(target[0])
				return obj
			except Exception:
				raise DeletedSongFoundException("No such song was found or an unexpected error has occured.")

@commands.command()
async def lookup(ctx, *, query: str):
	try:
		obj = get_song_object(query)
		await ctx.send(embed=generate_song_card(obj))
	except NoSongFoundException as e:
		await ctx.send(str(e))
	except DeletedSongFoundException as e:
		await ctx.send(str(e))
	except LowConfidenceException as e:
		await ctx.send(str(e))
	# except IndexError as e:
	# 	await ctx.send("No such song was found. This error occured probably because you tried to "
	# 				   "look up a deleted song.")

@commands.command()
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

@commands.command()
async def find(ctx, cc):
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
				await ctx.send(f"No songs was found with chart constant **{cc}**.")
			else:
				await ctx.send(f"No songs was found with level **{cc}**.")
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
		await ctx.send(str(e))
	except InvalidChartLevelException as e:
		await ctx.send(str(e))