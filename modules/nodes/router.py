from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from database import get_db
from . import Node, NodePost, NodeResponse, crud


node_router = APIRouter()


@node_router.post(
    '/',
    summary='Create node',
    status_code=status.HTTP_201_CREATED,
    response_model=NodeResponse
)
async def create_node(
        node_scheme: NodePost,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Node:
    node_db = await crud.create_node(db, node_scheme)
    return node_db


@node_router.put(
    '/{node_id}',
    summary='Node full update',
    status_code=status.HTTP_200_OK,
    response_model=NodeResponse
)
async def full_update(
        node_id: UUID,
        node_scheme: NodePost,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Node:
    node_db = await crud.update_node(db, node_scheme, node_id)
    return node_db


@node_router.delete(
    '/{node_id}',
    summary='Delete node',
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None
)
async def delete_node(
        node_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    await crud.delete_node(db, node_id)


@node_router.get(
    '/{node_id}',
    summary='Get node',
    status_code=status.HTTP_200_OK,
    response_model=NodeResponse
)
async def get_node(
        node_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Node:
    node_db = await crud.verify_node(db, node_id)
    return node_db