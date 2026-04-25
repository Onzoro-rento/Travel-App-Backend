import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.requests.user import UserUpdateRequest


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_by_id(self, user_id: uuid.UUID) -> User | None:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, id: uuid.UUID, email: str, name: str, avatar_url: str | None) -> User:
        user = User(id=id, email=email, name=name, avatar_url=avatar_url)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update(self, user: User, request: UserUpdateRequest) -> User:
        for key, value in request.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        await self.db.commit()
        await self.db.refresh(user)
        return user
