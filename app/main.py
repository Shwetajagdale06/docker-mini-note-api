from fastapi.responses import PlainTextResponse
from fastapi import FastAPI, Request
from pydantic import BaseModel
import datetime
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Note(BaseModel):
    message: str

# Route to write a note
@app.post("/note")
def write_note(note: Note):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    with open(f"{log_dir}/notes.log", "a") as f:
        f.write(f"{datetime.datetime.now()}: {note.message}\n")
    return {"status": "saved", "note": note.message}

# Route for basic POST instruction
@app.get("/note")
def note_info():
    return {"info": "Send a POST request with JSON like {'message': 'your note'}"}

# Health check or root route
@app.get("/")
def root():
    return {"message": "Mini Note API is running!"}

# Favicon route to suppress 404 in browsers
@app.get("/favicon.ico")
def favicon():
    return {}

# Route to read the saved logs
@app.get("/logs", response_class=PlainTextResponse)
def read_logs():
    log_file = "logs/notes.log"
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            return f.read()
    return "No notes found yet."
