from datetime import datetime, timezone
from sqlalchemy import Text, DateTime
from sqlalchemy.dialects.postgresql import UUID as db_uuid
from sqlalchemy.orm import mapped_column, Mapped
from uuid import UUID, uuid4
from database import Base


class Filter(Base):
    __tablename__ = 'filters'

    id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), primary_key=True, default=uuid4)
    label: Mapped[str] = mapped_column(Text, nullable=False)
    negative_label: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))