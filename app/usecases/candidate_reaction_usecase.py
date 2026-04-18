import uuid
from app.repositories.candidate_reaction_repository import CandidateReactionRepository
from app.repositories.candidate_spot_repository import CandidateSpotRepository
from app.repositories.trip_member_repository import TripMemberRepository
from app.schemas.requests.candidate_reaction import CandidateReactionUpsertRequest
from app.models.candidate_reaction import CandidateReaction
from app.exceptions.app_exceptions import NotFoundException
from app.usecases.permissions import require_member


class CandidateReactionUsecase:
    def __init__(
        self,
        reaction_repository: CandidateReactionRepository,
        candidate_spot_repository: CandidateSpotRepository,
        trip_member_repository: TripMemberRepository,
    ):
        self.reaction_repo = reaction_repository
        self.candidate_repo = candidate_spot_repository
        self.member_repo = trip_member_repository

    async def upsert(
        self,
        trip_id: uuid.UUID,
        candidate_id: uuid.UUID,
        user_id: uuid.UUID,
        request: CandidateReactionUpsertRequest,
    ) -> CandidateReaction:
        await require_member(self.member_repo, trip_id, user_id)
        candidate = await self.candidate_repo.find_by_id(candidate_id)
        if not candidate or candidate.trip_id != trip_id:
            raise NotFoundException("候補スポットが見つかりません")
        return await self.reaction_repo.upsert(candidate_id, user_id, request.emoji_type)

    async def delete(
        self,
        trip_id: uuid.UUID,
        candidate_id: uuid.UUID,
        user_id: uuid.UUID,
        emoji_type: str,
    ) -> None:
        await require_member(self.member_repo, trip_id, user_id)
        candidate = await self.candidate_repo.find_by_id(candidate_id)
        if not candidate or candidate.trip_id != trip_id:
            raise NotFoundException("候補スポットが見つかりません")
        reaction = await self.reaction_repo.find_by(candidate_id, user_id, emoji_type)
        if not reaction:
            raise NotFoundException("リアクションが見つかりません")
        await self.reaction_repo.delete(reaction)
