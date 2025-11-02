from typing import Annotated
from datetime import datetime, timedelta
from fastapi import APIRouter, Request, Response, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from database import get_db
from core import create_access_token, create_refresh_token, verify_access_token, verify_refresh_token, settings
from . import User, UserUpdate, UserPost, UserResponse,  TokenResponse, crud


user_router = APIRouter()


@user_router.post(
    '/login',
    summary='Create user',
    status_code=status.HTTP_201_CREATED,
    response_model=TokenResponse
)
async def create_user(
        response: Response,
        user_scheme: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Annotated[AsyncSession, Depends(get_db)]
) -> TokenResponse:
    user_db = await crud.create_user(db, user_scheme)
    response.set_cookie(
        key='refresh_token',
        value=create_refresh_token(user_db.id),
        secure=False,
        max_age=60 * 60 * 24 * settings.refresh_token_days,
        expires=datetime.utcnow() + timedelta(days=settings.refresh_token_days),
        httponly=True
    )
    token = TokenResponse(
        access_token=create_access_token(user_db.id)
    )
    return token


@user_router.post(
    '/refresh',
    summary='access_token updated by refresh_token',
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse
)
async def access_token_updated(
        request: Request,
        response: Response,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> TokenResponse:
    refresh_token = request.cookies.get('refresh_token')
    user_id = verify_refresh_token(refresh_token)
    response.set_cookie(
        key='refresh_token',
        value=create_refresh_token(user_id),
        secure=False,
        max_age=60 * 60 * 24 * settings.refresh_token_days,
        expires=datetime.utcnow() + timedelta(days=settings.refresh_token_days),
        httponly=True
    )
    token = TokenResponse(
        access_token=create_access_token(user_id)
    )
    return token


@user_router.put(
    '/',
    summary='User full update',
    status_code=status.HTTP_200_OK,
    response_model=UserResponse
)
async def full_update(
        auth_id: Annotated[UUID, Depends(verify_access_token)],
        user_scheme: UserUpdate,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    user_db = await crud.user_update(db, user_scheme, auth_id)
    return user_db


@user_router.patch(
    '/',
    summary='User partial update',
    status_code=status.HTTP_200_OK,
    response_model=UserResponse
)
async def partial_update(
        auth_id: Annotated[UUID, Depends(verify_access_token)],
        user_scheme: UserUpdate,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    user_db = await crud.user_update(db, user_scheme, auth_id, True)
    return user_db


@user_router.delete(
    '/',
    summary='Delete user',
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None
)
async def delete_user(
        response: Response,
        auth_id: Annotated[UUID, Depends(verify_access_token)],
        user_scheme: UserPost,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    await crud.delete_user(db, user_scheme, auth_id)
    response.delete_cookie('refresh_token')


@user_router.get(
    '/',
    summary='Get user',
    status_code=status.HTTP_200_OK,
    response_model=UserResponse
)
async def get_user(
        auth_id: Annotated[UUID, Depends(verify_access_token)],
        db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    user_db = await crud.verify_user(db, auth_id)
    return user_db