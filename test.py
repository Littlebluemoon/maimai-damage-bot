import os

from constants import DIFF_SPECTRUM
from utils.charts import convert_cc_to_difficulty
from dotenv import load_dotenv

load_dotenv()
print(os.getenv("RATING_LOOKUP_PATH"))
print(convert_cc_to_difficulty('9.7'))

# print(DIFF_SPECTRUM.index(convert_cc_to_difficulty(9.7)))