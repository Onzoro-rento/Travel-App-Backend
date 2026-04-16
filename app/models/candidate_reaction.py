import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.infrastructure.database import Base


class CandidateReaction(Base):
    __tablename__ = "candidate_reactions"

    # 複合ユニーク制約: 同一ユーザーが同一候補に同じ絵文字を重複登録するのを防止
    __table_args__ = (
        UniqueConstraint("candidate_spot_id", "user_id", "emoji_type", name="uq_reaction"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_spot_id = Column(
        UUID(as_uuid=True),
        ForeignKey("candidate_spots.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    emoji_type = Column(String(20), nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
