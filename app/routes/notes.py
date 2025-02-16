from fastapi import APIRouter
from app.schemas.note import NoteCreate,NoteResponse

router = APIRouter()

@router.post("/",response_model=NoteResponse)
async def create_note(note: NoteCreate):
    # check if user already exists
    pass