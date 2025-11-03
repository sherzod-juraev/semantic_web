from pydantic import BaseModel
from uuid import UUID
from .model import SenderType


class ContentResponse(BaseModel):
    model_config = {
        'from_attributes': True
    }

    id: UUID
    sender: SenderType
    title: str


class ContentPost(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    sender: SenderType = SenderType.SERVER
    title: str
    chat_id: UUID