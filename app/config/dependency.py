from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.repositories.user_repository import UserRepository
from app.repositories.trip_repository import TripRepository
from app.repositories.trip_member_repository import TripMemberRepository
from app.repositories.spot_repository import SpotRepository
from app.repositories.candidate_spot_repository import CandidateSpotRepository
from app.repositories.candidate_reaction_repository import CandidateReactionRepository
from app.repositories.itinerary_activity_repository import ItineraryActivityRepository
from app.usecases.user_usecase import UserUsecase
from app.usecases.trip_usecase import TripUsecase
from app.usecases.trip_member_usecase import TripMemberUsecase
from app.usecases.candidate_spot_usecase import CandidateSpotUsecase
from app.usecases.candidate_reaction_usecase import CandidateReactionUsecase
from app.usecases.itinerary_usecase import ItineraryUsecase


def get_user_usecase(db: AsyncSession = Depends(get_session)) -> UserUsecase:
    return UserUsecase(UserRepository(db))


def get_trip_usecase(db: AsyncSession = Depends(get_session)) -> TripUsecase:
    return TripUsecase(TripRepository(db), TripMemberRepository(db))


def get_trip_member_usecase(db: AsyncSession = Depends(get_session)) -> TripMemberUsecase:
    return TripMemberUsecase(TripRepository(db), TripMemberRepository(db))


def get_candidate_spot_usecase(db: AsyncSession = Depends(get_session)) -> CandidateSpotUsecase:
    return CandidateSpotUsecase(
        CandidateSpotRepository(db),
        SpotRepository(db),
        TripMemberRepository(db),
    )


def get_candidate_reaction_usecase(
    db: AsyncSession = Depends(get_session),
) -> CandidateReactionUsecase:
    return CandidateReactionUsecase(
        CandidateReactionRepository(db),
        CandidateSpotRepository(db),
        TripMemberRepository(db),
    )


def get_itinerary_usecase(db: AsyncSession = Depends(get_session)) -> ItineraryUsecase:
    return ItineraryUsecase(
        ItineraryActivityRepository(db),
        TripRepository(db),
        TripMemberRepository(db),
    )
