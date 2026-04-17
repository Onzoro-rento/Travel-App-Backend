from pydantic import BaseModel, Field
from typing import Literal


class TripMemberRoleUpdateRequest(BaseModel):
    """PATCH /trips/:tripId/members/:userId"""
    role: Literal["owner", "editor", "viewer"]
