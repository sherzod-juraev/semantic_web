from fastapi import APIRouter
from core import tag, prefixes

# import routers
from .users.router import user_router

# import models
from .users.model import User


__all__ = ['User',]


api_router = APIRouter()

# include routers
api_router.include_router(
    user_router,
    prefix=prefixes.users,
    tags=[tag.users]
)