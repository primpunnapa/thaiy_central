from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas.studio import Studio

class SeriesBase(BaseModel):
    title_th: str
    title_en: str
    description: Optional[str] = None
    release_year: Optional[int] = None
    poster_url: Optional[str] = None
    status: str = "ongoing"
    air_day: Optional[str] = None
    air_time: Optional[str] = None

class SeriesCreate(SeriesBase):
    studio_ids: Optional[List[int]] = []

class SeriesUpdate(SeriesBase):
    title_th: Optional[str] = None
    title_en: Optional[str] = None
    description: Optional[str] = None
    release_year: Optional[int] = None
    poster_url: Optional[str] = None
    status: Optional[str] = None
    air_day: Optional[str] = None
    air_time: Optional[str] = None
    studio_ids: Optional[List[int]] = None

class Series(SeriesBase):
    id: int
    views: int
    created_at: datetime
    updated_at: Optional[datetime]
    studios: List[Studio] = []
    
    class Config:
        from_attributes = True

class SeriesList(BaseModel):
    id: int
    title_th: str
    title_en: str
    poster_url: Optional[str]
    status: str
    air_day: Optional[str]
    air_time: Optional[str]
    
    class Config:
        from_attributes = True