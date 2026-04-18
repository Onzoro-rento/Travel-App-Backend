import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.spot import Spot


class SpotRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_by_id(self, spot_id: uuid.UUID) -> Spot | None:
        result = await self.db.execute(
            select(Spot).where(Spot.id == spot_id)
        )
        return result.scalar_one_or_none()

    async def find_by_google_place_id(self, google_place_id: str) -> Spot | None:
        result = await self.db.execute(
            select(Spot).where(Spot.google_place_id == google_place_id)
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        google_place_id: str,
        name: str,
        address: str | None,
        latitude: float,
        longitude: float,
    ) -> Spot:
        spot = Spot(
            google_place_id=google_place_id,
            name=name,
            address=address,
            latitude=latitude,
            longitude=longitude,
        )
        self.db.add(spot)
        await self.db.commit()
        await self.db.refresh(spot)
        return spot
