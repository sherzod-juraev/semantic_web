from fastapi import APIRouter
from core import tag, prefixes

# import routers
from .users.router import user_router
from .nodes.router import node_router
from .edges.router import edge_router


# import models
from .users.model import User
from .nodes.model import Node
from .edges.model import Edge


__all__ = ['User', 'Node', 'Edge']


api_router = APIRouter()

# include routers
api_router.include_router(
    user_router,
    prefix=prefixes.users,
    tags=[tag.users]
)

api_router.include_router(
    node_router,
    prefix=prefixes.nodes,
    tags=[tag.nodes]
)

api_router.include_router(
    edge_router,
    prefix=prefixes.edges,
    tags=[tag.edges]
)