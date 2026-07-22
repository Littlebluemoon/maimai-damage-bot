import math
from fractions import Fraction

from datasource.SongData import query_chart_stats_by_id


def calculate_edging_conditions(target_id, diff, edge_score=999999):
	chart_obj = query_chart_stats_by_id(target_id, diff)
	chart_weight = (chart_obj.num_tap + chart_obj.num_ttp + chart_obj.num_hld * 2
					+ chart_obj.num_sld * 3 + chart_obj.num_brk * 5)
	original_a = Fraction(100000, chart_weight)
	original_b = Fraction(500, chart_obj.num_brk)
	print(original_a, original_b)

	# Original problem: floor(1010000 - ax - by) = 999999
	# Now multiple all sides with lcm(a.denominator, b.denominator) to destroy floor sign

	mult = math.lcm(original_a.denominator, original_b.denominator)

	target_low = (1009999 - edge_score) * mult
	target_high = (1010000 - edge_score) * mult
	a = original_a * mult
	b = original_b * mult

	# Let's find solutions
	print(a, b, target_low, target_high)

	x = 2

	while True:
		if x == 3:
			x += 1
			continue
		else:
			lower_peak = (target_low - a * x) / b
			higher_peak = (target_high - a * x) / b
			if int(lower_peak) != int(higher_peak):
				print(lower_peak, higher_peak)
				print(f"({int(lower_peak), int(higher_peak)})")
		x += 1
		if lower_peak < 0 and higher_peak < 0:
			break