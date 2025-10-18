from fastapi import HTTPException
from logging import getLogger, StreamHandler, FileHandler, Formatter
from uvicorn.logging import ColourizedFormatter
from fastapi import Request

logger_instance_exists = False

class Logger(object):
	def __init__(self, logger_name = "my_logger", log_file_path = None):
		if logger_instance_exists: #singleton
			raise HTTPException(500, detail="An Instance of Logger already exists")
		
		logger_instance_exists = True
		
		self._logger = getLogger(logger_name)

		if log_file_path is not None:
			self._make_file_handler(log_file_path)
		
		console_handler = StreamHandler()
		console_formatter = ColourizedFormatter(
			"%(levelprefix)s -- %(message)s",
			use_colors=True
		)
		console_handler.setFormatter(console_formatter)
		self._logger.addHandler(console_handler)


	def _make_file_handler(self, log_file_path):
		file_handler = FileHandler(log_file_path)
		file_formatter = Formatter("%(levelname)s -- %(message)s")
		file_handler.setFormatter(file_formatter)
		self._logger.addHandler(file_handler)
		self._file_handler = file_handler


	def set_log_file_path(self, log_file_path):
		if self._file_handler:
			self._logger.removeHandler(self._file_handler)
			self._file_handler.close()
		
		self._make_file_handler(log_file_path)


	def info(content):
		return self._logger.info(content)
	
	def error(content):
		return self._logger.error(content)
		


logger = Logger()

def get_logger_middleware(log_file_path):
	logger.set_log_file_path(log_file_path)
	
	async def logger_middleware(req: Request, call_next):
		logger.info(f"{req.method} {req.url}")
		response = await call_next(req)
		logger.info(f"RESPONSE -- {response}")
	
	return logger_middleware