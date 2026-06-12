import json
import math
import os
from decimal import Decimal
from io import BytesIO

import discord
from PIL import ImageDraw, Image, ImageFont
from dotenv import load_dotenv

load_dotenv()

MARGINS = 50
CANVAS_DIMS = (2500, 300)
TOP_MARGIN = 50
COLUMN_PADDING = 3

heatmap_path = os.path.join(os.getcwd(), os.getenv('HEATMAP_PATH'))

def generate_song_heatmap(heatmap_file):
	with open(os.path.join(heatmap_path, heatmap_file), "r", encoding="utf-8") as f:
		json_object = json.load(f)

	timings = [Decimal(x) for x in json_object['measures'].values()]
	max_time = timings[-1]
	max_height = max([sum(x) for x in list(json_object['notes'].values())])
	note_count = sum([sum(x) for x in list(json_object['notes'].values())])
	max_measure = int(list(json_object['measures'].keys())[-1])

	rect = []

	for i in range(max_measure + 1):
		if str(i) in list(json_object['measures']):
			meas_time = Decimal(json_object['measures'][str(i)])
			note_data = json_object['notes'][str(i)]
			tmp = []
			bottom_y = CANVAS_DIMS[-1]
			for j in note_data:
				if j == 0:
					tmp.append(None)
				else:
					midpoint = MARGINS + (CANVAS_DIMS[0] - 2 * MARGINS) / max_time * meas_time
					coords = [[midpoint - COLUMN_PADDING, bottom_y - (CANVAS_DIMS[-1] - TOP_MARGIN) / max_height * j],
							  [midpoint + COLUMN_PADDING, bottom_y]]
					bottom_y = bottom_y - (CANVAS_DIMS[-1] - TOP_MARGIN) / max_height * j
					tmp.append(coords)
			rect.append(tmp)
		else:
			# print(f"Skip measure {i}")
			pass

	img = Image.new("RGB", CANVAS_DIMS, "white")

	draw = ImageDraw.Draw(img)

	DOTS_SPACING = 25
	DOTS_RADIUS = 3

	FONT = ImageFont.truetype("NotoSans-Regular.ttf", 45)
	# dotted time markers
	time_markers = list(range(30, int(max_time), 30))

	for time in time_markers:
		xcor = time / max_time * CANVAS_DIMS[0]
		length = math.hypot(0, CANVAS_DIMS[1])
		draw.text((xcor - 105, 0), f"{time // 60}:{time % 60:02d}", fill="black", font=FONT)
		for i in range(0, int(length), DOTS_SPACING):
			t = i / length
			x = xcor
			y = CANVAS_DIMS[1] * t
			draw.ellipse((x - DOTS_RADIUS, y - DOTS_RADIUS, x + DOTS_RADIUS, y + DOTS_RADIUS), fill="#D3D3D3")

	for item in rect:
		if item[0]:
			draw.rectangle(item[0], fill=(237, 95, 144))
		if item[1]:
			draw.rectangle(item[1], fill=(120, 148, 232))
		if item[2]:
			draw.rectangle(item[2], fill=(253, 172, 75))
	buffer = BytesIO()
	img.save(buffer, format="JPEG")
	buffer.seek(0)

	# Misc
	return {
			'image': discord.File(buffer, filename="heatmap.jpeg"),
			'note_count': note_count,
			'max_measure_density': max_height
		}