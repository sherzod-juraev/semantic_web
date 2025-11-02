from pydantic import BaseModel
from uuid import UUID


class NodeResponse(BaseModel):
    model_config = {
        'from_attributes': True
    }

    id: UUID
    label: str


class NodePost(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    label: str