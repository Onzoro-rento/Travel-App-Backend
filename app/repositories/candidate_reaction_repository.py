import uuid
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.candidate_reaction import CandidateReaction


class CandidateReactionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_by(
        self,
        candidate_spot_id: uuid.UUID,
        user_id: uuid.UUID,
        emoji_type: str,
    ) -> CandidateReaction | None:
        result = await self.db.execute(
            select(CandidateReaction).where(
                CandidateReaction.candidate_spot_id == candidate_spot_id,
                CandidateReaction.user_id == user_id,
                CandidateReaction.emoji_type == emoji_type,
            )
        )
        return result.scalar_one_or_none()

    async def upsert(
        self,
        candidate_spot_id: uuid.UUID,
        user_id: uuid.UUID,
        emoji_type: str,
    ) -> CandidateReaction:
        stmt = (
            insert(CandidateReaction)
            .values(
                candidate_spot_id=candidate_spot_id,
                user_id=user_id,
                emoji_type=emoji_type,
            )
            .on_conflict_do_nothing(constraint="uq_reaction")
        )
        await self.db.execute(stmt)
        await self.db.commit()
        return await self.find_by(candidate_spot_id, user_id, emoji_type)

    async def delete(self, reaction: CandidateReaction) -> None:
        await self.db.delete(reaction)
        await self.db.commit()
