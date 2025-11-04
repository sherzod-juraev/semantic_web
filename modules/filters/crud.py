from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from uuid import UUID
from . import Filter, FilterPost


async def save_to_db(
        db: AsyncSession,
        filter_db: Filter,
        /
) -> Filter:
    try:
        await db.commit()
        await db.refresh(filter_db)
        return filter_db
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating filter'
        )


async def create_filter(
        db: AsyncSession,
        filter_scheme: FilterPost,
        /
) -> Filter:
    filter_db = Filter(
        label=filter_scheme.label,
        negative_label=filter_scheme.negative_label
    )
    db.add(filter_db)
    filter_db = await save_to_db(db, filter_db)
    return filter_db


async def verify_filter(
        db: AsyncSession,
        filter_id: UUID,
        /
) -> Filter:
    filter_db = await db.get(Filter, filter_id)
    if not filter_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Filter not found'
        )
    return filter_db