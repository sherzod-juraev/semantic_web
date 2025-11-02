from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import delete
from fastapi import HTTPException, status
from uuid import UUID
from . import User, UserPost, UserUpdate
from core import hashed_pass, verify_pass


async def save_to_db(
        db: AsyncSession,
        user_db: User,
        /
) -> User:
    try:
        await db.commit()
        await db.refresh(user_db)
        return user_db
    except IntegrityError as exc:
        await db.rollback()
        error_msg = str(exc.orig)
        if 'ix_users_username' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Username already exists'
            )
        elif 'users_email_key' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email already exists'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating user'
        )


async def create_user(
        db: AsyncSession,
        user_scheme: UserPost,
        /
) -> User:
    user_db = User(
        username=user_scheme.username,
        password = hashed_pass(user_scheme.password)
    )
    db.add(user_db)
    user_db = await save_to_db(db, user_db)
    return user_db


async def user_update(
        db: AsyncSession,
        user_scheme: UserUpdate,
        user_id: UUID,
        exclude_unset: bool = False,
        /
) -> User:
    user_db = await verify_user(db, user_id)
    for field, value in user_scheme.model_dump(exclude_unset=exclude_unset).items():
        if field == 'password':
            setattr(user_db, field, hashed_pass(value))
        else:
            setattr(user_db, field, value)
    user_db = await save_to_db(db, user_db)
    return user_db


async def delete_user(
        db: AsyncSession,
        user_scheme: UserPost,
        user_id: UUID,
        /
) -> None:
    user_db = await verify_user(db, user_id)
    await verify_username_and_password(user_scheme, user_db)
    query = delete(User).where(User.id == user_id)
    result = await db.execute(query)
    await db.commit()
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )


async def verify_username_and_password(
        user_scheme: UserPost,
        user_db: User,
        /
) -> None:
    username = user_scheme.username != user_db.username
    password = verify_pass(user_scheme.password, user_db.password)
    if not username and not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username and password are wrong'
        )
    elif not username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username is wrong'
        )
    elif not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Password is wrong'
        )


async def verify_user(
        db: AsyncSession,
        user_id: UUID,
        /
) -> User:
    user_db = await db.get(User, user_id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return user_db