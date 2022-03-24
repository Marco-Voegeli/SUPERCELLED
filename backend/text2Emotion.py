import json
from fastapi import FastAPI, UploadFile, File, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
import text2emotion as te

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
def get_emotions(data: json):
    text = data['text']
    return te.get_emotion(text)

