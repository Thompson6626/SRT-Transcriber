from fastapi import FastAPI
from app.transcription.router import router as transcription_router

app = FastAPI()

app.include_router(transcription_router)
