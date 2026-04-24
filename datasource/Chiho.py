import os

from exceptions.ChihoException import NoChihoException
from models.ChihoItem import ChihoItem
from models.Chiho import Chiho
from utils.database import SessionLocal
import discord

session = SessionLocal()

def get_chiho_data_by_version(version_id):
	return session.query(Chiho).filter(Chiho.version == version_id).all()

def get_chiho_data_by_name(name):
	return session.query(Chiho).filter(Chiho.name == name).one()

def get_chiho_data_by_id(chiho_id):
	return session.query(Chiho).filter(Chiho.id == chiho_id).one()

def get_chiho_data_by_family(family):
	return session.query(Chiho).filter(Chiho.family == family).all()

def get_chiho_data_by_family_and_order(family, order):
	return session.query(Chiho).filter(Chiho.family == family, Chiho.family_order == order).one()

def get_chiho_items_by_id(chiho_id):
	chiho = get_chiho_data_by_id(chiho_id)
	if not chiho:
		raise NoChihoException("No such chiho exists")
	return {
		'chiho_id': chiho.id,
		'chiho_name': chiho.name,
		'chiho_localizedname': chiho.localized_name,
		'version': chiho.version,
		'data': session.query(ChihoItem).filter(ChihoItem.chiho_id == chiho_id).all(),
	}

def generate_chiho_item_embed(data):
	if int(data['version']) in [13, 14]:
		measure = 'm'
	else:
		measure = 'km'
	pages = []
	files = []
	for cnt, item in enumerate(data['data']):
		distance_text = f"Acquired from the beginning" if cnt == 0 else f"{data['data'][cnt].distance - data['data'][cnt-1].distance}{measure} ({item.distance}{measure} cumulative)"
		if os.path.isfile(f"{os.getcwd()}/map_items/{data['chiho_id']:06}/{data['data'][cnt].attachment}.png"):
			files.append([f"{os.getcwd()}/map_items/{data['chiho_id']:06}/{data['data'][cnt].attachment}.png",
						  f"{data['data'][cnt].attachment}.png"])
		else:
			files.append([f"{os.getcwd()}/dummy.png", f"dummy.png"])
		embed = discord.Embed(
			title=item.name,
			description=f"""*{item.kind}*
Distance: {distance_text}"""
		)
		if data['data'][cnt].attachment_kind == 'thumbnail':
			embed.set_thumbnail(url=f"attachment://{cnt+1}.png")
		else:
			embed.set_image(url=f"attachment://{cnt + 1}.png")
		if measure == 'm':
			embed.set_footer(text='In maimai DX and DX PLUS, the measurement is m instead of km.')
		pages.append([embed])
	return pages, files