from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid objectid")
        return ObjectId(value)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

#Schema for creating a note
class NoteCreate(BaseModel):
    title: str
    content: str
    done: Optional[bool] = False
    
class NoteResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    content: str
    done: bool
    created_at: datetime
    updated_at: datetime
    user_id: PyObjectId 