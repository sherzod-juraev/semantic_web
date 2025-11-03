from fastapi import APIRouter
from core import tag, prefixes

# import routers
from .users.router import user_router
from .nodes.router import node_router
from .edges.router import edge_router
from .relationship.router import relationship_router
from .chats.router import chat_router
from .contents.router import content_router


# import models
from .users.model import User
from .nodes.model import Node
from .edges.model import Edge
from .relationship.model import Relationship
from .chats.model import Chat
from .contents.model import Content


__all__ = ['User', 'Node', 'Edge', 'Relationship', 'Chat', 'Content']


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

api_router.include_router(
    relationship_router,
    prefix=prefixes.relationship,
    tags=[tag.relationship]
)

api_router.include_router(
    chat_router,
    prefix=prefixes.chats,
    tags=[tag.chats]
)

api_router.include_router(
    content_router,
    prefix=prefixes.contents,
    tags=[tag.contents]
)