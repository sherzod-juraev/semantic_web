from pydantic import BaseModel

# tags for FastAPI
class Tags(BaseModel):

    users: str = 'Authenticate'
    nodes: str = 'Nodes'
    edges: str = 'Edges'
    relationship: str = 'Relationship'
    chats: str = 'Chats'
    contents: str = 'Contents'
    filters: str = 'Filters'


# prefixes for FastAPI
class Prefixes(BaseModel):

    users: str = '/auth'
    nodes: str = '/nodes'
    edges: str = '/edges'
    relationship: str = '/relationship'
    chats: str = '/chats'
    contents: str = '/contents'
    filters: str = '/filters'


tag = Tags()
prefixes = Prefixes()