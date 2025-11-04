from fastapi import APIRouter, Depends, status
from . import Filter, FilterPost, FilterResponse, crud

filter_router = APIRouter()


@filter_router.post(
    '/',
    summary='Create filter',
    status_code=status.HTTP_201_CREATED,
    response_model=FilterResponse
)
async def create_filter(

)