from fastapi.responses import PlainTextResponse
from fastapi import FastAPI, Request
from pydantic import BaseModel
import datetime
from fastapi.middleware.cors import CORSMiddleware  # 👈 ADD THIS
import os

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Note(BaseModel):
    message: str

@app.post("/note")
def write_note(note: Note):
    log_dir = "/logs"
    os.makedirs(log_dir, exist_ok=True)
    with open(f"{log_dir}/notes.log", "a") as f:
        f.write(f"{datetime.datetime.now()}: {note.message}\n")
    return {"status": "saved", "note": note.message}

@app.get("/note")
def note_info():
    return {"info": "Send a POST request with JSON like {'message': 'your note'}"}

@app.get("/")
def root():
    return {"message": "Mini Note API is running!"}

@app.get("/favicon.ico")
def favicon():
    return {}


@app.get("/logs", response_class=PlainTextResponse)
def read_logs():
    log_file = "/logs/notes.log"
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            return f.read()
    return "No notes found yet."
