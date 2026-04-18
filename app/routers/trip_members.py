import uuid
from fastapi import APIRouter, Depends, status
from app.config.jwt import get_current_user_id
from app.config.dependency import get_trip_member_usecase
from app.usecases.trip_member_usecase import TripMemberUsecase
from app.schemas.requests.trip import TripJoinRequest
from app.schemas.requests.trip_member import TripMemberRoleUpdateRequest
from app.schemas.responses.trip_member import TripMemberResponse

router = APIRouter(prefix="/trips", tags=["trip_members"])


@router.post("/{trip_id}/join", response_model=TripMemberResponse, status_code=status.HTTP_201_CREATED)
async def join_trip(
    trip_id: uuid.UUID,
    request: TripJoinRequest,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    usecase: TripMemberUsecase = Depends(get_trip_member_usecase),
):
    return await usecase.join(request.invite_code, current_user_id)


@router.patch("/{trip_id}/members/{user_id}", response_model=TripMemberResponse)
async def update_member_role(
    trip_id: uuid.UUID,
    user_id: uuid.UUID,
    request: TripMemberRoleUpdateRequest,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    usecase: TripMemberUsecase = Depends(get_trip_member_usecase),
):
    return await usecase.update_role(trip_id, user_id, current_user_id, request)


@router.delete("/{trip_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    trip_id: uuid.UUID,
    user_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    usecase: TripMemberUsecase = Depends(get_trip_member_usecase),
):
    await usecase.remove(trip_id, user_id, current_user_id)
