from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class TripMemberDetailResponse(BaseModel):
    """TripDetailResponse の members[] ネスト用"""
    user_id: UUID
    name: str
    avatar_url: str | None
    role: str

    model_config = {"from_attributes": True}


class TripMemberResponse(BaseModel):
    """POST /trips/:tripId/join, PATCH /trips/:tripId/members/:userId のレスポンス"""
    trip_id: UUID
    user_id: UUID
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}
