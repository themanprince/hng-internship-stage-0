from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv
from datetime import datetime, timezone
from log import logger
import os
from facts_api_handler import facts_api_handler

load_env()

app = FastAPI()


limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
limit = os.getenv("RATE_LIMIT", "60/minute")


app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

app.middleware("http")(logger.get_logger_middleware(log_file_path = "log/logs.txt"))


@app.get("/me", response_class=ORJSONResponse)
@limiter.limit(limit or "60/minute")
async def handleGetMe(request: Request, response: Response):
	fact = await facts_api_handler.get_fact()
	timestamp = datetime.now(timezone.utc).isoformat()

	payload =  {
		"status": "success",
		"user": {
			"email": "princeadigwe29@gmail.com",
			"name": "Prince Adigwe",
			"stack": "Python/FastAPI"
		},
		"timestamp": timestamp,
		"fact": fact
	}
	
	response.status_code = 200
	return ORJSONResponse(payload) #this sets the response type to application/json


if __name__ == "__main__":
	import uvicorn
	uvicorn.run("main:app", reload=True)
