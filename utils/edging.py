import math
from fractions import Fraction

from datasource.SongData import query_chart_stats_by_id


def calculate_edging_conditions(target_id, diff, edge_score=999999):
	chart_obj = query_chart_stats_by_id(target_id, diff)
	chart_weight = (chart_obj.num_tap + chart_obj.num_ttp + chart_obj.num_hld * 2
					+ chart_obj.num_sld * 3 + chart_obj.num_brk * 5)
	a = Fraction(100000, chart_weight)
	b = Fraction(500, chart_obj.num_brk)
	print(a, b)

	# Original problem: floor(1010000 - ax - by) = 999999
	# Now multiple all sides with lcm(a.denominator, b.denominator) to destroy floor sign

	mult = math.lcm(a.denominator, b.denominator)

	target_low = (1010000 - edge_score) * mult
	target_high = (1010001 - edge_score) * mult
	a_modified = a * mult
	b_modified = b * mult

	print(a_modified, b_modified, target_low, target_high)