from pydantic import BaseModel
from typing import Literal


class TripMemberRoleUpdateRequest(BaseModel):
    """PATCH /trips/:tripId/members/:userId"""
    role: Literal["owner", "editor", "viewer"]
