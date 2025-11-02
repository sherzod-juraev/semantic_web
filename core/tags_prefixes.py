from pydantic import BaseModel

# tags for FastAPI
class Tags(BaseModel):

    users: str = 'Authenticate'
    nodes: str = 'Nodes'


# prefixes for FastAPI
class Prefixes(BaseModel):

    users: str = '/auth'
    nodes: str = '/nodes'


tag = Tags()
prefixes = Prefixes()