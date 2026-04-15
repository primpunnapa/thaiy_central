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
    studio_id: int
    platforms: List[str] = []
    platform_urls: dict = {}  # e.g. {"youtube": "https://youtube.com/...", "iqiyi": "https://..."}

class SeriesCreate(SeriesBase):
    updated_by_id: Optional[int] = None

class SeriesUpdate(BaseModel):
    title_th: Optional[str] = None
    title_en: Optional[str] = None
    description: Optional[str] = None
    release_year: Optional[int] = None
    poster_url: Optional[str] = None
    status: Optional[str] = None
    air_day: Optional[str] = None
    air_time: Optional[str] = None
    studio_id: Optional[int] = None
    platforms: Optional[List[str]] = None
    platform_urls: Optional[dict] = None
    updated_by_id: Optional[int] = None

class Series(SeriesBase):
    id: int
    views: int
    created_at: datetime
    updated_at: Optional[datetime]
    studio: Studio
    
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

class SeriesScheduleDay(BaseModel):
    """Series schedule grouped by day"""
    day: str
    series: List[SeriesList]

class SeriesSchedule(BaseModel):
    """Complete schedule response with series grouped by day"""
    monday: List[SeriesList] = []
    tuesday: List[SeriesList] = []
    wednesday: List[SeriesList] = []
    thursday: List[SeriesList] = []
    friday: List[SeriesList] = []
    saturday: List[SeriesList] = []
    sunday: List[SeriesList] = []