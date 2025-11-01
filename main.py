from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core import register_exception_handler, settings

# import api_router
from modules import api_router

app = FastAPI()

# connected api_router
app.include_router(api_router)

app.middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_api_url],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
    allow_headers=['*']
)

register_exception_handler(app)