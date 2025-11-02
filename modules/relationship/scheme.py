from pydantic import BaseModel
from modules.nodes import NodeResponse
from modules.edges import EdgeResponse
from uuid import UUID


class RelationshipResponse(BaseModel):
    model_config = {
        'from_attributes': True
    }

    id: UUID
    node1: NodeResponse
    node2: NodeResponse
    edge: EdgeResponse


class RelationshipPost(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    node1_id: UUID
    node2_id: UUID
    edge_id: UUID


class RelationshipUpdate(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    node1_id: UUID | None = None
    node2_id: UUID | None = None
    edge_id: UUID | None = None