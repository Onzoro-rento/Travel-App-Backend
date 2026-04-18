import uuid
from app.repositories.trip_repository import TripRepository
from app.repositories.trip_member_repository import TripMemberRepository
from app.schemas.requests.trip import TripCreateRequest, TripUpdateRequest
from app.models.trip import Trip
from app.exceptions.app_exceptions import NotFoundException
from app.usecases.permissions import require_member, require_role, validate_date_range


class TripUsecase:
    def __init__(
        self,
        trip_repository: TripRepository,
        trip_member_repository: TripMemberRepository,
    ):
        self.trip_repo = trip_repository
        self.member_repo = trip_member_repository

    async def create(self, request: TripCreateRequest, owner_id: uuid.UUID) -> Trip:
        validate_date_range(request.start_date, request.end_date)
        return await self.trip_repo.create(request, owner_id)

    async def get_list(self, user_id: uuid.UUID, page: int, per_page: int) -> tuple[list[dict], int]:
        return await self.trip_repo.find_all_by_user_id(user_id, page, per_page)

    async def get_detail(self, trip_id: uuid.UUID, user_id: uuid.UUID) -> Trip:
        await require_member(self.member_repo, trip_id, user_id)
        trip = await self.trip_repo.find_by_id(trip_id)
        if not trip:
            raise NotFoundException("旅行が見つかりません")
        return trip

    async def update(
        self, trip_id: uuid.UUID, user_id: uuid.UUID, request: TripUpdateRequest
    ) -> Trip:
        await require_role(self.member_repo, trip_id, user_id, ("owner", "editor"))
        trip = await self.trip_repo.find_by_id(trip_id)
        if not trip:
            raise NotFoundException("旅行が見つかりません")
        effective_start = request.start_date if request.start_date is not None else trip.start_date
        effective_end = request.end_date if request.end_date is not None else trip.end_date
        validate_date_range(effective_start, effective_end)
        return await self.trip_repo.update(trip, request)

    async def delete(self, trip_id: uuid.UUID, user_id: uuid.UUID) -> None:
        await require_role(self.member_repo, trip_id, user_id, ("owner",))
        trip = await self.trip_repo.find_by_id(trip_id)
        if not trip:
            raise NotFoundException("旅行が見つかりません")
        await self.trip_repo.delete(trip)
