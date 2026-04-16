import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.infrastructure.database import Base


class CandidateSpot(Base):
    __tablename__ = "candidate_spots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id = Column(
        UUID(as_uuid=True),
        ForeignKey("trips.id", ondelete="CASCADE"),
        nullable=False,
    )
    spot_id = Column(
        UUID(as_uuid=True),
        ForeignKey("spots.id", ondelete="CASCADE"),
        nullable=False,
    )
    added_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    status = Column(String(20), nullable=False, server_default="in_pool")  # in_pool / in_timeline
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
