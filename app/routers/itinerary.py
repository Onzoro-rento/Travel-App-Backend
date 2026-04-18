import uuid
from fastapi import APIRouter, Depends, status
from app.config.jwt import get_current_user_id
from app.config.dependency import get_itinerary_usecase
from app.usecases.itinerary_usecase import ItineraryUsecase
from app.schemas.requests.itinerary import (
    ActivityCreateRequest,
    ActivityUpdateRequest,
    ActivityReorderRequest,
)
from app.schemas.responses.itinerary import ActivityResponse, ItineraryResponse, ReorderResponse

router = APIRouter(prefix="/trips", tags=["itinerary"])


@router.get("/{trip_id}/itinerary", response_model=ItineraryResponse)
async def get_itinerary(
    trip_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    usecase: ItineraryUsecase = Depends(get_itinerary_usecase),
):
    return await usecase.get_itinerary(trip_id, current_user_id)


@router.post(
    "/{trip_id}/itinerary",
    response_model=ActivityResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_activity(
    trip_id: uuid.UUID,
    request: ActivityCreateRequest,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    usecase: ItineraryUsecase = Depends(get_itinerary_usecase),
):
    return await usecase.add_activity(trip_id, current_user_id, request)


@router.patch("/{trip_id}/itinerary/{activity_id}", response_model=ActivityResponse)
async def update_activity(
    trip_id: uuid.UUID,
    activity_id: uuid.UUID,
    request: ActivityUpdateRequest,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    usecase: ItineraryUsecase = Depends(get_itinerary_usecase),
):
    return await usecase.update_activity(trip_id, activity_id, current_user_id, request)


@router.delete("/{trip_id}/itinerary/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity(
    trip_id: uuid.UUID,
    activity_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    usecase: ItineraryUsecase = Depends(get_itinerary_usecase),
):
    await usecase.delete_activity(trip_id, activity_id, current_user_id)


@router.patch("/{trip_id}/itinerary/reorder", response_model=ReorderResponse)
async def reorder_activities(
    trip_id: uuid.UUID,
    request: ActivityReorderRequest,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    usecase: ItineraryUsecase = Depends(get_itinerary_usecase),
):
    updated_count = await usecase.reorder(trip_id, current_user_id, request)
    return {"updated_count": updated_count}
