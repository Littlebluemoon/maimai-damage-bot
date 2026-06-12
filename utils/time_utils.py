def time_string(time_numeric: float):
	return f"{round(time_numeric // 60)}:{round(time_numeric % 60, 3):06.3f}"