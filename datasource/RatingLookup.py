import json
import os

with open(os.getenv("RATING_LOOKUP_PATH"), 'r') as f:
    rating_lookup = json.load(f)