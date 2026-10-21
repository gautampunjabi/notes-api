from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Note(BaseModel):
    title: str
    content: str

notes = {}
next_id = 1

@app.get("/")
def home(name: str = "friend"):
    return {"message": f"Hello, {name}!"}

@app.post("/notes", status_code=201)
def create_note(note: Note):
    global next_id
    notes[next_id] = note
    next_id += 1
    return {"id": next_id - 1, **note.model_dump()}

@app.get("/notes")
def list_notes():
    return notes

@app.get("/notes/{note_id}")
def get_note(note_id: int):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note not found")
    return notes[note_id]
@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note not found")
    del notes[note_id]
    return None