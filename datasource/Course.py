import ast

from discord import Embed

from exceptions.CourseException import RankNotFoundException, GradeNotFoundException
from models.GradeBattle import GradeBattle
from models.Otomodachi import Otomodachi
from models.SongData import SongData
from utils.database import SessionLocal
from utils.charts import convert_cc_to_difficulty
from datasource.SongData import query_single_by_id
import discord
from constants import DIFF_COLOR, STD_EMOJI, DX_EMOJI, DIFF_NAME_MAPPING, OTOMODACHI_RANK_MAPPING

session = SessionLocal()

def course_song_card(song_id, diff):
	obj = query_single_by_id(song_id)
	title_emoji = STD_EMOJI if obj.type == 'ST' else DX_EMOJI
	embed = discord.Embed(title=f"{obj.title}   {title_emoji}", description=obj.artist,
						  color=DIFF_COLOR[diff])
	embed.add_field(name="**Difficulty:**", value=DIFF_NAME_MAPPING[diff])
	embed.set_thumbnail(url=f"https://dp4p6x0xfi5o9.cloudfront.net/maimai/img/cover/{obj.jacket}")
	if diff == 0:
		diff_str = f"**{convert_cc_to_difficulty(obj.bas)}** ({obj.bas})"
	elif diff == 1:
		diff_str = f"**{convert_cc_to_difficulty(obj.adv)}** ({obj.adv})"
	elif diff == 2:
		diff_str = f"**{convert_cc_to_difficulty(obj.exp)}** ({obj.exp})"
	elif diff == 3:
		diff_str = f"**{convert_cc_to_difficulty(obj.mas)}** ({obj.mas})"
	elif diff == 4:
		diff_str = f"**{convert_cc_to_difficulty(obj.rem)}** ({obj.rem})"
	embed.add_field(name="**Level:**", value=diff_str)
	return embed


def get_course_card(course_id):
	course_data = session.query(GradeBattle).filter(GradeBattle.id == course_id).one()
	if not course_data:
		raise GradeNotFoundException("Course ID invalid.")
	flavor_text = (f"**{course_data.name}**: {course_data.max} LIFE, "
				   f"-{course_data.great} / -{course_data.good} / -{course_data.miss} / +{course_data.clear}")
	embeds = [
		course_song_card(course_data.t1, course_data.t1_diff),
		course_song_card(course_data.t2, course_data.t2_diff),
		course_song_card(course_data.t3, course_data.t3_diff),
		course_song_card(course_data.t4, course_data.t4_diff),
	]
	return {
		'flavor_text': flavor_text,
		'embeds': embeds
	}

def get_otomodachi_course(rank):
	rank = rank.lower()
	if rank not in ['a', 's', 'ss', 'sss']:
		raise RankNotFoundException("Rank is invalid. Available values: A, S, SS, SSS")
	elif rank in ['b', 'c', 'd']:
		raise RankNotFoundException("Boss tracks are unavailable for grade B or below -- you automatically go up a "
									"rank while in grade B or below.")
	rank_list = [rank.upper() + str(x) for x in [5, 4, 3, 2, 1]]
	songs = session.query(Otomodachi).filter(Otomodachi.rank.in_(rank_list)).all()

	embed = []
	for song in songs:
		if song.boss == '???':
			tmp = Embed(title="???",
						description="???",
						color=DIFF_COLOR[3])
			tmp.add_field(name="Boss Rank: ", value="SSS1", inline=True)
			# buffer
			tmp.add_field(name="VS:", value="???", inline=True)
			tmp.add_field(name="Difficulty: ",
						  value=f"**14+** (???)",
						  inline=True)
			tmp.add_field(name="Boss Strength: ", value=f"**MAX** (101.0000%)")
			tmp.add_field(name="Score Range: ", value=f"??? ~ ???")
			embed.append(tmp)
		else:
			song_obj = query_single_by_id(int(song.boss))
			tmp = Embed(title=f"{song_obj.title}    {DX_EMOJI if int(song.boss) >= 10000 else STD_EMOJI}",
						description=song_obj.artist,
						color=DIFF_COLOR[int(song.bossDifficulty)])
			song_diff = [song_obj.bas, song_obj.adv, song_obj.exp, song_obj.mas, song_obj.rem]
			score_range = ast.literal_eval(song.scoreRange)
			score_range = [str(x)[:-4] + '.' + str(x)	[-4:] for x in score_range]
			tmp.add_field(name="Boss Rank: ", value=song.rank, inline=True)
			#buffer
			tmp.add_field(name="VS:", value=song.playerName, inline=True)
			tmp.add_field(name="Difficulty: ",
						  value=f"**{convert_cc_to_difficulty(song_diff[int(song.bossDifficulty)])}** ({song_diff[int(song.bossDifficulty)]})",
						  inline=True)
			tmp.add_field(name="Boss Strength: ", value=f"**{song.bossStrength}** ({OTOMODACHI_RANK_MAPPING[song.bossStrength]})")
			tmp.add_field(name="Score Range: ", value=f"{score_range[0]}% ~ {score_range[1]}%")
			tmp.set_thumbnail(url=f"https://dp4p6x0xfi5o9.cloudfront.net/maimai/img/cover/{song_obj.jacket}")
			embed.append(tmp)
	return embed