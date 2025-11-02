from pydantic import BaseModel
from uuid import UUID


class EdgeResponse(BaseModel):
    model_config = {
        'from_attrigutes': True
    }

    id: UUID
    label: str


class EdgePost(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    label: str