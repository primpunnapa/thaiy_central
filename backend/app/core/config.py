from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://bladmin:blpass@localhost:5432/blcentral"
    
    # API
    api_prefix: str = "/api"
    project_name: str = "Thai BL Central"
    environment: str = "development"
    
    class Config:
        env_file = ".env"
        extra = "ignore"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
