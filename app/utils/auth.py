from passlib.context import CryptContext
from app.database import users_collection
from app.exceptions import ResourceNotFoundException,PasswordMismatchException
from app.models.user import UserModel
from datetime import timedelta,datetime,timezone
import jwt
import os


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
    
pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
# create a new access token
def create_access_token(data : dict,expires_in : timedelta | None = None):
    to_encode = data.copy()
    if expires_in:
        expire = datetime.now(timezone.utc) + expires_in
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt



def verify_password(plain_password,hashed_password):
    """
    Verify if the plain password matches the hashed password.
    """
    if not pwd_context.verify(plain_password, hashed_password):
        raise PasswordMismatchException()
    return True

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username : str, password : str):
    user : UserModel = users_collection.find_one({"username" : username})
    if not user:
        raise ResourceNotFoundException("User","username",username)
    if not verify_password(password,user.hashed_password):
        return False
    return user


    