import uuid
from fastapi import APIRouter, Depends
from app.config.jwt import get_current_user_id, get_current_user_info, UserTokenInfo
from app.config.dependency import get_user_usecase
from app.usecases.user_usecase import UserUsecase
from app.schemas.requests.user import UserUpdateRequest
from app.schemas.responses.user import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_me(
    user_info: UserTokenInfo = Depends(get_current_user_info),
    usecase: UserUsecase = Depends(get_user_usecase),
):
    return await usecase.get_me(user_info)


@router.patch("/me", response_model=UserResponse)
async def update_me(
    request: UserUpdateRequest,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    usecase: UserUsecase = Depends(get_user_usecase),
):
    return await usecase.update_me(current_user_id, request)
