from datetime import datetime, timezone
from enum import Enum as py_enum
from sqlalchemy import Text, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as db_uuid
from sqlalchemy.orm import mapped_column, Mapped, relationship
from uuid import uuid4, UUID
from database import Base


class SenderType(py_enum):
    USER = 'user'
    SERVER = 'server'


class Content(Base):
    __tablename__ = 'contents'

    id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), primary_key=True, default=uuid4)
    sender: Mapped[SenderType] = mapped_column(Enum(SenderType), nullable=False, default=SenderType.SERVER)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    chat_id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), ForeignKey('chats.id', ondelete='CASCADE'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    chat: Mapped['Chat'] = relationship(
        'Chat',
        foreign_keys=[chat_id],
        back_populates='contents',
        lazy='noload'
    )