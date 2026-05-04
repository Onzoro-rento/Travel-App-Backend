from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime
from app.schemas.responses.trip_member import TripMemberDetailResponse


class TripResponse(BaseModel):
    id: UUID
    title: str
    cover_photo_url: str | None
    start_date: date | None
    end_date: date | None
    invite_code: str | None
    created_at: datetime
    

    model_config = {"from_attributes": True}


class TripDetailResponse(BaseModel):
    id: UUID
    title: str
    cover_photo_url: str | None
    start_date: date | None
    end_date: date | None
    invite_code: str | None
    members: list[TripMemberDetailResponse]
    created_at: datetime
    updated_at: datetime
    note:str | None

    model_config = {"from_attributes": True}


class TripListItemResponse(BaseModel):
    id: UUID
    title: str
    cover_photo_url: str | None
    start_date: date | None
    end_date: date | None
    my_role: str
    member_count: int
    note:str | None
    model_config = {"from_attributes": True}


class PaginationResponse(BaseModel):
    page: int
    per_page: int
    total_count: int
    total_pages: int


class TripListResponse(BaseModel):
    data: list[TripListItemResponse]
    pagination: PaginationResponse
