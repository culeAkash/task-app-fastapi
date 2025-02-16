from app.schemas.user import UserCreate
from app.schemas.response import ApiResponse
from fastapi import APIRouter
from app.utils.user import create_new_user

router = APIRouter()

@router.post("/create_user")
async def create_user(userData : UserCreate) -> ApiResponse:
    created_user = await create_new_user(userData)
    response = ApiResponse(
        success = True,
        message = "User created successfully",
        data = {"user" : created_user},
        http_status = 201,
    )
    return response