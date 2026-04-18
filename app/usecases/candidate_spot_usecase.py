import uuid
from app.repositories.candidate_spot_repository import CandidateSpotRepository
from app.repositories.spot_repository import SpotRepository
from app.repositories.trip_member_repository import TripMemberRepository
from app.schemas.requests.candidate_spot import (
    CandidateSpotCreateRequest,
    CandidateSpotStatusUpdateRequest,
)
from app.models.candidate_spot import CandidateSpot
from app.exceptions.app_exceptions import NotFoundException, ForbiddenException


class CandidateSpotUsecase:
    def __init__(
        self,
        candidate_spot_repository: CandidateSpotRepository,
        spot_repository: SpotRepository,
        trip_member_repository: TripMemberRepository,
    ):
        self.candidate_repo = candidate_spot_repository
        self.spot_repo = spot_repository
        self.member_repo = trip_member_repository

    async def add(
        self,
        trip_id: uuid.UUID,
        user_id: uuid.UUID,
        request: CandidateSpotCreateRequest,
    ) -> CandidateSpot:
        await self._require_role(trip_id, user_id, ("owner", "editor"))

        spot = await self.spot_repo.find_by_google_place_id(request.google_place_id)
        if not spot:
            raise NotFoundException("スポットが見つかりません。先にスポット検索で登録してください")

        return await self.candidate_repo.create(trip_id, spot.id, user_id)

    async def get_list(
        self,
        trip_id: uuid.UUID,
        user_id: uuid.UUID,
        status: str | None,
    ) -> list[dict]:
        await self._require_member(trip_id, user_id)
        return await self.candidate_repo.find_all_by_trip_id(trip_id, user_id, status)

    async def update_status(
        self,
        trip_id: uuid.UUID,
        candidate_id: uuid.UUID,
        user_id: uuid.UUID,
        request: CandidateSpotStatusUpdateRequest,
    ) -> CandidateSpot:
        await self._require_role(trip_id, user_id, ("owner", "editor"))
        candidate = await self.candidate_repo.find_by_id(candidate_id)
        if not candidate or candidate.trip_id != trip_id:
            raise NotFoundException("候補スポットが見つかりません")
        return await self.candidate_repo.update_status(candidate, request.status)

    async def delete(
        self, trip_id: uuid.UUID, candidate_id: uuid.UUID, user_id: uuid.UUID
    ) -> None:
        await self._require_role(trip_id, user_id, ("owner", "editor"))
        candidate = await self.candidate_repo.find_by_id(candidate_id)
        if not candidate or candidate.trip_id != trip_id:
            raise NotFoundException("候補スポットが見つかりません")
        await self.candidate_repo.delete(candidate)

    async def _require_member(self, trip_id: uuid.UUID, user_id: uuid.UUID) -> None:
        member = await self.member_repo.find_by_trip_and_user(trip_id, user_id)
        if not member:
            raise NotFoundException("旅行が見つかりません")

    async def _require_role(
        self, trip_id: uuid.UUID, user_id: uuid.UUID, roles: tuple
    ) -> None:
        member = await self.member_repo.find_by_trip_and_user(trip_id, user_id)
        if not member:
            raise NotFoundException("旅行が見つかりません")
        if member.role not in roles:
            raise ForbiddenException()
