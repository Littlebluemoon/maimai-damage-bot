import ast

from discord import Embed
from command.songdata import get_song_object
from constants import TITLE_RARITY_COLOR
from models.SongData import SongData
from models.Title import Title
from models.TitleList import TitleList
from utils.database import SessionLocal

session = SessionLocal()

def get_title_for_song(query):
	song_id = get_song_object(query)
	print(song_id)
	song_id = [x.id for x in song_id]
	title_list = session.query(TitleList).filter(TitleList.id.in_(song_id)).all()
	id_list = []
	for title in title_list:
		id_list += ast.literal_eval(title.titles)
	literal_list = session.query(Title).filter(Title.id.in_(id_list)).all()
	res = []
	# NO SPOILERS
	for item in literal_list:
		songs = ast.literal_eval(item.songs)
		songs_involved = session.query(SongData).filter(SongData.id.in_(songs)).all()
		if len(songs_involved) == len(songs):
			# Song list (by name) for yours truly
			footer = ""
			for song in songs_involved:
				if song.id >= 10000:
					footer += f"{song.title} [DX], "
				else:
					footer += f"{song.title} [STD], "
			footer = footer[:-2]
			res.append([item, footer])
		# else:
		# 	print("Dropped due to spoilers : " + item.text)

	emb = []
	for item in res:
		tmp = Embed(title=item[0].text,
						 description=item[0].normText,
						 color=TITLE_RARITY_COLOR[item[0].rarity])
		tmp.set_footer(text="Songs involved: " + item[1])
		emb.append(tmp)
	return emb