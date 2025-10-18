from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from log.logger import logger, logger_middleware


app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

app.middleware("http")(logger_middleware)


@app.get("/me")
async def handleGetMe():
	pass