from pydantic import BaseModel
from bson import ObjectId

class UserModel(BaseModel):
    def __init__(
        self,
        username : str,
        email : str,
        password : str,
        _id : ObjectId = None,
        about : str = None,
        ):
        self._id = _id
        self.username = username
        self.email = email
        self.password = password
        self.about = about
        
    def to_dict(self):
        return {
            "_id": self._id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "about": self.about,
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            _id=data.get("_id"),
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password"),
            about=data.get("about"),
        )
    