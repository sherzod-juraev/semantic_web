from pydantic import BaseModel

# tags for FastAPI
class Tags(BaseModel):

    users: str = 'Authenticate'
    nodes: str = 'Nodes'
    edges: str = 'Edges'


# prefixes for FastAPI
class Prefixes(BaseModel):

    users: str = '/auth'
    nodes: str = '/nodes'
    edges: str = '/edges'


tag = Tags()
prefixes = Prefixes()