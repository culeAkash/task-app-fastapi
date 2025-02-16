from pydantic import BaseModel,Field,EmailStr
from bson import ObjectId

class UserModel(BaseModel):
    username : str
    email : str
    hashed_password : str
    full_name : str | None = None
    disabled : bool = False
    _id : ObjectId = None
    about : str = None

    
    
        
    