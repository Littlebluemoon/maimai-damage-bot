import os
from typing import List

from rapidfuzz import fuzz
from datasource.BPM import find_bpm
from exceptions.SongQueryException import NoChartFoundException, InvalidChartLevelException, \
	InvalidChartConstantException
from models.SongData import SongData
from models.Stats import Stats00, Stats01, Stats02, Stats03, Stats04
from utils.database import SessionLocal
from utils.charts import convert_cc_to_difficulty
from constants import NOTE_NAMES, NOTE_MULTIPLIER_BY_INDEX, GREAT, GOOD, MISS, PERFECT, STD_EMOJI, DX_EMOJI, DIFF_COLOR, \
	LEVEL_LIST
from discord import Embed


session = SessionLocal()

# From DB (by title)
song_data_full = session.query(SongData).all()

# From aliases list
aliases = []
with open(os.getenv("ALIAS_PATH"), "r", encoding="utf-8") as f:
	lines = f.readlines()
	for line in lines:
		aliases.append(line.split('\t'))

def convert_to_timestamp(value: float):
	return f"{int(value // 60)}:{format(value % 60, '06.3f')}"

def find_song_title_from_db(query: str):
	ratio = 0
	match_name = ""
	for item in song_data_full:
		current_ratio = fuzz.ratio(query.lower(), item.title.lower())
		if current_ratio >= ratio:
			match_name = item.title.strip()
			ratio = current_ratio
			print(f"New match: {match_name} {ratio}")
	if ratio >= 70:
		return match_name, ratio, True
	if ratio >= 50:
		return match_name, ratio, False
	return None, 0, False

def find_song_title_from_aliases(query: str):
	ratio = 0
	match_name = ""
	for (cnt, line) in enumerate(aliases):
		for item in line:
			current_ratio = fuzz.ratio(query.lower(), item.lower())
			if "false amber" in line:
				print(query, item, current_ratio)
			if current_ratio >= ratio:
				match_name = aliases[cnt][0].strip()
				ratio = current_ratio
				print(f"New match: {match_name} {ratio}")
	if ratio >= 70:
		return match_name, ratio, True
	if ratio >= 50:
		return match_name, ratio, False
	return None, 0, False

def get_aliases(query: str):
	for item in aliases:
		if query.lower() == item[0].lower():
			return ', '.join(item[1:])
	return ''

def query_single(query: str):
	return session.query(SongData).filter(SongData.title == query).all()

def query_single_by_id(song_id: int):
	return session.query(SongData).filter(SongData.id == song_id).one()

def find_song_by_difficulty(cc, mode='cc'):
	if '.' not in cc:
		mode = 'difficulty'
	if mode == 'difficulty':
		if cc not in LEVEL_LIST:
			raise InvalidChartLevelException(f"Not a valid chart level: {cc}.")
		if '+' not in cc:
			level_range = [x / 10 for x in range(int(cc) * 10, int(cc) * 10 + 6)]
		else:
			level_range = [x / 10 for x in range(int(cc[:-1]) * 10 + 6, int(cc[:-1]) * 10 + 10)]
		find_results = [
			session.query(SongData).filter(SongData.bas.in_(level_range)).all(),
			session.query(SongData).filter(SongData.adv.in_(level_range)).all(),
			session.query(SongData).filter(SongData.exp.in_(level_range)).all(),
			session.query(SongData).filter(SongData.mas.in_(level_range)).all(),
			session.query(SongData).filter(SongData.rem.in_(level_range)).all()]
	else:
		if len(cc) - cc.find('.') != 2:
			raise InvalidChartConstantException("Invalid chart constant. Only 1 decimal point for chart constants.")
		try:
			cc = float(cc)
			if cc < 1.0 or cc > 15.0:
				raise InvalidChartConstantException("Invalid chart constant. Must be between 1.0 and 15.0 (inclusive).")
			find_results = [session.query(SongData).filter(SongData.bas == cc).all(),
					session.query(SongData).filter(SongData.adv == cc).all(),
					session.query(SongData).filter(SongData.exp == cc).all(),
					session.query(SongData).filter(SongData.mas == cc).all(),
					session.query(SongData).filter(SongData.rem == cc).all()]
		except ValueError:
			raise InvalidChartConstantException(f"Invalid chart constant. Following value is likely not a number: {cc}")
	return find_results

def generate_song_card(obj: List[SongData]):
	title = obj[0].title
	aka = ''
	if get_aliases(title).strip() != '':
		aka = '-#' + get_aliases(title).strip()
	artist = obj[0].artist
	category = obj[0].category
	version_str = ""
	for chart in obj:
		version_str += f"- **{chart.type}**: {chart.version}"
		if chart.release:
			version_str += f" ({chart.release})"
		version_str += '\n'
	version_str = version_str.strip()
	thumb_url = f"https://dp4p6x0xfi5o9.cloudfront.net/maimai/img/cover/{obj[0].jacket}"
	diff_str = ""
	for chart in obj:
		diff_str += (f"- **{chart.type}**: **{convert_cc_to_difficulty(chart.bas)}** ({chart.bas}) / "
					 f"**{convert_cc_to_difficulty(chart.adv)}** ({chart.adv}) / "
					 f"**{convert_cc_to_difficulty(chart.exp)}** ({chart.exp}) / "
					 f"**{convert_cc_to_difficulty(chart.mas)}** ({chart.mas})")
		if chart.rem:
			diff_str += f" / **{convert_cc_to_difficulty(chart.rem)}** ({chart.rem})"
		diff_str += '\n'
	diff_str = diff_str.strip()
	bpm = find_bpm(obj[0].id)['def']
	embed = Embed(title=title,
				 description=f"""
{aka}""")
	embed.add_field(name="", value=artist, inline=False)
	embed.add_field(name="", value=f"""
**Category**: {category}
**Version**: 
{version_str}
**BPM**: {str(bpm)}
**Difficulty**:
{diff_str}
""")
	embed.set_thumbnail(url=thumb_url)
	return embed

def query_chart_stats_by_id(chart_id, diff):
	try:
		if diff == 0:
			obj = session.query(Stats00).filter(Stats00.id == chart_id).one()
		if diff == 1:
			obj = session.query(Stats01).filter(Stats01.id == chart_id).one()
		if diff == 2:
			obj = session.query(Stats02).filter(Stats02.id == chart_id).one()
		if diff == 3:
			obj = session.query(Stats03).filter(Stats03.id == chart_id).one()
		if diff == 4:
			obj = session.query(Stats04).filter(Stats04.id == chart_id).one()
		return obj
	except Exception as e:
		raise NoChartFoundException("The song name, or the chart type/difficulty is incorrect.")


def generate_chart_detail(chart_id, diff):
	song_obj = query_single_by_id(chart_id)
	if not song_obj:
		return None
	diff_array = [song_obj.bas, song_obj.adv, song_obj.exp, song_obj.mas, song_obj.rem]
	obj = query_chart_stats_by_id(chart_id, diff)

	weight = obj.num_tap + 2 * obj.num_hld + 3 * obj.num_sld + 5 * obj.num_brk + obj.num_ttp
	tap_value = 100 / float(weight)
	break_value = 1 / float(obj.num_brk)
	embed_text = f"""
**General**
- Level: {convert_cc_to_difficulty(diff_array[diff])} ({diff_array[diff]})
- Notes Designer: {obj.charter}
- Note count: {obj.num_all}
- Total chart weight: {weight} ({format(tap_value, '.4f')} % per tap)
**Notes**
"""
	note_type_array = [obj.num_tap, obj.tap + obj.str, obj.xtp + obj.xst,
					   obj.num_hld, obj.hld, obj.xho, obj.tho,
					   obj.sld,
					   obj.ttp,
					   obj.num_brk, obj.brk + obj.bst, obj.bxx + obj.xbs, obj.bho, obj.bxh, obj.bsl]
	print(f"len : {len(note_type_array)}")
	for (i, item) in enumerate(note_type_array):
		if i in [0, 3, 7, 8, 9]:
			if item != 0:
				multiplier = NOTE_MULTIPLIER_BY_INDEX[i]
				embed_text += (f"- **{NOTE_NAMES[i]}: {item} "
							   f"({format(tap_value * item * multiplier + int(i == 9), '.4f')} %)**\n")
		else:
			if item != 0:
				multiplier = 1
				bonus = 0
				if i in range(4, 7):
					multiplier = 2
				if i == 7:
					multiplier = 3
				if i in range(9, 99):
					multiplier = 5
					bonus = item * break_value
				embed_text += f"  - {NOTE_NAMES[i]}: {item} ({format(tap_value * item * multiplier + bonus, '.4f')} %)\n"
	# to Embed
	chart_type_emoji = STD_EMOJI if chart_id < 10000 else DX_EMOJI
	emb = Embed(title=f"{song_obj.title}   {chart_type_emoji}", description=f"{song_obj.artist}\n{embed_text}",
				color=DIFF_COLOR[diff])
	emb.set_thumbnail(url=f"https://dp4p6x0xfi5o9.cloudfront.net/maimai/img/cover/{song_obj.jacket}")
	emb.set_author(name="General song data")
	# damage table
	stat_obj = query_chart_stats_by_id(chart_id, diff)
	weight = (stat_obj.num_tap + 2 * stat_obj.num_hld + 3 * stat_obj.num_sld
			  + 5 * stat_obj.num_brk + stat_obj.num_ttp)
	tap_value = 100 / float(weight)
	break_value = 1 / float(stat_obj.num_brk)
	ttp_dmg = tap_dmg = [format(tap_value * 0.2, '.4f'), format(tap_value * 0.5, '.4f'), format(tap_value, '.4f')]
	hld_dmg = [format(tap_value * 0.4, '.4f'), format(tap_value, '.4f'), format(tap_value * 2, '.4f')]
	sld_dmg = [format(tap_value * 0.6, '.4f'), format(tap_value * 1.5, '.4f'), format(tap_value * 3, '.4f')]
	brk_dmg = [['-', format(break_value * 0.25, '.4f'), format(break_value * 0.25, '.4f')],
			   ['-', format(break_value * 0.5, '.4f'), format(break_value * 0.5, '.4f')],
			   [format(tap_value, '.4f'), format(break_value * 0.6, '.4f'),
				format(break_value * 0.6 + tap_value, '.4f')],
			   [format(tap_value * 2, '.4f'), format(break_value * 0.6, '.4f'),
				format(tap_value * 2 + break_value * 0.6, '.4f')],
			   [format(tap_value * 2.5, '.4f'), format(break_value * 0.6, '.4f'),
				format(tap_value * 2.5 + break_value * 0.6, '.4f')],
			   [format(tap_value * 3, '.4f'), format(break_value * 0.7, '.4f'),
				format(tap_value * 3 + break_value * 0.7, '.4f')],
			   [format(tap_value * 5, '.4f'), format(break_value, '.4f'), format(tap_value * 5 + break_value, '.4f')]]
	damage_ctx = f"""```ansi
      \t\t   Great\t    Good\t    Miss
TAP:  \t\t{GREAT}-{tap_dmg[0]}%\t{GOOD}-{tap_dmg[1]}%\t{MISS}-{tap_dmg[2]}%
HOLD: \t\t{GREAT}-{hld_dmg[0]}%\t{GOOD}-{hld_dmg[1]}%\t{MISS}-{hld_dmg[2]}%
SLIDE:\t\t{GREAT}-{sld_dmg[0]}%\t{GOOD}-{sld_dmg[1]}%\t{MISS}-{sld_dmg[2]}%
TOUCH:\t\t{GREAT}-{ttp_dmg[0]}%\t{GOOD}-{ttp_dmg[1]}%\t{MISS}-{ttp_dmg[2]}%```"""
	break_ctx = f"""```ansi
       \t\t   Base\t   Bonus\t   Total
{PERFECT}PERFECT:{MISS}
High:  \t\t      -{PERFECT}\t-{brk_dmg[0][1]}%\t-{brk_dmg[0][2]}%{MISS}
Low:   \t\t      -{PERFECT}\t-{brk_dmg[1][1]}%\t-{brk_dmg[1][2]}%{MISS}
{GREAT}GREAT:{MISS}
High:  \t   {GREAT}-{brk_dmg[2][0]}%\t-{brk_dmg[2][1]}%\t-{brk_dmg[2][2]}%{MISS}
Mid:   \t   {GREAT}-{brk_dmg[3][0]}%\t-{brk_dmg[3][1]}%\t-{brk_dmg[3][2]}%{MISS}
Low:   \t   {GREAT}-{brk_dmg[4][0]}%\t-{brk_dmg[4][1]}%\t-{brk_dmg[4][2]}%{MISS}
{GOOD}GOOD:  \t   -{brk_dmg[5][0]}%\t-{brk_dmg[5][1]}%\t-{brk_dmg[5][2]}%{MISS}
MISS:  \t   -{brk_dmg[6][0]}%\t-{brk_dmg[6][1]}%\t-{brk_dmg[6][2]}%```"""

	# Note damage
	emb2 = Embed(
		title=f"{song_obj.title}   {chart_type_emoji}",
				description=song_obj.artist,
				color=DIFF_COLOR[diff])
	emb2.set_author(name="Score deductions per note")
	emb2.add_field(name="", value=f"Normal notes damage:\n{damage_ctx}\nBreak damage:{break_ctx}")
	# BPM
	bpm_data = find_bpm(chart_id)
	bpm_text = ("```\n"
				"   Time             BPM    \n"
				"---------------------------\n")
	for item in bpm_data['detail']:
		bpm_text += f"{convert_to_timestamp(item[0])}            {item[1]}\n"
	bpm_text += "```"

	emb3 = Embed(title=f"{song_obj.title}   {chart_type_emoji}",
				 description=song_obj.artist,
				 color=DIFF_COLOR[diff])
	emb3.add_field(name="", value=bpm_text)
	emb3.set_author(name="BPM data")
	return [[emb], [emb2], [emb3]]

