from models.note import Note
from schemas.note_schemas import CreateAndUpdateNoteSchema
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


def get_notes(db: Session, limit, page, search, user_info):
    # print("****", user_info)
    skip = (page - 1) * limit
    notes = db.query(Note).filter(
        Note.title.contains(search)).order_by(Note.updatedAt).limit(limit).offset(skip).all()
    
    return { "success": False, "message": "notes_fetched_successfully", "data": notes }

def create_note(payload: CreateAndUpdateNoteSchema, db: Session):
    new_note = Note(**payload.dict())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return { "success": True, "data": new_note, "message": "notes_created_successfully" }

def update_note(noteId: str, payload: CreateAndUpdateNoteSchema, db: Session):
    note_query = db.query(Note).filter(Note.id == noteId)
    db_note = note_query.first()

    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No note with this id: {noteId} found')
    update_data = payload.dict(exclude_unset=True)
    note_query.filter(Note.id == noteId).update(update_data, synchronize_session=False)

    db.commit()
    db.refresh(db_note)
    return { "success": True, "data": db_note, "message": "note_updated" }

def get_note(noteId: str, db: Session):
    note = db.query(Note).filter(Note.id == noteId).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No note with this id: {noteId} found")
    return { "success": True, "data": note, "message": "note_fetched" }

def delete_note(noteId: str, db: Session):
    note_query = db.query(Note).filter(Note.id == noteId)
    note = note_query.first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No note with this id: {noteId} found')
    note_query.delete(synchronize_session=False)
    db.commit()
    return { "success": True, "message": "note_deleted" }