# Notes API

A simple REST API built with FastAPI.

## Endpoints
- `GET /` - welcome message
- `POST /notes` - create a note
- `GET /notes` - list all notes
- `GET /notes/{note_id}` - get one note
- `PUT /notes/{note_id}` - update a note
- `DELETE /notes/{note_id}` - delete a note

## Run locally
    pip install "fastapi[standard]"
    fastapi dev main.py

Docs available at http://127.0.0.1:8000/docs