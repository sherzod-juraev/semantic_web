from datetime import datetime, timezone
from sqlalchemy import ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as db_uuid
from sqlalchemy.orm import mapped_column, Mapped, relationship
from uuid import uuid4, UUID
from database import Base


class Relationship(Base):
    __tablename__ = 'relationships'

    id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), primary_key=True, default=uuid4)
    node1_id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), ForeignKey('nodes.id', ondelete='RESTRICT'), nullable=False)
    node2_id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), ForeignKey('nodes.id', ondelete='RESTRICT'), nullable=False)
    edge_id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), ForeignKey('edges.id', ondelete='RESTRICT'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    node1: Mapped['Node'] = relationship(
        'Node',
        foreign_keys=[node1_id],
        back_populates='relationship_nodes1',
        lazy='selectin'
    )

    node2: Mapped['Node'] = relationship(
        'Node',
        foreign_keys=[node2_id],
        back_populates='relationship_nodes2',
        lazy='selectin'
    )

    edge: Mapped['Edge'] = relationship(
        'Edge',
        foreign_keys=[edge_id],
        back_populates='relationship_edges',
        lazy='selectin'
    )

    __table_args__ = (
        UniqueConstraint(node1_id, node2_id, edge_id, name='uq_relationships_three_columns'),
    )