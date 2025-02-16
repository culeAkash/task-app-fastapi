from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import Depends,HTTPException,status,APIRouter
import os
import jwt
from jwt.exceptions import InvalidTokenError,ExpiredSignatureError
from pydantic import BaseModel
from app.database import users_collection
from app.models.user import UserModel
from app.exceptions import ResourceNotFoundException
from app.utils.auth import authenticate_user,create_access_token
from datetime import timedelta
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class TokenModel(BaseModel):
    access_token : str
    token_type : str
    
class TokenData(BaseModel):
    username : str | None = None


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
router = APIRouter()

@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokenModel:
    user = authenticate_user(form_data.username,form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={
        "sub" : user.username,
    },expires_in=access_token_expires)
    return TokenModel(access_token=access_token, token_type="bearer")



def get_user(username:str):
    user = users_collection.find_one({"username": username})
    if not user:
        raise ResourceNotFoundException("User","username",username)
    return UserModel(**user)
    

async def get_current_user(token : Annotated[str,Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    expired_token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token has expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except ExpiredSignatureError:
        raise expired_token_exception
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
    