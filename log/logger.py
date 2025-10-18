from logging import getLogger, StreamHandler, FileHandler, Formatter
from uvicorn.logging import ColourizedFormatter
from fastapi import Request


logger = getLogger("my_logger")

console_handler = StreamHandler()
file_handler = FileHandler("logs.txt")

console_formatter = ColourizedFormatter(
	"%(levelprefix)s -- %(message)s",
	use_colors=True
)

file_formatter = Formatter("%(levelname)s -- %(message)s")

console_handler.setFormatter(console_formatter)
file_handler.setFormatter(file_formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


async def logger_middleware(req: Request, call_next):
	logger.info(f"{req.method} {req.url}")
	response = call_next(req)
	logger.info(f"RESPONSE -- {response}")