from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from database import get_db
from . import Filter, FilterPost, FilterResponse, crud

filter_router = APIRouter()


@filter_router.post(
    '/',
    summary='Create filter',
    status_code=status.HTTP_201_CREATED,
    response_model=FilterResponse
)
async def create_filter(
        filter_scheme: FilterPost,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Filter:
    filter_db = await crud.create_filter(db, filter_scheme)
    return filter_db


@filter_router.get(
    '/{filter_id}',
    summary='Get filter',
    status_code=status.HTTP_200_OK,
    response_model=FilterResponse
)
async def get_filter(
        filter_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Filter:
    filter_db = await crud.verify_filter(db, filter_id)
    return filter_db