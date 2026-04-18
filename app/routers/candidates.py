import uuid
from fastapi import APIRouter, Depends, Query, status
from app.config.jwt import get_current_user_id
from app.config.dependency import get_candidate_spot_usecase
from app.usecases.candidate_spot_usecase import CandidateSpotUsecase
from app.schemas.requests.candidate_spot import (
    CandidateSpotCreateRequest,
    CandidateSpotStatusUpdateRequest,
)
from app.schemas.responses.candidate_spot import CandidateSpotResponse, CandidateSpotListResponse

router = APIRouter(prefix="/trips", tags=["candidates"])


@router.post(
    "/{trip_id}/candidates",
    response_model=CandidateSpotResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_candidate(
    trip_id: uuid.UUID,
    request: CandidateSpotCreateRequest,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    usecase: CandidateSpotUsecase = Depends(get_candidate_spot_usecase),
):
    return await usecase.add(trip_id, current_user_id, request)


@router.get("/{trip_id}/candidates", response_model=CandidateSpotListResponse)
async def list_candidates(
    trip_id: uuid.UUID,
    status: str | None = Query(default=None),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    usecase: CandidateSpotUsecase = Depends(get_candidate_spot_usecase),
):
    items = await usecase.get_list(trip_id, current_user_id, status)
    return {"data": items}


@router.patch("/{trip_id}/candidates/{candidate_id}", response_model=CandidateSpotResponse)
async def update_candidate_status(
    trip_id: uuid.UUID,
    candidate_id: uuid.UUID,
    request: CandidateSpotStatusUpdateRequest,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    usecase: CandidateSpotUsecase = Depends(get_candidate_spot_usecase),
):
    return await usecase.update_status(trip_id, candidate_id, current_user_id, request)


@router.delete("/{trip_id}/candidates/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate(
    trip_id: uuid.UUID,
    candidate_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    usecase: CandidateSpotUsecase = Depends(get_candidate_spot_usecase),
):
    await usecase.delete(trip_id, candidate_id, current_user_id)
