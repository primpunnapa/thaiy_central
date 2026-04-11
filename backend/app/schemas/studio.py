from pydantic import BaseModel
from typing import Optional

class StudioBase(BaseModel):
    name: str
    website_url: Optional[str] = None
    logo_url: Optional[str] = None

class StudioCreate(StudioBase):
    pass

class Studio(StudioBase):
    id: int
    
    class Config:
        from_attributes = True