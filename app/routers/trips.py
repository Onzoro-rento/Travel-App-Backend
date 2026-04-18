import uuid
from fastapi import APIRouter, Depends, Query, status
from app.config.jwt import get_current_user_id
from app.config.dependency import get_trip_usecase
from app.usecases.trip_usecase import TripUsecase
from app.schemas.requests.trip import TripCreateRequest, TripUpdateRequest
from app.schemas.responses.trip import TripResponse, TripDetailResponse, TripListResponse

router = APIRouter(prefix="/trips", tags=["trips"])


@router.post("", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
async def create_trip(
    request: TripCreateRequest,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    usecase: TripUsecase = Depends(get_trip_usecase),
):
    return await usecase.create(request, current_user_id)


@router.get("", response_model=TripListResponse)
async def list_trips(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=50),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    usecase: TripUsecase = Depends(get_trip_usecase),
):
    items, total = await usecase.get_list(current_user_id, page, per_page)
    import math
    return {
        "data": items,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total_count": total,
            "total_pages": math.ceil(total / per_page) if total else 0,
        },
    }


@router.get("/{trip_id}", response_model=TripDetailResponse)
async def get_trip(
    trip_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    usecase: TripUsecase = Depends(get_trip_usecase),
):
    return await usecase.get_detail(trip_id, current_user_id)


@router.patch("/{trip_id}", response_model=TripResponse)
async def update_trip(
    trip_id: uuid.UUID,
    request: TripUpdateRequest,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    usecase: TripUsecase = Depends(get_trip_usecase),
):
    return await usecase.update(trip_id, current_user_id, request)


@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trip(
    trip_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    usecase: TripUsecase = Depends(get_trip_usecase),
):
    await usecase.delete(trip_id, current_user_id)
