from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from uuid import UUID
from . import Node, NodePost


async def save_to_db(
        db: AsyncSession,
        node_db: Node,
        /
) -> Node:
    try:
        await db.commit()
        await db.refresh(node_db)
        return node_db
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating node'
        )


async def create_node(
        db: AsyncSession,
        node_scheme: NodePost,
        /
) -> Node:
    node_db = Node(label=node_scheme.label)
    node_db = await save_to_db(db, node_db)
    return node_db


async def update_node(
        db: AsyncSession,
        node_scheme: NodePost,
        node_id: UUID,
        exclude_unset: bool = False,
        /
) -> Node:
    node_db = await verify_node(db, node_id)
    for field, value in node_scheme.model_dump(exclude_unset=exclude_unset).items():
        setattr(node_db, field, value)
    node_db = await save_to_db(db, node_db)
    return node_db


async def delete_node(
        db: AsyncSession,
        node_id: UUID,
        /
) -> None:
    node_db = await verify_node(db, node_id)
    await db.delete(node_db)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='the node has relationships with other tables'
        )


async def verify_node(
        db: AsyncSession,
        node_id: UUID,
        /
) -> Node:
    node_db = await db.get(Node, node_id)
    if not node_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Node not found'
        )
    return node_db