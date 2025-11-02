from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from uuid import UUID
from. import Edge, EdgePost


async def save_to_db(
        db: AsyncSession,
        edge_db: Edge,
        /
) -> Edge:
    try:
        await db.commit()
        await db.refresh(edge_db)
        return edge_db
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating edge'
        )


async def create_edge(
        db: AsyncSession,
        edge_scheme: EdgePost,
        /
) -> Edge:
    edge_db = Edge(label=edge_scheme.label)
    db.add(edge_db)
    edge_db = await save_to_db(db, edge_db)
    return edge_db


async def update_edge(
        db: AsyncSession,
        edge_scheme: EdgePost,
        edge_id: UUID,
        exclude_unset: bool = False,
        /
) -> Edge:
    edge_db = await verify_edge(db, edge_id)
    for field, value in edge_scheme.model_dump(exclude_unset=exclude_unset).items():
        setattr(edge_db, field, value)
    edge_db = await save_to_db(db, edge_db)
    return edge_db


async def delete_edge(
        db: AsyncSession,
        edge_id: UUID,
        /
) -> None:
    edge_db = await verify_edge(db, edge_id)
    db.delete(edge_db)
    try:
        await db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='the node has relationships with other tables'
        )



async def verify_edge(
        db: AsyncSession,
        edge_id: UUID,
        /
) -> Edge:
    edge_db = await db.get(Edge, edge_id)
    if not edge_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Edge not found'
        )
    return edge_db