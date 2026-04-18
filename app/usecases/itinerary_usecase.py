import uuid
from datetime import date, timedelta
from app.repositories.itinerary_activity_repository import ItineraryActivityRepository
from app.repositories.trip_repository import TripRepository
from app.repositories.trip_member_repository import TripMemberRepository
from app.schemas.requests.itinerary import (
    ActivityCreateRequest,
    ActivityUpdateRequest,
    ActivityReorderRequest,
)
from app.models.itinerary_activity import ItineraryActivity
from app.exceptions.app_exceptions import NotFoundException
from app.usecases.permissions import require_member, require_role


class ItineraryUsecase:
    def __init__(
        self,
        itinerary_repository: ItineraryActivityRepository,
        trip_repository: TripRepository,
        trip_member_repository: TripMemberRepository,
    ):
        self.itinerary_repo = itinerary_repository
        self.trip_repo = trip_repository
        self.member_repo = trip_member_repository

    async def get_itinerary(self, trip_id: uuid.UUID, user_id: uuid.UUID) -> dict:
        await require_member(self.member_repo, trip_id, user_id)
        trip = await self.trip_repo.find_by_id(trip_id)
        if not trip:
            raise NotFoundException("旅行が見つかりません")

        rows = await self.itinerary_repo.find_all_by_trip_id(trip_id)

        days: dict[int, dict] = {}
        for activity, spot in rows:
            day_num = activity.day_number
            if day_num not in days:
                date_val: date | None = None
                if trip.start_date:
                    date_val = trip.start_date + timedelta(days=day_num - 1)
                days[day_num] = {"day_number": day_num, "date": date_val, "activities": []}
            days[day_num]["activities"].append({"activity": activity, "spot": spot})

        return {"trip_id": trip_id, "days": list(days.values())}

    async def add_activity(
        self, trip_id: uuid.UUID, user_id: uuid.UUID, request: ActivityCreateRequest
    ) -> ItineraryActivity:
        await require_role(self.member_repo, trip_id, user_id, ("owner", "editor"))
        return await self.itinerary_repo.create(trip_id, request)

    async def update_activity(
        self,
        trip_id: uuid.UUID,
        activity_id: uuid.UUID,
        user_id: uuid.UUID,
        request: ActivityUpdateRequest,
    ) -> ItineraryActivity:
        await require_role(self.member_repo, trip_id, user_id, ("owner", "editor"))
        activity = await self.itinerary_repo.find_by_id(activity_id)
        if not activity or activity.trip_id != trip_id:
            raise NotFoundException("アクティビティが見つかりません")
        return await self.itinerary_repo.update(activity, request)

    async def delete_activity(
        self, trip_id: uuid.UUID, activity_id: uuid.UUID, user_id: uuid.UUID
    ) -> None:
        await require_role(self.member_repo, trip_id, user_id, ("owner", "editor"))
        activity = await self.itinerary_repo.find_by_id(activity_id)
        if not activity or activity.trip_id != trip_id:
            raise NotFoundException("アクティビティが見つかりません")
        await self.itinerary_repo.delete(activity)

    async def reorder(
        self, trip_id: uuid.UUID, user_id: uuid.UUID, request: ActivityReorderRequest
    ) -> int:
        await require_role(self.member_repo, trip_id, user_id, ("owner", "editor"))
        return await self.itinerary_repo.bulk_update_order(request.operations)
