import uuid
from app.repositories.trip_repository import TripRepository
from app.repositories.trip_member_repository import TripMemberRepository
from app.schemas.requests.trip_member import TripMemberRoleUpdateRequest
from app.models.trip_member import TripMember
from app.exceptions.app_exceptions import (
    NotFoundException,
    ForbiddenException,
    AlreadyMemberException,
    InvalidInviteCodeException,
)


class TripMemberUsecase:
    def __init__(
        self,
        trip_repository: TripRepository,
        trip_member_repository: TripMemberRepository,
    ):
        self.trip_repo = trip_repository
        self.member_repo = trip_member_repository

    async def join(self, invite_code: str, user_id: uuid.UUID) -> TripMember:
        trip = await self.trip_repo.find_by_invite_code(invite_code)
        if not trip:
            raise InvalidInviteCodeException()

        existing = await self.member_repo.find_by_trip_and_user(trip.id, user_id)
        if existing:
            raise AlreadyMemberException()

        return await self.member_repo.create(trip.id, user_id, "editor")

    async def get_members(self, trip_id: uuid.UUID, user_id: uuid.UUID) -> list:
        await self._require_member(trip_id, user_id)
        return await self.member_repo.find_all_by_trip_id(trip_id)

    async def update_role(
        self,
        trip_id: uuid.UUID,
        target_user_id: uuid.UUID,
        user_id: uuid.UUID,
        request: TripMemberRoleUpdateRequest,
    ) -> TripMember:
        await self._require_role(trip_id, user_id, ("owner",))
        member = await self.member_repo.find_by_trip_and_user(trip_id, target_user_id)
        if not member:
            raise NotFoundException("メンバーが見つかりません")
        return await self.member_repo.update_role(member, request.role)

    async def remove(
        self, trip_id: uuid.UUID, target_user_id: uuid.UUID, user_id: uuid.UUID
    ) -> None:
        await self._require_role(trip_id, user_id, ("owner",))
        if target_user_id == user_id:
            raise ForbiddenException("自分自身を削除することはできません")
        member = await self.member_repo.find_by_trip_and_user(trip_id, target_user_id)
        if not member:
            raise NotFoundException("メンバーが見つかりません")
        await self.member_repo.delete(member)

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
