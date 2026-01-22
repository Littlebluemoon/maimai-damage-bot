from datasource.RatingLookup import rating_lookup
from constants import PERFECT, MISS
import discord
import bisect

def convert_cc_to_difficulty(cc):
	cc = str(cc)
	if cc == '???':
		return cc
	if float(cc) < 7:
		return cc[0]
	else:
		if int(cc[-1:]) >= 6:
			return f'{cc[:-2]}+'
		return f'{cc[:-2]}'

def find_rating_target(value, lst):
	lst = sorted([int(x) for x in lst])
	i = bisect.bisect_left(lst, value)
	return lst[i] if i < len(lst) else None


def generate_rating_table(target):
	result_set = []
	init = target
	tgt_rating = int(target)
	while len(result_set) == 0:
		for i in range(10, 151):
			real_tgt = find_rating_target(tgt_rating, rating_lookup[str(i)])
			if not real_tgt:
				continue
			if int(rating_lookup[str(i)][str(real_tgt)]) >= 800000 and real_tgt - tgt_rating < 5:
				result_set.append([i, rating_lookup[str(i)][str(real_tgt)], real_tgt])
		tgt_rating += 1
	rating_table = '```\n' \
				  'Chart Level       Achievement       Rating\n' \
				  '------------------------------------------\n'
	for item in result_set:
		item[0] = str(item[0])
		item[1] = str(item[1])
		item[2] = str(item[2])
		item[0] = f'{item[0][:-1]}.{item[0][-1:]}'
		item[1] = f'{item[1][:-4]}.{item[1][-4:]}'
		rating_table += f'{item[0]:>11}       {item[1]:>10}%       {item[2]:>6}\n'
	rating_table += '```'
	# Paginate
	rating_table_ctx = rating_table.split('\n')[3:-1]
	rating_table_pages = [rating_table_ctx[i:i+10] for i in range(0, len(rating_table_ctx), 10)]
	result = {}
	if tgt_rating - 1 != int(init):
		result['exact_rating'] = False
	else:
		result['exact_rating'] = True
	embeds = []
	for item in rating_table_pages:
		table_ctx = '```\n' \
				  'Chart Level       Achievement       Rating\n' \
				  '------------------------------------------\n' + '\n'.join(item)
		embeds.append([discord.Embed(
			title="Rating Target Table",
			description=f"Rating value: {tgt_rating-1} {'' if result['exact_rating'] else'(because '}"
						f"{'' if result['exact_rating'] else init} {'' if result['exact_rating'] else ' is mathematically impossible)'}"
						f"\n{table_ctx}```",
									)])
	result['embeds'] = embeds
	return result

def generate_calculate_command_card(cc, ap=False):
	cc = cc.replace(".", "")
	if int(cc) < 10 or int(cc) > 150:
		return None
	rating_table_head = '```ansi\n' \
					  'Achievement       Rating\n' \
					  '------------------------\n'
	rating_table = rating_table1 = rating_table2 = ''
	result_set = rating_lookup[str(cc)]
	ap_rating = max([int(x) for x in list(result_set.keys())]) + 1
	for key in result_set:
		if result_set[key] >= 800000 and result_set[key] <= 899999:
			achv_rate = str(result_set[key])
			achv_rate = f'{achv_rate[:-4]}.{achv_rate[-4:]}'
			rating_table = (PERFECT * int(achv_rate[-3:] == '000') +
						   f'{achv_rate:>10}%       {key:>6}\n' + MISS + rating_table)
		elif result_set[key] >= 900000 and result_set[key] <= 969999:
			achv_rate = str(result_set[key])
			achv_rate = f'{achv_rate[:-4]}.{achv_rate[-4:]}'
			rating_table1 = (PERFECT * int(achv_rate[-3:] == '000') +
							f'{achv_rate:>10}%       {key:>6}\n' + MISS + rating_table1)
		elif result_set[key] >= 970000 and result_set[key] <= 1010000:
			achv_rate = str(result_set[key])
			achv_rate = f'{achv_rate[:-4]}.{achv_rate[-4:]}'
			rating_table2 = (PERFECT * int(achv_rate[-3:] == '000')
							+ f'{achv_rate:>10}%       {key:>6}\n' + MISS + rating_table2)
	rating_table2 = (PERFECT+ f'         AP       {ap_rating:>6}\n' + MISS + rating_table2)
	rating_table = rating_table_head + rating_table
	rating_table1 = rating_table_head + rating_table1
	rating_table2 = rating_table_head + rating_table2
	emb1 = discord.Embed(title='Rank A~AA', description=f"{rating_table}```")
	emb2 = discord.Embed(title='Rank AA~AAA', description=f"{rating_table1}```")
	emb3 = discord.Embed(title='Rank S~SSS+', description=f"{rating_table2}```")
	return [[emb3], [emb2], [emb1]]