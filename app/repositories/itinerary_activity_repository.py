import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.itinerary_activity import ItineraryActivity
from app.models.spot import Spot
from app.schemas.requests.itinerary import (
    ActivityCreateRequest,
    ActivityUpdateRequest,
    ReorderOperationItem,
)


class ItineraryActivityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_by_id(self, activity_id: uuid.UUID) -> ItineraryActivity | None:
        result = await self.db.execute(
            select(ItineraryActivity).where(ItineraryActivity.id == activity_id)
        )
        return result.scalar_one_or_none()

    async def find_all_by_trip_id(
        self, trip_id: uuid.UUID
    ) -> list[tuple[ItineraryActivity, Spot]]:
        result = await self.db.execute(
            select(ItineraryActivity, Spot)
            .join(Spot, Spot.id == ItineraryActivity.spot_id)
            .where(ItineraryActivity.trip_id == trip_id)
            .order_by(ItineraryActivity.day_number, ItineraryActivity.sort_order)
        )
        return list(result.tuples().all())

    async def create(
        self, trip_id: uuid.UUID, request: ActivityCreateRequest
    ) -> ItineraryActivity:
        activity = ItineraryActivity(trip_id=trip_id, **request.model_dump())
        self.db.add(activity)
        await self.db.commit()
        await self.db.refresh(activity)
        return activity

    async def update(
        self, activity: ItineraryActivity, request: ActivityUpdateRequest
    ) -> ItineraryActivity:
        for key, value in request.model_dump(exclude_unset=True).items():
            setattr(activity, key, value)
        await self.db.commit()
        await self.db.refresh(activity)
        return activity

    async def bulk_update_order(self, operations: list[ReorderOperationItem]) -> int:
        for op in operations:
            result = await self.db.execute(
                select(ItineraryActivity).where(ItineraryActivity.id == op.activity_id)
            )
            activity = result.scalar_one_or_none()
            if activity:
                activity.sort_order = op.sort_order
                activity.day_number = op.day_number
        await self.db.commit()
        return len(operations)

    async def delete(self, activity: ItineraryActivity) -> None:
        await self.db.delete(activity)
        await self.db.commit()
