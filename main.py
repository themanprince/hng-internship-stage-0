from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from log.logger import get_logger_middleware


app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

app.middleware("http")(get_logger_middleware("log/logs.txt"))


@app.get("/me")
async def handleGetMe():
	pass