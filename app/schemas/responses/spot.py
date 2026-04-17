from pydantic import BaseModel
from uuid import UUID


class SpotResponse(BaseModel):
    id: UUID
    google_place_id: str
    name: str
    address: str | None
    latitude: float
    longitude: float

    model_config = {"from_attributes": True}


class SpotListResponse(BaseModel):
    data: list[SpotResponse]
