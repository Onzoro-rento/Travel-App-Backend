from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class CandidateReactionResponse(BaseModel):
    """PUT /trips/:tripId/candidates/:candidateId/reactions のレスポンス"""
    id: UUID
    candidate_spot_id: UUID
    user_id: UUID
    emoji_type: str
    created_at: datetime

    model_config = {"from_attributes": True}
