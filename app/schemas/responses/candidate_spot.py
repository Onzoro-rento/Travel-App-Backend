from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from app.schemas.responses.spot import SpotResponse


class AddedByResponse(BaseModel):
    id: UUID
    name: str

    model_config = {"from_attributes": True}


class CandidateSpotResponse(BaseModel):
    """POST /trips/:tripId/candidates のレスポンス"""
    id: UUID
    trip_id: UUID
    spot: SpotResponse
    added_by: UUID
    status: str
    reactions_summary: dict[str, int] = Field(default_factory=dict)
    created_at: datetime

    model_config = {"from_attributes": True}


class CandidateSpotListItemResponse(BaseModel):
    """GET /trips/:tripId/candidates の data[] 各要素"""
    id: UUID
    spot: SpotResponse
    added_by: AddedByResponse
    status: str
    reactions_summary: dict[str, int]
    my_reaction: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class CandidateSpotListResponse(BaseModel):
    data: list[CandidateSpotListItemResponse]
