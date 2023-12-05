from database import get_db
from fastapi import APIRouter, Depends
from oauth2 import get_current_user
from repository.note import create_note, delete_note, get_note, get_notes, update_note
from schemas.note_schemas import CreateAndUpdateNoteSchema
from schemas.user_schemas import ResponseModal
from sqlalchemy.orm import Session

from database import get_db

router = APIRouter(tags=["Notes"], prefix="/notes")

# Get All Notes API
@router.get("/", response_model=ResponseModal)
def get_notes_route( db: Session = Depends(get_db), limit: int = 10, page:int = 1, search: str ="", user_info: Session=Depends(get_current_user) ):
    return get_notes(db, limit, page, search, user_info)

# Create Note API
@router.post("/", response_model=ResponseModal)
def create_note_route(request: CreateAndUpdateNoteSchema, db: Session = Depends(get_db)):
    return create_note(request, db)

# Update Note API
@router.patch("/{noteId}", response_model=ResponseModal)
def update_note_route(noteId, request: CreateAndUpdateNoteSchema, db: Session = Depends(get_db)):
    return update_note(noteId, request, db)

# Get Note API
@router.get('/{noteId}', response_model=ResponseModal)
def get_note_route(noteId, db: Session = Depends(get_db)):
    return get_note(noteId, db)

# Delete Note API
@router.delete('/{noteId}',  response_model=ResponseModal)
def delete_note_route(noteId, db: Session = Depends(get_db)):
    return delete_note(noteId, db)
