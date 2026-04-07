import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.infrastructure.database import Base


class ItineraryActivity(Base):
    __tablename__ = "itinerary_activities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id = Column(
        UUID(as_uuid=True),
        ForeignKey("trips.id", ondelete="CASCADE"),
        nullable=False,
    )
    day_number = Column(Integer, nullable=False)
    spot_id = Column(
        UUID(as_uuid=True),
        ForeignKey("spots.id", ondelete="RESTRICT"),
        nullable=False,
    )
    sort_order = Column(String(255), nullable=False)  # 辞書式順序文字列（ドラッグ&ドロップ用）
    start_time = Column(DateTime(timezone=True), nullable=True)
    memo = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
