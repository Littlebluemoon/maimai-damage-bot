import math
from fractions import Fraction


def split_great_good(value, coeff0, coeff1, coeff2=0.1):
	base = value / (coeff0 + coeff1 * 2.5 + coeff2 * 5)
	return f"{math.floor(base * coeff0)}-{math.floor(base * coeff1)}-{math.floor(base * coeff2)}"

def calculate_chart_border(chart_obj, brk):
	weight = (chart_obj.num_tap + 2 * chart_obj.num_hld + 3 * chart_obj.num_sld
			  + chart_obj.num_ttp + chart_obj.num_brk * 5)
	# Init losses
	init_score = 1010000 - Fraction(2500, chart_obj.num_brk) * brk
	score_per_great = Fraction(200000, weight)
	allowanceSSSP = (init_score - Fraction(1005000, 1)) / score_per_great
	allowanceSSS = (init_score - Fraction(1000000, 1)) / score_per_great
	allowanceSSP = (init_score - Fraction(995000, 1)) / score_per_great
	allowanceSS = (init_score - Fraction(990000, 1)) / score_per_great
	allowanceSP = (init_score - Fraction(980000, 1)) / score_per_great
	allowanceS = (init_score - Fraction(970000, 1)) / score_per_great
	border_str = f"""**SSS+**: {split_great_good(allowanceSSSP, 9, 1, 0.05)}
**SSS**: {split_great_good(allowanceSSS, 9, 1, 0.05)}
**SS+**: {split_great_good(allowanceSSP, 9, 1, 0.1)}
**SS**: {split_great_good(allowanceSS, 5, 1, 0.1)}
**S+**: {split_great_good(allowanceSP, 5, 1, 0.2)}
**S**: {split_great_good(allowanceS, 5, 1, 0.4)}
"""
	return border_str