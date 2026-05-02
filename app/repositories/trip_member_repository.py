import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.trip_member import TripMember
from app.models.user import User


class TripMemberRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_by_trip_and_user(
        self, trip_id: uuid.UUID, user_id: uuid.UUID
    ) -> TripMember | None:
        result = await self.db.execute(
            select(TripMember).where(
                TripMember.trip_id == trip_id,
                TripMember.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def find_all_by_trip_id(
        self, trip_id: uuid.UUID
    ) -> list[tuple[TripMember, User]]:
        result = await self.db.execute(
            select(TripMember, User)
            .join(User, User.id == TripMember.user_id)
            .where(TripMember.trip_id == trip_id)
        )
        return list(result.tuples().all())

    async def create(
        self, trip_id: uuid.UUID, user_id: uuid.UUID, role: str
    ) -> TripMember:
        member = TripMember(trip_id=trip_id, user_id=user_id, role=role)
        self.db.add(member)
        await self.db.commit()
        await self.db.refresh(member)
        return member

    async def update_role(self, member: TripMember, role: str) -> TripMember:
        member.role = role
        await self.db.commit()
        await self.db.refresh(member)
        return member

    async def delete(self, member: TripMember) -> None:
        await self.db.delete(member)
        await self.db.commit()
