from pydantic import BaseModel
from typing import Optional
from app.database.models import PlatformEnum

class StudioBase(BaseModel):
    name: str
    platform: PlatformEnum
    website_url: Optional[str] = None
    logo_url: Optional[str] = None

class StudioCreate(StudioBase):
    pass

class Studio(StudioBase):
    id: int
    
    class Config:
        from_attributes = True