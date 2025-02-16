from app.schemas.user import UserCreate,UserResponse
from app.database import users_collection
from app.exceptions import DuplicateKeyException
from app.utils.auth import get_password_hash
from fastapi.exceptions import HTTPException

async def create_new_user(userData : UserCreate) -> UserResponse:
    # check if user is already created
    existing_user = await users_collection.find_one({
        "$or":[{
            "email" : userData.email,
            "username" : userData.username
        }]
    })
    if existing_user:
        raise DuplicateKeyException("Username or email already exists")
    
    # hash the password
    hashed_password = get_password_hash(userData.password)
    
    #Create new user document
    user_dict = userData.model_dump()
    user_dict["password"] = hashed_password
    
    #Insert new user
    result = await users_collection.insert_one(user_dict)
    if result.inserted_id:
        return UserResponse({**result,"_id": result.inserted_id})
    raise HTTPException("Failed to insert user")
    