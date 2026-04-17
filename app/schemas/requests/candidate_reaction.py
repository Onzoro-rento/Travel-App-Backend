from pydantic import BaseModel, Field


class CandidateReactionUpsertRequest(BaseModel):
    """PUT /trips/:tripId/candidates/:candidateId/reactions"""
    emoji_type: str = Field(min_length=1)
