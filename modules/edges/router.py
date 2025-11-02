from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from database import get_db
from . import Edge, EdgePost, EdgeResponse, crud


edge_router = APIRouter()


@edge_router.post(
    '/',
    summary='Create edge',
    status_code=status.HTTP_201_CREATED,
    response_model=EdgeResponse
)
async def create_edge(
        edge_scheme: EdgePost,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Edge:
    edge_db = await crud.create_edge(db, edge_scheme)
    return edge_db


@edge_router.put(
    '/{edge_id}',
    summary='Edge full update',
    status_code=status.HTTP_200_OK,
    response_model=EdgeResponse
)
async def full_update(
        edge_id: UUID,
        edge_scheme: EdgePost,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Edge:
    edge_db = await crud.update_edge(db, edge_scheme, edge_id)
    return edge_db


@edge_router.delete(
    '/{edge_id}',
    summary='Delete edge',
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None
)
async def delete_edge(
        edge_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    await crud.delete_edge(db, edge_id)


@edge_router.get(
    '/{edge_id}',
    summary='Get edge',
    status_code=status.HTTP_200_OK,
    response_model=EdgeResponse
)
async def get_edge(
        edge_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Edge:
    edge_db = await crud.verify_edge(db, edge_id)
    return edge_db