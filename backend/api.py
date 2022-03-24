from fastapi import FastAPI, UploadFile, File, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
import text2emotion as te
from pydantic import BaseModel

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
    print("prout")
    text = data.text
    return te.get_emotion(text)

text = "I want to break free"
emotions = te.get_emotion(text)

print(emotions)