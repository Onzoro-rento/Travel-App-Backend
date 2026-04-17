from pydantic import BaseModel, Field, model_validator
from datetime import date


class TripCreateRequest(BaseModel):
    """POST /trips"""
    title: str = Field(min_length=1, max_length=100)
    cover_photo_url: str | None = Field(default=None)
    start_date: date | None = Field(default=None)
    end_date: date | None = Field(default=None)

    @model_validator(mode="after")
    def validate_date_range(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValueError("start_date は end_date より前である必要があります")
        return self


class TripUpdateRequest(BaseModel):
    """PATCH /trips/:tripId"""
    title: str | None = Field(default=None, min_length=1, max_length=100)
    cover_photo_url: str | None = Field(default=None)
    start_date: date | None = Field(default=None)
    end_date: date | None = Field(default=None)

    @model_validator(mode="after")
    def validate_date_range(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValueError("start_date は end_date より前である必要があります")
        return self


class TripJoinRequest(BaseModel):
    """POST /trips/:tripId/join"""
    invite_code: str = Field(min_length=1, max_length=20)
