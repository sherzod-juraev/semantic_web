from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from uuid import UUID
from . import Relationship, RelationshipPost, RelationshipUpdate


async def save_to_db(
        db: AsyncSession,
        relationship_db: Relationship,
        /
) -> Relationship:
    try:
        await db.commit()
        await db.refresh(relationship_db)
        return relationship_db
    except IntegrityError as exc:
        await db.rollback()
        error_msg = str(exc.orig)
        if 'uq_relationships_three_columns' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='these pairs are available in the database'
            )
        elif 'relationships_edge_id_fkey' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Edge not found'
            )
        elif 'relationships_node1_id_fkey' in error_msg or 'relationships_node2_id_fkey' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Node not found'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating relationship'
        )

async def create_relationship(
        db: AsyncSession,
        relationship_scheme: RelationshipPost,
        /
) -> Relationship:
    relationship_db = Relationship(
        node1_id=relationship_scheme.node1_id,
        node2_id=relationship_scheme.node2_id,
        edge_id=relationship_scheme.edge_id
    )
    db.add(relationship_db)
    relationship_db = await save_to_db(db, relationship_db)
    return relationship_db


async def update_relationship(
        db: AsyncSession,
        relationship_scheme: RelationshipUpdate,
        relationship_id: UUID,
        exclude_unset: bool = False,
        /
) -> Relationship:
    relationship_db = await verify_relationshipp(db, relationship_id)
    for field, value in relationship_scheme.model_dump(exclude_unset=exclude_unset).items():
        setattr(relationship_db, field, value)
    relationship_db = await save_to_db(db, relationship_db)
    return relationship_db


async def delete_relationship(
        db: AsyncSession,
        relationship_id: UUID,
        /
) -> None:
    relationship_db = await verify_relationshipp(db, relationship_id)
    await db.delete(relationship_db)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error deleting relationship'
        )


async def verify_relationshipp(
        db: AsyncSession,
        relationship_id: UUID,
        /
) -> Relationship:
    relationship_db = await db.get(Relationship, relationship_id)
    if not relationship_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Relationship not found'
        )
    return relationship_db