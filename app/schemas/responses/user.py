from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    avatar_url: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
