from pydantic import BaseModel
from uuid import UUID

class FilterResponse(BaseModel):
    model_config = {
        'from_attributes': True
    }

    id: UUID
    label: str
    negative_label: str


class FilterPost(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    label: str
    negative_label: str