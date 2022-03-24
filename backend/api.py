from fastapi import FastAPI, UploadFile, File, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
import text2emotion as te
from pydantic import BaseModel
import json

class textMessage(BaseModel):
    text: str

app = FastAPI(
    title="Our Python Backend",
    version="0.0.1")

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/get_emotions")
def get_emotions(data: textMessage):
    text = data.text
    emotions = te.get_emotion(text)
    max_value = 0
    best_emotion = ''
    for emotion in emotions:
        value = emotions[emotion]
        if value > max_value:
            best_emotion = emotion
    return {"emotion" : best_emotion}


