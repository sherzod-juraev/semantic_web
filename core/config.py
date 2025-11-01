from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    database_url: str
    access_token_minutes: int
    refresh_token_days: int
    secret_key: str
    algorithm: str
    frontend_api_url: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()