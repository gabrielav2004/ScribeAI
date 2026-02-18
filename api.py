from fastapi import FastAPI
from routers.transcription_router import router

app = FastAPI(title="Groq Whisper Transcription API")

app.include_router(router)

#test push 1