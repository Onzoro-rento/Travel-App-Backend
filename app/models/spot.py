import uuid

from sqlalchemy import Column, DateTime, Double, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.infrastructure.database import Base

class Spot(Base):
    __tablename__ = "spots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    google_place_id = Column(String(255), unique=True, nullable=True)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=True)
    latitude = Column(Double, nullable=False)
    longitude = Column(Double, nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
