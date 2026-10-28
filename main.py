from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from models import NoteModel
from schemas import NoteCreate, NoteOut

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home(name: str = "friend"):
    return {"message": f"Hello, {name}!"}


@app.post("/notes", response_model=NoteOut, status_code=201)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    db_note = NoteModel(**note.model_dump())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


@app.get("/notes", response_model=list[NoteOut])
def list_notes(db: Session = Depends(get_db)):
    return db.scalars(select(NoteModel)).all()


@app.get("/notes/{note_id}", response_model=NoteOut)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.get(NoteModel, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.put("/notes/{note_id}", response_model=NoteOut)
def update_note(note_id: int, data: NoteCreate, db: Session = Depends(get_db)):
    note = db.get(NoteModel, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    note.title = data.title
    note.content = data.content
    db.commit()
    db.refresh(note)
    return note


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.get(NoteModel, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()