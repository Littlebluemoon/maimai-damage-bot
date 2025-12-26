import json
import os
from dotenv import load_dotenv

load_dotenv()
with open(os.getenv("BPM_PATH"), encoding='utf-8', mode='r') as f:
	bpm_data = json.load(f)

def find_bpm(song_id):
	for i in bpm_data:
		if str(song_id) in i:
			return i[str(song_id)]
	return None