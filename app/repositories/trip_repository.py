import uuid
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.trip import Trip
from app.models.trip_member import TripMember
from app.schemas.requests.trip import TripCreateRequest, TripUpdateRequest


class TripRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_by_id(self, trip_id: uuid.UUID) -> Trip | None:
        result = await self.db.execute(
            select(Trip).where(Trip.id == trip_id)
        )
        return result.scalar_one_or_none()

    async def find_all_by_user_id(
        self, user_id: uuid.UUID, page: int, per_page: int
    ) -> tuple[list[dict], int]:
        # member_count サブクエリ
        member_count_sq = (
            select(func.count())
            .where(TripMember.trip_id == Trip.id)
            .correlate(Trip)
            .scalar_subquery()
        )

        stmt = (
            select(Trip, TripMember.role, member_count_sq.label("member_count"))
            .join(TripMember, (TripMember.trip_id == Trip.id) & (TripMember.user_id == user_id))
            .order_by(Trip.created_at.desc())
        )

        total = await self.db.scalar(
            select(func.count()).select_from(stmt.subquery())
        )
        rows = await self.db.execute(stmt.offset((page - 1) * per_page).limit(per_page))

        items = [
            {**row.Trip.__dict__, "my_role": row.role, "member_count": row.member_count}
            for row in rows
        ]
        return items, total

    async def create(self, request: TripCreateRequest, owner_id: uuid.UUID) -> Trip:
        trip = Trip(
            **request.model_dump(),
            invite_code=str(uuid.uuid4())[:8].upper(),
        )
        self.db.add(trip)
        await self.db.flush()  # IDを確定させてからmemberを追加

        member = TripMember(trip_id=trip.id, user_id=owner_id, role="owner")
        self.db.add(member)
        await self.db.commit()
        await self.db.refresh(trip)
        return trip

    async def update(self, trip: Trip, request: TripUpdateRequest) -> Trip:
        for key, value in request.model_dump(exclude_unset=True).items():
            setattr(trip, key, value)
        await self.db.commit()
        await self.db.refresh(trip)
        return trip

    async def delete(self, trip: Trip) -> None:
        await self.db.delete(trip)
        await self.db.commit()
