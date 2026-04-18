import uuid
from fastapi import APIRouter, Depends, Query, status
from app.config.jwt import get_current_user_id
from app.config.dependency import get_candidate_reaction_usecase
from app.usecases.candidate_reaction_usecase import CandidateReactionUsecase
from app.schemas.requests.candidate_reaction import CandidateReactionUpsertRequest
from app.schemas.responses.candidate_reaction import CandidateReactionResponse

router = APIRouter(prefix="/trips", tags=["reactions"])


@router.put(
    "/{trip_id}/candidates/{candidate_id}/reactions",
    response_model=CandidateReactionResponse,
)
async def upsert_reaction(
    trip_id: uuid.UUID,
    candidate_id: uuid.UUID,
    request: CandidateReactionUpsertRequest,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    usecase: CandidateReactionUsecase = Depends(get_candidate_reaction_usecase),
):
    return await usecase.upsert(trip_id, candidate_id, current_user_id, request)


@router.delete(
    "/{trip_id}/candidates/{candidate_id}/reactions",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_reaction(
    trip_id: uuid.UUID,
    candidate_id: uuid.UUID,
    emoji_type: str = Query(),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    usecase: CandidateReactionUsecase = Depends(get_candidate_reaction_usecase),
):
    await usecase.delete(trip_id, candidate_id, current_user_id, emoji_type)
