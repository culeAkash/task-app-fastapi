from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional
from bson import ObjectId

from pydantic.json_schema import JsonSchemaValue

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise ValueError("Invalid ObjectId")
        return str(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        json_schema.update(type="string")
        return json_schema

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