from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime
from app.schemas.responses.spot import SpotResponse


class ActivityResponse(BaseModel):
    """タイムラインの1アクティビティ"""
    id: UUID
    sort_order: str
    spot: SpotResponse
    start_time: datetime | None
    memo: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ItineraryDayResponse(BaseModel):
    day_number: int
    date: date | None
    activities: list[ActivityResponse]


class ItineraryResponse(BaseModel):
    """GET /trips/:tripId/itinerary のレスポンス"""
    trip_id: UUID
    days: list[ItineraryDayResponse]


class ReorderResponse(BaseModel):
    """PATCH /trips/:tripId/itinerary/reorder のレスポンス"""
    updated_count: int
