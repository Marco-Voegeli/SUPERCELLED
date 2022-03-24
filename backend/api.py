from fastapi import FastAPI, UploadFile, File, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
import text2emotion as te
from pydantic import BaseModel
import json
from profanity_check import predict


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
    profanity = predict([text])[0].item()

    max_value = 0
    best_emotion = ''
    for emotion in emotions:
        value = emotions[emotion]
        if value > max_value:
            max_value = value
            best_emotion = emotion
    return {"emotion" : best_emotion,
            "profanity" : profanity,
            "value" : max_value,
            "emotions": emotions}
