import math
from fractions import Fraction

from discord import Embed

from constants import (REGULAR_NOTE_RATIO, NOTE_TYPE_MULT, BREAK_BASE_MULT, BREAK_BONUS_MULT,
					   PERFECT, GREAT, GOOD, MISS, NOTE_LABEL)
from discord.ext import commands

from exceptions.DamageCommandException import NotReplyToPlayRecordException, ImpossiblePlayRecordException

# test = {'title': '**Glorious Crown - MASTER 14+ (14.8)**',
# 		'judge': [[365, 429, 145, 27, 23],
# 				  [11, 5, 1, 1, 0],
# 				  [86, 0, 1, 2, 0],
# 				  [0, 0, 0, 0, 0],
# 				  [16, 32, 6, 0, 0]],
# 		'achv': '956947',
# 		'thumb': 'https://mimixd.app/images/render/cover/0c142b42f0e37845.png'}
#
# test_breakdown = [[365, 429, 145, 27, 23],
# 				  [11, 5, 1, 1, 0],
# 				  [86, 0, 1, 2, 0],
# 				  [0, 0, 0, 0, 0],
# 				  [16, 18, 14, 4, 2, 0, 0, 0]]
#
# test_table = {'table': [['\x1b[0;0m      --', '\x1b[0;35m -1.8565', '\x1b[0;36m -0.8642', '\x1b[0;0m -1.4724'], ['\x1b[0;0m      --', '\x1b[0;35m -0.0256', '\x1b[0;36m -0.0640', '\x1b[0;0m      --'], ['\x1b[0;0m      --', '\x1b[0;35m -0.0384', '\x1b[0;36m -0.1920', '\x1b[0;0m      --'], ['\x1b[0;0m      --', '\x1b[0;0m      --', '\x1b[0;0m      --', '\x1b[0;0m      --'], ['\x1b[0;33m -0.2129', '\x1b[0;35m -0.5788', '\x1b[0;0m      --', '\x1b[0;0m      --']], 'perfect': [18, 14], 'great': [4, 2, 0]}

def calculate_score(judge):
	weight = sum(judge[0]) + 2 * sum(judge[1]) + 3 * sum(judge[2]) + sum(judge[3]) + 5 * sum(judge[4])
	score = Fraction(0, 1)
	note_score = Fraction(1000000, weight)
	break_score = Fraction(10000, sum(judge[-1]))
	for i in range(4):
		for j in range(5):
			score += note_score * judge[i][j] * NOTE_TYPE_MULT[i] * REGULAR_NOTE_RATIO[j]
	break_base = [note_score * 5,
				  note_score * 5, note_score * 5,
				  note_score * 4, note_score * 3, note_score * Fraction(5, 2),
				  note_score * 2]
	break_bonus = [break_score,
				   break_score * Fraction(3, 4), break_score * Fraction(1, 2),
				   break_score * Fraction(2, 5), break_score * Fraction(2, 5), break_score * Fraction(2, 5),
				   break_score * Fraction(3, 10)]
	for i in range(len(break_bonus)):
		score += (break_bonus[i] + break_base[i]) * judge[-1][i]
	return float(score)

def get_great_solution(diff, limit):
	print(diff, limit)
	if diff == 0:
		return [0, 0]
	if diff < 2:
		return None
	if diff % 3 == 0:
		x = 0
	elif diff % 3 == 1:
		x = 2
	else:
		x = 1
	y = (diff - 2*x) // 3
	while x+y > limit:
		x += 3
		y -= 1
	return [x, y]

def get_play_data_table(msg):
	# NOTE: Bot specifically extracts data from mimi xd bot
	content = msg.embeds[0].description
	thumbs = msg.embeds[0].thumbnail.url
	data = content.split('\n')

	title = data[0]
	note_type = [0, 0, 0, 0, 0]
	for i in range(4, 9):
		if len(data[i].split()) == 1:
			note_type[i - 4] = [0, 0, 0, 0, 0]
		else:
			# Not critical perfect
			tmp = [int(x) for x in (data[i].split())[1:]]
			if len(tmp) == 4:
				tmp.insert(0, 0)
			note_type[i - 4] = tmp
	achv = data[-2][data[-2].find("ACC") + 5:].replace('**', '').replace('.', '')[:-1]
	return {
		'title': title,
		'judge': note_type,
		'achv': achv,
		'thumb': thumbs
	}

def process_damage(damage_data):
	tap = [int(x) for x in damage_data['judge'][0]]
	hld = [int(x) for x in damage_data['judge'][1]]
	sld = [int(x) for x in damage_data['judge'][2]]
	ttp = [int(x) for x in damage_data['judge'][3]]
	brk = [int(x) for x in damage_data['judge'][4]]

	weight = sum(tap) + 2 * sum(hld) + 3 * sum(sld) + sum(ttp) + 5 * sum(brk)
	# print(weight)

	# Thank you python
	note_score = Fraction(1000000, weight)
	break_score = Fraction(10000, sum(brk))

	regular_note_score = [x * note_score for x in REGULAR_NOTE_RATIO]

	# 2500x3, 2000, 1500, 1250, 1000
	break_base = [note_score * 5,
				  note_score * 5, note_score * 5,
				  note_score * 4, note_score * 3, note_score * Fraction(5, 2),
				  note_score * 2]
	break_minimal_unit = note_score / 2
	# 75, 50, 40x3, 30
	break_bonus = [break_score,
				   break_score * Fraction(3, 4), break_score * Fraction(1, 2),
				   break_score * Fraction(2, 5), break_score * Fraction(2, 5), break_score * Fraction(2, 5),
				   break_score * Fraction(3, 10)]

	score_left = Fraction(int(damage_data['achv']), 1)

	for i in range(0, 4):
		score_left -= (tap[i] * regular_note_score[i] + hld[i] * regular_note_score[i] * 2
					   + sld[i] * 3 * regular_note_score[i] + ttp[i] * regular_note_score[i])
	score_left -= ((brk[0] + brk[1]) * break_base[0] + brk[0] * break_bonus[0] + brk[2] * break_bonus[3]
				   + brk[3] * break_bonus[-1] + brk[3] * break_base[-1])

	# Try all perfects
	for pf in range(brk[1], -1, -1):
		#                     v                v             v
		break_list = [brk[0], pf, brk[1] - pf, brk[2], 0, 0, brk[3], brk[4]]
		current_score = calculate_score([
			tap, hld, sld, ttp, break_list
		])
		diff = current_score - int(damage_data['achv'])
		if diff < 0:
			continue
		else:
			# print(f"Checking perfect break {break_list[1], break_list[2]} with {brk[2]} greats, score = {current_score}, diff = {diff}")
			diff_unit = diff / break_minimal_unit
			# print(f"diff_unit = {diff_unit}")
			if abs(diff_unit - math.floor(diff_unit) <= 1e-2):
				gr_candidate = get_great_solution(math.floor(diff_unit), brk[2])
				# print(f"Possible great distribution: {gr_candidate}")
				# Plug back
				break_list = [brk[0], pf, brk[1] - pf, brk[2] - sum(gr_candidate),
							  gr_candidate[0], gr_candidate[1], brk[3], brk[4]]
				actual_score = calculate_score([
					tap, hld, sld, ttp, break_list
				])
				# print(f"Actual score: {actual_score}", end='')
				if math.floor(actual_score) == int(damage_data['achv']):
					# print(" (Matches)")
					return [
					tap, hld, sld, ttp, break_list
				]
				# else:
				# 	print(" (Does not match)")
	return None

def get_normal_note_damage(amount, mult, weight):
	return Fraction(1000000, weight) * amount * mult

def get_break_note_damage(break_arr, weight, judge_level=0):
	max_break = sum(break_arr)
	if judge_level == 0:
		return sum([Fraction(10000, max_break) * BREAK_BONUS_MULT[i] * break_arr[i] for i in range(1, 3)])
	if judge_level == 1:
		return sum([Fraction(10000, max_break) * BREAK_BONUS_MULT[i] * break_arr[i] + Fraction(1000000, weight) * BREAK_BASE_MULT[i] * break_arr[i] for i in range(3, 6)])
	if judge_level == 2:
		return Fraction(10000, max_break) * BREAK_BONUS_MULT[6] * break_arr[6] + Fraction(1000000, weight) * BREAK_BASE_MULT[6] * break_arr[6]
	if judge_level == 3:
		return Fraction(10000, max_break) * BREAK_BONUS_MULT[7] * break_arr[7] + Fraction(1000000, weight) * BREAK_BASE_MULT[7] * break_arr[7]

def generate_damage_table(judges):
	weight = sum(judges[0]) + 2 * sum(judges[1]) + 3 * sum(judges[2]) + sum(judges[3]) + 5 * sum(judges[4])
	tap_damage = [0] + [int(get_normal_note_damage(judges[0][i], 1 - REGULAR_NOTE_RATIO[i], weight)) / -10000.0 for i in range(2, 5)]
	hold_damage = [0] + [int(get_normal_note_damage(judges[1][i], 1 - REGULAR_NOTE_RATIO[i], weight) * 2) / -10000.0 for i in range(2, 5)]
	slide_damage = [0] + [int(get_normal_note_damage(judges[2][i], 1 - REGULAR_NOTE_RATIO[i], weight) * 3) / -10000.0 for i in range(2, 5)]
	touch_damage = [0] + [int(get_normal_note_damage(judges[3][i], 1 - REGULAR_NOTE_RATIO[i], weight) * 3) / -10000.0 for i in range(2, 5)]
	break_damage = [int(get_break_note_damage(judges[4], weight, 0)) / -10000.0,
					int(get_break_note_damage(judges[4], weight, 1)) / -10000.0,
					int(get_break_note_damage(judges[4], weight, 2)) / -10000.0,
					int(get_break_note_damage(judges[4], weight, 3)) / -10000.0]
	result_table = [tap_damage, hold_damage, slide_damage, touch_damage, break_damage]
	note_color = [PERFECT, GREAT, GOOD, MISS]
	for lst in result_table:
		for i, it in enumerate(lst):
			lst[i] = format(it, '.4f')
			if lst[i] == '0.0000' or lst[i] == '-0.0000':
				lst[i] = f'{MISS}      --'
			else:
				lst[i] = note_color[i] + ' ' * (8 - len(lst[i])) + lst[i]
	return {
		'table': result_table,
		'perfect': judges[4][1:3],
		'great': judges[4][3:6]
	}

def generate_damage_table_text(table):
	table_content = table['table']
	note_labels = [f"{NOTE_LABEL}TAP:   ", f"{NOTE_LABEL}HOLD:  ", f"{NOTE_LABEL}SLIDE: ",
				   f"{NOTE_LABEL}TOUCH: ", f"{NOTE_LABEL}BREAK: "]
	table_str = f"{NOTE_LABEL}        Perfect     Great      Good      Miss\n"
	for i in range(5):
		table_str += note_labels[i]
		for j in range(4):
			table_str += table_content[i][j] + '  '
		table_str += '\n'
	table_str += f"{PERFECT}PERFECT break:    {table['perfect']}\n"
	table_str += f"{GREAT}GREAT break:      {table['great']}"
	return table_str

@commands.command()
async def damage(ctx):
	try:
		msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
		if msg is None:
			raise NotReplyToPlayRecordException("This command was not used to reply to any message.\n"
						"Try again while replying to a message.")
		msg_text = get_play_data_table(msg)
		damage_table = process_damage(msg_text)
		if damage_table is None:
			raise ImpossiblePlayRecordException("This play result is impossible in normal play.\n"
							"If you got the score legitimately and think that it's a bug, please contact the author.")
		damage_table = generate_damage_table(damage_table)
		table_text = generate_damage_table_text(damage_table)
		emb = Embed(title=msg_text['title'], description="```ansi\n" + table_text + "\n```")
		emb.set_author(name="Lost Score Information")
		emb.set_thumbnail(url=msg_text['thumb'])
		await ctx.send(embed=emb)
	except ImpossiblePlayRecordException as e:
		await ctx.send(str(e))
	except NotReplyToPlayRecordException as e:
		await ctx.send(str(e))

