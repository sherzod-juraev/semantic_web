from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from database import get_db
from . import Relationship, RelationshipPost, RelationshipUpdate, RelationshipResponse, crud


relationship_router = APIRouter()


@relationship_router.post(
    '/',
    summary='Create relationship',
    status_code=status.HTTP_201_CREATED,
    response_model=RelationshipResponse
)
async def create_relationship(
        relationship_scheme: RelationshipPost,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Relationship:
    relationship_db = await crud.create_relationship(db, relationship_scheme)
    return relationship_db


@relationship_router.put(
    '/{relationship_id}',
    summary='Relationship full update',
    status_code=status.HTTP_200_OK,
    response_model=RelationshipResponse
)
async def full_update(
        relationship_id: UUID,
        relationship_scheme: RelationshipUpdate,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Relationship:
    relationship_db = await crud.update_relationship(db, relationship_scheme, relationship_id)
    return relationship_db


@relationship_router.patch(
    '{relationship_id}',
    summary='Relationship partial update',
    status_code=status.HTTP_200_OK,
    response_model=RelationshipResponse
)
async def partial_update(
        relationship_id: UUID,
        relationship_scheme: RelationshipUpdate,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Relationship:
    relationship_db = await crud.update_relationship(db, relationship_scheme, relationship_id, True)
    return relationship_db


@relationship_router.delete(
    '/{relationship_id}',
    summary='Delete relationship',
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None
)
async def delete_relationship(
        relationship_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    await crud.delete_relationship(db, relationship_id)


@relationship_router.get(
    '/{relationship_id}',
    summary='Get relationship',
    status_code=status.HTTP_200_OK,
    response_model=RelationshipResponse
)
async def get_relationship(
        relationship_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Relationship:
    relationship_db = await crud.verify_relationshipp(db, relationship_id)
    return relationship_db