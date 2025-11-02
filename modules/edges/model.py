from datetime import datetime, timezone
from sqlalchemy import Text, DateTime
from sqlalchemy.dialects.postgresql import UUID as db_uuid
from sqlalchemy.orm import mapped_column, Mapped, relationship
from uuid import uuid4, UUID
from database import Base


class Edge(Base):
    __tablename__ = 'edges'

    id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), primary_key=True, default=uuid4)
    label: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    relationship_edges: Mapped['Relationship'] = relationship(
        'Relationship',
        back_populates='edge',
        lazy='noload'
    )