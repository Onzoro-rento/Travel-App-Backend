from pydantic import BaseModel, Field


class UserUpdateRequest(BaseModel):
    """PATCH /users/me"""
    name: str | None = Field(default=None, min_length=1, max_length=50)
    avatar_url: str | None = Field(default=None)
