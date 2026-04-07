from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.infrastructure.database import Base


class User(Base):
    __tablename__ = "users"

    # Supabase Auth の UUID をそのまま PK として使用（JWTのsubクレームと一致）
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    avatar_url = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
