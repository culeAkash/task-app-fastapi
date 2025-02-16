from pydantic import BaseModel,field_validator,Field
from datetime import datetime
from bson import ObjectId

class NoteModel(BaseModel):
    def __init__(
        self,
        user_id: ObjectId,
        title: str = Field(...,max_length=100,min_length=3),
        content: str = Field(...,max_length=100,min_length=3),
        done: bool = Field(False),
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now(),
        _id: ObjectId = None,
    ):
        self._id = _id
        self.title = title
        self.content = content
        self.user_id = user_id
        self.done = done
        self.created_at = created_at
        self.updated_at = updated_at
        
    
    def to_dict(self):
        return {
            "_id": self._id,
            "title": self.title,
            "content": self.content,
            "user_id": self.user_id,
            "done": self.done,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "tags": self.tags,
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            _id=data.get("_id"),
            title=data.get("title"),
            content=data.get("content"),
            user_id=data.get("user_id"),
            done=data.get("done", False),
            created_at=data.get("created_at", datetime.now()),
            updated_at=data.get("updated_at", datetime.now()),
            tags=data.get("tags", []),
        )
        
    @field_validator("title")
    def _validate_title(self, value: str):
        if len(value) < 3 or len(value) > 100:
            raise ValueError("Title must be between 3 and 100 characters long")
        return value
    
    @field_validator("content")
    def _validate_content(self, value: str):
        if len(value) < 3 or len(value) > 100:
            raise ValueError("Content must be between 3 and 100 characters long")
        return value