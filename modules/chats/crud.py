from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import delete
from fastapi import HTTPException, status
from uuid import UUID
from . import Chat, ChatPost


async def save_to_db(
        db: AsyncSession,
        chat_db: Chat,
        /
) -> Chat:
    try:
        await db.commit()
        await db.refresh(chat_db)
        return chat_db
    except IntegrityError as exc:
        await db.rollback()
        error_ms = str(exc.orig)
        if 'chats_owner_id_fkey' in error_ms:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating chat'
        )


async def create_chat(
        db: AsyncSession,
        chat_scheme: ChatPost,
        owner_id: UUID,
        /
) -> Chat:
    chat_db = Chat(
        title=chat_scheme.title,
        owner_id=owner_id
    )
    db.add(chat_db)
    chat_db = await save_to_db(db, chat_db)
    return chat_db


async def delete_chat(
        db: AsyncSession,
        chat_id: UUID,
        /
) -> None:
    query = delete(Chat).where(Chat.id == chat_id)
    result = await db.execute(query)
    await db.commit()
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Chat not found'
        )


async def verify_chat(
        db: AsyncSession,
        chat_id: UUID,
        /
) -> Chat:
    chat_db = await db.get(Chat, chat_id)
    if not chat_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Chat not found'
        )
    return chat_db