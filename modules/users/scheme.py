from re import match
from pydantic import BaseModel, Field, field_validator, EmailStr
from uuid import UUID

class UserResponse(BaseModel):
    model_config = {
        'from_attributes': True
    }

    id: UUID
    username: str
    email: str | None = None
    full_name: str | None = None


class UserPost(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    username: str = Field(max_length=50)
    password: str = Field(min_length=8, max_length=30)

    @field_validator('username')
    async def verify_username(cls, value):
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d_]{6,50}$'
        if not match(pattern, value):
            raise ValueError('Username invalid')
        return value

    @field_validator('password')
    async def verify_password(cls, value):
        pattern = r'^(?=.[A-Za-z])(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d_]{8,30}$'
        if not match(pattern, value):
            raise ValueError('Password invalid')
        return value


class UserUpdate(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    username: str | None = Field(min_length=6, max_length=50)
    password: str | None = Field(min_length=8, max_length=30)
    email: EmailStr | None = Field(max_length=200)
    full_name: str | None = Field(max_length=100)

    @field_validator('username')
    async def verify_username(cls, value):
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d_]{6,50}$'
        if not match(pattern, value):
            raise ValueError('Username invalid')
        return value

    @field_validator('password')
    async def verify_password(cls, value):
        pattern = r'^(?=.[A-Za-z])(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d_]{8,30}$'
        if not match(pattern, value):
            raise ValueError('Password invalid')
        return value

    @field_validator('full_name')
    async def verify_fullname(cls, value):
        pattern = r'^[A-Za-z -]{1,100}$'
        if not match(pattern, value):
            raise ValueError('Full name invalid')