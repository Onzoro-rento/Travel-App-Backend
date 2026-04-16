from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.infrastructure.database import Base


class TripMember(Base):
    __tablename__ = "trip_members"

    __table_args__ = (
        CheckConstraint(
            "role IN ('owner', 'editor', 'viewer')",
            name="ck_trip_members_role",
        ),
    )

    # 複合主キー: (trip_id, user_id)
    trip_id = Column(
        UUID(as_uuid=True),
        ForeignKey("trips.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    role = Column(String(20), nullable=False)  # owner / editor / viewer
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
