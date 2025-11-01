from pydantic import BaseModel

# tags for FastAPI
class Tags(BaseModel):

    users: str = 'Authenticate'


# prefixes for FastAPI
class Prefixes(BaseModel):

    users: str = '/auth'


tag = Tags()
prefixes = Prefixes()