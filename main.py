from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dotenv import dotenv_values
from log.logger import get_logger_middleware


limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
limit = (dotenv_values(".env"))["RATE_LIMIT"]

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

app.middleware("http")(get_logger_middleware(log_file_path = "log/logs.txt"))


@app.get("/me")
@limiter.limit(limit or "60/minute")
async def handleGetMe():
	pass