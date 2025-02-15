from fastapi import APIRouter, Depends, HTTPException
from app.database import notes_collection
from app.models.note import NoteModel
from app.schemas.note import NoteCreate,NoteResponse

router = APIRouter()

@router.post("/",response_model=NoteResponse)
async def create_note(note: NoteCreate):
    
    if result.inserted_id:
        return {"message": "Note created", "note_id": str(result.inserted_id)}
    raise HTTPException(status_code=500, detail="Failed to create note")