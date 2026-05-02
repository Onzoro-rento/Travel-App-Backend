import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.infrastructure.database import Base


class ItineraryActivity(Base):
    __tablename__ = "itinerary_activities"

    __table_args__ = (
        CheckConstraint(
            "day_number >= 1",
            name="ck_itinerary_activities_day_number",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("trips.id", ondelete="CASCADE"),
    )
    day_number: Mapped[int] = mapped_column(Integer)
    spot_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("spots.id", ondelete="RESTRICT"),
    )
    sort_order: Mapped[str] = mapped_column(String(255))  # 辞書式順序文字列（ドラッグ&ドロップ用）
    start_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    memo: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
