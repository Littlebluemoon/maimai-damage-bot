import datetime
from dateutil.relativedelta import relativedelta

def date_diff(date_string):
	d1 = datetime.datetime.strptime(date_string, "%Y-%m-%d")
	d2 = datetime.datetime.now()
	delta = d2 - d1
	r_delta = relativedelta(d2, d1)
	if delta.days == 0:
		return "today"
	if delta.days < 0:
		date_prefix = "in "
		date_suffix = ""
	else:
		date_prefix = ""
		date_suffix = " ago"
	render_y = int(r_delta.years != 0)
	render_m = int(r_delta.months != 0)
	render_d = int(r_delta.days != 0)
	year_part = (str(abs(r_delta.years)) + " y, ") * render_y
	mth_part = (str(abs(r_delta.months)) + " mo, ") * render_m
	day_part = (str(abs(r_delta.days)) + " d") * render_d
	full_str = date_prefix + year_part + mth_part + day_part
	if full_str.endswith(", "):
		full_str = full_str[:-2]
	return full_str + date_suffix
