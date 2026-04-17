from pydantic import BaseModel, Field
from typing import Literal


class CandidateSpotCreateRequest(BaseModel):
    """POST /trips/:tripId/candidates"""
    google_place_id: str = Field(min_length=1)


class CandidateSpotStatusUpdateRequest(BaseModel):
    """PATCH /trips/:tripId/candidates/:candidateId"""
    status: Literal["in_pool", "in_timeline"]
