import uuid
from collections import defaultdict
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.candidate_spot import CandidateSpot
from app.models.candidate_reaction import CandidateReaction
from app.models.spot import Spot
from app.models.user import User


class CandidateSpotRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_by_id(self, candidate_id: uuid.UUID) -> CandidateSpot | None:
        result = await self.db.execute(
            select(CandidateSpot).where(CandidateSpot.id == candidate_id)
        )
        return result.scalar_one_or_none()

    async def find_all_by_trip_id(
        self,
        trip_id: uuid.UUID,
        current_user_id: uuid.UUID,
        status: str | None = None,
    ) -> list[dict]:
        stmt = (
            select(CandidateSpot, Spot, User)
            .join(Spot, Spot.id == CandidateSpot.spot_id)
            .join(User, User.id == CandidateSpot.added_by)
            .where(CandidateSpot.trip_id == trip_id)
        )
        if status:
            stmt = stmt.where(CandidateSpot.status == status)

        rows = await self.db.execute(stmt)

        # reactions を一括取得して集計
        reaction_rows = await self.db.execute(
            select(
                CandidateReaction.candidate_spot_id,
                CandidateReaction.emoji_type,
                CandidateReaction.user_id,
                func.count().label("cnt"),
            )
            .where(CandidateReaction.candidate_spot_id.in_(
                select(CandidateSpot.id).where(CandidateSpot.trip_id == trip_id)
            ))
            .group_by(
                CandidateReaction.candidate_spot_id,
                CandidateReaction.emoji_type,
                CandidateReaction.user_id,
            )
        )
        reactions = reaction_rows.all()

        summary_map: dict[uuid.UUID, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        my_reactions_map: dict[uuid.UUID, list[str]] = defaultdict(list)
        for r in reactions:
            summary_map[r.candidate_spot_id][r.emoji_type] += r.cnt
            if r.user_id == current_user_id:
                my_reactions_map[r.candidate_spot_id].append(r.emoji_type)

        items = []
        for row in rows:
            candidate, spot, added_by_user = row
            items.append({
                "candidate": candidate,
                "spot": spot,
                "added_by": added_by_user,
                "reactions_summary": dict(summary_map[candidate.id]),
                "my_reactions": my_reactions_map[candidate.id],
            })
        return items

    async def create(
        self, trip_id: uuid.UUID, spot_id: uuid.UUID, added_by: uuid.UUID
    ) -> CandidateSpot:
        candidate = CandidateSpot(trip_id=trip_id, spot_id=spot_id, added_by=added_by)
        self.db.add(candidate)
        await self.db.commit()
        await self.db.refresh(candidate)
        return candidate

    async def update_status(self, candidate: CandidateSpot, status: str) -> CandidateSpot:
        candidate.status = status
        await self.db.commit()
        await self.db.refresh(candidate)
        return candidate

    async def delete(self, candidate: CandidateSpot) -> None:
        await self.db.delete(candidate)
        await self.db.commit()
