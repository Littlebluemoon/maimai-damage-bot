import asyncio
import json
import httpx
from bs4 import BeautifulSoup
import unicodedata
import os

from dotenv import load_dotenv

from datasource.SongData import query_single

load_dotenv()

DIFF = [None, None, 'expert', 'master', 'remaster']
CLEAR_TYPE = ['SSS+', 'SSS', 'SS', 'S', 'AP']

def transform_chart_id(id, chart_type):
	id = int(id)
	if chart_type == 'st':
		return id - 10000 if id > 10000 else id
	if chart_type == 'dx':
		return id + 10000 if id < 10000 else id

def scrape_rates(soup, cc, difficulty):
	result = {}
	song_blocks = soup.find_all('div', class_=f'music_{DIFF[int(difficulty)]}_score_back')
	reached_fuckass_song = False
	for song in song_blocks:
		# Again like fuck that song
		chart_type = song.find('img', class_='music_kind_icon').get('src')[19:-3][0:2]
		# print(f"Song : {song.find('div', class_='music_name_block').text}")
		chart_obj = query_single(song.find('div', class_='music_name_block').text)[0]
		# Again fuck these songs
		# Please at least delete the other link from the game since it sucks dick
		# Thank you
		if chart_obj.title == 'Link':
			if difficulty == 3:
				if not reached_fuckass_song:
					chart_id = 383
					reached_fuckass_song = True
				else:
					chart_id = 131
			elif difficulty == 2:
				if cc == 18:
					chart_id = 131
				else:
					chart_id = 383
			else: # 4
				chart_id = 131
		else:
			chart_id = transform_chart_id(chart_obj.id, chart_type)
		clear_rate = song.find('span', class_='f_r').text[:-1]
		if clear_rate == '--':
			clear_rate = None
		else:
			clear_rate = round(float(clear_rate), 2)
		result[chart_id] = clear_rate
	return result

def main():
	level_clear_data_exp = {}
	level_clear_data_mas = {}
	level_clear_data_remas = {}
	for cc in range(9, 24):
		level_clear_data_exp[cc] = {}
		level_clear_data_mas[cc] = {}
		level_clear_data_remas[cc] = {}
	# Level range: 9~23
	# Clear type range: 0~4 (SSS+ to S, AP)
	# Difficulty range: 2~4 (exp~remas)
	# Some heads up:
	# Easiest remaster chart is 12 (12.3) (17)
	# Easiest master chart is 10+ (10.7) (14)
	# Hardest expert chart is 13+ (13.9) (20)
	for cc in range(9, 24):
		if cc < 21:
			print(f"Now processing {cc:02d}_2.html")
			with open(f"clear_percent/{cc:02d}_2.html", "r", encoding="utf-8") as clear_data:
				soup = BeautifulSoup(clear_data, "html.parser")
				level_clear_data_exp[cc]['sssp'] = scrape_rates(soup, cc, 2)
		if cc >= 14 and cc < 23:
			print(f"Now processing {cc:02d}_3.html")
			with open(f"clear_percent/{cc:02d}_3.html", "r", encoding="utf-8") as clear_data:
				soup = BeautifulSoup(clear_data, "html.parser")
				level_clear_data_mas[cc]['sssp'] = scrape_rates(soup, cc, 3)
		if cc >= 17:
			print(f"Now processing {cc:02d}_4.html")
			with open(f"clear_percent/{cc:02d}_4.html", "r", encoding="utf-8") as clear_data:
				soup = BeautifulSoup(clear_data, "html.parser")
				level_clear_data_remas[cc]['sssp'] = scrape_rates(soup, cc, 4)

	final_data = {
		'expert': level_clear_data_exp,
		'master': level_clear_data_mas,
		'remas': level_clear_data_remas
	}
	with open("server_clear_data.json", "w") as clear_data_file:
		json.dump(final_data, clear_data_file)

main()