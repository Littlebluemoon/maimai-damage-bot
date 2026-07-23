import asyncio

import httpx
from bs4 import BeautifulSoup
import unicodedata
import os

from dotenv import load_dotenv

from datasource.SongData import query_single

load_dotenv()

AUTH = 'https://lng-tgk-aime-gw.am-all.net/common_auth/login/sid'
URL = 'https://maimaidx-eng.com/maimai-mobile/record/nationalData/search/'
AUTH2 = 'https://lng-tgk-aime-gw.am-all.net/common_auth/login?site_id=maimaidxex&redirect_url=https://maimaidx-eng.com/maimai-mobile/&back_url=https://maimai.sega.com/'
MAIMAI_HOMEPAGE = 'https://maimaidx-eng.com/maimai-mobile/'

creds = {
	'retention': '1',
	'sid': os.getenv("SEGAID"),
	'password': os.getenv("SEGAID_PASSWORD"),
}

print(creds)

headers_template = {
	"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
	"accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
	"sec-ch-ua": '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
	"sec-ch-ua-mobile": "?0",
	"sec-ch-ua-platform": '"Windows"',
	"sec-fetch-dest": "document",
	"sec-fetch-mode": "navigate",
	"sec-fetch-site": "same-origin",
	"sec-fetch-user": "?1",
	"upgrade-insecure-requests": "1",
	'Origin': 'https://lng-tgk-aime-gw.am-all.net',
	'Pragma': 'no-cache',
	'Referer': 'https://lng-tgk-aime-gw.am-all.net/common_auth/login?site_id=maimaidxex&redirect_url=https://maimaidx-eng.com/maimai-mobile/&back_url=https://maimai.sega.com/',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
					   'Chrome/93.0.4577.82 Safari/537.36',
}

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
		chart_type = song.find('img', class_='music_kind_icon').get('src')[49:-4][0:2]
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
		clear_rate = round(float(song.find('span', class_='f_r').text[:-1]), 2)
		result[chart_id] = clear_rate
	return result

async def main():
	async with httpx.AsyncClient() as client:
		resp2 = await client.post(AUTH2)
		jsession = resp2.cookies.get('JSESSIONID')
		clal = resp2.cookies.get('clal')
		print(jsession, clal)
		resp3 = await client.post(AUTH, data=creds, headers=headers_template, cookies={'JSESSIONID': jsession})
		print(resp3.text)
		redirect = resp3.headers.get('location')
		print(redirect)
		resp4 = await client.get(redirect, headers=headers_template)
		r5_headers = dict(resp4.headers)
		r5_headers['referer'] = 'https://maimaidx-eng.com/maimai-mobile/'
		r5_cookies = resp4.cookies
		level_clear_data = {}
		for cc in range (9, 24):
			level_clear_data[cc] = {}
		# Level range: 9~23
		# Clear type range: 0~4 (SSS+ to S, AP)
		# Difficulty range: 2~4 (exp~remas)
		# Some heads up:
		# Easiest remaster chart is 12 (12.3) (17)
		# Easiest master chart is 10+ (10.7) (14)
		# Hardest expert chart is 13+ (13.9) (20)
		for cc in range(9, 24):
			if cc < 21:
				resp_exp_sssp = await client.get(URL, headers=r5_headers,
					 params={'level': str(cc), 'clearType': '0', 'sort': '0', 'diff': '2'})
				# Wait 3 secs between reqs to prevent rate limiting
				print(f"Data got with length {len(resp_exp_sssp.text)}")
				soup = BeautifulSoup(resp_exp_sssp.text, 'html.parser')
				level_clear_data[cc]['sssp'] = scrape_rates(soup, cc, 2)
				await asyncio.sleep(3)
				# resp_exp_sss = await client.get(URL, headers=r5_headers,
				# 	 params={'level': str(cc), 'clearType': '1', 'sort': '0', 'diff': '2'})
				# await asyncio.sleep(3)
				# resp_exp_ss = await client.get(URL, headers=r5_headers,
				# 	params={'level': str(cc), 'clearType': '2', 'sort': '0', 'diff': '2'})
				# await asyncio.sleep(3)
				# resp_exp_s = await client.get(URL, headers=r5_headers,
				# 	params={'level': str(cc), 'clearType': '3', 'sort': '0', 'diff': '2'})
				# resp_exp_ap = await client.get(URL, headers=r5_headers,
				# 	params={'level': str(cc), 'clearType': '4', 'sort': '0', 'diff': '2'})

			# if cc >= 17:
			# 	resp5 = await client.get(URL, headers=r5_headers)
			# if cc >= 14:
			# 	resp5 = await client.get(URL, headers=r5_headers)
		# print(resp5.text)
	print(level_clear_data)

asyncio.run(main())