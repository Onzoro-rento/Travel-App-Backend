import uuid
from datetime import date

from app.repositories.trip_member_repository import TripMemberRepository
from app.exceptions.app_exceptions import (
    NotFoundException,
    ForbiddenException,
    InvalidDateRangeException,
)


async def require_member(
    member_repo: TripMemberRepository,
    trip_id: uuid.UUID,
    user_id: uuid.UUID,
) -> None:
    member = await member_repo.find_by_trip_and_user(trip_id, user_id)
    if not member:
        raise NotFoundException("旅行が見つかりません")


async def require_role(
    member_repo: TripMemberRepository,
    trip_id: uuid.UUID,
    user_id: uuid.UUID,
    roles: tuple,
) -> None:
    member = await member_repo.find_by_trip_and_user(trip_id, user_id)
    if not member:
        raise NotFoundException("旅行が見つかりません")
    if member.role not in roles:
        raise ForbiddenException()


def validate_date_range(start_date: date | None, end_date: date | None) -> None:
    if start_date and end_date and start_date > end_date:
        raise InvalidDateRangeException()
