from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from models import NoteModel, UserModel
from schemas import NoteCreate, NoteOut, UserCreate, UserOut, Token
from auth import hash_password, verify_password, create_access_token, get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home(name: str = "friend"):
    return {"message": f"Hello, {name}!"}


@app.post("/signup", response_model=UserOut, status_code=201)
def signup(data: UserCreate, db: Session = Depends(get_db)):
    existing = db.scalar(select(UserModel).where(UserModel.email == data.email))
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    user = UserModel(email=data.email, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.scalar(select(UserModel).where(UserModel.email == form.username))
    if user is None or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return {"access_token": create_access_token(user.id), "token_type": "bearer"}


@app.post("/notes", response_model=NoteOut, status_code=201)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    db_note = NoteModel(**note.model_dump(), owner_id=user.id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


@app.get("/notes", response_model=list[NoteOut])
def list_notes(
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    return db.scalars(select(NoteModel).where(NoteModel.owner_id == user.id)).all()


def get_owned_note(db: Session, note_id: int, user: UserModel) -> NoteModel:
    note = db.get(NoteModel, note_id)
    if note is None or note.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.get("/notes/{note_id}", response_model=NoteOut)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    return get_owned_note(db, note_id, user)


@app.put("/notes/{note_id}", response_model=NoteOut)
def update_note(
    note_id: int,
    data: NoteCreate,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    note = get_owned_note(db, note_id, user)
    note.title = data.title
    note.content = data.content
    db.commit()
    db.refresh(note)
    return note


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    note = get_owned_note(db, note_id, user)
    db.delete(note)
    db.commit()