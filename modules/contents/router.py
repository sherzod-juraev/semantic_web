from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from uuid import UUID
from . import Content, ContentPost, ContentResponse, crud, answer_to_question


content_router = APIRouter()


@content_router.post(
    '/',
    summary='Create content',
    status_code=status.HTTP_201_CREATED,
    response_model=list[str]
)
async def create_content(
        content_scheme: ContentPost,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> list[str]:
    content_db = await crud.create_content(db, content_scheme)
    answer_list = await answer_to_question(db, content_scheme.title)

    return answer_list


@content_router.get(
    '/{chat_id}',
    summary='Get contents by chat_id',
    status_code=status.HTTP_200_OK,
    response_model=list[ContentResponse]
)
async def get_contents(
        chat_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> list[Content]:
    contents_list = await crud.verify_content_by_chat_id(db, chat_id)
    return contents_list