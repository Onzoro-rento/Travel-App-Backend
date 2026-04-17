from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class ActivityCreateRequest(BaseModel):
    """POST /trips/:tripId/itinerary"""
    day_number: int = Field(ge=1)
    spot_id: UUID
    sort_order: str = Field(min_length=1)
    start_time: datetime | None = Field(default=None)
    memo: str | None = Field(default=None)


class ActivityUpdateRequest(BaseModel):
    """PATCH /trips/:tripId/itinerary/:activityId"""
    sort_order: str | None = Field(default=None, min_length=1)
    start_time: datetime | None = Field(default=None)
    memo: str | None = Field(default=None)


class ReorderOperationItem(BaseModel):
    activity_id: UUID
    sort_order: str = Field(min_length=1)
    day_number: int = Field(ge=1)


class ActivityReorderRequest(BaseModel):
    """PATCH /trips/:tripId/itinerary/reorder"""
    operations: list[ReorderOperationItem] = Field(min_length=1)
