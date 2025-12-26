class NoSongFoundException(BaseException):
	pass

class DeletedSongFoundException(BaseException):
	pass

class LowConfidenceException(BaseException):
	pass

class NoChartFoundException(BaseException):
	pass

class IncorrectChartTypeException(BaseException):
	pass

class InvalidChartConstantException(BaseException):
	pass

class InvalidChartLevelException(BaseException):
	pass